import os
import asyncio
import sys
from types import ModuleType

# 1. Pyrogram sync modulini bloklash
sys.modules["pyrogram.sync"] = ModuleType("pyrogram.sync")

# 2. Event loopni oldindan tayyorlab olish
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# Server (Uptime)
flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

async def main():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL")
    target_channel = os.environ.get("TARGET_CHANNEL")

    if not all([api_id, api_hash, session_string, source_channel, target_channel]):
        print("❌ XATOLIK: Muhit o'zgaruvchilari to'liq emas!")
        return

    # Userbotni ishga tushirish
    app = Client("my_bot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source_channel))
    async def forward_handler(client, message):
        try:
            print(f"📥 Yangi xabar keldi: {message.id}")
            await client.copy_message(chat_id=target_channel, from_chat_id=message.chat.id, message_id=message.id)
            print(f"✅ Muvaffaqiyatli uzatildi!")
        except Exception as e:
            print(f"❌ Xatolik: {e}")

    await app.start()
    print(f"🚀 Bot ishga tushdi: {source_channel} -> {target_channel}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    # O'zimiz yaratgan loopdan foydalanamiz
    loop.run_until_complete(main())
