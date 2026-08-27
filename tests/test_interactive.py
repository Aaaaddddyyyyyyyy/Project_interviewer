from graph.interview_graph import interview_graph
from graph.evaluation_graph import evaluation_graph


config = {
    "configurable": {
        "thread_id": "candidate_1"
    }
}


state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": []
}


print("\n==============================")
print("AI TECHNICAL INTERVIEW")
print("==============================")


# Generate first question
result = interview_graph.invoke(
    state,
    config=config
)


while True:

    print("\nQuestion:")
    print(result["question"])

    answer = input("\nYour Answer: ")

    if answer.lower() == "exit":
        print("\nInterview ended.")
        break

    # Evaluate + save history
    result = evaluation_graph.invoke(
        {
            "question": result["question"],
            "answer": answer,
            "feedback": "",
            "history": result.get("history", [])
        },
        config=config
    )

    print("\n------------------------------")
    print("FEEDBACK")
    print("------------------------------")

    print(result["feedback"])

    print("\nQuestions answered:",
          len(result["history"]))

    # Generate next question
    result = interview_graph.invoke(
        {
            "question": result["question"],
            "answer": answer,
            "feedback": result["feedback"],
            "history": result["history"]
        },
        config=config
    )