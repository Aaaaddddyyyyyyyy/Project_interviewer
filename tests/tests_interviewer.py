from graph.interview_graph import interview_graph
from agents.evaluator import evaluate_answer


state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": []
}


# ==========================================
# QUESTION 1
# ==========================================

result = interview_graph.invoke(state)

question = result["question"]

print("\n================================")
print("AI INTERVIEWER")
print("================================")

print("\nQuestion 1:")
print(question)


# ==========================================
# ANSWER 1
# ==========================================

answer = input("\nYour Answer:\n")


# ==========================================
# EVALUATION 1
# ==========================================

evaluation_state = {
    "question": question,
    "answer": answer,
    "feedback": "",
    "history": []
}

evaluation = evaluate_answer(evaluation_state)

feedback = evaluation["feedback"]

print("\n================================")
print("EVALUATION")
print("================================")

print(feedback)


# ==========================================
# SAVE INTERVIEW HISTORY
# ==========================================

state["history"].append({
    "question": question,
    "answer": answer,
    "feedback": feedback
})


# ==========================================
# QUESTION 2
# ==========================================

next_state = {
    "question": question,
    "answer": answer,
    "feedback": feedback,
    "history": state["history"]
}

result = interview_graph.invoke(next_state)

next_question = result["question"]

print("\n================================")
print("AI INTERVIEWER")
print("================================")

print("\nQuestion 2:")
print(next_question)