import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.title("Teste Audio Recorder")

audio_bytes = audio_recorder(
    text="Clique e fale",
    recording_color="#f472b6",
    neutral_color="#6b7280",
    icon_name="microphone",
    icon_size="2x",
    pause_threshold=2.0,
)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    st.success(f"Recebi {len(audio_bytes)} bytes de áudio!")