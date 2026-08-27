from graph.interview_graph import interview_graph
from agents.evaluator import evaluate_answer


class InterviewEngine:

    def __init__(self, thread_id: str):

        self.thread_id = thread_id

        self.config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

    def start(self):

        initial_state = {
            "question": "",
            "answer": "",
            "feedback": "",
            "history": []
        }

        result = interview_graph.invoke(
            initial_state,
            config=self.config
        )

        return result["question"]

    def submit_answer(self, answer: str):

        current_state = interview_graph.get_state(
            self.config
        )

        state = current_state.values

        question = state["question"]

        evaluation_state = {
            "question": question,
            "answer": answer,
            "feedback": "",
            "history": state.get("history", [])
        }

        evaluation = evaluate_answer(evaluation_state)

        feedback = evaluation["feedback"]

        history = state.get("history", []).copy()

        history.append({
            "question": question,
            "answer": answer,
            "feedback": feedback
        })

        updated_state = {
            "question": question,
            "answer": answer,
            "feedback": feedback,
            "history": history
        }

        interview_graph.update_state(
            self.config,
            updated_state
        )

        return feedback

    def next_question(self):

        current_state = interview_graph.get_state(
            self.config
        )

        state = current_state.values

        result = interview_graph.invoke(
            state,
            config=self.config
        )

        return result["question"]

    def get_history(self):

        current_state = interview_graph.get_state(
            self.config
        )

        return current_state.values.get(
            "history",
            []
        )

    def get_current_state(self):

        current_state = interview_graph.get_state(
            self.config
        )

        return current_state.values