from telethon.sync import TelegramClient
from telethon import events
from telethon.tl.functions.messages import GetHistoryRequest
import json
import pyodbc
from env_setup import DB_CONNECTION_STRING, API_ID, API_HASH, PHONE

class NewsParser:
    def __init__(self, db_connection_string, phone, api_id, api_hash):
        self.db_connection_string = db_connection_string
        self.client = TelegramClient(phone, api_id, api_hash, system_version='4.16.30-vxCUSTOM')

    async def start(self):
        @self.client.on(events.NewMessage(chats=self.chats))
        async def handler(message):
            with pyodbc.connect(self.db_connection_string) as conn:
                cursor = conn.cursor()
                message_data = {
                    "model": "mp_messages.message",
                    "fields": {
                        "id": message.id,
                        "chat_id": message.chat_id,
                        "date": message.date,
                        "message_text": message.message.text
                    }
                }
                sql = """\
                DECLARE @HAS_OLD_NEWS int;
                EXEC [NEWS].[dbo].[NEWS_AddNews] @HAS_OLD_NEWS OUTPUT, @JSON_DATA=?;
                SELECT @HAS_OLD_NEWS AS hasOldNews;
                """
                json_data = json.dumps(message_data, ensure_ascii=False, default=str).replace('\\\\', '\\')
                cursor.execute(sql, json_data)
                conn.commit()

        self.client.run_until_disconnected()

    async def stop(self):
        await self.client.disconnect()

    async def parse(self, limit=100, total_count_limit=2000):
        await self.client.start()
        dialogs = await self.client.get_dialogs()
        self.chats = [dialog for dialog in dialogs if dialog.is_group or dialog.is_channel]

        with pyodbc.connect(self.db_connection_string) as conn:
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
                                        "message_text": msg.message
                                    }
                                })
                        offset_id = history.messages[-1].id
                        cursor = conn.cursor()
                        sql = """\
                        DECLARE @HAS_OLD_NEWS int;
                        EXEC [NEWS].[dbo].[NEWS_AddNews] @HAS_OLD_NEWS OUTPUT, @JSON_DATA=?;
                        SELECT @HAS_OLD_NEWS AS hasOldNews;
                        """
                        json_data = json.dumps(all_messages, ensure_ascii=False, default=str).replace('\\\\', '\\')
                        cursor.execute(sql, json_data)
                        has_old_news = cursor.fetchval()
                        conn.commit()

                        total_messages += len(history.messages)
                        if total_messages >= total_count_limit or has_old_news == 1:
                            break
                except Exception as e:
                    print(f"Error processing chat {chat.id}: {e}")
                    continue