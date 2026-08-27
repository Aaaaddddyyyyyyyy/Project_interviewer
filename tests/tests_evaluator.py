from agents.evaluator import evaluate_answer


state = {
    "candidate_name": "Aditya",
    "role": "AI/ML Engineer",
    "experience_level": "Entry Level",

    "current_question": (
        "What is the difference between supervised "
        "and unsupervised learning?"
    ),

    "candidate_answer": (
        "Supervised learning uses labeled data to learn "
        "the relationship between input and output. "
        "Unsupervised learning works with unlabeled data "
        "to find patterns or structures."
    ),

    "question_number": 1,
    "total_questions": 5,

    "conversation_history": [],

    "evaluation": "",

    "final_score": 0.0,
    "final_feedback": "",
}


result = evaluate_answer(state)

print("\nAI INTERVIEW EVALUATION")
print("=" * 50)
print(result["evaluation"])