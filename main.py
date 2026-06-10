import asyncio
import sys

# 1. LOOPNI KODNING ENG TEPA QISMIDA YARATAMIZ (Python 3.14 uchun shart)
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# 2. ENDI QOLGAN KUTUBXONALARNI IMPORT QILAMIZ
import os
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# ... qolgan kodlar o'zgarishsiz qoladi ...

# Render uchun web-server (UptimeRobot bilan ishlash uchun)
flask_app = Flask("")
@flask_app.route("/")
def home():
    return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# Sozlamalar
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "eltuzar_live"    # @ belgisiz
TARGET_CHANNEL = "tuztuzttt"   # @ belgisiz

# Client yaratish (StringSession xatosini oldini olish uchun .strip() qo'shildi)
app = Client(
    "render_userbot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING.strip() if SESSION_STRING else None
)

# Xabarlarni to'g'ridan-to'g'ri forward qilish (barcha turdagi xabarlar)
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_handler(client, message):
    try:
        # .copy() funksiyasi xabarni to'liq (media + caption) bilan o'tkazadi
        await message.copy(chat_id=TARGET_CHANNEL)
        print("✅ Xabar muvaffaqiyatli forward qilindi!")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

async def main():
    async with app:
        print("🚀 Bot muvaffaqiyatli ishga tushdi!")
        await asyncio.Event().wait() # Botni o'chmasligini ta'minlash

if __name__ == "__main__":
    asyncio.run(main())
