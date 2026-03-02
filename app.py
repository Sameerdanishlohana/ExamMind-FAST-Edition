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
        margin-bottom: 0px;
    }
    .subtitle { font-size: 1.2rem; color: #9CA3AF; margin-bottom: 2rem; }
    .stButton>button {
        background: linear-gradient(45deg, #00ADB5, #007D83);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 173, 181, 0.3);
    }
    .response-box {
        background-color: #1A1C23;
        padding: 30px;
        border-radius: 12px;
        border-left: 5px solid #00ADB5;
        color: #E5E7EB;
        line-height: 1.6;
    }
    .exam-header {
        color: #FF4B4B;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 FAST NUCES AI Tutor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Scenario-Based • Conceptual • Mock Exam Ready</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Engine Room")
    api_key = st.text_input("Gemini API Key", type="password", value=st.secrets.get("GEMINI_API_KEY", ""))
    
    st.markdown("---")
    temperature = st.slider("Strictness Level", 0.0, 1.0, 0.4)
    max_tokens = st.slider("Content Depth", 500, 4000, 2000)

    mode = st.selectbox(
        "Pedagogy Style",
        ["Full Deep Lecture", "Scenario Practice Only", "Revision Mode", "Exam Survival Mode"]
    )
    
    st.markdown("---")
    exam_type = st.radio("Mock Exam Simulator", ["None", "Mid-Term (1.5 Hours)", "Final Exam (3 Hours)"])

topic = st.text_input("📚 Subject / Topic Name", placeholder="e.g. Dijkstra's Algorithm or Deadlocks")

col1, col2 = st.columns([1, 1])
with col1:
    teach_button = st.button("🚀 GENERATE LECTURE")
with col2:
    exam_button = st.button("📝 GENERATE MOCK EXAM")

def call_gemini(prompt, system_text):
    client = genai.Client(api_key=api_key)
    return client.models.generate_content(
        model="gemini-1.5-flash",
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_text
        ),
        contents=prompt
    )

if teach_button or exam_button:
    if not api_key:
        st.error("Please provide an API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a topic to begin.")
    else:
        try:
            with st.spinner("Processing..."):
                if exam_button:
                    system_msg = "You are a strict FAST NUCES Karachi Examiner. You create extremely difficult, scenario-based exam papers."
                    prompt = f"Create a {exam_type} paper for the topic: {topic}. Include Q1 (MCQs with traps), Q2 (Short scenario analysis), and Q3 (A long integrated problem). Provide a marking scheme at the end."
                    header_text = "📝 Official Mock Exam Paper"
                else:
                    system_msg = "You are a brilliant FAST NUCES Professor."
                    mode_prompts = {
                        "Full Deep Lecture": "Intuition, derivations, 2 scenarios, 1 long question, and common mistakes.",
                        "Scenario Practice Only": "4 complex scenarios and 1 integrated problem with hidden traps.",
                        "Revision Mode": "Key formulas, core bullets, and 2 quick scenario checks.",
                        "Exam Survival Mode": "Examiners' twisting tactics and high probability question types."
                    }
                    prompt = f"Mode: {mode_prompts[mode]}\nTopic: {topic}"
                    header_text = "📖 Professor's Lecture Notes"

                response = call_gemini(prompt, system_msg)

            st.markdown(f"### {header_text}")
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button("📥 Download Material", response.text, file_name=f"{topic}_FAST_Prep.md")

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.divider()
