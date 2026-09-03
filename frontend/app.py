import base64
import json
import requests
import streamlit as st

from frontend.audio_recorder import record_and_transcribe
from frontend.video_recorder import record_interview_video


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Interviewer",
    page_icon="🎯",
    layout="centered",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "token": None,
    "candidate_id": "",
    "question": "",
    "round": 0,
    "feedback": "",
    "final_report": "",
    "started": False,
    "completed": False,
    "interview_id": None,
    "history": [],
    "interview_audio_frames": [],
    "interview_video_path": "",
    "video_analysis": None,
}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_auth_headers():

    token = st.session_state.get("token")

    if not token:
        return {}

    return {
        "Authorization": f"Bearer {token}"
    }


def decode_jwt_candidate_id(token):

    """
    Extract candidate_id from JWT payload.

    This does NOT verify the JWT.
    JWT verification is handled by the backend.
    """

    try:

        payload = token.split(".")[1]

        padding = "=" * (
            4 - len(payload) % 4
        )

        decoded = base64.urlsafe_b64decode(
            payload + padding
        )

        data = json.loads(
            decoded.decode("utf-8")
        )

        return data.get("sub", "")

    except Exception:

        return ""


def handle_unauthorized():

    st.session_state.token = None
    st.session_state.candidate_id = ""
    st.session_state.question = ""
    st.session_state.round = 0
    st.session_state.feedback = ""
    st.session_state.final_report = ""
    st.session_state.started = False
    st.session_state.completed = False
    st.session_state.interview_id = None
    st.session_state.interview_audio_frames = []
    st.session_state.interview_video_path = ""
    st.session_state.video_analysis = None

    if "current_answer" in st.session_state:

        del st.session_state.current_answer

    st.rerun()


def logout():

    for key, value in DEFAULT_STATE.items():

        st.session_state[key] = value

    if "current_answer" in st.session_state:

        del st.session_state.current_answer

    st.rerun()


def reset_interview():

    st.session_state.question = ""
    st.session_state.round = 0
    st.session_state.feedback = ""
    st.session_state.final_report = ""
    st.session_state.started = False
    st.session_state.completed = False
    st.session_state.interview_id = None
    st.session_state.interview_audio_frames = []
    st.session_state.interview_video_path = ""
    st.session_state.video_analysis = None

    if "current_answer" in st.session_state:

        del st.session_state.current_answer

    if "video_recording_id" in st.session_state:

        del st.session_state.video_recording_id


# ============================================================
# VIDEO ANALYSIS HELPER
# ============================================================

def analyze_current_video():

    video_path = st.session_state.get(
        "interview_video_path",
        ""
    )

    if not video_path:

        return None

    try:

        response = requests.post(
            f"{API_URL}/interview/video-analysis",
            params={
                "video_path": video_path
            },
            headers=get_auth_headers(),
            timeout=180,
        )

        if response.status_code == 200:

            data = response.json()

            analysis = data.get(
                "video_analysis",
                {}
            )

            st.session_state.video_analysis = analysis

            return analysis

        if response.status_code == 401:

            st.error(
                "Your session has expired. Please log in again."
            )

            handle_unauthorized()

            return None

        st.error(
            f"Video analysis failed "
            f"(HTTP {response.status_code}): "
            f"{response.text}"
        )

        return None

    except requests.RequestException as e:

        st.error(
            f"Could not connect to FastAPI for video analysis: {e}"
        )

        return None

    except Exception as e:

        st.error(
            f"Video analysis failed: {e}"
        )

        return None


# ============================================================
# LOGIN / REGISTRATION
# ============================================================

