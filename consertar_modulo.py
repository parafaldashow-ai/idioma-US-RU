from pathlib import Path

conteudo = '''import streamlit as st
import random
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dados import carregar_modulo, listar_modulos_flat
from logica.gerenciador_progresso import registrar, progresso_modulo
from logica.gerenciador_audio import gerar_audio


def render():
    idioma = st.session_state.get("idioma")
    modulo_id = st.session_state.get("modulo_atual")

    if not idioma or not modulo_id:
        ir_para("modulos")
        return

    info = IDIOMAS[idioma]
    codigo = info["codigo_audio"]

    modulos = listar_modulos_flat(idioma)
    mod_info = next((m for m in modulos if m["id"] == modulo_id), None)

    if mod_info:
        nome_modulo = mod_info["nome"]
        icone_modulo = mod_info["icone"]
        nome_nivel = mod_info.get("nivel_nome", "")
        cor_nivel = mod_info.get("nivel_cor", "#34d399")
    else:
        nome_modulo = modulo_id
        icone_modulo = "?"
        nome_nivel = ""
        cor_nivel = "#34d399"

    itens = carregar_modulo(idioma, modulo_id)

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_modulo"):
            voltar()
    with col_b:
        st.markdown(f"## {icone_modulo} {nome_modulo}")
        if nome_nivel:
            st.caption(f"Nivel: {nome_nivel}")

    if not itens:
        st.warning("Este modulo ainda esta vazio.")
        return

    if "idx_modulo" not in st.session_state:
        st.session_state.idx_modulo = 0
    if "mostrar" not in st.session_state:
        st.session_state.mostrar = False

    if st.session_state.get("_modulo_anterior") != modulo_id:
        st.session_state.idx_modulo = 0
        st.session_state.mostrar = False
        st.session_state._modulo_anterior = modulo_id

    if st.session_state.idx_modulo >= len(itens):
        st.session_state.idx_modulo = 0

    idx = st.session_state.idx_modulo
    item = itens[idx]
    mostrar = st.session_state.mostrar

    progresso_atual = progresso_modulo(idioma, modulo_id)
    dominados = sum(1 for p in progresso_atual if p["dominado"])
    total = len(itens)

    st.progress((idx + 1) / total)
    st.caption(f"Card {idx + 1} de {total} - {dominados} dominadas")

    traducao = item.get(codigo, "???")
    pronuncia = item.get("pron", "")

    cor_traducao = "#34d399" if mostrar else "transparent"
    texto_traducao = traducao if mostrar else "..."
    texto_pron = pronuncia if mostrar else ""

    card_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 48px 32px; '
        'text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">Portugues</div>'
        f'<div style="font-size: 42px; font-weight: bold; color: #ffffff; margin: 16px 0 24px 0;">{item["pt"]}</div>'
        f'<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">{info["bandeira"]} {info["nome"]}</div>'
        f'<div style="font-size: 38px; font-weight: bold; margin-top: 16px; color: {cor_traducao};">{texto_traducao}</div>'
        f'<div style="font-size: 20px; color: #60a5fa; font-style: italic; margin-top: 12px; min-height: 24px;">{texto_pron}</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    if mostrar:
        try:
            audio_bytes = gerar_audio(traducao, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"Audio indisponivel: {e}")

    if not mostrar:
        col_mostrar, col_acerto, col_erro = st.columns([2, 1, 1])
        with col_mostrar:
            if st.button("Mostrar resposta", use_container_width=True, type="primary", key="btn_mostrar"):
                st.session_state.mostrar = True
                st.rerun()
        with col_acerto:
            if st.button("Acertei", use_container_width=True, key="btn_acerto_direto"):
                registrar(idioma, modulo_id, item["pt"], True)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.success(f"Bom! +1 acerto em {item['pt']}")
                st.rerun()
        with col_erro:
            if st.button("Errei", use_container_width=True, key="btn_erro_direto"):
                registrar(idioma, modulo_id, item["pt"], False)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.error(f"Ok, {item['pt']} vai voltar mais vezes")
                st.rerun()
    else:
        col_acerto, col_erro = st.columns(2)
        with col_acerto:
            if st.button("Acertei", use_container_width=True, type="primary", key="btn_acerto"):
                registrar(idioma, modulo_id, item["pt"], True)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.success(f"Bom! +1 acerto em {item['pt']}")
                st.rerun()
        with col_erro:
            if st.button("Errei", use_container_width=True, key="btn_erro"):
                registrar(idioma, modulo_id, item["pt"], False)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.error(f"Ok, {item['pt']} vai voltar mais vezes")
                st.rerun()

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("Anterior", use_container_width=True, key="nav_anterior"):
            st.session_state.idx_modulo = (idx - 1) % total
            st.session_state.mostrar = False
            st.rerun()

    with nav2:
        if st.button("Aleatorio", use_container_width=True, key="nav_aleatorio"):
            novo = random.randrange(total)
            if novo == idx and total > 1:
                novo = (novo + 1) % total
            st.session_state.idx_modulo = novo
            st.session_state.mostrar = False
            st.rerun()

    with nav3:
        if st.button("Proximo", use_container_width=True, key="nav_proximo"):
            st.session_state.idx_modulo = (idx + 1) % total
            st.session_state.mostrar = False
            st.rerun()
'''

caminho = Path(__file__).parent / "telas" / "tela_modulo.py"
caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho} reescrito")
print("Reinicie o Streamlit.")