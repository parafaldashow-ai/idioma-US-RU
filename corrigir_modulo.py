from pathlib import Path

conteudo = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para
from logica.gerenciador_dados import carregar_modulo, listar_modulos_flat
from logica.gerenciador_progresso import registrar
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
        cor_nivel = mod_info.get("nivel_cor", "#4ade80")
        nome_nivel = mod_info.get("nivel_nome", "")
    else:
        nome_modulo = modulo_id
        icone_modulo = "📖"
        cor_nivel = "#4ade80"
        nome_nivel = ""

    itens = carregar_modulo(idioma, modulo_id)

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("← Voltar"):
            ir_para("modulos")
    with col_b:
        st.markdown(f"## {icone_modulo} {nome_modulo}")
        if nome_nivel:
            st.caption(f"Nível: {nome_nivel}")

    if not itens:
        st.warning(f"⚠️ Este módulo ainda está vazio. Volte e escolha outro.")
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

    item = itens[st.session_state.idx_modulo]
    mostrar = st.session_state.mostrar

    st.progress((st.session_state.idx_modulo + 1) / len(itens))
    st.caption(f"Card {st.session_state.idx_modulo + 1} de {len(itens)}")

    traducao = item.get(codigo, "???")
    pronuncia = item.get("pron", "")

    cor_traducao = "#4ade80" if mostrar else "transparent"
    texto_traducao = traducao if mostrar else "•••••"
    texto_pron = pronuncia if mostrar else ""

    card_html = (
        '<div style="background: linear-gradient(135deg, #1e1e2e, #2a2a3e); '
        'border: 1px solid #333; border-radius: 24px; padding: 48px 32px; '
        'text-align: center; margin: 24px 0;">'
        '<div style="color: #888; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">Português</div>'
        f'<div style="font-size: 42px; font-weight: bold; color: #fafafa; margin: 16px 0 24px 0;">{item["pt"]}</div>'
        f'<div style="color: #888; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">{info["bandeira"]} {info["nome"]}</div>'
        f'<div style="font-size: 38px; font-weight: bold; margin-top: 16px; color: {cor_traducao};">{texto_traducao}</div>'
        f'<div style="font-size: 20px; color: #60a5fa; font-style: italic; margin-top: 12px; min-height: 24px;">{texto_pron}</div>'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    if not mostrar:
        if st.button("👁️ Mostrar resposta", use_container_width=True, type="primary"):
            st.session_state.mostrar = True
            st.rerun()
    else:
        col_audio, col_resp = st.columns([1, 1])
        with col_audio:
            try:
                audio_bytes = gerar_audio(traducao, codigo)
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.caption(f"🔇 Áudio indisponível: {e}")
        with col_resp:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Acertei", use_container_width=True):
                    registrar(idioma, modulo_id, item["pt"], True)
                    st.session_state.idx_modulo = (st.session_state.idx_modulo + 1) % len(itens)
                    st.session_state.mostrar = False
                    st.rerun()
            with c2:
                if st.button("❌ Errei", use_container_width=True):
                    registrar(idioma, modulo_id, item["pt"], False)
                    st.session_state.idx_modulo = (st.session_state.idx_modulo + 1) % len(itens)
                    st.session_state.mostrar = False
                    st.rerun()

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        if st.button("⬅️ Anterior", use_container_width=True):
            st.session_state.idx_modulo = (st.session_state.idx_modulo - 1) % len(itens)
            st.session_state.mostrar = False
            st.rerun()
    with nav2:
        if st.button("🔀 Aleatório", use_container_width=True):
            import random
            novo = random.randrange(len(itens))
            if novo == st.session_state.idx_modulo and len(itens) > 1:
                novo = (novo + 1) % len(itens)
            st.session_state.idx_modulo = novo
            st.session_state.mostrar = False
            st.rerun()
    with nav3:
        if st.button("Próximo ➡️", use_container_width=True):
            st.session_state.idx_modulo = (st.session_state.idx_modulo + 1) % len(itens)
            st.session_state.mostrar = False
            st.rerun()
'''

caminho = Path(__file__).parent / "telas" / "tela_modulo.py"
caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho} sobrescrito")
print("Reinicie o Streamlit e teste novamente.")