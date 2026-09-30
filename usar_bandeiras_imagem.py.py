from pathlib import Path

BASE = Path(__file__).parent

# ============================================================
# PARTE 1: Atualizar config.py
# ============================================================
print("Atualizando config.py...")

caminho_cfg = BASE / "config.py"
conteudo = caminho_cfg.read_text(encoding="utf-8")

# Substituir o IDIOMAS
config_novo = '''from pathlib import Path

BASE_DIR = Path(__file__).parent

DADOS_DIR = BASE_DIR / "dados"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BANCO_DIR = BASE_DIR / "banco"
DB_PATH = BANCO_DIR / "progresso.db"

IDIOMAS = {
    "ingles": {
        "nome": "Inglês",
        "nome_nativo": "English",
        "bandeira": "🇺🇸",
        "bandeira_alt": "",
        "bandeira_img": "bandeira_ingles.png",
        "codigo_audio": "en",
    },
    "russo": {
        "nome": "Russo",
        "nome_nativo": "Русский",
        "bandeira": "🇷🇺",
        "bandeira_alt": "",
        "bandeira_img": "bandeira_russia.png",
        "codigo_audio": "ru",
    },
}

# Bandeiras pros labels (Português, Inglês, Russo)
BANDEIRA_PT = "bandeira_brasil.png"

CORES = {
    "bg": "#0f1419",
    "bg_alt": "#1a2332",
    "card_bg": "#1a2332",
    "card_border": "#2d3748",
    "texto": "#ffffff",
    "texto_sub": "#a8b2c1",
    "texto_muted": "#6b7280",
    "primaria": "#34d399",
    "secundaria": "#3b82f6",
    "terciaria": "#a78bfa",
    "erro": "#ef4444",
    "aviso": "#fbbf24",
    "sucesso": "#34d399",
}

BANCO_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def caminho_bandeira(nome_arquivo):
    """Retorna o caminho completo de uma imagem de bandeira."""
    return IMAGES_DIR / nome_arquivo
'''

caminho_cfg.write_text(config_novo, encoding="utf-8")
print("OK: config.py atualizado")

# ============================================================
# PARTE 2: Atualizar tela_inicial.py
# ============================================================
print()
print("Atualizando tela_inicial.py...")

conteudo_inicial = '''import streamlit as st
from config import IDIOMAS, CORES, caminho_bandeira
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
    }
    .card-idioma:hover {
        border-color: #34d399;
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(52, 211, 153, 0.25);
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
            # Card com a bandeira (imagem)
            st.markdown('<div class="card-idioma">', unsafe_allow_html=True)
            st.image(str(caminho_bandeira(info["bandeira_img"])), width=200)
            st.markdown(f'<div class="titulo-idioma">{info["nome"].upper()}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="subtitulo-idioma">{info["nome_nativo"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

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
'''

caminho_inicial = BASE / "telas" / "tela_inicial.py"
caminho_inicial.write_text(conteudo_inicial, encoding="utf-8")
print("OK: tela_inicial.py atualizada")

# ============================================================
# PARTE 3: Atualizar tela_modulo.py
# ============================================================
print()
print("Atualizando tela_modulo.py...")

conteudo_modulo = '''import streamlit as st
import random
from config import IDIOMAS, caminho_bandeira, BANDEIRA_PT
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
    else:
        nome_modulo = modulo_id
        icone_modulo = "📖"
        nome_nivel = ""

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
        'text-transform: uppercase; font-weight: 600;">📖 Portugues</div>'
        f'<div style="font-size: 38px; font-weight: 800; color: #ffffff; '
        f'margin: 12px 0 28px 0;">{pt}</div>'
        f'<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; '
        f'text-transform: uppercase; font-weight: 600;">🎯 {info["nome"]}</div>'
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

caminho_modulo = BASE / "telas" / "tela_modulo.py"
caminho_modulo.write_text(conteudo_modulo, encoding="utf-8")
print("OK: tela_modulo.py atualizada")

# ============================================================
# PARTE 4: Atualizar tela_menu_idioma.py
# ============================================================
print()
print("Atualizando tela_menu_idioma.py...")

conteudo_menu = '''import streamlit as st
from config import IDIOMAS, caminho_bandeira
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
        st.markdown(f"## {info['nome'].upper()}")

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
'''

caminho_menu = BASE / "telas" / "tela_menu_idioma.py"
caminho_menu.write_text(conteudo_menu, encoding="utf-8")
print("OK: tela_menu_idioma.py atualizada")

print()
print("=" * 50)
print("Bandeiras como imagem configuradas!")
print("Agora reinicie o Streamlit.")
print("=" * 50)