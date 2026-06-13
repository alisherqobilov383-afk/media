import sys
import os
import asyncio
import copy
from threading import Thread

# PYROGRAM SYNC PATCH (Python 3.14 uchun)
class FakeSync:
    def __getattr__(self, name):
        return None

sys.modules["pyrogram.sync"] = FakeSync()

from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

# ================= FLASK =================

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot ishlayapti"

def run_flask():
    flask_app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

Thread(target=run_flask, daemon=True).start()

# ================= TEXT EDIT =================

def edit_caption_text(message: Message):
    text = message.caption or message.text

    if not text:
        return "", []

    entities = copy.deepcopy(
        message.caption_entities or message.entities or []
    )

    for entity in entities:
        if entity.type == MessageEntityType.TEXT_LINK:

            word = text[
                entity.offset:
                entity.offset + entity.length
            ].upper()

            if any(
                x in word for x in [
                    "ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ",
                    "ЮБОРМОҚЧИ",
                    "УШБУ"
                ]
            ):
                entity.url = "https://t.me/eltuzar_uz_bot"

            elif "LIVE" in word:
                entity.url = "https://t.me/eltuzar_livee"

            elif "MEDIA" in word:
                entity.url = "https://t.me/eltuzar_media"

            elif "X" == word:
                entity.url = "https://x.com/eltuzar_uz"

            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"

            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"

    return text, entities

# ================= BOT =================

async def start_bot():

    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    source_channel = os.environ.get(
        "SOURCE_CHANNEL",
        "@eltuzar_live"
    )

    target_channel = os.environ.get(
        "TARGET_CHANNEL",
        "@eltuzar_livee"
    )

    app = Client(
        "render_userbot",
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string
    )

    @app.on_message()
    async def debug_all(client, message):

        try:
            print(
                f"POST => "
                f"CHAT_ID={message.chat.id} | "
                f"USERNAME={message.chat.username} | "
                f"TITLE={message.chat.title} | "
                f"MSG_ID={message.id}"
            )
        except Exception as e:
            print("DEBUG ERROR:", e)

    @app.on_message(filters.chat(source_channel))
    async def forward_post(client, message):

        print(
            f"TARGET TOPILDI => "
            f"{message.chat.title} | "
            f"{message.id}"
        )

        try:

            new_text, new_entities = edit_caption_text(message)

            if message.photo:

                await client.send_photo(
                    target_channel,
                    photo=message.photo.file_id,
                    caption=new_text,
                    caption_entities=new_entities
                )

            elif message.video:

                await client.send_video(
                    target_channel,
                    video=message.video.file_id,
                    caption=new_text,
                    caption_entities=new_entities
                )

            elif message.audio:

                await client.send_audio(
                    target_channel,
                    audio=message.audio.file_id,
                    caption=new_text,
                    caption_entities=new_entities
                )

            elif message.voice:

                await client.send_voice(
                    target_channel,
                    voice=message.voice.file_id,
                    caption=new_text,
                    caption_entities=new_entities
                )

            elif message.document:

                await client.send_document(
                    target_channel,
                    document=message.document.file_id,
                    caption=new_text,
                    caption_entities=new_entities
                )

            elif message.text:

                await client.send_message(
                    target_channel,
                    text=new_text,
                    entities=new_entities
                )

            print("SUCCESS")

        except Exception as e:
            print("SEND ERROR:", repr(e))

    await app.start()

    me = await app.get_me()

    print("=" * 50)
    print("USERBOT ISHGA TUSHDI")
    print("USER:", me.first_name)
    print("SOURCE:", source_channel)
    print("TARGET:", target_channel)
    print("=" * 50)

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_bot())
