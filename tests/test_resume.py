from langgraph.types import Command

from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "resume_test_001"
    }
}


initial_state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": [],
    "round": 1,
    "max_rounds": 3,
}


print("Starting interview...")

result = interview_graph.invoke(
    initial_state,
    config=config
)


print("\nAI QUESTION:")
print(result["question"])

print("\nGraph paused and state was saved.")


answer = input("\nYour Answer: ")


print("\nResuming interview...")


result = interview_graph.invoke(
    Command(resume=answer),
    config=config
)


print("\nFEEDBACK:")
print(result["feedback"])


print("\nCURRENT STATE:")
saved_state = interview_graph.get_state(config)

print(saved_state.values)