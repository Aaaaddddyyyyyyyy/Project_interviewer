from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "candidate_001"
    }
}


initial_state = {
    "question": "",
    "answer": "",
    "feedback": "",
    "history": []
}


result = interview_graph.invoke(
    initial_state,
    config=config
)


print("\nQuestion:")
print(result["question"])


saved_state = interview_graph.get_state(config)

print("\nSaved State:")
print(saved_state.values)