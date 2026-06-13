import os
import asyncio
from pyrogram import Client, filters

app = Client(
    "bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    session_string=os.environ["SESSION_STRING"]
)

SOURCE = os.environ["SOURCE_CHANNEL"]
TARGET = os.environ["TARGET_CHANNEL"]

@app.on_message(filters.chat(SOURCE))
async def handler(client, message):
    try:
        await message.copy(TARGET)
        print("OK:", message.id)
    except Exception as e:
        print("ERROR:", e)


async def main():
    await app.start()
    print("BOT ISHGA TUSHDI")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
