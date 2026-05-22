from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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