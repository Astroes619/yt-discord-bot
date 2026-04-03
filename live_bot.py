import time
import feedparser
import requests

# YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCKy4l0oocEWF7El3HHV0tWg"
WEBHOOK_URL = "https://discord.com/api/webhooks/1489646556264272066/F7txI4ttaJ7KaFkHNnWk5M1WRAjiltj8LuUkmy8yvMkAuPI_6G39W1MDW8JGnanQCjSl"




CHANNELS = [
    {
        "name": "Astroes619",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCKy4l0oocEWF7El3HHV0tWg",
        "role": "1078662849133559842"
    },
    {
        "name": "GamingWithNecro",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCms_4PGXdBzVRE2m8NCFncw"
    }
]




        
posted_videos = set()
initialized = True 

def check_youtube():
    global posted_videos, initialized

    for channel in CHANNELS:
        feed = feedparser.parse(channel["rss"])

        for entry in feed.entries[:3]:
            video_id = entry.id

            # 🧠 FIRST RUN: just store videos (NO sending)
            if not initialized:
                posted_videos.add(video_id)
                continue

            # 🚀 AFTER INIT: send notifications
            if video_id not in posted_videos:
                posted_videos.add(video_id)

                title = entry.title
                link = entry.link

                message = f"Hey <@&1104153271158968461>! 🚨\n\n🔴 **{channel['name']} is now LIVE!**\n\n🎬 **{title}**\n{link}"

                requests.post(WEBHOOK_URL, json={"content": message})

    # ✅ mark initialized AFTER processing ALL channels
    initialized = True




while True:
    check_youtube()
    time.sleep(60)  # check every 1 min