# server/app/services/web_search.py
import logging
from ..config import settings

def web_search(query: str, limit: int = 3):
    """
    If SERPAPI_KEY is configured, run a simple search and return snippets.
    If not configured, return [].
    """
    if not settings.SERPAPI_KEY:
        return []

    try:
        import requests
        url = "https://serpapi.com/search"
        params = {"q": query, "api_key": settings.SERPAPI_KEY}
        r = requests.get(url, params=params, timeout=8)
        data = r.json()
        snippets = []
        for r in data.get("organic_results", [])[:limit]:
            snip = r.get("snippet") or r.get("title") or ""
            if snip:
                snippets.append(snip)
        return snippets
    except Exception as e:
        logging.warning("Web search failed: %s", e)
        return []
