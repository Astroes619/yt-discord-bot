# import time
# import feedparser
# import requests

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

# # 🔥 Track currently live videos (to avoid spam)
# already_live = set()


# def check_youtube():
#     global already_live

#     print("🔍 Checking YouTube...")

#     for channel in CHANNELS:
#         print(f"📺 Checking {channel['name']}")

#         feed = feedparser.parse(channel["rss"])

#         if not feed.entries:
#             continue

#         latest = feed.entries[0]  # 👈 ONLY CHECK LATEST VIDEO

#         video_id = latest.id
#         title = latest.title
#         link = latest.link

#         # 🔥 DETECT LIVE STREAM
#         # YouTube marks live streams in title OR sometimes in link/metadata
#         is_live = (
#             "live" in title.lower()
#             or "yt:livebroadcastcontent" in str(latest)
#         )

#         if is_live:
#             if video_id not in already_live:
#                 already_live.add(video_id)

#                 message = f"<@&{1406947307802591282}> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"
#                 print("📢 Sending LIVE notification...")
#                 response = requests.post(WEBHOOK_URL, json={"content": message})
#                 print("Status:", response.status_code)

#         else:
#             # 🔄 If no longer live, remove from memory
#             if video_id in already_live:
#                 already_live.remove(video_id)


# while True:
#     check_youtube()
#     time.sleep(60)

import time
import feedparser
import requests
from datetime import datetime, timezone

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


# 🔥 Track currently live videos
currently_live = set()

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

            


while True:
    check_youtube()
    time.sleep(60)