from langsmith import Client
from langsmith.evaluation import evaluate
import pandas as pd

from bot_connection import predict_rag_answer
from evaluators import answer_evaluator


client = Client()

test_db = pd.read_csv("news_query.csv", nrows=10)

dataset_name = "Test RAG system"
dataset = client.create_dataset(dataset_name=dataset_name)
inputs, outputs = zip(
    *[
        ({"question": row["query"]}, {"ground_truth": row["news"]})
        for _, row in test_db.iterrows()
    ]
)
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)

experiment_results = evaluate(
    predict_rag_answer,
    data=dataset_name,
    evaluators=[answer_evaluator],
    experiment_prefix="rag-answer-v-reference",
)


scores = [
    result["evaluation_results"]["results"][0].score for result in experiment_results
]

# Output numerical metrics
average_score = sum(scores) / len(scores)
print(f"Average Score: {average_score}")
print(f"All Scores: {scores}")
