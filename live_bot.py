
import time
import feedparser
import requests
from datetime import datetime, timezone
from flask import Flask
from threading import Thread
import os

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

# 🔥 Tracks ONLY active live streams
currently_live = set()
app = Flask('')

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return "Bot is alive!", 200

def run():
     app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# 🔥 Track currently live videos

# 👇 ADD THIS FUNCTION RIGHT HERE
def is_live_stream(entry):
    title = entry.title.lower()
    raw = str(entry).lower()

    looks_live = (
        " live " in f" {title} "
        or "yt:livebroadcastcontent" in raw
    )

    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    time_diff = (now - published).total_seconds()
    is_recent = time_diff < 3600  # 1 hrs

    return looks_live and is_recent




def check_youtube():
    global currently_live

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

        # 🚀 CASE 1: NEW LIVE → SEND
        if live and video_id not in currently_live:
            currently_live.add(video_id)

            message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

            print("📢 Sending LIVE notification...")
            response = requests.post(WEBHOOK_URL, json={"content": message})
            print("Status:", response.status_code)

        # 🧹 CASE 2: STREAM ENDED → REMOVE
        if not live and video_id in currently_live:
            print(f"🛑 {channel['name']} stream ended")
            currently_live.remove(video_id)

            

keep_alive()

while True:
    check_youtube()
    time.sleep(60)

#monna huttak dha mandha fucking work bn

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

# # 🔥 Track live + already notified videos
# currently_live = set()
# notified_videos = set()

# # 🌐 Flask server (for uptime robot)
# app = Flask('')

# @app.route('/')
# def home():
#     return "Bot is alive!"

# def run():
#     app.run(host='0.0.0.0', port=8080)

# def keep_alive():
#     t = Thread(target=run)
#     t.start()


# # 🧠 LIVE DETECTION FUNCTION
# def is_live_stream(entry):
#     title = entry.title.lower()
#     raw = str(entry).lower()

#     # Detect "live"
#     looks_live = (
#         " live " in f" {title} "
#         or "yt:livebroadcastcontent" in raw
#     )

#     # Time check (1 hour window)
#     published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
#     now = datetime.now(timezone.utc)

#     time_diff = (now - published).total_seconds()
#     is_recent = time_diff < 3600  # 1 hour

#     return looks_live and is_recent


# # 🔁 MAIN CHECK FUNCTION
# def check_youtube():
#     global currently_live, notified_videos

#     print("🔍 Checking YouTube...")

#     for channel in CHANNELS:
#         print(f"📺 Checking {channel['name']}")

#         feed = feedparser.parse(channel["rss"])

#         if not feed.entries:
#             continue

#         latest = feed.entries[0]

#         video_id = latest.id
#         title = latest.title
#         link = latest.link

#         live = is_live_stream(latest)

#         # 🚀 CASE 1: NEW LIVE → SEND ONLY ONCE EVER
#         if live and video_id not in notified_videos:
#             notified_videos.add(video_id)
#             currently_live.add(video_id)

#             message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

#             print("📢 Sending LIVE notification...")
#             response = requests.post(WEBHOOK_URL, json={"content": message})
#             print("Status:", response.status_code)

#         # 🧹 CASE 2: STREAM ENDED → REMOVE FROM ACTIVE (but NOT notified)
#         elif not live and video_id in currently_live:
#             print(f"🛑 {channel['name']} stream ended")
#             currently_live.remove(video_id)


# # 🚀 START EVERYTHING
# keep_alive()

# while True:
#     check_youtube()
#     time.sleep(60)

# this is a beta test