import os
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

SOURCE_CHANNEL = os.environ["SOURCE_CHANNEL"]
TARGET_CHANNEL = os.environ["TARGET_CHANNEL"]

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def new_message_handler(event):
    try:
        await client.forward_messages(
            TARGET_CHANNEL,
            event.message
        )
        print(f"Forward qilindi: {event.message.id}")

    except Exception as e:
        print(f"Xatolik: {e}")


async def main():
    await client.start()

    me = await client.get_me()
    print(f"Ishga tushdi: {me.first_name}")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
