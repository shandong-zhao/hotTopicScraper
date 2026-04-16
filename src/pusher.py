"""
Feishu webhook pusher module.
"""

import requests
from dotenv import load_dotenv
import os


def load_env():
    load_dotenv()
    return os.getenv("FEISHU_WEBHOOK_URL")


def build_feishu_card(trends: list[dict]) -> dict:
    """
    Build a Feishu interactive card with trending topics.

    Args:
        trends: List of dicts with 'name', 'url', 'tweet_count' (optional)

    Returns:
        Feishu card payload dict
    """
    elements = []
    for i, trend in enumerate(trends, 1):
        name = trend.get("name", "")
        url = trend.get("url", "")
        tweet_count = trend.get("tweet_count", "")

        # Truncate long trend names
        if len(name) > 50:
            name = name[:47] + "..."

        element = {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{i}. {name}**" + (f" ({tweet_count} posts)" if tweet_count else "")
            }
        }
        elements.append(element)

        if url:
            elements.append({
                "tag": "a",
                "text": {"tag": "lark_md", "content": f"🔗 View on X"},
                "href": url
            })

        elements.append({"tag": "hr"})

    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "🔥 X 全球热门趋势"},
                "template": "orange"
            },
            "elements": elements
        }
    }
    return card


def push_to_feishu(trends: list[dict]) -> bool:
    """
    Push trending topics to Feishu via webhook.

    Args:
        trends: List of trend dicts

    Returns:
        True if successful, False otherwise
    """
    webhook_url = load_env()
    if not webhook_url:
        print("❌ FEISHU_WEBHOOK_URL not set")
        return False

    card = build_feishu_card(trends)
    try:
        resp = requests.post(webhook_url, json=card, timeout=10)
        if resp.status_code == 200:
            print(f"✅ Pushed {len(trends)} trends to Feishu")
            return True
        else:
            print(f"❌ Feishu API error: {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        print(f"❌ Failed to push to Feishu: {e}")
        return False


if __name__ == "__main__":
    # Quick test
    test_trends = [
        {"name": "Test Trend #1", "url": "https://x.com/search?q=test", "tweet_count": "10K"},
        {"name": "Another Trend", "url": "", "tweet_count": ""},
    ]
    push_to_feishu(test_trends)
