import requests
import os


headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
}
url = f"http://localhost:{os.getenv("RAG_MANAGER_PORT")}/answer"


def predict_rag_answer(message: dict):
    json_data = {
            'query': message['question']
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    response = {'answer': response['answer']}
    return response.json()


def predict_rag_answer_with_context(message: dict):
    json_data = {
            'query': message['question']
    }
    response = requests.post(url, headers=headers, json=json_data).json()
    response = {
        'question': message['question'],
        'answer': response['answer'],
        'context': response['faiss_news']
        }
    return response.json()

