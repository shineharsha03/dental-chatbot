import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# --- PAGE SETUP ---
st.set_page_config(page_title="Dental AI", page_icon="🦷")
st.title("🦷 AI Dental Assistant")

# --- API KEY SETUP ---
# This block automatically detects if you are on Replit or Streamlit Cloud
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.environ.get("GOOGLE_API_KEY")
except FileNotFoundError:
    # If no secrets file is found (local run), fallback to environment
    api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    st.error("🚨 API Key not found! Please set GOOGLE_API_KEY in Secrets.")
    st.stop()

# Configure the AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- TAB INTERFACE ---
tab1, tab2 = st.tabs(["💬 Chatbot", "🩻 X-Ray Analyzer"])

# --- TAB 1: CHATBOT ---
with tab1:
    st.write("### Ask me anything about dental health!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Type your dental question here..."):
        # Show user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate AI response
        try:
            response = model.generate_content(prompt)
            st.chat_message("assistant").markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

# --- TAB 2: X-RAY ANALYZER ---
with tab2:
    st.header("🩻 Upload a Dental X-Ray")
    st.write("Upload a clear image of your teeth or X-ray.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze X-Ray"):
            with st.spinner("Analyzing with AI..."):
                vision_prompt = """
                You are an expert dental assistant. Analyze this image for:
                1. Cavities (caries)
                2. Bone loss
                3. Visible infections
                Start with: "⚠️ AI Analysis Only - Not a Medical Diagnosis."
                """
                try:
                    response = model.generate_content([vision_prompt, image])
                    st.success("Analysis Complete!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")