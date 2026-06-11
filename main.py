import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render'dan o'zgaruvchilarni olish
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Manba va maqsad kanallar
# Kanal ID'lari yoki usernamelarini shu yerga qo'ying
SOURCE_CHANNELS = [-1003545472423, "eltuzar_live"] 
DESTINATION_CHANNELS = [-1003797840044, "tuztuzttt"]

# Clientni ishga tushirish
client = TelegramClient(StringSession(STRING_SESSION.strip()), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_handler(event):
    for dest in DESTINATION_CHANNELS:
        try:
            # Shunchaki forward qilish
            await client.forward_messages(dest, event.message)
            # Spamga tushmaslik uchun kichik tanaffus
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Xabar yuborishda xatolik: {e}")

async def main():
    await client.start()
    print("Bot 24/7 rejimda ishlamoqda...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    if not API_ID or not API_HASH or not STRING_SESSION:
        print("XATOLIK: API_ID, API_HASH yoki STRING_SESSION topilmadi!")
    else:
        asyncio.run(main())
