import subprocess
from bs4 import BeautifulSoup 
from lxml import etree 
import requests 
import re
import time
import random
import string
import asyncio
import edge_tts
import os
from datetime import datetime

# Get user input
clean_up = input("Do you want to remove audio and subs after the script ends? (Y/N):").lower() == 'y'
post_count = int(input("How many posts would like to generate?: "))

reddit_links = {}

# Function to validate Reddit link
def get_reddit_link(i):
    while True:
        link = input(f"Please input the {i}# link: ")
        if "reddit.com" in link:
            return link
        print(f"Please make sure the link {link} is correct")

# Fetch the Reddit links
for i in range(1, post_count+1):
    reddit_links[f"reddit_post{i}_link"] = get_reddit_link(i)

# Request headers
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
}

# Function to make request and parse Reddit post data
def req_reddit_post(reddit_post_link):
    try:
        webpage = requests.get(reddit_post_link, headers=headers)
        soup = BeautifulSoup(webpage.text, "html.parser")
        dom = etree.HTML(str(soup))
        return dom
    except requests.RequestException as e:
        print(f"Error fetching Reddit post: {e}")
        return None

# Fetch titles and body of posts
for i in range(1, post_count+1):
    dom = req_reddit_post(reddit_links.get(f"reddit_post{i}_link"))
    if dom is not None:
        title = dom.xpath('/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/h1')[0].text.strip()
        post_body = []
        text = dom.xpath('/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[2]/div/div')[0]
        for elements in text.xpath('.//*[not(self::a[@href])]'):
            post_body.append(elements.text.strip())

        reddit_links.update({
            f"reddit_post{i}_title": title,
            f"reddit_post{i}_body": ' '.join(post_body)
        })
    else:
        print(f"Skipping post {i} due to errors.")

# TTS generation using edge_tts
async def generate_tts(text, voice, audio_file, subtitle_file):
    try:
        communicate = edge_tts.Communicate(text, voice)
        submaker = edge_tts.SubMaker()
        with open(audio_file, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

        with open(subtitle_file, "w", encoding="utf-8") as file:
            file.write(submaker.generate_subs())
    except Exception as e:
        print(f"Error during TTS generation: {e}")

# Generate audio and subtitles for each post
for i in range(1, post_count+1):
    TEXT = reddit_links.get(f'reddit_post{i}_body')
    VOICE = "en-US-AndrewNeural"
    OUTPUT_FILE = f"audio{i}.mp3"
    WEBVTT_FILE = f"subs{i}.srt"

    if TEXT:
        asyncio.run(generate_tts(TEXT, VOICE, OUTPUT_FILE, WEBVTT_FILE))
    else:
        print(f"Skipping TTS for post {i}, no valid body text found.")

# Merge audio and video using ffmpeg
for i in range(1, post_count+1):
    print(f"Post #{i} is going to render now, please wait...")
    time.sleep(5)  # Simulate rendering delay
    os.system(f"ffmpeg -i minecraft.mp4 -i audio{i}.mp3 -vf \"subtitles=subs{i}.srt:force_style='Alignment=10,MarginV=0'\" -c:v libx264 -c:a aac -map 0:v -map 1:a -shortest result{i}.mp4")
# Cleanup if requested
if clean_up:
    for i in range(1, post_count+1):
        os.remove(f"audio{i}.mp3")
        os.remove(f"subs{i}.srt")
    print("Cleanup complete: Removed audio and subtitle files.")
else:
    print("Cleanup skipped.")
