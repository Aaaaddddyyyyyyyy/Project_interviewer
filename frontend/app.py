import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Interviewer",
    page_icon="🎯",
    layout="centered",
)


st.title("🎯 AI Technical Interviewer")

st.write(
    "Practice technical interviews with an AI interviewer."
)


# --------------------------------
# Session State
# --------------------------------

if "candidate_id" not in st.session_state:
    st.session_state.candidate_id = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "round" not in st.session_state:
    st.session_state.round = 0

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "completed" not in st.session_state:
    st.session_state.completed = False


# --------------------------------
# Candidate ID
# --------------------------------

candidate_id = st.text_input(
    "Candidate ID",
    value=st.session_state.candidate_id,
    placeholder="e.g. candidate_1001",
)


role = st.selectbox(
    "Interview Role",
    [
        "AI Engineer",
        "Python Developer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Backend Developer",
    ],
)


difficulty = st.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard",
    ],
)


interview_type = st.selectbox(
    "Interview Type",
    [
        "Technical",
        "System Design",
        "Mixed",
    ],
)


max_rounds = st.selectbox(
    "Number of Rounds",
    [
        3,
        5,
        10,
    ],
)


# --------------------------------
# Start Interview
# --------------------------------

if st.button("Start Interview"):

    if not candidate_id.strip():

        st.error("Please enter a Candidate ID.")

    else:

        try:

            response = requests.post(
    f"{API_URL}/interview/start",
    params={
        "candidate_id": candidate_id,
        "role": role,
        "difficulty": difficulty,
        "interview_type": interview_type,
        "max_rounds": max_rounds,
    },
    timeout=120,
)

            if response.status_code == 200:

                data = response.json()

                st.session_state.candidate_id = (
                    candidate_id
                )

                st.session_state.question = (
                    data["question"]
                )

                st.session_state.round = (
                    data["round"]
                )

                st.session_state.feedback = ""
                st.session_state.final_report = ""
                st.session_state.started = True
                st.session_state.completed = False

                st.rerun()

            else:

                st.error(
                    f"API Error: {response.text}"
                )

        except requests.RequestException as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# --------------------------------
# Interview
# --------------------------------

if st.session_state.started:

    st.divider()

    if not st.session_state.completed:

        st.subheader(
            f"Round {st.session_state.round}"
        )

        st.markdown(
            f"### {st.session_state.question}"
        )

        answer = st.text_area(
            "Your Answer",
            height=200,
            placeholder=(
                "Type your technical answer here..."
            ),
        )

        if st.button("Submit Answer"):

            if not answer.strip():

                st.warning(
                    "Please enter an answer."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/interview/answer",
                        params={
                            "candidate_id":
                                st.session_state.candidate_id,
                            "answer": answer,
                        },
                        timeout=120,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.feedback = (
                            data.get("feedback", "")
                        )

                        if data.get("completed"):

                            st.session_state.completed = True

                            st.session_state.final_report = (
                                data.get(
                                    "final_report",
                                    ""
                                )
                            )

                        else:

                            st.session_state.round = (
                                data["round"]
                            )

                            st.session_state.question = (
                                data["next_question"]
                            )

                        st.rerun()

                    else:

                        st.error(
                            f"API Error: {response.text}"
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )


# --------------------------------
# Feedback
# --------------------------------

if st.session_state.feedback:

    st.divider()

    st.subheader("AI Feedback")

    st.markdown(
        st.session_state.feedback
    )


# --------------------------------
# Final Report
# --------------------------------

if st.session_state.completed:

    st.divider()

    st.success(
        "🎉 Interview Completed!"
    )

    st.subheader(
        "Final Interview Report"
    )

    if st.session_state.final_report:

        st.markdown(
            st.session_state.final_report
        )

    else:

        st.warning(
            "Final report was not returned by the API."
        )


# --------------------------------
# New Interview
# --------------------------------

if st.session_state.completed:

    st.divider()

    if st.button("Start New Interview"):

        st.session_state.candidate_id = ""
        st.session_state.question = ""
        st.session_state.round = 0
        st.session_state.feedback = ""
        st.session_state.final_report = ""
        st.session_state.started = False
        st.session_state.completed = False

        st.rerun()


st.divider()

st.header("📊 Interview History")

history_candidate = st.text_input(
    "Candidate ID for History",
    value=st.session_state.candidate_id,
    key="history_candidate",
)


if st.button("Load Interview History"):

    if not history_candidate.strip():

        st.warning(
            "Please enter a Candidate ID."
        )

    else:

        try:

            response = requests.get(
                f"{API_URL}/interview/history/"
                f"{history_candidate}",
                timeout=30,
            )

            if response.status_code == 200:

                data = response.json()

                interviews = data.get(
                    "interviews",
                    []
                )

                if not interviews:

                    st.info(
                        "No interview history found."
                    )

                else:

                    for interview in interviews:

                        st.subheader(
                            f"Interview "
                            f"#{interview['interview_id']}"
                        )

                        st.write(
                            f"Role: "
                            f"{interview['role']}"
                        )

                        st.write(
                            f"Difficulty: "
                            f"{interview['difficulty']}"
                        )

                        st.write(
                            f"Type: "
                            f"{interview['interview_type']}"
                        )

                        st.write(
                            f"Status: "
                            f"{interview['status']}"
                        )

                        st.write(
                            f"Rounds: "
                            f"{interview['max_rounds']}"
                        )

                        for item in interview[
                            "answers"
                        ]:

                            with st.expander(
                                f"Round "
                                f"{item['round']}"
                            ):

                                st.markdown(
                                    "**Question**"
                                )

                                st.write(
                                    item["question"]
                                )

                                st.markdown(
                                    "**Answer**"
                                )

                                st.write(
                                    item["answer"]
                                )

                                st.markdown(
                                    "**AI Feedback**"
                                )

                                st.write(
                                    item["feedback"]
                                )

                        if interview[
                            "final_report"
                        ]:

                            st.markdown(
                                "### Final Report"
                            )

                            st.markdown(
                                interview[
                                    "final_report"
                                ]
                            )

                        st.divider()

            else:

                st.error(
                    f"API Error: "
                    f"{response.text}"
                )

        except requests.RequestException as e:

            st.error(
                f"Could not connect to API: {e}"
            )

if st.button("Resume Interview"):

    if not candidate_id.strip():

        st.error(
            "Please enter a Candidate ID."
        )

    else:

        try:

            response = requests.get(
                f"{API_URL}/interview/resume/"
                f"{candidate_id}",
                timeout=30,
            )

            if response.status_code == 200:

                data = response.json()

                if data.get(
                    "resume_available"
                ):

                    st.session_state.candidate_id = (
                        candidate_id
                    )

                    st.session_state.question = (
                        data["question"]
                    )

                    st.session_state.round = (
                        data["round"]
                    )

                    st.session_state.started = True
                    st.session_state.completed = False
                    st.session_state.feedback = ""
                    st.session_state.final_report = ""

                    st.success(
                        "Interview resumed!"
                    )

                    st.rerun()

                else:

                    st.warning(
                        data.get(
                            "message",
                            "No interview to resume."
                        )
                    )

            else:

                st.error(
                    f"API Error: "
                    f"{response.text}"
                )

        except requests.RequestException as e:

            st.error(
                f"Could not connect to API: {e}"
            )