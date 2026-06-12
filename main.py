import sys
import os
import asyncio
from types import ModuleType

# PYROGRAM SYNC MODULINI BUTUNLAY O'CHIRIB TASHLAYMIZ
sys.modules["pyrogram.sync"] = ModuleType("pyrogram.sync")

from flask import Flask
from threading import Thread
from pyrogram import Client

# Server (24/7 Uptime)
app_server = Flask(__name__)
@app_server.route("/")
def home(): return "Bot ishlamoqda"

def run_server():
    app_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_server, daemon=True).start()

async def main():
    # Environment Variables
    api_id = int(os.environ.get("API_ID"))
    api_hash = os.environ.get("API_HASH")
    session = os.environ.get("SESSION_STRING")
    src = os.environ.get("SOURCE_CHANNEL")
    dst = os.environ.get("TARGET_CHANNEL")

    # Botni ishga tushirish
    client = Client("bot", api_id=api_id, api_hash=api_hash, session_string=session)

    @client.on_message(filters=None) # Barcha xabarlarni kuzatish
    async def handler(c, m):
        if str(m.chat.id) == src or m.chat.username == src.replace("@", ""):
            await c.copy_message(dst, m.chat.id, m.id)

    await client.start()
    print("Bot muvaffaqiyatli ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
