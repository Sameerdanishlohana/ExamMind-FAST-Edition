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
    .stApp {
        background-color: #0E1117;
    }
    .main-title {
        font-size: 56px;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #00ADB5, #00FFF5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #9CA3AF;
        margin-bottom: 2rem;
    }
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
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .sidebar-card {
        background-color: #1F2937;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 FAST NUCES AI Tutor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Scenario-Based • Conceptual • Brutal Checking Style</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Engine Room")
    api_key = st.text_input("Gemini API Key", type="password", value=st.secrets.get("GEMINI_API_KEY", ""))
    
    st.markdown("---")
    temperature = st.slider("Strictness Level", 0.0, 1.0, 0.4)
    max_tokens = st.slider("Content Depth", 500, 4000, 2000)

    mode = st.selectbox(
        "Pedagogy Style",
        [
            "Full Deep Lecture",
            "Scenario Practice Only",
            "Revision Mode (Short + Sharp)",
            "Exam Survival Mode"
        ]
    )
    
    st.markdown("---")
    st.caption("Optimized for FAST NUCES Karachi Standard")

topic = st.text_input("📚 Subject / Topic Name", placeholder="e.g. Memory Management in OS")
teach_button = st.button("🚀 GENERATE FAST-STYLE LECTURE")

if teach_button:
    if not api_key:
        st.error("Please provide an API Key in the sidebar.")
    elif not topic:
        st.warning("Please enter a topic to begin.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            base_prompt = """
            You are a senior professor at FAST NUCES Karachi. 
            The target students are highly competitive.
            Exams are scenario-based, integrated, and test edge cases.
            """

            mode_prompts = {
                "Full Deep Lecture": "Start with intuition, then deep conceptual foundation. Include WHY, derivations, 2 scenario-based exam questions, 1 integrated long question, tricky MCQs, and common mistakes.",
                "Scenario Practice Only": "Provide 4 complex scenario-based questions and 1 integrated problem with hidden traps. Provide high-standard solutions.",
                "Revision Mode (Short + Sharp)": "Focus on key formulas, core bullet points, 2 quick scenario checks, and common traps.",
                "Exam Survival Mode": "Focus on examiners' twisting tactics, pattern recognition, high probability question types, and time management."
            }

            final_prompt = f"{base_prompt}\nMode: {mode_prompts[mode]}\nTopic: {topic}"

            with st.spinner("Analyzing FAST historical patterns..."):
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                        system_instruction="You are a strict, brilliant FAST NUCES Professor."
                    ),
                    contents=final_prompt
                )

            st.success("Lecture Delivered 🔥")
            st.snow()
            
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Prep Material",
                data=response.text,
                file_name=f"FAST_{topic.replace(' ', '_')}.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")

st.divider()
