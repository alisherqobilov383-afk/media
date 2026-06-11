import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import events

# Muhit o'zgaruvchilari
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Manba va maqsad kanallar
SOURCE_CHANNELS = [-1003545472423, "eltuzar_live"] 
DESTINATION_CHANNELS = [-1003797840044, "tuztuzttt"]

# Clientni ishga tushirish (StringSession dan foydalanish shart!)
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_handler(event):
    try:
        for dest in DESTINATION_CHANNELS:
            await client.forward_messages(dest, event.message)
            await asyncio.sleep(1) 
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    # StringSession bo'lsa, start() hech narsa so'ramasdan ulanadi
    await client.start()
    print("Bot muvaffaqiyatli ishga tushdi va kuzatmoqda...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    if not API_ID or not API_HASH or not STRING_SESSION:
        print("XATOLIK: API_ID, API_HASH yoki STRING_SESSION aniqlanmagan!")
    else:
        asyncio.run(main())
