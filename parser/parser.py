from telethon.sync import TelegramClient
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime
import json
import os
import aiohttp
import asyncio
import csv

class NewsParser:
    def __init__(self, phone, api_id, api_hash, url):
        self.client = TelegramClient(phone, api_id, api_hash, system_version='4.16.30-vxCUSTOM')
        self.url = url
        
    async def start(self):
        @self.client.on(events.NewMessage(chats=self.chats))
        async def handler(message):
                url = f"{os.getenv('DB_SERVICE_URL')}/update"
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                data = {
                    "chat_id": str(message.chat_id),
                    "message_id": str(message.id),
                    "content": str(message.message.text),
                    "message_date": str(datetime.strptime(str(message.date), '%Y-%m-%dT%H:%M:%S%z').date()),
                    "theme": str(self.get_theme_by_id(message.chat_id))
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as resp:
                        response = await resp.json()

        await self.client.run_until_disconnected()

    async def stop(self):
        await self.client.disconnect()

    async def parse(self, limit=100, total_count_limit=2000):
        await self.client.start()
        dialogs = await self.client.get_dialogs()
        self.chats = [dialog for dialog in dialogs if dialog.is_group or dialog.is_channel]

        for chat in self.chats:
            try:
                total_messages = 0
                offset_id = 0
                while True:
                    all_messages = []
                    history = await self.client(
                        GetHistoryRequest(peer=chat, 
                                          offset_id=offset_id, 
                                          limit=limit,
                                          offset_date=None,
                                          add_offset=0,
                                          max_id=0,
                                          min_id=0,
                                          hash=0)
                    )
                    if not history.messages:
                        break
                    for msg in history.messages:
                        
                        if msg.message:
                            all_messages.append(
                                {
                                    "message_id": str(msg.id),
                                    "chat_id": str(msg.chat_id),
                                    "message_date": str(datetime.strptime(msg.date.isoformat(), '%Y-%m-%dT%H:%M:%S%z').date()),
                                    "content": str(msg.message),
                                    "theme": self.get_theme_by_id(msg.chat_id)
                                }
                            )
                    offset_id = history.messages[-1].id
                    
                    for msg in all_messages:
                        url = f"{os.getenv('DB_SERVICE_URL')}/update"
                        headers = {
                            'accept': 'application/json',
                            'Content-Type': 'application/json'
                        }
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url, headers=headers, json=msg) as resp:
                                response = await resp.json()

                    total_messages += len(history.messages)
                    if total_messages >= total_count_limit:
                        break
            except Exception as e:
                print(f"Error processing chat {chat.id}: {e}")
                continue

    def get_theme_by_id(self, id):
        chat_ids = {
            "спорт": -1001289211298,
            "экономика": -1001565562058,
            "технологии": -1001760916140,
            "наука": -1001223201453,
            "нейросети": -1001466120158
        }
        inv_map = {v: k for k, v in chat_ids.items()}
        return inv_map[id]

if __name__ == "__main__":
    if os.getenv("USE_PARSER") == "1":
        parser = NewsParser(os.getenv("PHONE"), os.getenv("API_ID"), os.getenv("API_HASH"), os.getenv("DB_SERVICE_URL"))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(parser.parse())
        loop.run_until_complete(parser.start())