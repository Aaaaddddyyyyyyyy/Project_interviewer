from graph.interview_graph import interview_graph


config = {
    "configurable": {
        "thread_id": "candidate_003"
    }
}


result = interview_graph.invoke(
    {
        "question": "",
        "answer": "",
        "feedback": "",
        "history": [],
        "round": 1,
        "max_rounds": 3,
    },
    config=config
)


print("\nFINAL QUESTION:")
print(result["question"])

print("\nFINAL FEEDBACK:")
print(result["feedback"])

print("\nROUND:")
print(result["round"])