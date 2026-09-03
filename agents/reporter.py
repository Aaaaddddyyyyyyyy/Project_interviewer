from graph.state import InterviewState
from services.llm import llm


def generate_final_report(state: InterviewState):

    history = state.get("history", [])

    interview_data = ""

    for item in history:

        interview_data += f"""
Round {item.get("round", "N/A")}

Question:
{item.get("question", "")}

Candidate Answer:
{item.get("answer", "")}

Evaluation:
{item.get("feedback", "")}

-------------------------
"""

    prompt = f"""
You are a senior technical interviewer.

Create a final assessment for the candidate based ONLY on
the interview history provided below.

Candidate Role:
{state.get("role", "Software Engineer")}

Interview Type:
{state.get("interview_type", "Technical")}

Difficulty:
{state.get("difficulty", "Medium")}

Interview History:
{interview_data}

Provide the assessment in exactly this structure:

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

Rules:
- Base the assessment only on the candidate's answers.
- Do not invent achievements or experience.
- Consider correctness, depth, reasoning, clarity, and completeness.
- Keep the assessment objective and concise.
"""

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }