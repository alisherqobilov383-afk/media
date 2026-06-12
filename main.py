import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)

# 1. 24/7 Server
app_server = Flask(__name__)
@app_server.route("/")
def home(): return "Bot 24/7 faol"

def run_server():
    app_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_server, daemon=True).start()

# 2. Bot Mantiqi
async def main():
    # Environment Variables ni o'qish
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
    session_string = os.environ["SESSION_STRING"]
    source = os.environ["SOURCE_CHANNEL"]
    target = os.environ["TARGET_CHANNEL"]

    # Client (faqat asinxron rejimda)
    app = Client("userbot", api_id=api_id, api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source))
    async def forwarder(client, message):
        try:
            # Xabarni nusxalash
            await client.copy_message(chat_id=target, from_chat_id=message.chat.id, message_id=message.id)
        except Exception as e:
            logging.error(f"Xatolik: {e}")

    await app.start()
    logging.info("Bot muvaffaqiyatli ishga tushdi!")
    
    # 3.4+ talabiga mos kutish mexanizmi
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
