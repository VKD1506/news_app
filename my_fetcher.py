import requests
from config import Config

def fetch_raw_news(query="technology"):
    if not Config.NEWS_API_KEY:
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "apiKey": Config.NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get("articles", [])
    except requests.RequestException:
        pass

    return []