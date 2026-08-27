print("1. TEST STARTED")

from graph.interview_graph import interview_graph

print("2. GRAPH IMPORTED")


state = {
    "candidate_name": "Aditya",
    "role": "AI/ML Engineer",
    "experience_level": "Entry Level",

    "current_question": "What is machine learning?",

    "candidate_answer": (
        "Machine learning is a branch of AI where "
        "models learn patterns from data."
    ),

    "question_number": 1,
    "total_questions": 5,

    "conversation_history": [],

    "evaluation": "",

    "final_score": 0.0,
    "final_feedback": "",
}

print("3. STATE CREATED")
print("4. INVOKING GRAPH")

result = interview_graph.invoke(state)

print("5. GRAPH FINISHED")

print("\nQUESTION:")
print(result["current_question"])

print("\nANSWER:")
print(result["candidate_answer"])

print("\nEVALUATION:")
print(result["evaluation"])

print("\n6. TEST FINISHED")