import asyncio
import sys

# 1. Eng avvalo loopni yaratamiz (Importlardan oldin!)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Keyin kutubxonalarni import qilamiz
import os
from threading import Thread
from flask import Flask

# 3. Pyrogram ni import qilamiz
from pyrogram import Client, filters, idle

# Flask serveri
app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "Userbot 24/7 ishlamoqda"

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Userbot sozlamalari
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Xabarlarni nusxalash
@app.on_message(filters.chat("eltuzar_media")) 
async def copy_handler(client, message):
    TARGET_CHAT = "eltuzar_mediaa" 
    try:
        await client.copy_message(
            chat_id=TARGET_CHAT,
            from_chat_id=message.chat.id,
            message_id=message.id
        )
    except Exception as e:
        print(f"Xatolik: {e}")

async def start_userbot():
    await app.start()
    print("Userbot muvaffaqiyatli ishga tushdi!")
    await idle()

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    # 4. Asosiy loopni ishlatamiz
    loop.run_until_complete(start_userbot())
