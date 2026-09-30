import streamlit as st

st.title("Teste de Botão")

if "contador" not in st.session_state:
    st.session_state.contador = 0

st.write(f"### Contador: {st.session_state.contador}")

if st.button("CLICA AQUI", key="btn_unico"):
    st.session_state.contador += 1
    st.success("✅ Funcionou!")
    st.balloons()