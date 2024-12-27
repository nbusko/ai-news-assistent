import os
from langchain import hub
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# LLM grader
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("GPT_TOKEN"),
    base_url=os.getenv("BASE_GPT_URL"),
)

grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")
grade_prompt_answer_helpfulness = prompt = hub.pull("langchain-ai/rag-answer-helpfulness")
grade_prompt_hallucinations = prompt = hub.pull("langchain-ai/rag-answer-hallucination")
grade_prompt_doc_relevance = hub.pull("langchain-ai/rag-document-relevance")


def answer_evaluator(run, example) -> dict:
    input_question = example.inputs["question"]
    reference = example.outputs["ground_truth"]
    prediction = run.outputs["answer"]

    answer_grader = grade_prompt_answer_accuracy | llm

    score = answer_grader.invoke(
        {
            "question": input_question,
            "correct_answer": reference,
            "student_answer": prediction,
        }
    )
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}


# Response vs input
def answer_helpfulness_evaluator(run, example) -> dict:
    input_question = example.inputs["question"]
    prediction = run.outputs["answer"]

    answer_grader = grade_prompt_answer_helpfulness | llm

    score = answer_grader.invoke({"question": input_question,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}


# Response vs retrieved docs
def answer_hallucination_evaluator(run, example) -> dict:
    contexts = run.outputs["contexts"]
    prediction = run.outputs["answer"]    

    answer_grader = grade_prompt_hallucinations | llm

    score = answer_grader.invoke({"documents": contexts,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_hallucination", "score": score}


# Retrieved docs vs input
def docs_relevance_evaluator(run, example) -> dict:
    input_question = example.inputs["question"]
    contexts = run.outputs["contexts"]

    answer_grader = grade_prompt_doc_relevance | llm

    score = answer_grader.invoke({"question":input_question,
                                  "documents":contexts})
    score = score["Score"]

    return {"key": "document_relevance", "score": score}
