import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Exam Mind | FAST Edition",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0E1117; }
    .main-title {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(90deg, #00ADB5, #00FFF5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00ADB5, #007D83);
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    .response-box {
        background-color: #1A1C23;
        padding: 30px;
        border-radius: 12px;
        border-left: 5px solid #00ADB5;
        color: #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 FAST NUCES AI Tutor</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Engine Room")
    # REMOVED: API Key text input for security. 
    # It now pulls directly from st.secrets or Environment Variables.
    
    temperature = st.slider("Strictness Level", 0.0, 1.0, 0.4)
    max_tokens = st.slider("Content Depth", 500, 4000, 2000)
    mode = st.selectbox("Pedagogy Style", ["Full Deep Lecture", "Scenario Practice Only", "Revision Mode", "Exam Survival Mode"])
    exam_type = st.radio("Mock Exam Simulator", ["None", "Mid-Term", "Final Exam"])

topic = st.text_input("📚 Subject / Topic Name", placeholder="e.g. Polymorphism in OOP")

col1, col2 = st.columns(2)
with col1:
    teach_button = st.button("🚀 GENERATE LECTURE")
with col2:
    exam_button = st.button("📝 GENERATE MOCK EXAM")

# Robust API Key fetching
key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if teach_button or exam_button:
    if not key:
        st.error("API Key not found! Add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            client = genai.Client(api_key=key)
            
            with st.spinner("Professor is thinking..."):
                if exam_button:
                    sys_msg = "You are a strict FAST NUCES Karachi Examiner."
                    prompt = f"Create a {exam_type} for: {topic}. Include MCQ traps, scenarios, and a long question."
                else:
                    sys_msg = "You are a brilliant FAST NUCES Professor."
                    prompt = f"Explain {topic} in {mode} style with FAST-level difficulty."

                # FIXED: Model string format to avoid 404
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                        system_instruction=sys_msg
                    ),
                    contents=prompt
                )

            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
