from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from services.cache_service import (
    get_cached_summary,
    save_summary,
)
from services.ai_summary import summarize_text
from services.article_extractor import extract_article_text
from services.hackernews import (
    fetch_hackernews,
    get_trending_news,
)

import os

SECRET_KEY = os.getenv("TECHPULSE_SECRET")

app = FastAPI()

# ---------------------------
# Rate Limiter
# ---------------------------

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)

# ---------------------------
# CORS
# ---------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Models
# ---------------------------

class SummaryRequest(BaseModel):
    url: str
    secret: str


# ---------------------------
# Search
# ---------------------------

@app.get("/search")
async def search_news(q: str):

    results = await fetch_hackernews(q)

    return {
        "results": results
    }


# ---------------------------
# Trending
# ---------------------------

@app.get("/trending")
def trending():

    return {
        "results": get_trending_news(10)
    }


# ---------------------------
# Secret Verification
# ---------------------------

@app.post("/verify-secret")
async def verify_secret(data: dict):

    return {
        "valid": data.get("secret") == SECRET_KEY
    }


# ---------------------------
# AI Summary
# ---------------------------

@app.post("/summarize")
@limiter.limit("10/hour")
async def summarize_article(
    request: Request,
    body: SummaryRequest,
):

    # Secret validation
    if body.secret != SECRET_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid secret key"
        )

    # Check cache
    cached = get_cached_summary(body.url)

    if cached:
        return {
            "summary": cached,
            "cached": True
        }

    # Extract article
    article_text = extract_article_text(
        body.url
    )

    if not article_text:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract article."
        )

    # Generate summary
    summary = await summarize_text(
        article_text
    )

    # Save cache
    save_summary(
        body.url,
        summary
    )

    return {
        "summary": summary,
        "cached": False
    }