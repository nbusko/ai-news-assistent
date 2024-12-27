from langsmith import Client
from langsmith.evaluation import evaluate
import pandas as pd
from dotenv import load_dotenv

from bot_connection import predict_rag_answer, predict_rag_answer_with_context
from evaluators import answer_evaluator, answer_hallucination_evaluator, answer_helpfulness_evaluator, docs_relevance_evaluator
from dotenv import load_dotenv
load_dotenv()

client = Client()
test_db = pd.read_csv("/home/nbusko/itmo/ai-news-assistent/tests/news_query.csv", nrows=10)

dataset_name = "Test RAG system 5"
dataset = client.create_dataset(dataset_name=dataset_name)
inputs, outputs = zip(
    *[
        ({"question": row["query"]}, {"ground_truth": row["news"]})
        for _, row in test_db.iterrows()
    ]
)
client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)


answer_evaluator_results = evaluate(
    predict_rag_answer,
    data=dataset_name,
    evaluators=[answer_evaluator],
    experiment_prefix="rag-answer-v-reference",
)
answer_evaluator_scores = [
    result["evaluation_results"]["results"][0].score for result in answer_evaluator_results
]


answer_helpfulness_results = evaluate(
    predict_rag_answer,
    data=dataset_name,
    evaluators=[answer_helpfulness_evaluator],
    experiment_prefix="rag-answer-helpfulness",
)
helpfulness_scores = [
    result["evaluation_results"]["results"][0].score for result in answer_helpfulness_results
]


answer_hallucination_results = evaluate(
    predict_rag_answer_with_context, # return question, answer, contexts(list)
    data=dataset_name,
    evaluators=[answer_hallucination_evaluator],
    experiment_prefix="rag-answer-hallucination",
)
hallucination_scores = [
    result["evaluation_results"]["results"][0].score for result in answer_hallucination_results
]


docs_relevance_results = evaluate(
    predict_rag_answer_with_context,
    data=dataset_name,
    evaluators=[docs_relevance_evaluator],
    experiment_prefix="rag-doc-relevance",
)
relevance_scores = [
    result["evaluation_results"]["results"][0].score for result in docs_relevance_results
]


# Print all tests results:
print(f"Average answer evaluating: {sum(answer_evaluator_scores) / len(answer_evaluator_scores)}")
print(f"Average answer helpfulness: {sum(helpfulness_scores) / len(helpfulness_scores)}")
print(f"Average answer hallucination: {sum(hallucination_scores) / len(hallucination_scores)}")
print(f"Average docs relevance: {sum(relevance_scores) / len(relevance_scores)}")