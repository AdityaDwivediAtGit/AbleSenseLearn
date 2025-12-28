import streamlit as st
import os
import time
from datetime import datetime
from config import Config
from models.user import User, InteractionLog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ai_services.vision_processor import VisionProcessor
from ai_services.text_processor import TextProcessor
from ai_services.voice_assistant import VoiceAssistant
from utils.ui_helpers import load_css

# Initialize Engines/Services
# using st.cache_resource for persistent services
@st.cache_resource
def get_services():
    # Ensure directories exist
    Config.init_app()
    return {
        'vision': VisionProcessor(),
        'text': TextProcessor(),
        'voice': VoiceAssistant()
    }

services = get_services()

# Database Setup
engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(bind=engine)

# Ensure tables exist (Robustness for Streamlit Cloud/Local)
from models.user import Base
Base.metadata.create_all(engine)

def get_db_session():
    return Session()

# --- Page Functions ---

def render_dashboard(user):
    st.header(f"Welcome back, {user.username}!")
    
    st.info(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Actions")
        if st.button("👁️ Describe surroundings", use_container_width=True):
            st.session_state.page = 'Vision Assistant'
            st.rerun()
            
        if st.button("🗣️ Voice Companion", use_container_width=True):
            st.session_state.page = 'Voice Companion'
            st.rerun()
            
        if st.button("📚 Simplify Text", use_container_width=True):
            st.session_state.page = 'Visual & Learning'
            st.rerun()

    with col2:
        st.subheader("Status")
        st.write(f"**Disability Profile:** {user.disability_type.title()}")
        st.write(f"**Medical Info:** {user.medical_info or 'None set'}")
        
        if st.button("🆘 EMERGENCY ALERT", type="primary", use_container_width=True):
            st.error("EMERGENCY PROTOCOL ACTIVATED")
            # In real app, call emergency_features.trigger_emergency(user)
            st.toast("Alert sent to emergency contacts!", icon="🚑")
            time.sleep(2)

def render_vision():
    st.header("👁️ Vision Assistant")
    st.write("Upload an image or use your camera to get a description.")
    
    tab1, tab2 = st.tabs(["Camera", "Upload"])
    
    img_file = None
    
    with tab1:
        cam_img = st.camera_input("Take a picture")
        if cam_img:
            img_file = cam_img
            
    with tab2:
        up_img = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])
        if up_img:
            img_file = up_img
            
    if img_file:
        st.image(img_file, caption="Analyzing...", width=300)
        with st.spinner("AI is looking at the image..."):
            # Convert to PIL/bytes for processor
            from PIL import Image
            image = Image.open(img_file)
            description = services['vision'].describe_image(image)
        
        st.success("Description:")
        st.markdown(f"### {description}")
        
        if st.button("🔊 Read Aloud"):
            audio_path, is_temp = services['voice'].speak(description)
            if audio_path:
                st.audio(audio_path, format='audio/mp3', autoplay=True)
                if is_temp:
                    # Clean up is tricky in Streamlit reruns, but we rely on OS temp cleaner or handle later
                    pass

def render_voice_companion():
    st.header("🗣️ Voice Companion")
    
    # Chat Interface
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
    # Voice Input
    if st.button("🎤  Click to Speak"):
        with st.spinner("Listening..."):
            text = services['voice'].listen_for_command()
            if text:
                st.session_state.messages.append({"role": "user", "content": text})
                
                # Simple response logic for now (mocking the conversational AI)
                response = f"I heard you say: '{text}'. How can I help with that?"
                if "time" in text:
                    response = f"The current time is {datetime.now().strftime('%H:%M')}."
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                audio_path, is_temp = services['voice'].speak(response)
                if audio_path:
                    st.audio(audio_path, format='audio/mp3', autoplay=True)
                st.rerun()
            else:
                st.warning("I couldn't hear you. Please try again.")

def render_learning():
    st.header("📚 Learning & Simplification")
    
    input_text = st.text_area("Enter text to simplify or explain:", height=150)
    
    mode = st.radio("Choose Mode:", ["Simplify", "Summarize", "Explain like I'm 5"])
    
    if st.button("Process Text"):
        if not input_text:
            st.warning("Please enter some text first.")
            return
            
        with st.spinner("Processing..."):
            if mode == "Simplify":
                result = services['text'].simplify_text(input_text, level="simple")
            elif mode == "Summarize":
                result = services['text'].summarize_text(input_text)
            else:
                result = services['text'].simplify_text(input_text, level="explain_like_im_5")
                
        st.markdown("### Result:")
        st.write(result)
        if st.button("🔊 Read Result"):
            audio_path, is_temp = services['voice'].speak(result)
            if audio_path:
                st.audio(audio_path, format='audio/mp3', autoplay=True)

