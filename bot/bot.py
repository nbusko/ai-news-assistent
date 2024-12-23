import telebot
import json
import os
import requests
import asyncio
import logging

from pprint import pprint

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsBot:
    def __init__(self, bot_api_token, url):
        self.bot = telebot.TeleBot(bot_api_token)
        self._set_handlers()
        self.url = url
        logger.info("Бот инициализирован")

    def _set_handlers(self):
        @self.bot.message_handler(content_types=['text'])
        def handle_text_messages(message):
            logger.info(f"Получено сообщение: {message.text} от пользователя {message.from_user.id}")
            if len(message.text) <= 100:
                if message.text != "/start":
                    try:
                        headers = {
                            'accept': 'application/json',
                            'Content-Type': 'application/json',
                        }
                        json_data = {
                            'query': message.text
                        }
                        response = requests.post(f"{self.url}/answer", headers=headers, json=json_data)
                        result = response.json()["answer"]                     
                        logger.info(f"Ответ от сервера: {result}")
                    except Exception as e:
                        logger.error(f"Ошибка при запросе к серверу: {e}")
                        result = "Произошла ошибка при получении данных"
                else:
                    result = "Привет, ты можешь узнать у меня новости по интересующей тебя теме за указанный период времени"
            else:
                result = "Извини, но твое сообщение слишком длинное, сократи его пожалуйста"
                logger.warning("Сообщение слишком длинное")

            if isinstance(result, list):
                for r in result: 
                    self.bot.send_message(message.from_user.id, r)
                    logger.info(f"Отправлено сообщение: {r} пользователю {message.from_user.id}")
            else:
                self.bot.send_message(message.from_user.id, result)
                logger.info(f"Отправлено сообщение: {result} пользователю {message.from_user.id}")

    async def start(self):
        logger.info("Бот запущен")
        self.bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    if os.getenv("USE_BOT") == "1":
        bot = NewsBot(os.getenv("BOT_API_TOKEN"), os.getenv("RAG_MANAGER_URL"))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.start())
