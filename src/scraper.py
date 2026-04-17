"""
X (Twitter) trending topics scraper using Nitter instances.
"""

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import random


NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.kavin.rocks",
    "https://nitter.universeodon.com",
]


def load_env():
    load_dotenv()
    return os.getenv("NITTER_INSTANCE", random.choice(NITTER_INSTANCES))


def fetch_trending(nitter_instance: str = None) -> list[dict]:
    """
    Fetch trending topics from X via Nitter.

    Args:
        nitter_instance: Nitter instance URL. If None, picks a random one.

    Returns:
        List of dicts with 'name', 'url', 'tweet_count'
    """
    if not nitter_instance:
        nitter_instance = load_env()

    # X's trending endpoint
    url = f"{nitter_instance}/api/trends"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    trends = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # API returns a list of trend objects
            for item in data.get("trends", [])[:10]:  # Top 10
                trends.append({
                    "name": item.get("name", ""),
                    "url": f"https://x.com/search?q={item.get('name', '')}",
                    "tweet_count": item.get("tweet_count", ""),
                })
        else:
            print(f"❌ Nitter API error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Failed to fetch trending: {e}")

    # Fallback: try scraping the web version if API fails
    if not trends:
        print("🔄 Trying web scraping fallback...")
        trends = scrape_trending_web(nitter_instance)

    return trends


def scrape_trending_web(nitter_instance: str) -> list[dict]:
    """
    Fallback: scrape trending topics from Nitter web page.
    """
    url = nitter_instance.rstrip("/")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "lxml")
            trends = []
            for a in soup.find_all("a", href=True)[:15]:
                text = a.get_text(strip=True)
                href = a["href"]
                if text and (text.startswith("#") or "search" in href):
                    trends.append({
                        "name": text,
                        "url": f"https://x.com{href}" if href.startswith("/") else href,
                        "tweet_count": "",
                    })
                    if len(trends) >= 10:
                        break
            return trends
        else:
            print(f"❌ Nitter web scrape failed: HTTP {resp.status_code}")
    except Exception as e:
        print(f"❌ Web scraping fallback failed: {e}")

    return []


def fetch_trending_with_retry(max_retries: int = 3) -> list[dict]:
    """
    Try multiple Nitter instances until one works.
    """
    instances = NITTER_INSTANCES.copy()
    random.shuffle(instances)

    for inst in instances[:max_retries]:
        trends = fetch_trending(inst)
        if trends:
            return trends

    print("❌ All Nitter instances failed")
    return []


if __name__ == "__main__":
    trends = fetch_trending_with_retry()
    print(f"Found {len(trends)} trends:")
    for t in trends:
        print(f"  - {t['name']} ({t['tweet_count']})")
