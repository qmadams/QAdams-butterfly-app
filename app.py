import base64
import requests
import streamlit as st

# ---------------- CONFIG ----------------
ENDPOINT_URL = "https://askai.aiclub.world/f6c44628-dab2-418f-8840-2f646738cdd8"

st.set_page_config(page_title="Butterfly Classifier", layout="centered")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe, #bae6fd);
    color: #111827;
}
</style>
""", unsafe_allow_html=True)
# ---------------- SIMPLE LOGIN ----------------
password = st.text_input("Enter access code", type="password")

if password != "STEM2026":
    st.warning("Please enter the correct access code")
    st.stop()

# ---------------- HEADER ----------------
st.title("🦋 Butterfly Classifier")

# ---------------- FUNCTION ----------------
def call_model_endpoint(image_bytes: bytes):
    payload = base64.b64encode(image_bytes)

    try:
        r = requests.post(ENDPOINT_URL, data=payload, timeout=30)
        r.raise_for_status()
        return r.json().get("predicted_label", "Unknown")
    except Exception as e:
        st.error(f"Error: {e}")
        return "Error"

# ---------------- UI ----------------
st.write("Upload or take a picture of a butterfly to classify it.")

tabs = st.tabs(["Upload Image", "Camera"])

# -------- Upload --------
with tabs[0]:
    image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if image:
        st.image(image)

        if st.button("Predict"):
            label = call_model_endpoint(image.getvalue())
            st.success(f"Prediction: {label}")

# -------- Camera --------
with tabs[1]:
    cam = st.camera_input("Take a photo")

    if cam:
        st.image(cam)

        if st.button("Predict Camera"):
            label = call_model_endpoint(cam.getvalue())
            st.success(f"Prediction: {label}")
