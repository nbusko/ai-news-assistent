import logging
import asyncio
import aiohttp
import os
import json
from datetime import datetime
from text_searcher import AsyncTextSearch
from config import (
    check_date_time_prompt,
    max_new_tokens,
    map_reduce_news,
    generate_final_answer_prompt,
    is_bad_answer_prompt,
    is_no_news_prompt,
    check_bad_request_prompt
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RequestManager:
    def __init__(self):
        self.text_searcher = AsyncTextSearch()
        logger.info("RequestManager initialized")

    async def get_gpt_answer(self, messages: list) -> str:
        logger.info("Getting GPT answer")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{os.getenv('NEURAL_URL')}/generate",
                    json={
                        "messages": messages,
                        "max_new_tokens": max_new_tokens,
                    },
                ) as resp:
                    response = await resp.json()
                    logger.info(f"Response from GPT: {response}")
            except Exception as e:
                logger.error(f"Error during GPT request: {e}")
                return None

        try:
            answer = response["answer"].replace('```json\n', '').replace('\n```', '')
            logger.info(f"GPT ANSWER: {answer}")
        except Exception as e:
            logger.error(f"Error parsing GPT answer: {e}")

        return answer

    async def check_date_theme(self, query: str) -> dict:
        logger.info(f"Checking date and theme for query: {query}")
        messages = [
            {"role": "user", "content": check_date_time_prompt.format(request=query, date=datetime.now().date())}
        ]
        
        ans = await self.get_gpt_answer(messages)
        ans = json.loads(ans)
        if ans:
            logger.info(f"Date and theme info: {ans}")
            return ans
        
        logger.warning("No date or theme found")
        return {"date": "no", "theme": "no"}

    async def get_news_from_db(self, date_theme_info: dict) -> list:
        logger.info(f"Fetching news from DB with info: {date_theme_info}")
        today = datetime.now().date()
        
        if date_theme_info["date"] == "no" and date_theme_info["theme"] == "no":
            route = "get"
            params = None
        elif date_theme_info["date"] != "no" and date_theme_info["theme"] != "no":
            route = "get_by_theme_date"
            params = date_theme_info

        elif date_theme_info["date"] == "no" and date_theme_info["theme"] != "no":
            route = "get_by_theme"
            params = {"theme": date_theme_info["theme"]}

        elif date_theme_info["date"] != "no" and date_theme_info["theme"] == "no":
            route = "get_by_date"
            params = {"date": date_theme_info["date"]}

        async with aiohttp.ClientSession() as session:     
            try:
                async with session.get(
                    f"{os.getenv('DB_SERVICE_URL')}/{route}",
                    params=params,
                    headers={"accept": "application/json"}
                ) as resp:
                    news = await resp.json()
                    logger.info(f"News fetched: {news}")
                    return list(set(news["messages"]))
            except Exception as e:
                logger.error(f"Error fetching news from DB: {e}")
                return []

    async def get_top_news(self, messages: list, request: str) -> list:
        logger.info(f"Getting top news for request: {request}")
        await self.text_searcher.add_texts(messages)
        top_news = await self.text_searcher.search(request, 18)
        logger.info(f"Top news found: {top_news}")
        return top_news

    async def perfom_map(self, messages: list) -> str:
        logger.info(f"Performing map operation with messages: {messages}")
        news_answer = await self.get_gpt_answer(messages)

        logger.info(f"Map operation result: {news_answer}")
        return news_answer

    async def async_starmap(self, fn, iterable) -> list:
        logger.info("Starting async starmap operation")
        tasks = [fn(args) for args in iterable]
        results = await asyncio.gather(*tasks)
        logger.info(f"Starmap results: {results}")
        return results
    
    async def get_best_news_from_list(self, news: list, request: str, chunk_size: int = 3) -> list:
        logger.info(f"Getting best news from list for request: {request}")
        news = list(set(news))
        passages = [news[i:i + chunk_size] for i in range(0, len(news), chunk_size)]
        logger.info(f"Passages are prepared: {passages}")
        messages = [
            [
                {
                    "role": "user",
                    "content": map_reduce_news.format(request=request, news=line),
                }
            ]
            for line in passages
        ]

        map_response = await self.async_starmap(self.perfom_map, messages)
        map_response = map_response
        if map_response:
            logger.info(f"Best news found: {map_response}")
            return map_response
        logger.warning("No best news found, returning original news list")
        return news

    async def generate_final_answer(self, news: list, request: str) -> str:
        logger.info(f"Generating final answer for request: {request}")
        messages = [
            {"role": "user", "content": generate_final_answer_prompt.format(news=news, request=request)}
        ]

        ans = await self.get_gpt_answer(messages)
        logger.info(f"Final answer generated: {ans}")
        return ans.replace("**", "")

    async def check_bad_request(self, request: str) -> str:
        logger.info(f"Checking if request is bad: {request}")
        messages = [
            {"role": "user", "content": check_bad_request_prompt.format(request=request)}
        ]

        ans = await self.get_gpt_answer(messages)
        ans = json.loads(ans)
        result = ans["result"] == "no"
        logger.info(f"Request is {'bad' if result else 'good'}")
        return result
    
    async def get_full_answer(self, request: str) -> str:
        logger.info(f"Getting full answer for request: {request}")
        
        is_bad = await self.check_bad_request(request)
        if is_bad:
            logger.warning("Bad request detected")
            return is_bad_answer_prompt
        
        data = await self.check_date_theme(request)

        news = await self.get_news_from_db(data)
        if not news:
            logger.warning("No news found")
            return is_no_news_prompt
        
        faiss_news = await self.get_top_news(news, request)
        best_news = await self.get_best_news_from_list(faiss_news, request)
        final_result = await self.generate_final_answer(best_news, request)
        
        logger.info(f"Final result: {final_result}")
        return final_result

    async def get_faiss_answer(self, request: str) -> dict:
        logger.info(f"Getting full answer for request: {request}")
        
        is_bad = await self.check_bad_request(request)
        if is_bad:
            logger.warning("Bad request detected")
            return is_bad_answer_prompt
        
        data = await self.check_date_theme(request)

        news = await self.get_news_from_db(data)
        if not news:
            logger.warning("No news found")
            return is_no_news_prompt
        
        faiss_news = await self.get_top_news(news, request)
        best_news = await self.get_best_news_from_list(faiss_news, request)
        final_result = await self.generate_final_answer(best_news, request)
        
        logger.info(f"Final result: {final_result}")
        return {"map_reduced_news": best_news, "final_answer": final_result}