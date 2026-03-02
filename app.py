import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(
    page_title="Exam Mind | FAST Edition",
    page_icon="🎓",
    layout="wide"
)

# ---------------- UI Styling ----------------
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

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Room")

    temperature = st.slider("Strictness Level", 0.0, 1.0, 0.4)
    max_tokens = st.slider("Content Depth", 500, 4000, 2000)
    mode = st.selectbox("Pedagogy Style", 
        ["Full Deep Lecture", 
         "Scenario Practice Only", 
         "Revision Mode", 
         "Exam Survival Mode"]
    )
    exam_type = st.radio("Mock Exam Simulator", 
        ["None", "Mid-Term", "Final Exam"]
    )

# ---------------- Main ----------------
topic = st.text_input("📚 Subject / Topic Name", 
                      placeholder="e.g. Polymorphism in OOP")

col1, col2 = st.columns(2)
with col1:
    teach_button = st.button("🚀 GENERATE LECTURE")
with col2:
    exam_button = st.button("📝 GENERATE MOCK EXAM")

# ---------------- API KEY ----------------
key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if teach_button or exam_button:
    if not key:
        st.error("API Key not found! Add 'GEMINI_API_KEY' to Streamlit Secrets.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            genai.configure(api_key=key)

            with st.spinner("Professor is thinking..."):

                if exam_button:
                    system_prompt = """
                    You are a strict FAST NUCES Karachi Examiner.
                    Exams are scenario-based, tricky, conceptual,
                    and punish superficial understanding.
                    """
                    user_prompt = f"""
                    Create a {exam_type} for: {topic}.
                    Include:
                    - MCQs with traps
                    - 2 scenario-based short questions
                    - 1 long analytical question
                    """

                else:
                    system_prompt = """
                    You are a brilliant FAST NUCES Professor.
                    Teach deeply. Use conceptual rigor.
                    Use scenario-based explanations.
                    Assume students face tough exams.
                    """
                    user_prompt = f"""
                    Explain {topic} in {mode} style.
                    Make it FAST-level difficulty.
                    """

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_prompt
                )

                response = model.generate_content(
                    user_prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens
                    }
                )

            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
