import os
from openai import OpenAI

from config import NEURAL_MODEL

class Worker:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GPT_TOKEN"),
            base_url=os.getenv("BASE_GPT_URL"),
        )

    def answer(self, data):
        try:
            response = self.client.chat.completions.create(
                model=NEURAL_MODEL,
                messages=data.messages,
                max_tokens=data.max_new_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == "__main__":

    w = Worker()

    r = w.answer(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "how are you"
                }
            ],
            "max_new_tokens": 512
        }
    )
    print(r)