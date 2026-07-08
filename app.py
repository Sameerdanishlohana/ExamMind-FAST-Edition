import streamlit as st
import os
from openai import OpenAI 

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
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 FAST NUCES AI Tutor</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Engine Room")
    temperature = st.slider("Strictness Level (Temp)", 0.0, 2.0, 0.7)
    max_tokens = st.slider("Content Depth", 500, 8000, 3000)
    
    mode = st.selectbox("Pedagogy Style", 
        ["Full Deep Lecture", 
         "Scenario Practice Only", 
         "Revision Mode", 
         "Exam Survival Mode"]
    )
    exam_type = st.radio("Mock Exam Simulator", 
        ["Mid-Term", "Final Exam"]
    )
    
    selected_model = st.selectbox("Brain Model", [
        "gemini-3.5-flash",
        "gemini-3.1-pro",
        "deepseek/deepseek-chat"       
    ])

topic = st.text_input("📚 Subject / Topic Name", 
                      placeholder="e.g. Polymorphism in OOP")

col1, col2 = st.columns(2)
with col1:
    teach_button = st.button("🚀 GENERATE LECTURE")
with col2:
    exam_button = st.button("📝 GENERATE MOCK EXAM")


or_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if teach_button or exam_button:
    if "gemini" in selected_model and not gemini_key:
        st.error("Gemini API Key (GEMINI_API_KEY) not found!")
    elif "deepseek" in selected_model and not or_key:
        st.error("OpenRouter API Key (OPENROUTER_API_KEY) not found!")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            if "gemini" in selected_model:
                client = OpenAI(
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                    api_key=gemini_key
                )
            else:
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=or_key,
                    default_headers={
                        "HTTP-Referer": "http://localhost:8501", 
                        "X-Title": "Exam Mind Fast Edition",     
                    }
                )

            if exam_button:
                sys_msg = "You are a strict FAST NUCES Karachi Examiner. Exams are scenario-based and analytical."
                user_msg = f"Create a {exam_type} exam for: {topic}. Include tricky MCQs and 2 scenario questions."
            else:
                sys_msg = "You are a brilliant FAST NUCES Professor. Teach deeply with rigor."
                user_msg = f"Explain {topic} in {mode} style. Use industry scenarios."

            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            response_placeholder = st.empty()
            full_text = ""

            with st.spinner("Professor is thinking..."):
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": sys_msg},
                        {"role": "user", "content": user_msg}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )

                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_text += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_text)

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
