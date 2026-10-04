import streamlit as st
import speech_recognition as sr
import io
import wave

st.title("Teste de Microfone 🎤")

audio = st.audio_input("Fale algo:")

if audio:
    st.audio(audio)
    
    try:
        audio_bytes = audio.read()
        
        # O Streamlit grava em WAV — usa wave nativo pra ler
        wav_io = io.BytesIO(audio_bytes)
        
        # Verifica se é WAV válido
        with wave.open(wav_io, 'rb') as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            sample_rate = wav_file.getframerate()
            sample_width = wav_file.getsampwidth()
            n_channels = wav_file.getnchannels()
        
        # Cria AudioData pro speech_recognition
        recognizer = sr.Recognizer()
        audio_data = sr.AudioData(frames, sample_rate, sample_width)
        
        # Transcreve com Google
        texto = recognizer.recognize_google(audio_data, language="en-US")
        st.success(f"Você falou: **{texto}**")
    
    except wave.Error as e:
        st.error(f"Erro ao ler WAV: {e}")
    except sr.UnknownValueError:
        st.error("Não entendi o que você falou. Tenta de novo.")
    except sr.RequestError as e:
        st.error(f"Erro na API do Google: {e}")
    except Exception as e:
        st.error(f"Erro: {type(e).__name__}: {e}")