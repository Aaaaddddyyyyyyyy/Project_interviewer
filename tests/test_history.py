from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "candidate_002"
    }
}


saved_state = interview_graph.get_state(config)

print("\nINTERVIEW HISTORY:\n")

history = saved_state.values.get("history", [])

if not history:
    print("No interview history found.")
else:
    for item in history:

        print(f"Round: {item['round']}")
        print(f"Question: {item['question']}")
        print(f"Answer: {item['answer']}")
        print(f"Feedback: {item['feedback']}")
        print("-" * 60)