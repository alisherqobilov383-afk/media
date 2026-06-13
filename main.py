import os
import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================= WEB SERVER (RENDER PORT FIX) =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_web, daemon=True).start()

# ================= TELEGRAM BOT =================

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

source = os.environ["SOURCE_CHANNEL"]
target = os.environ["TARGET_CHANNEL"]

client = TelegramClient(StringSession(session), api_id, api_hash)

# ================= LINK REPLACE =================
LINK_MAP = {
    "https://t.me/eltuzportali_bot": "https://t.me/eltuzar_uz_bot",
    "https://t.me/eltuzar_live": "https://t.me/eltuzar_livee"
}

def replace_links(text):
    if not text:
        return text

    for old, new in LINK_MAP.items():
        text = text.replace(old, new)

    return text

# ================= ALBUM =================
@client.on(events.Album(chats=source))
async def album_handler(event):
    try:
        media = []
        caption = ""

        for msg in event.messages:
            text = msg.text or msg.message or ""

            if not caption:
                caption = replace_links(text)

            if msg.photo:
                media.append(msg.photo)
            elif msg.video:
                media.append(msg.video)
            elif msg.document:
                media.append(msg.document)

        await client.send_file(target, media, caption=caption)

        print("ALBUM OK")

    except Exception as e:
        print("ALBUM ERROR:", e)

# ================= NORMAL MESSAGES =================
@client.on(events.NewMessage(chats=source))
async def handler(event):
    try:
        msg = event.message

        text = replace_links(msg.text or msg.message or "")

        if msg.text:
            await client.send_message(target, text)

        elif msg.photo:
            await client.send_file(target, msg.photo, caption=text)

        elif msg.video:
            await client.send_file(target, msg.video, caption=text)

        elif msg.document:
            await client.send_file(target, msg.document, caption=text)

        elif msg.audio:
            await client.send_file(target, msg.audio, caption=text)

        elif msg.voice:
            await client.send_file(target, msg.voice, caption=text)

        print("OK:", msg.id)

    except Exception as e:
        print("ERROR:", e)

# ================= START =================
async def main():
    await client.start()
    print("BOT STARTED")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
