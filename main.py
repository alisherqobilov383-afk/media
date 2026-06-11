import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityType

# Muhit o'zgaruvchilari
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Manba va maqsad kanallar
SOURCE_CHANNELS = [-1003545472423, "eltuzar_live"] 
DESTINATION_CHANNELS = [-1003797840044, "tuztuzttt"]

# StringSession ni tozalash (Renderdagi bo'sh joylarni olib tashlash uchun)
client = TelegramClient(StringSession(STRING_SESSION.strip()), API_ID, API_HASH)

def process_entities(text, entities):
    if not entities or not text:
        return text, entities
    
    # TextLink larni tekshiramiz
    for entity in entities:
        if isinstance(entity, MessageEntityType.TextLink):
            word = text[entity.offset : entity.offset + entity.length].upper()
            if any(x in word for x in ["ХАБАРИНГИЗНИ ЮБОРМОҚЧИ БЎЛСАНГИЗ УШБУ ҲАВОЛА УСТИГА БОСИНГ", "ЮБОРМОҚЧИ", "УШБУ"]):
                entity.url = "https://t.me/eltuzar_uz_bot"
            elif "LIVE" in word:
                entity.url = "https://t.me/eltuzar_livee"
            elif "MEDIA" in word:
                entity.url = "https://t.me/eltuzar_mediaa"
            elif "X" in word and len(word) == 1:
                entity.url = "https://x.com/eltuzar_uz"
            elif "INSTAGRAM" in word:
                entity.url = "https://www.instagram.com/eltuzaar_uz"
            elif "FACEBOOK" in word:
                entity.url = "https://www.facebook.com/profile.php?id=61585818251235"
    return text, entities

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_handler(event):
    try:
        new_text, new_entities = process_entities(event.message.text, event.message.entities)
        
        for dest in DESTINATION_CHANNELS:
            # forward_messages o'rniga send_message ishlatamiz, 
            # chunki faqat shu orqali havolalarni o'zgartira olamiz
            await client.send_message(
                dest,
                message=new_text or event.message.message,
                file=event.message.media,
                formatting_entities=new_entities
            )
            await asyncio.sleep(1) 
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

async def main():
    await client.start()
    print("Bot muvaffaqiyatli ishga tushdi va kuzatmoqda...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    if not API_ID or not API_HASH or not STRING_SESSION:
        print("XATOLIK: API_ID, API_HASH yoki STRING_SESSION aniqlanmagan!")
    else:
        asyncio.run(main())
