from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "checkpoint_test"
    }
}


initial_state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": []
}


print("\nStarting interview...")

result = interview_graph.invoke(
    initial_state,
    config=config
)

print("\nGenerated Question:")
print(result["question"])


# Read saved checkpoint
saved_state = interview_graph.get_state(config)

print("\n==============================")
print("SAVED CHECKPOINT")
print("==============================")

print(saved_state.values)