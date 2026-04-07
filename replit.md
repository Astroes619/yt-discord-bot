# YouTube Live Stream Notifier Bot

## Overview
A Python bot that monitors YouTube channels and sends Discord notifications when a live stream starts. It uses Flask as a lightweight keep-alive web server.

## Tech Stack
- **Language:** Python 3.12
- **Web Framework:** Flask (keep-alive server on port 5000)
- **Libraries:** feedparser, requests, flask
- **Package Manager:** pip (requirements.txt)

## Project Structure
- `live_bot.py` — Main bot logic (YouTube polling + Flask keep-alive server)
- `requirements.txt` — Python dependencies
- `Procfile` — Process configuration for deployment

## How It Works
1. Flask runs in a background thread on port 5000, serving a `/` health-check endpoint
2. The main loop polls YouTube RSS feeds every 60 seconds
3. Detects live streams by checking for `yt:livebroadcastcontent` or "live" in the title (within the last hour)
4. Sends Discord notifications via webhook when a new live stream is detected
5. Tracks currently-live streams to avoid duplicate notifications

## Configuration
- `WEBHOOK_URL` — Discord webhook URL (hardcoded in live_bot.py)
- `CHANNELS` — List of YouTube channels to monitor (hardcoded in live_bot.py)
- `PORT` environment variable — Defaults to 5000

## Deployment
- Target: `vm` (always-running, needs persistent state for tracking live streams)
- Run command: `python live_bot.py`
