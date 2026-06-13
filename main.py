import os
import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

source = os.environ["SOURCE_CHANNEL"]
target = os.environ["TARGET_CHANNEL"]

client = TelegramClient(StringSession(session), api_id, api_hash)

# ================= LINK MAP =================
LINK_MAP = {
    "https://t.me/eltuzportali_bot": "https://t.me/eltuzar_uz_bot",
    "https://t.me/eltuzar_live": "https://t.me/eltuzar_livee",
    "instagram.com/old": "instagram.com/new"
}

def replace_links(text: str):
    if not text:
        return text

    for old, new in LINK_MAP.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)

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

# ================= SINGLE MESSAGES =================
@client.on(events.NewMessage(chats=source))
async def handler(event):
    try:
        msg = event.message

        text = replace_links(msg.text or msg.message or "")

        # TEXT
        if msg.text:
            await client.send_message(target, text)

        # PHOTO
        elif msg.photo:
            await client.send_file(target, msg.photo, caption=text)

        # VIDEO
        elif msg.video:
            await client.send_file(target, msg.video, caption=text)

        # DOCUMENT
        elif msg.document:
            await client.send_file(target, msg.document, caption=text)

        # AUDIO
        elif msg.audio:
            await client.send_file(target, msg.audio, caption=text)

        # VOICE
        elif msg.voice:
            await client.send_file(target, msg.voice, caption=text)

        # GIF
        elif msg.gif:
            await client.send_file(target, msg.gif, caption=text)

        print("OK:", msg.id)

    except Exception as e:
        print("ERROR:", e)

# ================= START =================
async def main():
    await client.start()
    print("PRO+ BOT STARTED")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
