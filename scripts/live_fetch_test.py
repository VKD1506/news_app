import os
import sys

# Ensure project root is on sys.path so imports work when running from /scripts
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import Config

if not Config.NEWS_API_KEY:
    print('NO_KEY')
else:
    from my_fetcher import fetch_raw_news
    arts = fetch_raw_news('technology')
    print('HAS_KEY')
    print(len(arts))
    for a in arts[:3]:
        print(a.get('title'))
