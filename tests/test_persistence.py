from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "persistence_test_001"
    }
}


initial_state = {
    "question": "Test question",
    "answer": "This is a test answer.",
    "feedback": "Test feedback",
    "history": [],
    "round": 1,
    "max_rounds": 3,
}


print("Running graph...")

result = interview_graph.invoke(
    initial_state,
    config=config
)

print("\nGraph result:")
print(result)

print("\nReading saved state...")

saved_state = interview_graph.get_state(config)

print("\nSaved state:")
print(saved_state.values)

print("\nCheckpoint next:")
print(saved_state.next)