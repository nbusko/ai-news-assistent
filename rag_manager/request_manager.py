from text_searcher import AsyncTextSearch
from config import check_date_time_prompt, max_new_tokens

import asyncio
import aiohttp
import os
import json


class RequestManager:
    def __init__(self):
        self.text_searcher = AsyncTextSearch()

    async def get_gpt_answer(self, messages : list) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{os.getenv('NEURAL_URL')}/generate",
                json={
                    "messages": messages,
                    "max_new_tokens": max_new_tokens,
                },
            ) as resp:
                response = await resp.json()

        try:
            answer = json.loads(response["answer"])["answer"]
        except:
            answer = None

        return answer

    async def check_date_theme(self, query : str) -> dict:
        messages = [
            {"role": "user", "content": check_date_time_prompt + query} # TODO add prompts
        ]
        
        ans = await self.get_gpt_answer(messages)
        if ans:
            return ans
        
        return "no date or theme"


    async def 

