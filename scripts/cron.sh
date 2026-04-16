#!/bin/bash
# Cron wrapper for X Trending Scraper
# Runs every 3 hours

LOGFILE="/var/log/hotTopicScraper.log"
PROJECT_DIR="/opt/hotTopicScraper"

cd "$PROJECT_DIR" || exit 1

echo "$(date '+%Y-%m-%d %H:%M:%S') - Running scraper..." >> "$LOGFILE"
python3 src/main.py >> "$LOGFILE" 2>&1
