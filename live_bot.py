


# import time
# import feedparser
# import requests
# from datetime import datetime, timezone
# from flask import Flask
# from threading import Thread

# WEBHOOK_URL = "https://discord.com/api/webhooks/1489646556264272066/F7txI4ttaJ7KaFkHNnWk5M1WRAjiltj8LuUkmy8yvMkAuPI_6G39W1MDW8JGnanQCjSl"

# CHANNELS = [
#     {
#         "name": "Astroes619",
#         "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCKy4l0oocEWF7El3HHV0tWg"
#     },
#     {
#         "name": "GamingWithNecro",
#         "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCms_4PGXdBzVRE2m8NCFncw"
#     }
# ]

# # 🔥 Track live + processed videos
# currently_live = set()

# # 🌐 Flask keep alive
# app = Flask('')

# @app.route('/', methods=['GET', 'HEAD'])
# def home():
#     return "Bot is alive!", 200

# def run():
#     app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

# def keep_alive():
#     t = Thread(target=run)
#     t.daemon = True
#     t.start()

# # 🔍 Detect LIVE stream
# def is_live_stream(entry):
#     title = entry.title.lower()
#     raw = str(entry).lower()

#     looks_live = (
#         " live " in f" {title} "
#         or "yt:livebroadcastcontent" in raw
#     )

#     published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
#     now = datetime.now(timezone.utc)

#     time_diff = (now - published).total_seconds()
#     is_recent = time_diff < 7200  # 2 hours buffer

#     return looks_live and is_recent

# # 🔁 Main checker
# def check_youtube():
#     global currently_live, seen_videos

#     print("\n🔍 Checking YouTube...")

#     for channel in CHANNELS:
#         print(f"\n📺 Checking {channel['name']}")

#         feed = feedparser.parse(channel["rss"])

#         if not feed.entries:
#             continue

#         # 🔥 Check last 3 entries (important)
#         for entry in feed.entries[:3]:
#             video_id = entry.id
#             title = entry.title
#             link = entry.link

#             live = is_live_stream(entry)

#             print(f"📌 Title: {title}")
#             print(f"📡 Live detected: {live}")

#             # 🚀 CASE 1: NEW LIVE → SEND
#             if live and video_id not in currently_live:
#                 currently_live.add(video_id)

#                 message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

#                 print("📢 Sending LIVE notification...")
#                 response = requests.post(WEBHOOK_URL, json={"content": message})
#                 print("✅ Status:", response.status_code)

#             # 🧹 CASE 2: STREAM ENDED → REMOVE
#             elif not live and video_id in currently_live:
#                 print(f"🛑 Stream ended for {channel['name']}")
#                 currently_live.remove(video_id)
# # 🔁 Loop
# def bot_loop():
#     while True:
#         check_youtube()
#         time.sleep(60)

# # 🚀 Start everything
# keep_alive()

# t = Thread(target=bot_loop)
# t.daemon = True
# t.start()

# while True:
#     time.sleep(1)


import time
import feedparser
import requests
from datetime import datetime, timezone
from flask import Flask
from threading import Thread
import os
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1489646556264272066/F7txI4ttaJ7KaFkHNnWk5M1WRAjiltj8LuUkmy8yvMkAuPI_6G39W1MDW8JGnanQCjSl"

CHANNELS = [
    {
        "name": "Astroes619",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCKy4l0oocEWF7El3HHV0tWg"
    },
    {
        "name": "GamingWithNecro",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCms_4PGXdBzVRE2m8NCFncw"
    }
]

# 🔥 Track state
currently_live = set()
sent_notifications = set()

# 📁 Persistent storage (prevents duplicates after restart)
def save_sent():
    with open("sent.json", "w") as f:
        json.dump(list(sent_notifications), f)

def load_sent():
    global sent_notifications
    try:
        with open("sent.json", "r") as f:
            sent_notifications = set(json.load(f))
    except:
        sent_notifications = set()

# 🌐 Flask server (for uptime)
app = Flask('')

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return "Bot is alive!", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 🔍 Detect live stream properly
def is_live_stream(entry):
    title = entry.title.lower()
    raw = str(entry).lower()

    looks_live = (
        " live " in f" {title} " or
        "🔴" in title or
        "yt:livebroadcastcontent" in raw
    )

    # Ensure it's recent (avoid old uploads)
    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    time_diff = (now - published).total_seconds()
    is_recent = time_diff < 7200  # 2 hours window

    return looks_live and is_recent

# 🚀 Main logic (NO DUPLICATES EVER)
def check_youtube():
    global currently_live, sent_notifications

    print("🔍 Checking YouTube...")

    for channel in CHANNELS:
        print(f"📺 Checking {channel['name']}")

        feed = feedparser.parse(channel["rss"])

        if not feed.entries:
            continue

        latest = feed.entries[0]

        video_id = latest.id
        title = latest.title
        link = latest.link

        live = is_live_stream(latest)

        print(f"Title: {title}")
        print(f"Live detected: {live}")

        # 🚀 SEND ONLY ONCE EVER
        if live and video_id not in sent_notifications:
            print("📢 Sending LIVE notification...")

            message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

            response = requests.post(WEBHOOK_URL, json={"content": message})
            print("Status:", response.status_code)

            # 🔒 Lock forever
            sent_notifications.add(video_id)
            currently_live.add(video_id)
            save_sent()

        # 🧹 Track state (no sending)
        if live:
            currently_live.add(video_id)
        else:
            if video_id in currently_live:
                print(f"🛑 Stream ended for {channel['name']}")
                currently_live.remove(video_id)

# 🔁 Loop
def bot_loop():
    while True:
        check_youtube()
        time.sleep(60)  # check every 1 min

# 🚀 Start everything
load_sent()
keep_alive()

t = Thread(target=bot_loop)
t.daemon = True
t.start()

# Keep main thread alive
while True:
    time.sleep(1)
