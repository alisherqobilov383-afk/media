import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle

# Flask serveri (Render 24/7 ishlashi uchun)
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

# Handler: Manba kanaldan xabarni olib, manbani ko'rsatmasdan nusxalash
# "SOURCE_CHANNEL" o'rniga kanal username yoki ID sini yozing
@app.on_message(filters.chat("eltuzar_media")) 
async def copy_handler(client, message):
    TARGET_CHAT = "eltuzar_mediaa" # Qayerga yuborilishi
    try:
        # copy_message - manbani ko'rsatmaydi, xabarni toza nusxalaydi
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
    # Flask ni fon rejimida ishga tushiramiz
    Thread(target=run_flask, daemon=True).start()
    # Userbot ni Python 3.14+ uchun mos usulda ishga tushiramiz
    asyncio.run(start_userbot())
