from graph.state import InterviewState
from services.llm import llm


def generate_final_report(state: InterviewState):

    history = state.get("history", [])

    interview_data = ""

    for item in history:

        interview_data += f"""
Round {item["round"]}

Question:
{item["question"]}

Candidate Answer:
{item["answer"]}

Evaluation:
{item["feedback"]}

-------------------------
"""

    prompt = f"""
You are a senior technical interviewer.

Create a final assessment for the candidate.

Candidate Role:
{state.get("role", "Software Engineer")}

Interview Type:
{state.get("interview_type", "Technical")}

Difficulty:
{state.get("difficulty", "Medium")}

Interview History:
{interview_data}

Provide:

Overall Score: <score>/10

Technical Performance:
<assessment>

Strengths:
- <strength>
- <strength>

Weaknesses:
- <weakness>
- <weakness>

Areas for Improvement:
- <area>
- <area>

Final Recommendation:
<Strong Hire / Hire / Needs Improvement / Reject>

Keep the assessment objective and concise.
"""

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }