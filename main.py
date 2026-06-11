import os
import asyncio
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# ================= SERVER (UPTIME) =================
# Render botni "yotib qolmasligi" uchun oddiy web server
app_server = Flask("")
@app_server.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    app_server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# ================= ASOSIY BOT =================
async def start_bot():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")
    source_channel = os.environ.get("SOURCE_CHANNEL", "@eltuzar_live")
    target_channel = os.environ.get("TARGET_CHANNEL", "@tuztuzttt")

    if not all([api_id, api_hash, session_string]):
        print("❌ XATOLIK: API_ID, API_HASH yoki SESSION_STRING topilmadi!")
        return

    # Clientni ishga tushirish
    app = Client(
        "render_userbot", 
        api_id=int(api_id), 
        api_hash=api_hash, 
        session_string=session_string
    )

    @app.on_message(filters.chat(source_channel))
    async def forward_handler(client, message):
        try:
            # Xabarni to'g'ridan-to'g'ri forward qilish
            await message.forward(target_channel)
        except Exception as e:
            print(f"❌ Forward qilishda xatolik: {e}")

    await app.start()
    print(f"🚀 Bot ishga tushdi va 24/7 kuzatmoqda: {source_channel}")
    # Bot to'xtamasligi uchun abadiy kutish
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_bot())
