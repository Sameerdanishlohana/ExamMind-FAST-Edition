import streamlit as st
import os
from sambanova import SambaNova
st.set_page_config(
    page_title="Exam Mind",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 92px;
    font-weight: 800;
    color: #00ADB5;
}
.subtitle {
    font-size: 18px;
    color: gray;
}
.stButton>button {
    background-color: #00ADB5;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.response-box {
    background-color: #111;
    padding: 25px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎓 FAST NUCES Karachi – AI Tutor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Scenario-Based | Conceptual | Exam-Oriented | Brutal Checking Style</p>', unsafe_allow_html=True)
st.divider()

st.sidebar.header("⚙️ Configuration")

temperature = st.sidebar.slider("Creativity Level", 0.0, 1.0, 0.4)
max_tokens = st.sidebar.slider("Max Response Length", 500, 4000, 2000)

mode = st.sidebar.selectbox(
    "Teaching Mode",
    [
        "Full Deep Lecture",
        "Scenario Practice Only",
        "Revision Mode (Short + Sharp)",
        "Exam Survival Mode"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("Built for FAST NUCES (KHI) level preparation.")

topic = st.text_input("📚 Enter the topic you want to master:")

teach_button = st.button("🚀 Teach Me Like FAST")

st.caption("Press the button to generate a FAST-style explanation.")
st.divider()

client = SambaNova(
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

base_prompt = """
You are a senior professor teaching at FAST NUCES Karachi.
Students are intelligent and competitive.

FAST exams are:
- Scenario-based
- Multi-concept integrated
- Application-heavy
- Designed to test deep understanding
- Sometimes tricky with edge cases
- Time pressured

Teach in a way that prepares students to survive tough grading.

"""

if mode == "Full Deep Lecture":
    mode_prompt = """
    1. Start with intuitive understanding.
    2. Build strong conceptual foundation.
    3. Explain WHY each concept exists.
    4. Show derivations (if applicable).
    5. Give real-world applications.
    6. Add at least 2 scenario-based exam questions.
    7. Add one integrated long question.
    8. Add tricky MCQs.
    9. Mention common mistakes.
    10. Give exam-solving strategy.
    """

elif mode == "Scenario Practice Only":
    mode_prompt = """
    Do not explain theory deeply.
    Directly give:
    - 4 scenario-based questions
    - 1 integrated long problem
    - Include hidden traps
    - Provide detailed solutions
    """

elif mode == "Revision Mode (Short + Sharp)":
    mode_prompt = """
    Give:
    - Key formulas
    - Core concepts in bullets
    - 2 quick scenario checks
    - Common traps
    Keep it concise but powerful.
    """

elif mode == "Exam Survival Mode":
    mode_prompt = """
    Focus on:
    - How examiners twist questions
    - Pattern recognition
    - Time management tips
    - Concept linking tricks
    - Most tested areas
    - High probability question types
    """

final_prompt = base_prompt + mode_prompt + "\n\nTopic: " + topic

if teach_button:

    if not topic:
        st.warning("Please enter a topic first.")
    else:
        try:
            with st.spinner("Preparing FAST-level academic content..."):

                response = client.chat.completions.create(
                    model="DeepSeek-V3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a strict but brilliant FAST NUCES professor. You train students for scenario-based, difficult exams."
                        },
                        {
                            "role": "user",
                            "content": final_prompt
                        }
                    ],
                    temperature=temperature,
                    top_p=0.1,
                    max_tokens=max_tokens,
                    
                )

            st.success("Lecture Generated Successfully 🔥")
            st.snow()

            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.write(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
