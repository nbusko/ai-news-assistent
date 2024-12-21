import gradio as gr
import aiohttp
import ast

async def chat_with_server(user_input, history):
    # Send user input to the server
    url = os.getenv("RAG_MANAGER_PORT")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/get?data={user_input}") as resp:
            response = await resp.json()

    # Update chat history
    history.append({"role": "user", "content": user_input})
    history.append({"role": "bot", "content": response})

    # Save history in cookies
    gr.set_cookie('chat_history', str(history))

    return response, history

def get_initial_history():
    # Retrieve chat history from cookies if available
    history_str = gr.get_cookie('chat_history', default='[]')
    return ast.literal_eval(history_str)

iface = gr.Interface(
    fn=chat_with_server,
    inputs=[
        gr.inputs.Textbox(label="Your Message"),
        gr.inputs.State(get_initial_history, label="Chat History")
    ],
    outputs=[
        gr.outputs.Textbox(label="Bot Response"),
        gr.outputs.State(label="Updated History")
    ],
    live=False
)

iface.launch()