if not st.session_state.token:

    st.title("🎯 AI Technical Interviewer")

    st.write(
        "Practice technical interviews with an AI interviewer."
    )

    tab_login, tab_register = st.tabs(
        [
            "Login",
            "Create Account",
        ]
    )

    # ========================================================
    # LOGIN
    # ========================================================

    with tab_login:

        st.subheader("Login")

        login_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="login_email",
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button(
            "Login",
            type="primary",
            use_container_width=True,
        ):

            if not login_email.strip():

                st.error(
                    "Please enter your email."
                )

            elif not login_password:

                st.error(
                    "Please enter your password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "email": login_email.strip(),
                            "password": login_password,
                        },
                        timeout=30,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        token = data.get(
                            "access_token"
                        )

                        if not token:

                            st.error(
                                "Login succeeded but no token was returned."
                            )

                        else:

                            candidate_id = (
                                decode_jwt_candidate_id(
                                    token
                                )
                            )

                            if not candidate_id:

                                st.error(
                                    "Login succeeded, but candidate identity could not be read from the token."
                                )

                            else:

                                st.session_state.token = token

                                st.session_state.candidate_id = (
                                    candidate_id
                                )

                                st.success(
                                    "Login successful!"
                                )

                                st.rerun()

                    else:

                        try:

                            detail = response.json().get(
                                "detail",
                                response.text,
                            )

                        except Exception:

                            detail = response.text

                        st.error(
                            f"Login failed: {detail}"
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )


    # ========================================================
    # REGISTRATION
    # ========================================================

    with tab_register:

        st.subheader("Create Account")

        register_candidate_id = st.text_input(
            "Candidate ID",
            placeholder="e.g. candidate_1001",
            key="register_candidate_id",
        )

        register_email = st.text_input(
            "Email",
            placeholder="you@example.com",
            key="register_email",
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )

        register_password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="register_password_confirm",
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True,
        ):

            if not register_candidate_id.strip():

                st.error(
                    "Please enter a Candidate ID."
                )

            elif not register_email.strip():

                st.error(
                    "Please enter your email."
                )

            elif not register_password:

                st.error(
                    "Please enter a password."
                )

            elif register_password != register_password_confirm:

                st.error(
                    "Passwords do not match."
                )

            elif len(register_password) < 8:

                st.error(
                    "Password must contain at least 8 characters."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "candidate_id": register_candidate_id.strip(),
                            "email": register_email.strip(),
                            "password": register_password,
                        },
                        timeout=30,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        token = data.get(
                            "access_token"
                        )

                        if token:

                            st.session_state.token = token

                            st.session_state.candidate_id = (
                                register_candidate_id.strip()
                            )

                            st.success(
                                "Account created successfully!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "Account created but no token was returned."
                            )

                    else:

                        try:

                            detail = response.json().get(
                                "detail",
                                response.text,
                            )

                        except Exception:

                            detail = response.text

                        st.error(
                            f"Registration failed: {detail}"
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )

    st.stop()


# ============================================================
# AUTHENTICATED APPLICATION
# ============================================================

st.title("🎯 AI Technical Interviewer")

