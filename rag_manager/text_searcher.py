import faiss
import numpy as np
import aiohttp
import os
import asyncio
import logging

logger = logging.getLogger(__name__)

class AsyncTextSearch:
    def __init__(self):
        self.embeddings = []
        self.texts = []
        self.index = None
        logger.info("AsyncTextSearch initialized")

    async def _get_embedding(self, texts):
        logger.info(f"Getting embedding for text: {texts}")
        url = f"{os.getenv('EMBEDDER_URL')}/search"
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'texts': texts
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as resp:
                response = await resp.json()
                return response

    async def add_texts(self, texts):
        # Асинхронное получение эмбеддингов для всех текстов
        tasks = await self._get_embedding(texts)
        new_embeddings = [emb["query_embedding"] for emb in tasks]
        # new_embeddings = await asyncio.gather(*tasks)

        self.embeddings.extend(new_embeddings)
        self.texts.extend(texts)

        # Обновление FAISS индекса
        self._update_index()

    def _update_index(self):
        # Создание или обновление FAISS индекса
        if self.index is None:
            dimension = len(self.embeddings[0])
            self.index = faiss.IndexFlatL2(dimension)
        
        # Преобразование списка эмбеддингов в numpy массив
        embeddings_array = np.array(self.embeddings).astype('float32')
        self.index.add(embeddings_array)

    async def search(self, query, top_n=5):
        # Получение эмбеддинга для запроса
        query_embedding = await self._get_embedding([query])
        query_embedding = query_embedding[0]["query_embedding"]
        # Поиск ближайших соседей
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_n)

        # Возврат текстов, соответствующих найденным индексам
        return [self.texts[idx] for idx in indices[0]]
