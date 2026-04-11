import streamlit as st
from streamlit_oauth import OAuth2Component

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Butterfly App", layout="centered")

# -----------------------------
# GOOGLE OAUTH SETUP
# -----------------------------
CLIENT_ID = st.secrets["google"]["client_id"]
CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = st.secrets["google"]["redirect_uri"]

oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    "https://accounts.google.com/o/oauth2/v2/auth",
    "https://oauth2.googleapis.com/token"
)

# -----------------------------
# LOGIN SECTION
# -----------------------------
st.title("🦋 Butterfly App")

result = oauth2.authorize_button(
    name="Login with Google",
    redirect_uri=REDIRECT_URI,
    scope="openid email profile",
    key="google_login"
)

# -----------------------------
# SESSION HANDLING
# -----------------------------
if result:
    st.session_state["token"] = result.get("token")
    st.session_state["user"] = result.get("user_info", {})

# If not logged in → stop app
if "token" not in st.session_state:
    st.warning("Please log in with your Google account to continue.")
    st.stop()

# -----------------------------
# USER INFO
# -----------------------------
user_info = st.session_state.get("user", {})
user_email = user_info.get("email", "Unknown")

st.success(f"Welcome, {user_email}!")

# OPTIONAL: Restrict to school emails
# if not user_email.endswith("@yourschool.org"):
#     st.error("Access restricted to school accounts only.")
#     st.stop()

# -----------------------------
# YOUR ORIGINAL APP STARTS HERE
# -----------------------------
st.header("Main App")

st.write("Your app is now secure and connected to Google 🚀")

# Example content (replace with your real app)
student_name = st.text_input("Enter your name")
if student_name:
    st.write(f"Hello {student_name}, you're logged in as {user_email}")
