from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.cache_service import (
    get_cached_summary,
    save_summary
)

from services.ai_summary import summarize_text
from services.article_extractor import extract_article_text

from services.hackernews import fetch_hackernews

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Search endpoint
"""
@app.get("/search")
async def search_news(q: str):

    results = await fetch_hackernews(q)
    return {
        "results": results
    }

class SummaryRequest(BaseModel):
    url: str


@app.post("/summarize")
async def summarize_article(
    request: SummaryRequest
):
    cached = get_cached_summary(
        request.url
    )
    if cached:

        return {
            "summary": cached,
            "cached": True
        }
    article_text = extract_article_text(
        request.url
    )

    if not article_text:

        return {
            "summary":
            "Unable to extract article."
        }

    summary = await summarize_text(
        article_text
    )

    return {
        "summary": summary,
        "cached":False
    }    