healthcheck_timeout = 30
healthcheck_sleep = 5

path_to_index = "init_data/flat.index"
# path_to_index = "/home/orange_lime/projects/ai-news-assistent/rag_engine/init_data/flat.index"

def faiss_func(x):
    return f'Новость: {x["content"]}; Тема: {x["category"]}'