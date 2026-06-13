import sys
import os
import asyncio
import copy
from threading import Thread
from flask import Flask

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# PYROGRAM FIX (3.14 uchun)
class FakeSync:
    def __getattr__(self, name):
        return None

sys.modules["pyrogram.sync"] = FakeSync()

# ================= FLASK =================
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot ishlayapti"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

Thread(target=run_flask, daemon=True).start()

# ================= BOT =================
async def start_bot():

    print("START FUNCTION CHAQLANDI")

    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    session_string = os.getenv("SESSION_STRING")

    source = os.getenv("SOURCE_CHANNEL", "@eltuzar_live")
    target = os.getenv("TARGET_CHANNEL", "@eltuzar_livee")

    if not api_id or not api_hash or not session_string:
        print("❌ ENV YO‘Q (API_ID / API_HASH / SESSION_STRING)")
        return

    app = Client(
        "bot",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string
    )

    @app.on_message()
    async def debug(_, m):
        try:
            print("POST:", m.chat.id, m.chat.username)
        except:
            pass

    @app.on_message(filters.chat(source))
    async def forward(_, m):

        print("TARGET TOPILDI")

        try:
            text = m.caption or m.text or ""

            if m.photo:
                await app.send_photo(target, m.photo.file_id, caption=text)

            elif m.video:
                await app.send_video(target, m.video.file_id, caption=text)

            elif m.text:
                await app.send_message(target, text)

            print("SUCCESS")

        except Exception as e:
            print("ERROR:", repr(e))

    await app.start()

    me = await app.get_me()
    print("LOGGED IN:", me.first_name)

    while True:
        await asyncio.sleep(3600)

# ================= RUN =================
if __name__ == "__main__":
    print("MAIN START")
    asyncio.run(start_bot())
