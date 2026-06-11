import os
import asyncio
from telethon import TelegramClient, events

# Muhit o'zgaruvchilari (Environment Variables)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Manba va maqsad kanallar (ID yoki username yozing)
SOURCE_CHANNELS = [-1003545472423, "@eltuzar_live"] 
DESTINATION_CHANNELS = [-1003797840044, "@tuztuzttt"]

# Clientni ishga tushirish
client = TelegramClient('userbot', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_handler(event):
    """
    Manba kanalga xabar kelganda, uni belgilangan maqsadli
    kanallarga forward qiladi.
    """
    try:
        for dest in DESTINATION_CHANNELS:
            # Xabarni forward qilish
            await client.forward_messages(dest, event.message)
            # Yoki faqat matn/media nusxasini yuborish uchun:
            # await client.send_message(dest, event.message)
            
            await asyncio.sleep(1) # Kanallar ko'p bo'lsa, limitga tushmaslik uchun kutish
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    await client.start()
    print("Bot muvaffaqiyatli ishga tushdi va kuzatmoqda...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
