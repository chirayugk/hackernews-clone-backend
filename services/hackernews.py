import asyncio
import httpx
import requests

"""
Fetch single Hacker News story
"""
async def fetch_story(client, story_id):

    story_url = (
        f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    )

    response = await client.get(story_url)

    return response.json()


"""
Fetch and filter Hacker News stories
"""
async def fetch_hackernews(search: str):

    ids_url = (
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    )

    async with httpx.AsyncClient() as client:

        # Fetch story IDs
        ids_response = await client.get(ids_url)

        ids = ids_response.json()

        top_ids = ids[:500]

        # Fetch all stories concurrently
        tasks = [
            fetch_story(client, story_id)
            for story_id in top_ids
        ]

        stories = await asyncio.gather(*tasks,return_exceptions=True)

    filtered = []

    for story in stories:
        if isinstance(story, Exception):
            continue
        if not story:
            continue

        title = story.get("title", "").lower()

        text = story.get("text", "").lower()

        if (
            search.lower() in title or
            search.lower() in text
        ):

            filtered.append({
                "id": story.get("id"),
                "title": story.get("title"),
                "by": story.get("by"),
                "score": story.get("score"),
                "url": story.get("url")
            })

    return filtered

def get_trending_news(limit=10):
    top_stories=requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
    results=[]

    for story_id in top_stories[:limit]:
        story=requests.get( f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()

        results.append({
            "id":story.get("id"),
            "title":story.get("title"),
            "by":story.get("by"),
            "score": story.get("score"),
            "url": story.get("url")
        })
    return results    