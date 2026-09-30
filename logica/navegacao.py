import streamlit as st
import importlib

TELAS = {
    "inicio":            "telas.tela_inicial",
    "menu":              "telas.tela_menu_idioma",
    "modulos":           "telas.tela_modulos",
    "modulo":            "telas.tela_modulo",
    "flashcards":        "telas.tela_flashcards",
    "exercicio":         "telas.tela_exercicio",
    "dicionario":        "telas.tela_dicionario",
    "progresso":         "telas.tela_progresso",
    "progresso_idioma":  "telas.tela_progresso_idioma",
    "anotacoes":         "telas.tela_anotacoes",
    "config":            "telas.tela_config",
    "ajuda":      "telas.tela_ajuda",
}


def init_estado():
    if "tela" not in st.session_state:
        st.session_state.tela = "inicio"
    if "idioma" not in st.session_state:
        st.session_state.idioma = None
    if "modulo_atual" not in st.session_state:
        st.session_state.modulo_atual = None
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if "idioma_progresso" not in st.session_state:
        st.session_state.idioma_progresso = None


def ir_para(tela: str, guardar_historico=True):
    if tela not in TELAS:
        st.error(f"Tela desconhecida: {tela}")
        return

    if guardar_historico:
        tela_atual = st.session_state.get("tela", "inicio")
        if tela_atual != tela:
            st.session_state.historico.append(tela_atual)
            st.session_state.historico = st.session_state.historico[-10:]

    st.session_state.tela = tela
    st.rerun()


def voltar():
    if st.session_state.historico:
        tela_anterior = st.session_state.historico.pop()
        st.session_state.tela = tela_anterior
        st.rerun()
    else:
        st.session_state.tela = "inicio"
        st.rerun()


def renderizar_tela_atual():
    tela = st.session_state.tela
    modulo_path = TELAS.get(tela, "telas.tela_inicial")
    mod = importlib.import_module(modulo_path)
    mod.render()