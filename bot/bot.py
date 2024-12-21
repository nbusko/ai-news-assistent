import telebot
import json
import os
import aiohttp

class NewsBot:
    def __init__(self, bot_api_token, url):
        self.bot = telebot.TeleBot(bot_api_token)
        self._set_handlers()
        self.url = url

    def _set_handlers(self):
        @self.bot.message_handler(content_types=['text'])
        async def handle_text_messages(message):
            if len(message.text) <= 100:
                if message.text != "/start":
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                                f"{self.url}/get?data={message.text}"
                            ) as resp:
                            result = await resp.json()

                else:
                    result = "Привет, ты можешь узнать у меня новости по интересующей тебя теме за указанный период времени"
            else:
                result = "Извини, но твое сообщение слишком длинное, сократи его пожалуйста"
            if isinstance(result, list):
                for r in result: 
                    self.bot.send_message(message.from_user.id, r)
            else:
                self.bot.send_message(message.from_user.id, result)

    async def start(self):
        self.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    bot = NewsBot(os.getenv("BOT_API_TOKEN"), os.getenv("RAG_MANAGER_PORT"))
    bot.start()