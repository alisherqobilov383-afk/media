import os
import asyncio
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# --- Sozlamalar ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
# StringSession ishlatish uchun (avvalgi javobdagi kabi)
SESSION_STRING = os.environ.get("SESSION_STRING")

# Kanal username'lari (masalan: '@kanalnomi')
SOURCE_CHANNEL = '@eltuzar_live' 
TARGET_CHANNEL = '@tuztuzttt'

from telethon.sessions import StringSession
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- Forward logikasi ---
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        # Xabarni forward qilish
        await client.forward_messages(TARGET_CHANNEL, event.message)
        print(f"Xabar {SOURCE_CHANNEL} dan {TARGET_CHANNEL} ga forward qilindi.")
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    await client.start()
    print("Userbot muvaffaqiyatli ishga tushdi!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Flask serverini ishga tushirish
    Thread(target=run_web).start()
    # Botni ishga tushirish
    asyncio.run(main())
