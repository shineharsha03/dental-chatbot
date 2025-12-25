import streamlit as st
import time

st.set_page_config(page_title="Appeal Denial Swarm (Sim Mode)", layout="wide")
st.title("🐝 Medical Appeal Swarm (Simulation Mode)")

# --- FAKE AGENTS (Placeholders) ---


def radiologist_agent(image_file):
    """Agent 1: Simulates looking at an image."""
    time.sleep(2)  # Fake "thinking" time
    return "Analysis: Severe decay detected in lower right molar (Tooth #30). Evidence of bone loss visible in X-Ray."


def intake_agent(audio_file):
    """Agent 2: Simulates listening to audio."""
    time.sleep(2)  # Fake "listening" time
    return "Transcript: 'Patient is in extreme pain. Conservative treatment failed. Root canal is medically necessary.'"


def writer_agent(radiology_report, voice_notes):
    """Agent 3: Simulates writing a letter."""
    time.sleep(2)  # Fake "writing" time
    return f"""
    SUBJECT: URGENT APPEAL FOR MEDICAL COVERAGE

    BASED ON RADIOLOGY EVIDENCE:
    {radiology_report}

    BASED ON DOCTOR'S NOTES:
    {voice_notes}

    CONCLUSION:
    The denial is unfounded. The clinical evidence matches the patient symptoms. 
    Coverage is required immediately.
    """


# --- THE SWARM DASHBOARD ---

col1, col2, col3 = st.columns(3)

# 1. RADIOLOGIST WORKSTATION
with col1:
    st.header("👁️ Radiologist")
    uploaded_file = st.file_uploader("Upload X-Ray", key="rad")

    if uploaded_file and st.button("Analyze Image"):
        with st.spinner("Agent 1 is scanning..."):
            st.session_state['rad_result'] = radiologist_agent(uploaded_file)
            st.success("Analysis Done")

    if 'rad_result' in st.session_state:
        st.info(st.session_state['rad_result'])

# 2. INTAKE NURSE WORKSTATION
with col2:
    st.header("👂 Intake Nurse")
    audio_val = st.audio_input("Record Clinical Note", key="voice")

    if audio_val:
        with st.spinner("Agent 2 is transcribing..."):
            st.session_state['voice_result'] = intake_agent(audio_val)
            st.success("Transcribed")

    if 'voice_result' in st.session_state:
        st.info(f"Dictation: '{st.session_state['voice_result']}'")

# 3. CASE MANAGER WORKSTATION
with col3:
    st.header("🧠 Case Manager")

    if st.button("Generate Appeal"):
        # Check if previous agents did their job
        rad = st.session_state.get('rad_result')
        voice = st.session_state.get('voice_result')

        if rad and voice:
            with st.spinner("Agent 3 is writing..."):
                final_letter = writer_agent(rad, voice)
                st.text_area("Final Appeal Letter", final_letter, height=500)
        else:
            st.error(
                "Please complete the X-Ray Analysis AND Voice Dictation first."
            )
