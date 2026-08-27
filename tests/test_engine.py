from services.interview_engine import InterviewEngine


engine = InterviewEngine(
    thread_id="test_candidate_001"
)


# ==========================================
# START INTERVIEW
# ==========================================

question = engine.start()

print("\n================================")
print("AI INTERVIEWER")
print("================================")

print("\nQuestion:")
print(question)


# ==========================================
# CANDIDATE ANSWER
# ==========================================

answer = input("\nYour Answer:\n")


# ==========================================
# EVALUATE
# ==========================================

feedback = engine.submit_answer(answer)

print("\n================================")
print("EVALUATION")
print("================================")

print(feedback)


# ==========================================
# NEXT QUESTION
# ==========================================

next_question = engine.next_question()

print("\n================================")
print("NEXT QUESTION")
print("================================")

print(next_question)


# ==========================================
# HISTORY
# ==========================================

history = engine.get_history()

print("\n================================")
print("INTERVIEW HISTORY")
print("================================")

for index, turn in enumerate(history, start=1):

    print(f"\n--- Turn {index} ---")

    print("Question:")
    print(turn["question"])

    print("\nAnswer:")
    print(turn["answer"])

    print("\nFeedback:")
    print(turn["feedback"])