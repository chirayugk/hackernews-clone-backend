import json
import os

CACHE_FILE="cache/summaries.json"

def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}
    
    with open(CACHE_FILE,"r") as f:
            return json.load(f)


def save_cache():
     
    with open(CACHE_FILE, "w") as f:
        json.dump("cache", f, indent=2)

def get_cached_summary(url: str):

    cache = load_cache()

    return cache.get(url)


def save_summary(url: str, summary: str):

    cache = load_cache()

    cache[url] = summary

    save_cache(cache)   