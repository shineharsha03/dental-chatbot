import streamlit as st
import pdfplumber
import base64
from crewai import Agent, Task, Crew, Process
import os
from openai import OpenAI

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Medical AI Suite", page_icon="🏥", layout="wide")

# GET API KEY SAFELY
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        os.environ["OPENAI_API_KEY"] = api_key
    except:
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY in secrets.")
        st.stop()

# Initialize Vision Client
client = OpenAI(api_key=api_key)

# --- 2. FUNCTIONS ---
def get_pdf_text(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except:
        return "Error reading PDF."

def analyze_image(image_file):
    """Sends image to AI Vision Model with PRO Instructions."""
    encoded_image = base64.b64encode(image_file.getvalue()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                You are a Senior Consultant Radiologist. 
                Analyze this medical image with clinical precision.

                OUTPUT FORMAT:
                1. **Exam Type:** (e.g., MRI, CT, X-Ray)
                2. **Findings:** (Bone, Soft Tissue, Pathology)
                3. **Impression:** Diagnostic conclusion.

                Be professional and concise.
                """
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this scan."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ],
            }
        ],
        max_tokens=800
    )
    return response.choices[0].message.content

# --- 3. THE APP ---
st.title("🏥 Medical AI Workstation")

# TABS
tab1, tab2 = st.tabs(["🦷 Dental Appeals (Text)", "🩻 AI Radiologist (Vision)"])

# === TAB 1: DENTAL ===
with tab1:
    st.header("Automated Insurance Defense")
    uploaded_file = st.file_uploader("Upload Denial (PDF)", type="pdf")

    if uploaded_file and st.button("Generate Appeal"):
        with st.spinner('Agents are working...'):
            analyst = Agent(role='Analyst', goal='Extract Details', backstory='Expert Biller', verbose=True)
            writer = Agent(role='Writer', goal='Write Appeal', backstory='Legal Expert', verbose=True)

            raw_text = get_pdf_text(uploaded_file)
            task1 = Task(description=f"Analyze: {raw_text}", expected_output='Details', agent=analyst)
            task2 = Task(description="Write appeal with Markdown.", expected_output='Letter', agent=writer)

            crew = Crew(agents=[analyst, writer], tasks=[task1, task2])
            result = crew.kickoff()
            st.markdown(result)

# === TAB 2: RADIOLOGY ===
with tab2:
    st.header("General Radiology Analysis")
    st.info("Upload any X-Ray, MRI, or CT Scan.")

    medical_image = st.file_uploader("Upload Scan", type=["jpg", "png", "jpeg"])

    if medical_image:
        st.image(medical_image, width=300)

        if st.button("Analyze Scan"):
            with st.spinner('Radiologist is examining...'):
                report = analyze_image(medical_image)
                st.markdown("### 📋 Clinical Report")
                st.markdown(report)
                st.warning("⚠️ AI Assistant Only. Verify with human doctor.")