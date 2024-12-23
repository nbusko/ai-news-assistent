import requests
import os


def predict_rag_answer(message: dict):
    headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
    }
    json_data = {
                'query': message['question']
    }

    url = f"http://localhost:{os.getenv("RAG_MANAGER_PORT")}/answer"
    response = requests.post(url, headers=headers, json=json_data)
    return response.json()


def predict_rag_answer_with_context(example: dict):
    """Use this for evaluation of retrieved documents and hallucinations"""
    pass

