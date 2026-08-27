from graph.interview_graph import question_graph, evaluation_graph


def main():

    state = {
        "question": "",
        "answer": "",
        "feedback": "",
        "history": [],
        "question_number": 1,
        "max_questions": 5
    }

    config = {
        "configurable": {
            "thread_id": "interview_001"
        }
    }

    print("\n================================")
    print("       AI TECHNICAL INTERVIEW")
    print("================================")

    for i in range(state["max_questions"]):

        state["question_number"] = i + 1

        # Generate question
        result = question_graph.invoke(
            state,
            config=config
        )

        question = result["question"]

        print(f"\nQuestion {i + 1}:")
        print(question)

        # Candidate answers
        answer = input("\nYour answer: ")

        # Update state
        state["question"] = question
        state["answer"] = answer

        # Evaluate answer
        result = evaluation_graph.invoke(
            state,
            config=config
        )

        print("\n---------- EVALUATION ----------")
        print(result["feedback"])
        print("--------------------------------")

        # Update state
        state["feedback"] = result["feedback"]
        state["history"] = result["history"]

    print("\n================================")
    print("       INTERVIEW COMPLETE")
    print("================================")

    print(f"\nTotal questions: {state['max_questions']}")

    print("\nInterview history:")

    for i, item in enumerate(state["history"], start=1):

        print(f"\nQuestion {i}:")
        print(item["question"])

        print("\nAnswer:")
        print(item["answer"])

        print("\nEvaluation:")
        print(item["evaluation"])


if __name__ == "__main__":
    main()