import requests
import os
from dotenv import load_dotenv
load_dotenv()

headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
}
url = f"http://localhost:{os.getenv("RAG_MANAGER_PORT")}/validate"


def predict_rag_answer(message: dict):
    json_data = {
            'query': message['question']
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    response = {'answer': response['answer']}
    return response


def predict_rag_answer_with_context(message: dict):
    json_data = {
            'query': message['question']
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    response = {
        'question': message['question'],
        'answer': response['answer'],
        'contexts': response['faiss_news']
        }
    return response

