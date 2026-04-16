"""
Main script: scrape X trends and push to Feishu.
"""

import time
import logging
from dotenv import load_dotenv
import os

from scraper import fetch_trending_with_retry
from pusher import push_to_feishu


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("🚀 Starting X Trending Scraper")

    # Fetch trending topics
    trends = fetch_trending_with_retry()

    if not trends:
        logger.error("❌ No trends fetched, exiting")
        return 1

    logger.info(f"📊 Fetched {len(trends)} trending topics")

    # Push to Feishu
    success = push_to_feishu(trends)

    if success:
        logger.info("✅ Done!")
        return 0
    else:
        logger.error("❌ Push failed")
        return 1


if __name__ == "__main__":
    load_dotenv()
    exit(main())
