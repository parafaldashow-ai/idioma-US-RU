import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar


def render():
    idioma = st.session_state.idioma
    if not idioma:
        ir_para("inicio")
        return

    info = IDIOMAS[idioma]

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_menu"):
            voltar()
    with col_b:
        st.markdown(f"## {info['bandeira']} {info['nome'].upper()}")

    st.markdown("---")

    opcoes = [
        ("📖", "Modulos",         "modulos",          "#34d399"),
        ("✏️", "Exercicios",      "exercicio",        "#60a5fa"),
        ("🎴", "Flashcards",      "flashcards",       "#a78bfa"),
        ("🔍", "Dicionario",      "dicionario",       "#fbbf24"),
        ("📊", "Progresso",       "progresso_idioma", "#ef4444"),
        ("📝", "Anotacoes",       "anotacoes",        "#ec4899"),
    ]

    for i in range(0, len(opcoes), 2):
        cols = st.columns(2)
        for col, (icone, nome, tela, cor) in zip(cols, opcoes[i:i+2]):
            with col:
                card_html = (
                    f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                    f'border: 2px solid {cor}44; '
                    f'border-radius: 18px; padding: 32px 20px; text-align: center; '
                    f'margin-bottom: 12px; '
                    f'box-shadow: 0 4px 16px rgba(0,0,0,0.2);">'
                    f'<div style="font-size: 52px; line-height: 1;">{icone}</div>'
                    f'<div style="font-size: 20px; font-weight: 700; color: {cor}; margin-top: 14px;">{nome}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button(f"Abrir {nome}", use_container_width=True, key=f"menu_{tela}_{idioma}"):
                    if tela == "progresso_idioma":
                        st.session_state.idioma_progresso = idioma
                    ir_para(tela)

    st.markdown("---")

    st.stop()
