import json
import os
import gradio as gr
import os
import json
import requests

def chat_with_server(request, history):

    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": request})

    url = os.getenv("RAG_MANAGER_URL")
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    json_data = {
        'query': request,
    }
    response = requests.post(f"{url}/answer", headers=headers, json=json_data)
    return response.json()["answer"]

iface = gr.ChatInterface(fn=chat_with_server, title="Chat with AI News Assistent")

iface.launch(server_name="0.0.0.0", server_port=int(os.getenv("GRADIO_PORT")))
