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
        padding: 40px 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 16px;
        min-height: 260px;
    }
    .card-idioma:hover {
        border-color: #34d399;
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(52, 211, 153, 0.25);
    }
    .bandeira-emoji {
        font-size: 100px;
        line-height: 1;
    }
    .titulo-idioma {
        font-size: 26px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 20px;
        letter-spacing: 2px;
    }
    .subtitulo-idioma {
        font-size: 15px;
        color: #a8b2c1;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('# \U0001F30D L\u00edngua App', unsafe_allow_html=True)
    st.markdown('<p style="color: #a8b2c1; font-size: 19px;">Aprenda ingl\u00eas, russo e espanhol do seu jeito</p>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown('### \u2728 Qual idioma voc\u00ea quer estudar?', unsafe_allow_html=True)
    st.markdown("")

    # Cria uma coluna por idioma (funciona com 2, 3, 4... idiomas)
    colunas = st.columns(len(IDIOMAS))

    for col, (codigo, info) in zip(colunas, IDIOMAS.items()):
        with col:
            st.markdown(
                f'<div class="card-idioma">'
                f'<div class="bandeira-emoji">{info["bandeira"]}</div>'
                f'<div class="titulo-idioma">{info["nome"].upper()}</div>'
                f'<div class="subtitulo-idioma">{info["nome_nativo"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if st.button(f"\U0001F680 Estudar {info['nome']}", key=f"btn_{codigo}", use_container_width=True, type="primary"):
                st.session_state.idioma = codigo
                ir_para("menu")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("\U0001F4CA Meu Progresso", key="home_progresso", use_container_width=True):
            ir_para("progresso")
    with c2:
        if st.button("\u2699\uFE0F Configura\u00e7\u00f5es", key="home_config", use_container_width=True):
            ir_para("config")

    st.markdown("")

    if st.button("\u2753 Ajuda - Como usar o app", key="home_ajuda", use_container_width=True):
        ir_para("ajuda")
        return