import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sports Intelligence Assistant",
    page_icon="🏆",
    layout="centered"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================================================
# APPLICATION ROUTING
# =========================================================

if st.session_state.logged_in:

    # User is already authenticated
    st.title("🏆 Sports Intelligence Assistant")

    if st.session_state.user:

        st.success(
            f"Welcome, {st.session_state.user['name']}!"
        )

        st.write(
            f"Account Type: "
            f"{st.session_state.user['account_type'].capitalize()}"
        )


    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        # Clear authentication session
        st.session_state.logged_in = False
        st.session_state.user = None

        # Refresh application
        st.rerun()


    st.info(
        "Sports AI application will be connected here "
        "after authentication navigation is completed."
    )


else:

    # User is not logged in
    st.title("🏆 Sports Intelligence Assistant")

    st.subheader("Welcome")

    st.write(
        "Sign in or create an account to access "
        "your personalized sports intelligence assistant."
    )

    if st.button(
        "Sign In",
        use_container_width=True
    ):
        st.switch_page("pages/login.py")

    if st.button(
        "Create an Account",
        use_container_width=True
    ):
        st.switch_page("pages/register.py")