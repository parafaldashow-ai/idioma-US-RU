import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.title("Teste Mic Recorder")

audio = mic_recorder(
    start_prompt="⏺️ Gravar",
    stop_prompt="⏹️ Parar",
    key='recorder'
)

if audio:
    st.audio(audio['bytes'])
    st.success(f"Recebi {len(audio['bytes'])} bytes! Sample rate: {audio['sample_rate']}")