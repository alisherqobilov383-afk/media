import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
session = os.environ["SESSION_STRING"]

source = os.environ.get("SOURCE_CHANNEL", "@werwe2323")
target = os.environ.get("TARGET_CHANNEL", "@wergfdgsdfsfwerw")

client = TelegramClient(StringSession(session), api_id, api_hash)

@client.on(events.NewMessage(chats=source))
async def handler(event):
    try:
        message = event.message

        # text
        if message.text:
            await client.send_message(target, message.text)

        # photo
        elif message.photo:
            await client.send_file(target, message.photo, caption=message.text or "")

        # video
        elif message.video:
            await client.send_file(target, message.video, caption=message.text or "")

        print("FORWARDED:", message.id)

    except Exception as e:
        print("ERROR:", e)


async def main():
    await client.start()
    print("BOT STARTED")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
