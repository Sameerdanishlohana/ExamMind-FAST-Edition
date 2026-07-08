import streamlit as st
import os
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Exam Mind | FAST VIP Edition",
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

st.markdown('<p class="main-title">🎓 FAST NUCES AI VIP Hub</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ VIP Engine Room")
    
    app_mode = st.radio(
        "Select Operation Hub",
        ["Text Academy (Tutor & Exam)", "Creative Suite (Image Generator)"]
    )
    
    st.markdown("---")
    
    if app_mode == "Text Academy (Tutor & Exam)":
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
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-3.5-flash"
        ])
        
        st.markdown("<br>" * 8, unsafe_allow_html=True)
    else:
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["1:1", "16:9", "4:3", "9:16"]
        )
        image_format = st.selectbox(
            "Format",
            ["JPEG", "PNG"]
        )
        
        st.markdown("<br>" * 8, unsafe_allow_html=True)

gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if app_mode == "Text Academy (Tutor & Exam)":
    topic = st.text_input("📚 Subject / Topic Name", placeholder="e.g. Polymorphism in OOP")
    
    col1, col2 = st.columns(2)
    with col1:
        teach_button = st.button("🚀 GENERATE LECTURE")
    with col2:
        exam_button = st.button("📝 GENERATE MOCK EXAM")
        
    if teach_button or exam_button:
        if not gemini_key:
            st.error("Gemini API Key (GEMINI_API_KEY) not found!")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            try:
                client = genai.Client(api_key=gemini_key)
                
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
                    config = types.GenerateContentConfig(
                        system_instruction=sys_msg,
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                    
                    response = client.models.generate_content_stream(
                        model=selected_model,
                        contents=user_msg,
                        config=config
                    )

                    for chunk in response:
                        if chunk.text:
                            full_text += chunk.text
                            response_placeholder.markdown(full_text)

                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.markdown("### 🎨 VIP Image Generator (Imagen 3)")
    image_prompt = st.text_area(
        "Describe the visual/diagram you want to generate",
        placeholder="e.g., An abstract conceptual software diagram illustrating polymorphism in object-oriented programming, modern tech aesthetic..."
    )
    generate_image_button = st.button("🖼️ GENERATE VIP VISUAL")
    
    if generate_image_button:
        if not gemini_key:
            st.error("Gemini API Key (GEMINI_API_KEY) not found!")
        elif not image_prompt:
            st.warning("Please provide an image prompt description.")
        else:
            try:
                client = genai.Client(api_key=gemini_key)
                
                with st.spinner("Generating VIP visual artwork via Imagen..."):
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=image_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio=aspect_ratio,
                            output_mime_type=f"image/{image_format.lower()}"
                        )
                    )
                    
                    for generated_image in result.generated_images:
                        st.image(generated_image.image.image_bytes, caption=image_prompt, use_container_width=True)
                        
            except Exception as e:
                st.error(f"Error generating visual: {str(e)}")
