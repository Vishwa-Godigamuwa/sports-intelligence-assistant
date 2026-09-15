import streamlit as st

from auth.auth_manager import login_user


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sports Intelligence Assistant - Login",
    page_icon="🏆",
    layout="centered"
)

st.markdown("""
<style>
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
        "✎ Register",
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


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# LOGIN PAGE
# =========================================================

st.title("🏆 Sports Intelligence Assistant")

st.subheader("Welcome Back")

st.write(
    "Sign in to access your personalized sports intelligence assistant."
)


# =========================================================
# LOGIN FORM
# =========================================================

with st.form("login_form"):

    email = st.text_input(
        "Email Address",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    login_button = st.form_submit_button(
        "Sign In",
        use_container_width=True
    )


# =========================================================
# HANDLE LOGIN
# =========================================================

if login_button:

    result = login_user(
        email=email,
        password=password
    )

    if result["success"]:

        # Store login state
        st.session_state.logged_in = True

        # Store logged-in user information
        st.session_state.user = result["user"]

        # Return to main application
        st.switch_page("app.py")

    else:

        st.error(result["message"])

# =========================================================
# REGISTER SECTION
# =========================================================

st.divider()

st.write("Don't have an account?")

if st.button(
    "Create an Account",
    use_container_width=True
):

    st.switch_page("pages/register.py")