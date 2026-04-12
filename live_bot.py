

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

# # 🔥 Track currently live streams only
# currently_live = set()

# # 🌐 Flask (for UptimeRobot)
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


# # 🧠 LIVE DETECTION
# def is_live_stream(entry):
#     title = entry.title.lower()

#     # 🔥 Stronger keyword detection
#     keywords = ["live", "stream", "watching", "🔴"]

#     looks_live = any(word in title for word in keywords)

#     try:
#         published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
#         now = datetime.now(timezone.utc)
#         time_diff = (now - published).total_seconds()

#         # ⏱ shorter window (important)
#         is_recent = time_diff < 7200  # 2 hours
#     except:
#         is_recent = False

#     return looks_live and is_recent


# # 🔁 MAIN CHECK
# def check_youtube():
#     global currently_live

#     print("🔍 Checking YouTube...")

#     for channel in CHANNELS:
#         print(f"\n📺 Checking {channel['name']}")

#         feed = feedparser.parse(channel["rss"])

#         if not feed.entries:
#             print("⚠️ No entries found")
#             continue

#         # 🔥 CHECK MULTIPLE ENTRIES (FIX)
#         for entry in feed.entries[:3]:
#             video_id = entry.id
#             title = entry.title
#             link = entry.link

#             live = is_live_stream(entry)

#             # 🧪 DEBUG
#             print(f"➡️ Title: {title}")
#             print(f"➡️ Live detected: {live}")

#             # 🚀 NEW LIVE
#             if live and video_id not in currently_live:
#                 currently_live.add(video_id)

#                 message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

#                 print("📢 Sending LIVE notification...")
#                 response = requests.post(WEBHOOK_URL, json={"content": message})
#                 print("Status:", response.status_code)

#             # 🧹 STREAM ENDED
#             if not live and video_id in currently_live:
#                 print(f"🛑 {channel['name']} stream ended")
#                 currently_live.remove(video_id)


# # 🔁 LOOP
# def bot_loop():
#     while True:
#         check_youtube()
#         time.sleep(60)


# # 🚀 START
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

# 🔥 Track live + processed videos
currently_live = set()
seen_videos = set()

# 🌐 Flask keep alive
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

# 🔍 Detect LIVE stream
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
    is_recent = time_diff < 7200  # 2 hours buffer

    return looks_live and is_recent

# 🔁 Main checker
def check_youtube():
    global currently_live, seen_videos

    print("\n🔍 Checking YouTube...")

    for channel in CHANNELS:
        print(f"\n📺 Checking {channel['name']}")

        feed = feedparser.parse(channel["rss"])

        if not feed.entries:
            continue

        # 🔥 Check last 3 entries (important)
        for entry in feed.entries[:3]:
            video_id = entry.id

            if video_id in seen_videos:
                continue

            seen_videos.add(video_id)

            title = entry.title
            link = entry.link

            live = is_live_stream(entry)

            print(f"📌 Title: {title}")
            print(f"📡 Live detected: {live}")

            # 🚀 SEND ONLY IF LIVE
            if live:
                currently_live.add(video_id)

                message = f"<@&1406947307802591282> 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

                print("📢 Sending LIVE notification...")
                response = requests.post(WEBHOOK_URL, json={"content": message})
                print("✅ Status:", response.status_code)

# 🔁 Loop
def bot_loop():
    while True:
        check_youtube()
        time.sleep(60)

# 🚀 Start everything
keep_alive()

t = Thread(target=bot_loop)
t.daemon = True
t.start()

while True:
    time.sleep(1)