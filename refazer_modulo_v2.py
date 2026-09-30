import sqlite3
from pathlib import Path
from config import DB_PATH

# ============================================================
# PARTE 1: Atualizar o banco (adicionar coluna visualizacoes)
# ============================================================
print("Atualizando banco...")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("PRAGMA table_info(progresso)")
colunas = [row[1] for row in c.fetchall()]

if "visualizacoes" not in colunas:
    c.execute("ALTER TABLE progresso ADD COLUMN visualizacoes INTEGER DEFAULT 0")
    conn.commit()
    print("OK: coluna 'visualizacoes' adicionada")
else:
    print("OK: coluna 'visualizacoes' ja existe")

conn.close()

# ============================================================
# PARTE 2: Atualizar gerenciador_progresso.py
# ============================================================
print()
print("Atualizando gerenciador_progresso.py...")

caminho_ger = Path(__file__).parent / "logica" / "gerenciador_progresso.py"
conteudo = caminho_ger.read_text(encoding="utf-8")

funcoes_visualizacao = '''


# ============================================================
# VISUALIZACOES (progresso dos modulos)
# ============================================================

def registrar_visualizacao(idioma, modulo, item):
    """Registra que o usuario viu o card (sem contar acerto/erro)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO progresso (idioma, modulo, item, visualizacoes)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(idioma, modulo, item) DO UPDATE SET
            visualizacoes = visualizacoes + 1
    """, (idioma, modulo, item))
    conn.commit()
    conn.close()


def contar_visualizacoes_modulo(idioma, modulo):
    """Retorna quantos itens unicos do modulo ja foram vistos."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM progresso
        WHERE idioma=? AND modulo=? AND visualizacoes > 0
    """, (idioma, modulo))
    total = c.fetchone()[0]
    conn.close()
    return total or 0
'''

if "registrar_visualizacao" not in conteudo:
    conteudo += funcoes_visualizacao
    caminho_ger.write_text(conteudo, encoding="utf-8")
    print("OK: funcoes adicionadas")
else:
    print("OK: funcoes ja existiam")

# ============================================================
# PARTE 3: Reescrever tela_modulo.py
# ============================================================
print()
print("Reescrevendo tela_modulo.py...")

conteudo_modulo = '''import streamlit as st
import random
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dados import carregar_modulo, listar_modulos_flat
from logica.gerenciador_progresso import registrar_visualizacao, contar_visualizacoes_modulo
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
        icone_modulo = "📖"
        nome_nivel = ""
        cor_nivel = "#34d399"

    itens = carregar_modulo(idioma, modulo_id)

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_modulo"):
            voltar()
    with col_b:
        st.markdown(f"## {icone_modulo} {nome_modulo}")
        if nome_nivel:
            st.caption(f"📊 Nivel: {nome_nivel}")

    if not itens:
        st.warning("Este modulo ainda esta vazio.")
        return

    if "idx_modulo" not in st.session_state:
        st.session_state.idx_modulo = 0

    if st.session_state.get("_modulo_anterior") != modulo_id:
        st.session_state.idx_modulo = 0
        st.session_state._modulo_anterior = modulo_id

    if st.session_state.idx_modulo >= len(itens):
        st.session_state.idx_modulo = 0

    idx = st.session_state.idx_modulo
    item = itens[idx]
    total = len(itens)

    registrar_visualizacao(idioma, modulo_id, item["pt"])
    vistos = contar_visualizacoes_modulo(idioma, modulo_id)

    st.progress(vistos / total)
    st.caption(f"📌 Card {idx + 1} de {total} · 👁️ {vistos}/{total} vistos")

    traducao = item.get(codigo, "???")
    pronuncia = item.get("pron", "")
    pt = item.get("pt", "?")

    if pronuncia:
        bloco_pron = (
            f'<div style="background: rgba(96, 165, 250, 0.15); '
            f'border: 2px solid #60a5fa; border-radius: 14px; '
            f'padding: 14px 28px; margin-top: 20px; '
            f'display: inline-block; box-shadow: 0 4px 20px rgba(96, 165, 250, 0.2);">'
            f'<span style="font-size: 24px; color: #60a5fa; font-weight: 700;">'
            f'🔊 {pronuncia}'
            f'</span>'
            f'</div>'
        )
    else:
        bloco_pron = ""

    card_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 48px 32px; '
        'text-align: center; margin: 24px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">'
        '<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; '
        'text-transform: uppercase; font-weight: 600;">🇧🇷 Portugues</div>'
        f'<div style="font-size: 38px; font-weight: 800; color: #ffffff; '
        f'margin: 12px 0 28px 0;">{pt}</div>'
        f'<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; '
        f'text-transform: uppercase; font-weight: 600;">{info["bandeira"]} {info["nome"]}</div>'
        f'<div style="font-size: 38px; font-weight: 800; color: #34d399; '
        f'margin: 12px 0 4px 0; text-shadow: 0 0 20px rgba(52, 211, 153, 0.3);">{traducao}</div>'
        f'{bloco_pron}'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    try:
        audio_bytes = gerar_audio(traducao, codigo)
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.caption(f"🔇 Audio indisponivel: {e}")

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("⬅️ Anterior", use_container_width=True, key="nav_anterior"):
            st.session_state.idx_modulo = (idx - 1) % total
            st.rerun()

    with nav2:
        if st.button("🎲 Aleatorio", use_container_width=True, key="nav_aleatorio"):
            novo = random.randrange(total)
            if novo == idx and total > 1:
                novo = (novo + 1) % total
            st.session_state.idx_modulo = novo
            st.rerun()

    with nav3:
        if st.button("➡️ Proximo", use_container_width=True, key="nav_proximo"):
            st.session_state.idx_modulo = (idx + 1) % total
            st.rerun()
'''

caminho_mod = Path(__file__).parent / "telas" / "tela_modulo.py"
caminho_mod.write_text(conteudo_modulo, encoding="utf-8")
print("OK: tela_modulo.py reescrita")

print()
print("=" * 50)
print("Modulo reformulado v2!")
print("Reinicie o Streamlit.")
print("=" * 50)