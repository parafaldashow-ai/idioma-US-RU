import streamlit as st
from audiorecorder import audiorecorder

st.title("Teste Audio Recorder 2")

audio = audiorecorder("Clique pra gravar", "Clique pra parar")

if len(audio) > 0:
    st.audio(audio.export().read())
    st.success(f"Recebi {len(audio)} ms de áudio!")