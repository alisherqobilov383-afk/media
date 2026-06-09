import os
import asyncio

# 1. PYTHON 3.14 UCHUN PYROGRAM EVENT-LOOP XATOSINI TUZATISH
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message

# ================= RENDER UCHUN VEB SERVER =================
flask_app = Flask("")

@flask_app.route("/")
def home():
    return "Bot 24/7 rejimida muvaffaqiyatli ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

Thread(target=run_flask, daemon=True).start()
print("🌐 Web-server Render uchun muvaffaqiyatli ishga tushdi...")


# ================= USERBOT SOZLAMALARI =================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

SOURCE_CHANNEL = "@eltuzar_live"
TARGET_CHANNEL = "@eltuzar_livee"

app = Client("render_userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)


# ================= QO'SHIMCHA MATN =================
FOOTER_TEXT = "\n\n[ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ 👈](https://t.me/eltuzar_uz_bot)"


# ================= XABARLARNI USHLASH VA YUBORISH =================
@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_and_edit(client: Client, message: Message):
    try:
        # Matn yoki captionni yangilash
        new_text = (message.caption or message.text or "") + FOOTER_TEXT

        if message.photo:
            await client.send_photo(chat_id=TARGET_CHANNEL, photo=message.photo.file_id, caption=new_text)
            print("📸 Rasm yuborildi!")
        elif message.video:
            await client.send_video(chat_id=TARGET_CHANNEL, video=message.video.file_id, caption=new_text)
            print("🎥 Video yuborildi!")
        elif message.audio or message.voice:
            file_id = message.audio.file_id if message.audio else message.voice.file_id
            await client.send_audio(chat_id=TARGET_CHANNEL, audio=file_id, caption=new_text)
            print("🎵 Audio yuborildi!")
        elif message.text:
            await client.send_message(chat_id=TARGET_CHANNEL, text=new_text)
            print("📝 Matnli xabar yuborildi!")
    except Exception as e:
        print(f"❌ Xabar uzatishda xatolik: {e}")


# ================= BOTNI 24/7 ISHLATISH VA AVTO-RESTART =================
async def main():
    while True:
        try:
            print("🚀 Bot ishga tushirilmoqda...")
            await app.start()
            print("✅ Bot onlayn!")
            await asyncio.Future()
        except Exception as e:
            print(f"⚠️ Xatolik yuz berdi: {e}. 5 soniyadan so'ng qayta ishga tushiriladi...")
            await asyncio.sleep(5)
        finally:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
