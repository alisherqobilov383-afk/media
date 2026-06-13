import os
import asyncio
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# -------- FLASK (Render port uchun) --------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ishlayapti"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# -------- TELEGRAM BOT --------
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

source = os.environ["SOURCE_CHANNEL"]
target = os.environ["TARGET_CHANNEL"]

client = TelegramClient(StringSession(session), api_id, api_hash)

@client.on(events.NewMessage(chats=source))
async def handler(event):
    try:
        msg = event.message

        if msg.text:
            await client.send_message(target, msg.text)

        elif msg.photo:
            await client.send_file(target, msg.photo, caption=msg.text or "")

        elif msg.video:
            await client.send_file(target, msg.video, caption=msg.text or "")

        print("OK:", msg.id)

    except Exception as e:
        print("ERROR:", e)

async def telegram_main():
    await client.start()
    print("BOT STARTED")
    await client.run_until_disconnected()

# -------- RUN --------
if __name__ == "__main__":
    import threading

    threading.Thread(target=run_web).start()  # Flask port ochadi
    asyncio.run(telegram_main())
