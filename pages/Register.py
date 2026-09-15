import streamlit as st

from auth.auth_manager import register_user


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sports Intelligence Assistant - Register",
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
# REGISTER PAGE
# =========================================================

st.title("🏆 Sports Intelligence Assistant")

st.subheader("Create Your Account")

st.write(
    "Create an account to start using your personalized "
    "sports intelligence assistant."
)


# =========================================================
# REGISTRATION FORM
# =========================================================

with st.form("register_form"):

    name = st.text_input(
        "Full Name",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "Email Address",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Enter your password again"
    )

    register_button = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )


# =========================================================
# HANDLE REGISTRATION
# =========================================================

if register_button:

    # Check that all fields are completed
    if not name.strip() or not email.strip() or not password or not confirm_password:

        st.error("Please complete all fields.")

    # Check whether passwords match
    elif password != confirm_password:

        st.error("Passwords do not match.")

    # Basic password-length validation
    elif len(password) < 8:

        st.error(
            "Password must contain at least 8 characters."
        )

    else:

        result = register_user(
            name=name,
            email=email,
            password=password
        )

        if result["success"]:

            st.success(
                "Account created successfully!"
            )

            st.info(
                "Your account has been created with the Free plan. "
                "You can now sign in."
            )

        else:

            st.error(
                result["message"]
            )


# =========================================================
# LOGIN SECTION
# =========================================================

st.divider()

st.write("Already have an account?")

if st.button(
    "Back to Sign In",
    use_container_width=True
):

    st.switch_page("pages/login.py")