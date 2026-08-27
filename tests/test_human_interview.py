from langgraph.types import Command

from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "candidate_002"
    }
}


initial_state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": [],
    "round": 1,
    "max_rounds": 3,
    "final_report": "",
}


print("\nStarting AI Interview...")


result = interview_graph.invoke(
    initial_state,
    config=config
)


while True:

    print("\n" + "=" * 60)
    print(f"ROUND {result['round']}")
    print("=" * 60)

    print("\nAI QUESTION:")
    print(result["question"])

    answer = input("\nYour Answer: ")

    result = interview_graph.invoke(
        Command(resume=answer),
        config=config
    )

    print("\nFEEDBACK:")
    print(result["feedback"])

    if result["round"] > result["max_rounds"]:

     print("\n" + "=" * 60)
     print("INTERVIEW COMPLETED")
     print("=" * 60)

     print("\nFINAL REPORT:")
     print(result["final_report"])

     break