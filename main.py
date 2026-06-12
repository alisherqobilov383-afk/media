import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message

# ================= SERVER (UPTIME) =================
# Render yoki boshqa hostinglar botni uyquga ketishdan saqlash uchun
flask_app = Flask(__name__)
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= ASOSIY BOT =================
async def main():
    # Environment variables (Render sozlamalaridan oling)
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL") # Masalan: -100123456789
    target_channel = os.environ.get("TARGET_CHANNEL") # Masalan: -100987654321

    if not all([api_id, api_hash, session_string, source_channel, target_channel]):
        print("❌ XATOLIK: Barcha kerakli ma'lumotlar kiritilmagan!")
        return

    # Userbotni ishga tushirish
    app = Client("render_userbot", api_id=int(api_id), api_hash=api_hash, session_string=session_string)

    @app.on_message(filters.chat(int(source_channel) if source_channel.startswith('-') else source_channel))
    async def forward_handler(client: Client, message: Message):
        try:
            # copy_message - barcha media va caption'ni asl holicha ko'chiradi
            await client.copy_message(
                chat_id=int(target_channel) if target_channel.startswith('-') else target_channel,
                from_chat_id=message.chat.id,
                message_id=message.id
            )
            print(f"✅ Xabar muvaffaqiyatli uzatildi: {message.id}")
        except Exception as e:
            print(f"❌ Xatolik: {e}")

    await app.start()
    print(f"🚀 Bot ishga tushdi! {source_channel} -> {target_channel}")
    # Botni to'xtamasdan ishlashini ta'minlash
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
