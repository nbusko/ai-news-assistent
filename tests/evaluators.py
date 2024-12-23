import os
from langchain import hub
from langchain_openai import ChatOpenAI


grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")


def answer_evaluator(run, example) -> dict:
    """
    A simple evaluator for RAG answer accuracy
    """

    # Get question, ground truth answer, RAG chain answer
    input_question = example.inputs["question"]
    reference = example.outputs["ground_truth"]
    prediction = run.outputs["answer"]

    # LLM grader
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("GPT_TOKEN"),
        base_url=os.getenv("BASE_GPT_URL"),
    )

    # Structured prompt
    answer_grader = grade_prompt_answer_accuracy | llm

    # Run evaluator
    score = answer_grader.invoke(
        {
            "question": input_question,
            "correct_answer": reference,
            "student_answer": prediction,
        }
    )
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}
