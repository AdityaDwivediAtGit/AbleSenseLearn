import streamlit as st
import time

def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = True

def load_css():
    st.markdown("""
        <style>
        .big-font {
            font-size:24px !important;
        }
        .stButton button {
            height: 60px;
            font-size: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
