import sys
import asyncio

# --- IMPORTDAN OLDIN LOOPNI YARATAMIZ ---
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# ----------------------------------------

# --- PYROGRAM IMPORTINI YASHIRAMIZ ---
from types import ModuleType
import pyrogram
# Pyrogram ichidagi sync modulini o'chirib tashlaymiz
sys.modules["pyrogram.sync"] = ModuleType("pyrogram.sync")

import os
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# 1. Flask Uptime Server
app_server = Flask(__name__)
@app_server.route("/")
def home(): return "Bot 24/7 ishlamoqda"

def run_server():
    app_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_server, daemon=True).start()

# 2. Bot Mantiqi
async def main():
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
    session_string = os.environ["SESSION_STRING"]
    source = os.environ["SOURCE_CHANNEL"]
    target = os.environ["TARGET_CHANNEL"]

    app = Client("userbot", api_id=api_id, api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(source))
    async def forwarder(client, message):
        try:
            await client.copy_message(target, message.chat.id, message.id)
        except Exception as e:
            print(f"Xatolik: {e}")

    await app.start()
    print("🚀 Bot ishga tushdi!")
    
    # Python 3.14 uchun loopni ushlab turish
    await asyncio.Future() 

if __name__ == "__main__":
    loop.run_until_complete(main())
