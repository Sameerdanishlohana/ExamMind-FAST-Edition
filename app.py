import streamlit as st
import os
from google import genai
from google.genai import types

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
    enable_search = st.toggle("Enable Google Search Tool")

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
        st.error("API Key not found! Add GEMINI_API_KEY to Streamlit secrets.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            client = genai.Client(api_key=key)

            # ---------------- SYSTEM PROMPT ----------------
            if exam_button:
                system_instruction = """
                You are a strict FAST NUCES Karachi Examiner.
                Exams are scenario-based and conceptual.
                Include tricky MCQs and analytical questions.
                """
                user_prompt = f"""
                Create a {exam_type} exam for:
                {topic}

                Include:
                - MCQs with traps
                - 2 scenario-based questions
                - 1 long analytical question
                """

            else:
                system_instruction = """
                You are a brilliant FAST NUCES Professor.
                Teach deeply and conceptually.
                Use scenario-based explanations.
                Assume exams are tough.
                """
                user_prompt = f"""
                Explain {topic} in {mode} style.
                Maintain FAST-level rigor.
                """

            # ---------------- CONTENT STRUCTURE ----------------
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=user_prompt)
                    ],
                ),
            ]

            # ---------------- TOOLS (OPTIONAL) ----------------
            tools = []
            if enable_search:
                tools.append(
                    types.Tool(
                        googleSearch=types.GoogleSearch()
                    )
                )

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                system_instruction=system_instruction,
                tools=tools,
                thinking_config=types.ThinkingConfig(
                    thinking_level="HIGH"
                )
            )

            # ---------------- STREAMING RESPONSE ----------------
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            response_placeholder = st.empty()

            full_text = ""

            with st.spinner("Professor is thinking..."):
                for chunk in client.models.generate_content_stream(
                    model="gemini-2.0-flash-exp",
                    contents=contents,
                    config=config,
                ):
                    if chunk.text:
                        full_text += chunk.text
                        response_placeholder.markdown(full_text)

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
