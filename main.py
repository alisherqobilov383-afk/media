import time
import asyncio
import os
from telethon.sync import TelegramClient
from telethon import errors
from telethon.sessions import StringSession # Bu qator qo'shildi

class TelegramForwarder:
    def __init__(self, api_id, api_hash, session_string):
        self.api_id = api_id
        self.api_hash = api_hash
        # StringSession orqali sessiyani ochish
        self.client = TelegramClient(StringSession(session_string), api_id, api_hash)

    async def list_chats(self):
        await self.client.connect()

        # Get a list of all the dialogs (chats)
        dialogs = await self.client.get_dialogs()
        # Fayl nomini o'zgartirdik (phone_number o'rniga session ishlatilgani uchun)
        chats_file = open("chats_list.txt", "w", encoding="utf-8")
        
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
            chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title} \n")
          
        print("List of groups printed successfully!")

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, keywords):
        await self.client.connect()

        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                if keywords:
                    if message.text and any(keyword in message.text.lower() for keyword in keywords):
                        print(f"Message contains a keyword: {message.text}")
                        await self.client.send_message(destination_channel_id, message.text)
                        print("Message forwarded")
                else:
                        await self.client.send_message(destination_channel_id, message.text)
                        print("Message forwarded")

                last_message_id = max(last_message_id, message.id)

            await asyncio.sleep(5)

async def main():
    # Environment o'zgaruvchilardan o'qish
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    forwarder = TelegramForwarder(api_id, api_hash, session_string)
    
    print("Choose an option:")
    print("1. List Chats")
    print("2. Forward Messages")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        await forwarder.list_chats()
    elif choice == "2":
        source_chat_id = int(input("Enter the source chat ID: "))
        destination_channel_id = int(input("Enter the destination chat ID: "))
        print("Enter keywords if you want to forward messages with specific keywords, or leave blank!")
        keywords = input("Put keywords (comma separated): ").split(",")
        
        await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id, [k.strip() for k in keywords if k.strip()])
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())