st.write(
    "Practice technical interviews with an AI interviewer."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Candidate")

    st.write(
        f"**ID:** {st.session_state.candidate_id}"
    )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        logout()


# ============================================================
# ACTIVE INTERVIEW
# ============================================================

if st.session_state.started:

    st.divider()

    st.subheader(
        f"Round {st.session_state.round}"
    )

    if st.session_state.question:

        st.markdown(
            f"### {st.session_state.question}"
        )


    if not st.session_state.completed:

        # ====================================================
        # CAMERA RECORDING
        # ====================================================

        record_interview_video()

        st.markdown("---")


        # ====================================================
        # TEXT ANSWER
        # ====================================================

        answer = st.text_area(
            "Your Answer",
            height=200,
            placeholder="Type your technical answer here...",
            key="current_answer",
        )

        st.markdown("---")


        # ====================================================
        # VOICE ANSWER
        # ====================================================

        record_and_transcribe()


        # Get the latest answer after transcription.

        answer = st.session_state.get(
            "current_answer",
            answer,
        )

        st.markdown("---")


        # ====================================================
        # VIDEO STATUS
        # ====================================================

        video_path = st.session_state.get(
            "interview_video_path",
            "",
        )

        if video_path:

            st.success(
                "🎥 Interview video is ready for analysis."
            )

            st.caption(
                f"Video: {video_path}"
            )

        else:

            st.info(
                "🎥 No completed video recording detected yet."
            )


        # ====================================================
        # SUBMIT ANSWER
        # ====================================================

        if st.button(
            "Submit Answer",
            type="primary",
            use_container_width=True,
        ):

            if not answer.strip():

                st.warning(
                    "Please enter or record an answer."
                )

            else:

                # =================================================
                # STEP 1 — ANALYZE VIDEO FIRST
                # =================================================

                video_path = st.session_state.get(
                    "interview_video_path",
                    "",
                )

                if video_path:

                    st.info(
                        "🎥 Analyzing your interview video..."
                    )

                    with st.spinner(
                        "Running face and video analysis..."
                    ):

                        analysis = analyze_current_video()

                    if analysis:

                        st.success(
                            "✅ Video analysis completed."
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.metric(
                                "Face Visibility",
                                f"{analysis.get('face_visibility_percentage', 0)}%"
                            )

                            st.metric(
                                "Video Duration",
                                f"{analysis.get('duration_seconds', 0)} sec"
                            )

                            st.metric(
                                "FPS",
                                analysis.get("fps", 0)
                            )

                        with col2:

                            st.metric(
                                "Resolution",
                                f"{analysis.get('width', 0)} × {analysis.get('height', 0)}"
                            )

                            st.metric(
                                "Frames Analyzed",
                                analysis.get(
                                    "analyzed_frames",
                                    0
                                )
                            )

                            st.metric(
                                "Face Detected Frames",
                                analysis.get(
                                    "face_detected_frames",
                                    0
                                )
                            )

                else:

                    st.warning(
                        "No video recording was found. "
                        "The answer will still be submitted."
                    )


                # =================================================
                # STEP 2 — SUBMIT ANSWER
                # =================================================

                try:

                    response = requests.post(
                        f"{API_URL}/interview/answer",
                        params={
                            "answer": answer.strip(),
                        },
                        headers=get_auth_headers(),
                        timeout=120,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.feedback = (
                            data.get(
                                "feedback",
                                "",
                            )
                        )


                        if data.get("completed"):

                            st.session_state.completed = True

                            st.session_state.final_report = (
                                data.get(
                                    "final_report",
                                    "",
                                )
                            )

                        else:

                            st.session_state.round = (
                                data.get(
                                    "round",
                                    st.session_state.round,
                                )
                            )

                            st.session_state.question = (
                                data.get(
                                    "next_question",
                                    "",
                                )
                            )


                        # Clear current answer.

                        if "current_answer" in st.session_state:

                            del st.session_state.current_answer


                        # Clear recorded audio.

                        st.session_state.interview_audio_frames = []


                        # Clear video path for the next round.

                        st.session_state.interview_video_path = ""

                        st.session_state.video_analysis = None


                        # Clear video recorder ID so a new
                        # recording is created next round.

                        if "video_recording_id" in st.session_state:

                            del st.session_state.video_recording_id


                        st.rerun()


                    elif response.status_code == 401:

                        st.error(
                            "Your session has expired. Please log in again."
                        )

                        handle_unauthorized()


                    else:

                        st.error(
                            f"API Error {response.status_code}: "
                            f"{response.text}"
                        )

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to FastAPI: {e}"
                    )


# ============================================================
# FEEDBACK
# ============================================================

if st.session_state.feedback:

    st.divider()

    st.subheader("AI Feedback")

    st.markdown(
        st.session_state.feedback
    )


# ============================================================
# FINAL REPORT
# ============================================================

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


    st.divider()

    if st.button(
        "Start New Interview",
        use_container_width=True,
    ):

        reset_interview()

        st.rerun()


# ============================================================
# START NEW INTERVIEW
# ============================================================

if not st.session_state.started:

    st.divider()

    st.subheader("Interview Setup")

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


    if st.button(
        "Start Interview",
        type="primary",
        use_container_width=True,
    ):

        try:

            response = requests.post(
                f"{API_URL}/interview/start",
                params={
                    "role": role,
                    "difficulty": difficulty,
                    "interview_type": interview_type,
                    "max_rounds": max_rounds,
                },
                headers=get_auth_headers(),
                timeout=120,
            )


            if response.status_code == 200:

                data = response.json()


                st.session_state.candidate_id = (
                    data.get(
                        "candidate_id",
                        st.session_state.candidate_id,
                    )
                )


                st.session_state.interview_id = (
                    data.get(
                        "interview_id"
                    )
                )


                st.session_state.question = (
                    data.get(
                        "question",
                        "",
                    )
                )


                st.session_state.round = (
                    data.get(
                        "round",
                        1,
                    )
                )


                st.session_state.feedback = ""

                st.session_state.final_report = ""

                st.session_state.started = True

                st.session_state.completed = False

                st.session_state.interview_audio_frames = []

                st.session_state.interview_video_path = ""

                st.session_state.video_analysis = None


                # Clear previous video recording ID.

                if "video_recording_id" in st.session_state:

                    del st.session_state.video_recording_id


                st.rerun()


            elif response.status_code == 401:

                st.error(
                    "Your session has expired. Please log in again."
                )

                handle_unauthorized()


            else:

                st.error(
                    f"API Error {response.status_code}: "
                    f"{response.text}"
                )


        except requests.RequestException as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )


# ============================================================
# RESUME INTERVIEW
# ============================================================

if not st.session_state.started:

    st.divider()

    st.header("🔄 Resume Interview")

    if st.button(
        "Resume Interview",
        use_container_width=True,
    ):

        candidate_id = (
            st.session_state.candidate_id
        )


        if not candidate_id:

            st.error(
                "Candidate identity could not be determined from your login."
            )

        else:

            try:

                response = requests.get(
                    f"{API_URL}/interview/resume/{candidate_id}",
                    headers=get_auth_headers(),
                    timeout=30,
                )


                if response.status_code == 200:

                    data = response.json()


                    if data.get("resume_available"):

                        st.session_state.interview_id = (
                            data.get(
                                "interview_id"
                            )
                        )


                        st.session_state.question = (
                            data.get(
                                "question",
                                "",
                            )
                        )


                        st.session_state.round = (
                            data.get(
                                "round",
                                1,
                            )
                        )


                        st.session_state.started = True

                        st.session_state.completed = False

                        st.session_state.feedback = ""

                        st.session_state.final_report = ""

                        st.session_state.interview_audio_frames = []

                        st.session_state.interview_video_path = ""

                        st.session_state.video_analysis = None


                        # Clear previous video recording ID.

                        if "video_recording_id" in st.session_state:

                            del st.session_state.video_recording_id


                        st.success(
                            "Interview resumed!"
                        )

                        st.rerun()


                    else:

                        st.warning(
                            data.get(
                                "message",
                                "No interview to resume.",
                            )
                        )


                elif response.status_code == 401:

                    st.error(
                        "Your session has expired. Please log in again."
                    )

                    handle_unauthorized()


                elif response.status_code == 403:

                    st.error(
                        "You are not authorized to access this interview."
                    )


                else:

                    st.error(
                        f"API Error {response.status_code}: "
                        f"{response.text}"
                    )


            except requests.RequestException as e:

                st.error(
                    f"Could not connect to FastAPI: {e}"
                )

# ============================================================
# INTERVIEW HISTORY
# ============================================================

st.divider()

st.header("📊 Interview History")


if st.button(
    "Load Interview History",
    use_container_width=True,
):

    candidate_id = (
        st.session_state.candidate_id
    )


    if not candidate_id:

        st.error(
            "Candidate identity could not be determined."
        )

    else:

        try:

            response = requests.get(
                f"{API_URL}/interview/history/{candidate_id}",
                headers=get_auth_headers(),
                timeout=30,
            )


            if response.status_code == 200:

                data = response.json()

                interviews = data.get(
                    "interviews",
                    [],
                )


                if not interviews:

                    st.info(
                        "No interview history found."
                    )


                else:

                    for interview in interviews:

                        st.subheader(
                            f"Interview #{interview['interview_id']}"
                        )


                        st.write(
                            f"Role: {interview['role']}"
                        )


                        st.write(
                            f"Difficulty: {interview['difficulty']}"
                        )


                        st.write(
                            f"Type: {interview['interview_type']}"
                        )


                        st.write(
                            f"Status: {interview['status']}"
                        )


                        st.write(
                            f"Rounds: {interview['max_rounds']}"
                        )


                        # ========================================
                        # VIDEO ANALYSIS HISTORY
                        # ========================================

                        video_analysis = interview.get(
                            "video_analysis"
                        )


                        if video_analysis:

                            st.markdown(
                                "### 🎥 Video Analysis"
                            )

                            col1, col2 = st.columns(2)

                            with col1:

                                visibility = (
                                    video_analysis.get(
                                        "face_visibility_percentage"
                                    )
                                )

                                if visibility is not None:

                                    st.write(
                                        f"**Face Visibility:** "
                                        f"{visibility}%"
                                    )

                                duration = (
                                    video_analysis.get(
                                        "duration_seconds"
                                    )
                                )

                                if duration is not None:

                                    st.write(
                                        f"**Duration:** "
                                        f"{duration} sec"
                                    )

                                fps = (
                                    video_analysis.get(
                                        "fps"
                                    )
                                )

                                if fps is not None:

                                    st.write(
                                        f"**FPS:** "
                                        f"{fps}"
                                    )

                            with col2:

                                width = (
                                    video_analysis.get(
                                        "width"
                                    )
                                )

                                height = (
                                    video_analysis.get(
                                        "height"
                                    )
                                )

                                if width and height:

                                    st.write(
                                        f"**Resolution:** "
                                        f"{width} × {height}"
                                    )

                                analyzed_frames = (
                                    video_analysis.get(
                                        "analyzed_frames"
                                    )
                                )

                                if analyzed_frames is not None:

                                    st.write(
                                        f"**Frames Analyzed:** "
                                        f"{analyzed_frames}"
                                    )

                                face_frames = (
                                    video_analysis.get(
                                        "face_detected_frames"
                                    )
                                )

                                if face_frames is not None:

                                    st.write(
                                        f"**Face Detected Frames:** "
                                        f"{face_frames}"
                                    )


                        # ========================================
                        # ANSWERS
                        # ========================================

                        answers = interview.get(
                            "answers",
                            [],
                        )


                        for item in answers:

                            with st.expander(
                                f"Round {item['round']}"
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
                                    item.get(
                                        "feedback",
                                        "",
                                    )
                                )


                        # ========================================
                        # FINAL REPORT
                        # ========================================

                        final_report = interview.get(
                            "final_report"
                        )


                        if final_report:

                            st.markdown(
                                "### Final Report"
                            )

                            st.markdown(
                                final_report
                            )


                        st.divider()


            elif response.status_code == 401:

                st.error(
                    "Your session has expired. Please log in again."
                )

                handle_unauthorized()


            elif response.status_code == 403:

                st.error(
                    "You are not authorized to access this history."
                )


            else:

                st.error(
                    f"API Error {response.status_code}: "
                    f"{response.text}"
                )


        except requests.RequestException as e:

            st.error(
                f"Could not connect to FastAPI: {e}"
            )