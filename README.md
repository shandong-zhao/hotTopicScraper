# hotTopicScraper

X (Twitter) trending topics scraper with Feishu webhook delivery.

## Overview

Scrapes trending topics from X (Twitter) and pushes them to a Feishu bot every 3 hours.

## Project Structure

```
hotTopicScraper/
├── src/
│   ├── __init__.py
│   ├── pusher.py       # Feishu webhook pusher
│   ├── scraper.py      # X trends scraper
│   └── main.py         # Main script
├── scripts/
│   └── cron.sh         # Cron wrapper
├── docs/
│   └── deployment.md   # VPS deployment guide
├── tests/
│   └── test_scraper.py
├── requirements.txt
└── .env.example
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

## Usage

```bash
python src/main.py
```

## License

MIT
