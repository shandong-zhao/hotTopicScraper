# VPS Deployment Guide

## Prerequisites

- VPS with public IP (Ubuntu 20.04+ recommended)
- SSH access configured
- Feishu bot webhook URL

## Step 1: Clone the Repository

```bash
cd ~/
git clone https://github.com/shandong-zhao/hotTopicScraper.git
cd hotTopicScraper
```

## Step 2: Install Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
cp .env.example .env
nano .env
# Set FEISHU_WEBHOOK_URL
```

## Step 4: Set Up Feishu Bot

1. Open Feishu → **Settings** → **Bots** → **Create Bot**
2. Copy the **Webhook URL** from bot settings
3. Paste into `.env` as `FEISHU_WEBHOOK_URL`

## Step 5: Set Up Cron Job

```bash
# Edit crontab
crontab -e

# Add this line for every 3 hours
0 */3 * * * /opt/hotTopicScraper/scripts/cron.sh
```

## Step 6: Create Log Directory

```bash
sudo mkdir -p /var/log
sudo chown $USER /var/log/hotTopicScraper.log
```

## Step 7: Test It

```bash
source venv/bin/activate
python3 src/main.py
```

## Troubleshooting

### Nitter instances are blocked
If all Nitter instances fail, try:
- Using a proxy in the scraper
- Switching to a different Nitter mirror

### Feishu webhook fails
- Verify the webhook URL is correct
- Check if the bot has permission to send messages
- Test with: `curl -X POST <WEBHOOK_URL> -H "Content-Type: application/json" -d '{"msg_type":"text","content":{"text":"test"}}'`
