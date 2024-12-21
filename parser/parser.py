from telethon.sync import TelegramClient
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
import json
import os
import aiohttp

class NewsParser:
    def __init__(self, phone, api_id, api_hash, url):
        self.client = TelegramClient(phone, api_id, api_hash, system_version='4.16.30-vxCUSTOM')
        self.url = url
        
    async def start(self):
        @self.client.on(events.NewMessage(chats=self.chats))
        async def handler(message):
                message_data = {
                    "model": "mp_messages.message",
                    "fields": {
                        "id": message.id,
                        "chat_id": message.chat_id,
                        "date": message.date,
                        "message_text": message.message.text,
                        "theme": self.get_theme_by_id(message.chat_id)
                    }
                }
                json_data = json.dumps(message_data, ensure_ascii=False, default=str).replace('\\\\', '\\')

                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            f"{self.url}/update?data={json_data}"
                        ) as resp:
                        result = await resp.json()

        self.client.run_until_disconnected()

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
                            all_messages.append({
                                "model": "mp_messages.message",
                                "fields": {
                                    "id": msg.id,
                                    "chat_id": msg.chat_id,
                                    "date": msg.date,
                                    "message_text": msg.message,
                                    "theme": self.get_theme_by_id(msg.chat_id)
                                }
                            })
                    offset_id = history.messages[-1].id
                    json_data = json.dumps(all_messages, ensure_ascii=False, default=str).replace('\\\\', '\\')
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f"{self.url}/update?data={json_data}"
                        ) as resp:
                            result = await resp.json()
                    has_old_news = False
                    total_messages += len(history.messages)
                    if total_messages >= total_count_limit or has_old_news == 1:
                        break
            except Exception as e:
                print(f"Error processing chat {chat.id}: {e}")
                continue

    def get_theme_by_id(self, id):
        chat_ids = {
            "спорт": -1001167948059,
            "экономика": -1001565562058,
            "технологии": -1001551519421,
            "наука": -1001371219605,
            "нейросети": -1001466120158
        }
        inv_map = {v: k for k, v in chat_ids.items()}
        return inv_map[id]
        # for theme, chat_id in chat_ids.items():
        #     if chat_id == id:
        #         return theme

if __name__ == "__main__":
    if os.getenv("USE_PARSER") == 1:
        parser = NewsParser(os.getenv("PHONE"), os.getenv("API_ID"), os.getenv("API_HASH"), os.getenv("DB_PORT"))
        parser.start()