import requests

"""
Fetch and filter Hacker News stories
"""
def fetch_hackernews(search: str):

    # Fetch story IDs
    ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"

    ids = requests.get(ids_url).json()

    # Limit stories
    top_ids = ids[:30]

    stories = []

    for story_id in top_ids:

        story_url = (
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )

        story = requests.get(story_url).json()

        if not story:
            continue

        title = story.get("title", "").lower()

        text = story.get("text", "").lower()

        if (
            search.lower() in title or
            search.lower() in text
        ):

            stories.append({
                "id": story.get("id"),
                "title": story.get("title"),
                "by": story.get("by"),
                "score": story.get("score"),
                "url": story.get("url")
            })

    return stories