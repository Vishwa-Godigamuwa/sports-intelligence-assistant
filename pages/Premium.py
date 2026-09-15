import streamlit as st

from auth.auth_manager import upgrade_user


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sports Intelligence Assistant - Premium",
    page_icon="⭐",
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
# SESSION STATE / PAGE PROTECTION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# User must be logged in to access the upgrade page
if not st.session_state.logged_in or not st.session_state.user:

    st.warning(
        "Please sign in before accessing Premium features."
    )

    if st.button(
        "Go to Sign In",
        use_container_width=True
    ):
        st.switch_page("pages/login.py")

    st.stop()


# =========================================================
# GET CURRENT USER
# =========================================================

user = st.session_state.user

account_type = user["account_type"].lower()


# =========================================================
# PREMIUM PAGE
# =========================================================

st.title("⭐ Sports Intelligence Premium")

st.subheader(
    "Unlock the Full Sports Intelligence Experience"
)

st.write(
    "Upgrade your account to access the complete set of "
    "Sports Intelligence Assistant features."
)

st.divider()


# =========================================================
# PREMIUM FEATURES
# =========================================================

st.markdown(
    """
### Premium Includes

- 🧠 Detailed AI-generated sports analysis
- 🎯 Personalized training recommendations
- 📈 Complete coaching guidance
- 📄 Downloadable coaching reports
- ⭐ Full Premium responses
"""
)

st.divider()


# =========================================================
# ALREADY PREMIUM USER
# =========================================================

if account_type == "premium":

    st.success(
        "Your account already has Premium access."
    )

    if st.button(
        "Back",
        use_container_width=True
    ):
        st.switch_page("app.py")


# =========================================================
# FREE USER
# =========================================================

else:

    st.info(
        "You are currently using the Free plan."
    )

    st.caption(
        "Payment integration will be added in a future "
        "version. For now, this button activates Premium "
        "for demonstration purposes."
    )

    # -----------------------------------------------------
    # UPGRADE BUTTON
    # -----------------------------------------------------

    if st.button(
        "⭐ Upgrade to Premium",
        use_container_width=True
    ):

        result = upgrade_user(
            user["user_id"]
        )

        if result["success"]:

            # Update the current session
            st.session_state.user[
                "account_type"
            ] = "premium"

            st.success(
                "Your account has been upgraded to Premium!"
            )

            st.balloons()

            # Refresh the page so Premium status is shown
            st.rerun()

        else:

            st.error(
                result["message"]
            )

    # -----------------------------------------------------
    # CANCEL / BACK BUTTON
    # -----------------------------------------------------

    if st.button(
        "Maybe Later",
        use_container_width=True
    ):
        st.switch_page("main.py")