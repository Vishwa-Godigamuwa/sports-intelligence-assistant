import html
import os
import streamlit as st
from dotenv import load_dotenv


# ==================================================
# Streamlit Page Configuration
# ==================================================

st.set_page_config(
    page_title="Sports Intelligence Assistant",
    page_icon="🏆",
    layout="wide"
)

st.markdown("""
<style>

/* Hide default Streamlit page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

.st-key-dashboard_nav_button button,
.st-key-dashboard_nav_button button:hover,
.st-key-login_nav_button button,
.st-key-login_nav_button button:hover,
.st-key-register_nav_button button,
.st-key-register_nav_button button:hover {
    background: #343541 !important;
    color: white !important;
    border: 1px solid #4b4d57 !important;
    box-shadow: none !important;
}

.st-key-premium_nav_button button,
.st-key-premium_nav_button button:hover {
    background: linear-gradient(120deg, #ff9a00, #f05a00) !important;
    color: white !important;
    border: none !important;
    box-shadow: none !important;
}

.st-key-logout_button button {
    background: rgba(229, 57, 53, 0.35) !important;
    color: white !important;
    border: 1px solid rgba(229, 57, 53, 0.9) !important;
    box-shadow: none !important;
}

.st-key-logout_button button:hover {
    background: rgba(229, 57, 53, 0.5) !important;
    color: white !important;
    border: 1px solid rgba(229, 57, 53, 1) !important;
    box-shadow: none !important;
}

.st-key-upgrade_button button {
    background: transparent !important;
    color: white !important;
    border: 1px solid #4b4d57 !important;
    box-shadow: none !important;
}

.st-key-upgrade_button button:hover {
    background: transparent !important;
    color: white !important;
    border: 1px solid #737783 !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button(
        "⌂ Dashboard",
        use_container_width=True,
        key="dashboard_nav_button"
    ):
        st.switch_page("app.py")

    if st.button(
        "◌ Login",
        use_container_width=True,
        key="login_nav_button"
    ):
        st.switch_page("pages/Login.py")

    if st.button(
        "✎  Register",
        use_container_width=True,
        key="register_nav_button"
    ):
        st.switch_page("pages/Register.py")

    if st.button(
        "✦ Premium",
        use_container_width=True,
        key="premium_nav_button"
    ):
        st.switch_page("pages/Premium.py")

    st.divider()


# ==================================================
# Session State
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ==================================================
# Follow-up Conversation State
# ==================================================

if "original_question" not in st.session_state:
    st.session_state.original_question = None

if "original_response" not in st.session_state:
    st.session_state.original_response = None

if "followup_messages" not in st.session_state:
    st.session_state.followup_messages = []

if "conversation_sport" not in st.session_state:
    st.session_state.conversation_sport = None

if "conversation_feature" not in st.session_state:
    st.session_state.conversation_feature = None

if "report_data" not in st.session_state:
    st.session_state.report_data = None


# ==================================================
# Authentication Check
# ==================================================

if not st.session_state.logged_in:

    st.title("🏆 Sports Intelligence Assistant")

    st.subheader("Welcome")

    st.write(
        "Please sign in or create an account to access "
        "the Sports Intelligence Assistant."
    )

    if st.button(
        "Sign In",
        use_container_width=True
    ):
        st.switch_page("pages/Login.py")

    if st.button(
        "Create an Account",
        use_container_width=True
    ):
        st.switch_page("pages/Register.py")

    st.stop()


# Logged-in user
current_user = st.session_state.user


# ==================================================
# Professional UI Styling
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #0F172A;
}

.hero {
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg,#1e3a8a,#2563eb);
    color: white;
    text-align:center;
    margin-bottom:20px;
}

.feature-card {
    background-color:#1E293B;
    padding:15px;
    border-radius:12px;
    text-align:center;
    margin-bottom:10px;
    border:1px solid #334155;
}

.result-card{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border-left:5px solid #2563eb;
}

div[data-testid="metric-container"]{
    background:#1E293B;
    border:1px solid #334155;
    padding:15px;
    border-radius:12px;
}

.stButton>button {
    background: linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    border:none;
    border-radius:12px;
    font-weight:bold;
}

[data-testid="stSidebar"]{
    background-color:#111827;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# Agent Imports
# ==================================================

from agents.query_agent import QueryUnderstandingAgent
from agents.retrieval_agent import DataRetrievalAgent
from agents.analytics_agent import DataAnalyticsAgent
from agents.response_agent import ResponseGenerationAgent
from utils.pdf_generator import generate_pdf


# ==================================================
# Load Environment Variables
# ==================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API Key not found in .env file")
    st.stop()


# ==================================================
# Helper Functions
# ==================================================

DATABASE_PATH = "database"


def get_sports():
    """
    Load sports from database folders.
    """

    if not os.path.exists(DATABASE_PATH):
        return []

    return sorted(
        [
            folder
            for folder in os.listdir(DATABASE_PATH)
            if os.path.isdir(
                os.path.join(DATABASE_PATH, folder)
            )
        ]
    )


def get_features(sport):
    """
    Load feature names from txt files.
    """

    sport_path = os.path.join(
        DATABASE_PATH,
        sport.lower()
    )

    if not os.path.exists(sport_path):
        return []

    features = []

    for file in os.listdir(sport_path):

        if file.endswith(".txt"):

            feature_name = (
                file.replace(".txt", "")
                .replace("_", " ")
                .title()
            )

            features.append(feature_name)

    return sorted(features)


# ==================================================
# Create Agent Objects
# ==================================================

query_agent = QueryUnderstandingAgent(
    GEMINI_API_KEY
)

retrieval_agent = DataRetrievalAgent(
    GEMINI_API_KEY
)

analytics_agent = DataAnalyticsAgent(
    GEMINI_API_KEY
)

response_agent = ResponseGenerationAgent(
    GEMINI_API_KEY
)


# ==================================================
# Streamlit UI
# ==================================================

st.markdown("""
<style>

.big-title{
    text-align:center;
    font-size:52px;
    color:white;
    font-weight:300;
    margin-top:120px;
}

.sub-title{
    text-align:center;
    color:#A1A1AA;
    margin-bottom:40px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="big-title">
        What can I help with today?
    </div>

    <div class="sub-title">
        AI Sports Intelligence Assistant
    </div>
    """,
    unsafe_allow_html=True
)

sports = get_sports()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("◍ Sports", len(sports))

with col2:
    feature_count = len(get_features(sports[0])) if sports else 0
    st.metric("◈ Features", feature_count)

with col3:
    st.metric("⌬ AI Agents", "4")

with col4:
    st.metric("⦿ Status", "Online")

if not sports:
    st.error("No sports found in database folder.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    selected_sport = st.selectbox(
        " Select Sport",
        sports
    )

features = get_features(selected_sport)

if not features:
    st.error(
        "No features found for the selected sport."
    )
    st.stop()

with col2:
    selected_feature = st.selectbox(
        "Select Feature",
        features
    )


# ==================================================
# Sidebar
# ==================================================

# ==================================================
# Logged-in User Information
# ==================================================

account_type = current_user["account_type"].capitalize()

st.sidebar.markdown("""
<h2 style="
text-align:center;
color:white;
margin-bottom:20px;
">
⚇ User Profile
</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    f"""
    <div style="
        background-color:#1e3a5f;
        color:white;
        text-align:center;
        padding:1rem;
        min-height:70px;
        display:flex;
        align-items:center;
        justify-content:center;
        border-radius:0.5rem;
        border:none;
        box-sizing:border-box;
        margin-bottom:1rem;
    ">
        Welcome {html.escape(current_user['name'])} !
    </div>
    """,
    unsafe_allow_html=True
)

if account_type == "Premium":
    st.sidebar.markdown(
        """
        <div style="
            background-color:#193d35;
            color:#4ade80;
            padding:1rem;
            min-height:70px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:0.75rem;
            border-radius:0.5rem;
            box-sizing:border-box;
            margin-bottom:1rem;
        ">
            <span>⭐</span>
            <span>Premium Member</span>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        """
        <div style="
            background-color:#414322;
            color:#fff4b8;
            padding:1rem;
            min-height:70px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:0.75rem;
            border-radius:0.5rem;
            box-sizing:border-box;
            margin-bottom:1rem;
        ">
            <span>◔</span>
            <span>Free Member</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# Upgrade Button
# ==================================================

if account_type == "Free":

    if st.sidebar.button(
        "⭐ Upgrade to Premium",
        use_container_width=True,
        key="upgrade_button"
    ):
        st.switch_page("pages/Premium.py")


# ==================================================
# Logout Button
# ==================================================

if st.sidebar.button(
    "⎋ Logout",
    use_container_width=True,
    key="logout_button"
):

    st.session_state.logged_in = False
    st.session_state.user = None

    # Clear coaching conversation too
    st.session_state.original_question = None
    st.session_state.original_response = None
    st.session_state.followup_messages = []
    st.session_state.conversation_sport = None
    st.session_state.conversation_feature = None
    st.session_state.report_data = None

    st.rerun()


# ==================================================
# Question Area
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### Popular Questions")

c1, c2 = st.columns(2)

with c1:
    st.info("🏏 Create a batting improvement plan")
    st.info("⚽ How to improve sprint speed?")

with c2:
    st.info("🏀 Improve shooting accuracy")
    st.info("🏃 Create a weekly training schedule")

question = st.text_area(
    "",
    height=120,
    placeholder="Ask Sports AI anything about training, performance, fitness, coaching, or athlete development..."
)

col1, col2, col3 = st.columns([4, 2, 4])

with col2:
    submit = st.button(
        "⌘ Ask Sports AI",
        use_container_width=True
    )


# ==================================================
# Main Processing
# ==================================================

if submit:

    if question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Analysing your request..."):

        try:

            # ==========================================
            # Query Agent
            # ==========================================

            query_result = query_agent.analyse_query(
                selected_sport=selected_sport,
                selected_feature=selected_feature,
                available_features=features,
                user_question=question
            )


            # ==========================================
            # Relevance Check
            # ==========================================

            if not query_result["relevance"]:

                st.error(
                    query_result["error_message"]
                )

                if query_result["suggested_feature"]:

                    st.info(
                        f"Suggested Feature: "
                        f"{query_result['suggested_feature']}"
                    )

                st.stop()


            # ==========================================
            # Missing Information Check
            # ==========================================

            missing = query_result[
                "missing_information"
            ]

            if len(missing) > 0:

                st.warning(
                    "Additional information required:"
                )

                for item in missing:
                    st.write(f"• {item}")

                st.stop()


            # ==========================================
            # Retrieval Agent
            # ==========================================

            retrieval_result = (
                retrieval_agent.retrieve_information(
                    sport=selected_sport,
                    feature=selected_feature,
                    question=question
                )
            )


            # ==========================================
            # Analytics Agent
            # ==========================================

            analytics_result = (
                analytics_agent.analyse(
                    sport=selected_sport,
                    feature=selected_feature,
                    question=question,
                    extracted_information=
                    query_result[
                        "extracted_information"
                    ],
                    knowledge_base=
                    retrieval_result[
                        "combined_content"
                    ]
                )
            )


            # ==========================================
            # Response Agent
            # ==========================================

            final_response = (
                response_agent.generate_response(
                    sport=selected_sport,
                    feature=selected_feature,
                    question=question,
                    analytics_result=analytics_result,
                    retrieved_content=
                    retrieval_result[
                        "combined_content"
                    ],
                    account_type=account_type
                )
            )


            # ==========================================
            # Save Conversation Context
            # ==========================================

            st.session_state.original_question = question
            st.session_state.original_response = final_response

            st.session_state.conversation_sport = (
                selected_sport
            )

            st.session_state.conversation_feature = (
                selected_feature
            )

            # New main advice = new follow-up conversation
            st.session_state.followup_messages = []


            # ==========================================
            # Save PDF Data
            # ==========================================

            st.session_state.report_data = {
                "Sport": selected_sport,
                "Feature": selected_feature,
                "Question": question,
                "AI Advice": final_response
            }


            if isinstance(analytics_result, dict):

                st.session_state.report_data.update({
                    "Performance Score":
                    analytics_result.get(
                        "performance_score",
                        "N/A"
                    ),

                    "Readiness Level":
                    analytics_result.get(
                        "readiness_level",
                        "N/A"
                    ),

                    "Training Hours/Week":
                    analytics_result.get(
                        "weekly_training_hours",
                        "N/A"
                    )
                })


        except Exception as e:

            st.exception(e)


# ==================================================
# Display Stored Coaching Advice
# ==================================================

if st.session_state.original_response:

    st.chat_message("user").markdown(
        st.session_state.original_question
    )

    st.chat_message("assistant").markdown(
        st.session_state.original_response
    )


    # ==================================================
    # PDF Report
    # ==================================================

    if st.session_state.report_data:

        pdf_file = generate_pdf(
            st.session_state.report_data
        )

        if account_type == "Premium":

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📄 Download Coaching Report",
                    data=file,
                    file_name="coaching_report.pdf",
                    mime="application/pdf"
                )

        else:

            st.info(
                "⭐ Upgrade to Premium to "
                "download coaching reports."
            )


    # ==================================================
    # Follow-up Conversation
    # ==================================================

    st.divider()

    st.subheader(
        "💬 Ask a Follow-up Question"
    )

    st.caption(
        "Ask another question about the coaching advice above."
    )


    # ==============================================
    # Display Previous Follow-up Messages
    # ==============================================

    for message in st.session_state.followup_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ==============================================
    # Follow-up Input
    # ==============================================

    followup_question = st.chat_input(
        "Ask something about your coaching plan..."
    )


    # ==============================================
    # Process Follow-up
    # ==============================================

    if followup_question:

        # Display user's new message
        with st.chat_message("user"):

            st.markdown(
                followup_question
            )


        # Preserve previous history before adding
        # the new question.
        previous_history = list(
            st.session_state.followup_messages
        )


        # Save user's follow-up
        st.session_state.followup_messages.append(
            {
                "role": "user",
                "content": followup_question
            }
        )


        # ==========================================
        # Generate Follow-up Response
        # ==========================================

        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking about your follow-up question..."
            ):

                try:

                    followup_response = (
                        response_agent.generate_followup_response(
                            sport=
                            st.session_state.conversation_sport,

                            feature=
                            st.session_state.conversation_feature,

                            original_question=
                            st.session_state.original_question,

                            original_response=
                            st.session_state.original_response,

                            followup_question=
                            followup_question,

                            chat_history=
                            previous_history
                        )
                    )


                    st.markdown(
                        followup_response
                    )


                    # Save assistant response
                    st.session_state.followup_messages.append(
                        {
                            "role": "assistant",
                            "content": followup_response
                        }
                    )


                except Exception as e:

                    st.error(
                        "Unable to answer the "
                        "follow-up question."
                    )

                    st.exception(e)