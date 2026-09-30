import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para


def render():
    st.markdown("""
    <style>
    .card-idioma {
        background: linear-gradient(135deg, #1a2332, #253045);
        border: 2px solid #2d3748;
        border-radius: 24px;
        padding: 48px 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 16px;
    }
    .card-idioma:hover {
        border-color: #34d399;
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(52, 211, 153, 0.25);
    }
    .bandeira-emoji {
        font-size: 120px;
        line-height: 1;
    }
    .titulo-idioma {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 20px;
        letter-spacing: 2px;
    }
    .subtitulo-idioma {
        font-size: 17px;
        color: #a8b2c1;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('# 🌍 Língua App', unsafe_allow_html=True)
    st.markdown('<p style="color: #a8b2c1; font-size: 19px;">Aprenda ingles e russo do seu jeito</p>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown('### ✨ Qual idioma voce quer estudar?', unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)
    for col, (codigo, info) in zip([col1, col2], IDIOMAS.items()):
        with col:
            st.markdown(
                f'<div class="card-idioma">'
                f'<div class="bandeira-emoji">{info["bandeira"]}</div>'
                f'<div class="titulo-idioma">{info["nome"].upper()}</div>'
                f'<div class="subtitulo-idioma">{info["nome_nativo"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if st.button(f"🚀 Estudar {info['nome']}", key=f"btn_{codigo}", use_container_width=True, type="primary"):
                st.session_state.idioma = codigo
                ir_para("menu")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 Meu Progresso", key="home_progresso", use_container_width=True):
            ir_para("progresso")
    with c2:
        if st.button("⚙️ Configuracoes", key="home_config", use_container_width=True):
            ir_para("config")

    st.markdown("")

    if st.button("❓ Ajuda - Como usar o app", key="home_ajuda", use_container_width=True):
        ir_para("ajuda")
        return

    st.stop()
