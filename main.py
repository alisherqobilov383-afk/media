import time
import asyncio
import os
from telethon.sync import TelegramClient
from telethon import errors
from telethon.sessions import StringSession

class TelegramForwarder:
    def __init__(self, api_id, api_hash, session_string):
        self.api_id = int(api_id)
        self.api_hash = api_hash
        # StringSession orqali sessiyani ochish
        self.client = TelegramClient(StringSession(session_string), self.api_id, self.api_hash)

    async def list_chats(self):
        await self.client.connect()
        
        dialogs = await self.client.get_dialogs()
        print("--- Chatlar ro'yxati ---")
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
          
        print("--------------------------")
        print("List of groups printed successfully!")

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, keywords):
        await self.client.connect()
        
        # Oxirgi xabarni olish
        messages = await self.client.get_messages(source_chat_id, limit=1)
        last_message_id = messages[0].id if messages else 0

        print(f"Monitoring started for Chat ID: {source_chat_id}...")

        while True:
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                if message.text:
                    should_forward = False
                    if not keywords or keywords == ['']:
                        should_forward = True
                    elif any(keyword.lower() in message.text.lower() for keyword in keywords):
                        should_forward = True

                    if should_forward:
                        print(f"Forwarding message: {message.text[:50]}...")
                        await self.client.send_message(destination_channel_id, message.text)
                        print("Message forwarded!")

                last_message_id = max(last_message_id, message.id)

            await asyncio.sleep(5)

async def main():
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_HASH")
    session_string = os.environ.get("SESSION_STRING")

    if not all([api_id, api_hash, session_string]):
        print("XATOLIK: API_ID, API_HASH yoki SESSION_STRING muhit o'zgaruvchilarida topilmadi!")
        return

    try:
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
            print("Enter keywords (comma separated) or press Enter to skip:")
            keywords_input = input("Keywords: ")
            keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else []
            
            await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id, keywords)
        else:
            print("Invalid choice")
    except Exception as e:
        print(f"Dasturda xatolik yuz berdi: {e}")

if __name__ == "__main__":
    asyncio.run(main())