def render_settings(user, db_session):
    st.header("⚙️ Settings")
    
    with st.form("profile_form"):
        st.subheader("Disability Profile")
        d_type = st.selectbox("Type", ["Visual", "Hearing", "Motor", "Cognitive", "None"], index=0)
        severity = st.select_slider("Severity", ["Mild", "Moderate", "Severe"], value="Moderate")
        
        st.subheader("Preferences")
        font_size = st.number_input("Font Size", 12, 32, user.font_size)
        high_contrast = st.checkbox("High Contrast Mode", user.high_contrast)
        
        if st.form_submit_button("Save Profile"):
            user.disability_type = d_type.lower()
            user.severity = severity.lower()
            user.font_size = font_size
            user.high_contrast = high_contrast
            db_session.commit()
            st.success("Profile updated!")
            st.rerun()

# --- Main App ---

def main():
    st.set_page_config(
        page_title="Able Sense AI Buddy",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()
    
    if 'page' not in st.session_state:
        st.session_state.page = 'Dashboard'
        
    # Sidebar
    with st.sidebar:
        st.title("🤖 Able Sense")
        
        # Configuration Section
        with st.expander("⚙️ System Config", expanded=True):
            # Model Provider Selection
            provider = st.selectbox("AI Provider", ["DeepSeek", "OpenAI", "HuggingFace"], index=0)
            Config.AI_PROVIDER = provider
            
            # Dynamic Link & Config
            if provider == "DeepSeek":
                st.markdown("[Get API Key (DeepSeek)](https://platform.deepseek.com/)")
                Config.AI_BASE_URL = "https://api.deepseek.com"
                Config.AI_MODEL_NAME = "deepseek-chat"
            elif provider == "OpenAI":
                st.markdown("[Get API Key (OpenAI)](https://platform.openai.com/api-keys)")
                Config.AI_BASE_URL = "https://api.openai.com/v1"
                Config.AI_MODEL_NAME = "gpt-3.5-turbo"
            elif provider == "HuggingFace":
                st.markdown("[Get Token (HuggingFace)](https://huggingface.co/settings/tokens)")
                # HF Logic handled in processor (uses local or API)
            
            # API Key Input
            api_key = st.text_input(f"{provider} API Key", type="password", placeholder="Paste key/token here...")
            if api_key:
                Config.OPENAI_API_KEY = api_key # We reuse this variable for the active key
            
            # Test Mode
            st.divider()
            test_mode = st.checkbox("Enable Test Data Mode", value=Config.ENABLE_TEST_DATA, help="Mock data (Free/Fast)")
            Config.ENABLE_TEST_DATA = test_mode
            if test_mode:
                st.warning("⚠️ Test Mode Active")

        # Load user
        db = get_db_session()
        # For prototype, just get first user or create one
        user = db.query(User).first()
        if not user:
            # Auto-create user if missing (Fail-safe)
            user = User(
                username="demo_user",
                disability_type="visual",
                severity="moderate",
                font_size=20,
                voice_enabled=True,
                medical_info="Diabetic. Allergic to penicillin."
            )
            db.add(user)
            db.commit()
            st.toast("Created demo user profile")
            
        st.write(f"User: **{user.username}**")
        
        st.divider()
        
        nav_options = ['Dashboard', 'Vision Assistant', 'Voice Companion', 'Visual & Learning', 'Settings']
        
        # Sync widget with session state if needed, or just let widget drive state
        selected_page = st.radio("Navigation", nav_options, index=nav_options.index(st.session_state.page) if st.session_state.page in nav_options else 0)
        st.session_state.page = selected_page
        
        st.divider()
        st.caption("v1.0.0 - Accessibility First")

    # Routing
    if st.session_state.page == 'Dashboard':
        render_dashboard(user)
    elif st.session_state.page == 'Vision Assistant':
        render_vision()
    elif st.session_state.page == 'Voice Companion':
        render_voice_companion()
    elif st.session_state.page == 'Visual & Learning':
        render_learning()
    elif st.session_state.page == 'Settings':
        render_settings(user, db)
        
    db.close()

if __name__ == "__main__":
    main()