from pathlib import Path

BASE = Path(__file__).parent

print("Atualizando telas...")
print()

# ============================================================
# 1. tela_modulo.py - flashcard
# ============================================================
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
    st.caption(f"📌 Card {idx + 1} de {total} · ✅ {dominados} dominadas")

    traducao = item.get(codigo, "???")
    pronuncia = item.get("pron", "")

    if mostrar:
        bloco_traducao = (
            f'<div style="font-size: 46px; font-weight: 800; color: #34d399; '
            f'margin-top: 20px; text-shadow: 0 0 20px rgba(52, 211, 153, 0.3);">{traducao}</div>'
        )
        bloco_pron = (
            f'<div style="background: rgba(96, 165, 250, 0.15); '
            f'border: 2px solid #60a5fa; border-radius: 14px; '
            f'padding: 16px 28px; margin-top: 24px; '
            f'display: inline-block; box-shadow: 0 4px 20px rgba(96, 165, 250, 0.2);">'
            f'<span style="font-size: 28px; color: #60a5fa; font-weight: 700;">'
            f'🔊 {pronuncia}'
            f'</span>'
            f'</div>'
        )
    else:
        bloco_traducao = '<div style="font-size: 46px; font-weight: 800; color: #2d3748; margin-top: 20px;">•••••</div>'
        bloco_pron = ''

    card_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 56px 32px; '
        'text-align: center; margin: 24px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">'
        '<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 3px; text-transform: uppercase;">🇧🇷 Portugues</div>'
        f'<div style="font-size: 44px; font-weight: 800; color: #ffffff; margin: 20px 0 28px 0;">{item["pt"]}</div>'
        f'<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 3px; text-transform: uppercase;">{info["bandeira"]} {info["nome"]}</div>'
        f'{bloco_traducao}'
        f'{bloco_pron}'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    if not mostrar:
        st.caption("💭 Tente lembrar a traducao antes de clicar")
        if st.button("👁️ Mostrar resposta", use_container_width=True, type="primary", key="btn_mostrar"):
            st.session_state.mostrar = True
            st.rerun()
    else:
        try:
            audio_bytes = gerar_audio(traducao, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"🔇 Audio indisponivel: {e}")

        st.caption("🤔 Voce lembrou? Marque pra registrar:")
        col_acerto, col_erro = st.columns(2)
        with col_acerto:
            if st.button("✅ Acertei", use_container_width=True, type="primary", key="btn_acerto"):
                registrar(idioma, modulo_id, item["pt"], True)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.success(f"🎉 Bom! +1 acerto em {item['pt']}")
                st.rerun()
        with col_erro:
            if st.button("❌ Errei", use_container_width=True, key="btn_erro"):
                registrar(idioma, modulo_id, item["pt"], False)
                st.session_state.idx_modulo = (idx + 1) % total
                st.session_state.mostrar = False
                st.error(f"💪 Ok, {item['pt']} vai voltar mais vezes")
                st.rerun()

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("⬅️ Anterior", use_container_width=True, key="nav_anterior"):
            st.session_state.idx_modulo = (idx - 1) % total
            st.session_state.mostrar = False
            st.rerun()

    with nav2:
        if st.button("🎲 Aleatorio", use_container_width=True, key="nav_aleatorio"):
            novo = random.randrange(total)
            if novo == idx and total > 1:
                novo = (novo + 1) % total
            st.session_state.idx_modulo = novo
            st.session_state.mostrar = False
            st.rerun()

    with nav3:
        if st.button("➡️ Proximo", use_container_width=True, key="nav_proximo"):
            st.session_state.idx_modulo = (idx + 1) % total
            st.session_state.mostrar = False
            st.rerun()
'''

(BASE / "telas" / "tela_modulo.py").write_text(conteudo, encoding="utf-8")
print("OK: tela_modulo.py")

# ============================================================
# 2. tela_modulos.py - grid
# ============================================================
conteudo = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dados import carregar_indice_modulos, carregar_modulo
from logica.gerenciador_progresso import progresso_modulo


def render():
    idioma = st.session_state.idioma
    info = IDIOMAS[idioma]

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_modulos"):
            voltar()
    with col_b:
        st.markdown(f"## 📖 Modulos · {info['bandeira']} {info['nome']}")

    st.markdown("---")

    indice = carregar_indice_modulos(idioma)
    niveis = indice.get("niveis", [])

    if not niveis:
        st.warning("Nenhum modulo encontrado.")
        return

    for nivel in niveis:
        st.markdown(
            f'<div style="'
            f'background: linear-gradient(90deg, {nivel["cor"]}22, transparent); '
            f'border-left: 5px solid {nivel["cor"]}; '
            f'padding: 16px 20px; '
            f'border-radius: 10px; '
            f'margin: 32px 0 20px 0; '
            f'box-shadow: 0 4px 16px rgba(0,0,0,0.2);">'
            f'<div style="font-size: 24px; font-weight: 800; color: {nivel["cor"]}; letter-spacing: 1px;">'
            f'{nivel["icone"]} {nivel["nome"].upper()}'
            f'</div>'
            f'<div style="font-size: 14px; color: #a8b2c1; margin-top: 4px;">{nivel.get("descricao", "")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        modulos = nivel.get("modulos", [])

        for i in range(0, len(modulos), 3):
            cols = st.columns(3)
            for col, mod in zip(cols, modulos[i:i+3]):
                with col:
                    itens = carregar_modulo(idioma, mod["id"])
                    prog = progresso_modulo(idioma, mod["id"])
                    dominados = sum(1 for p in prog if p["dominado"])
                    total = len(itens)
                    pct = int((dominados / total * 100) if total else 0)

                    if total == 0:
                        contador = "vazio"
                        cor_contador = "#666"
                    else:
                        contador = f"✅ {dominados}/{total} · {pct}%"
                        cor_contador = "#a8b2c1"

                    card_html = (
                        f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                        f'border: 2px solid {nivel["cor"]}33; '
                        f'border-radius: 18px; padding: 28px 20px; text-align: center; '
                        f'margin-bottom: 12px; min-height: 180px; '
                        f'box-shadow: 0 4px 16px rgba(0,0,0,0.2);">'
                        f'<div style="font-size: 48px; line-height: 1;">{mod["icone"]}</div>'
                        f'<div style="font-size: 17px; font-weight: 700; color: #ffffff; margin: 12px 0;">{mod["nome"]}</div>'
                        f'<div style="font-size: 13px; color: {cor_contador};">{contador}</div>'
                        f'<div style="height: 8px; background: #0f1419; border-radius: 4px; margin-top: 12px; overflow: hidden;">'
                        f'<div style="width: {pct}%; height: 100%; background: {nivel["cor"]}; transition: width 0.5s ease;"></div>'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

                    if st.button(
                        "📖 Abrir",
                        key=f'abrir_{mod["id"]}',
                        use_container_width=True,
                        disabled=(total == 0),
                    ):
                        st.session_state.modulo_atual = mod["id"]
                        st.session_state.idx_modulo = 0
                        st.session_state.mostrar = False
                        ir_para("modulo")
'''

(BASE / "telas" / "tela_modulos.py").write_text(conteudo, encoding="utf-8")
print("OK: tela_modulos.py")

# ============================================================
# 3. tela_menu_idioma.py
# ============================================================
conteudo = '''import streamlit as st
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
        ("📖", "Modulos",     "modulos",      "#34d399"),
        ("✏️", "Exercicios",  "exercicio",    "#60a5fa"),
        ("🎴", "Flashcards",  "flashcards",   "#a78bfa"),
        ("🔍", "Dicionario",  "dicionario",   "#fbbf24"),
        ("📊", "Progresso",   "progresso_idioma", "#ef4444"),
        ("📝", "Anotacoes",   "anotacoes",    "#ec4899"),
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

(BASE / "telas" / "tela_menu_idioma.py").write_text(conteudo, encoding="utf-8")
print("OK: tela_menu_idioma.py")

# ============================================================
# 4. tela_config.py - refinar visual
# ============================================================
caminho_cfg = BASE / "telas" / "tela_config.py"
conteudo_cfg = caminho_cfg.read_text(encoding="utf-8")

# Trocar "← Voltar" por "⬅️ Voltar"
conteudo_cfg = conteudo_cfg.replace('"← Voltar"', '"⬅️ Voltar"')
conteudo_cfg = conteudo_cfg.replace('"<- Voltar"', '"⬅️ Voltar"')

# Adicionar emojis nos botoes principais
conteudo_cfg = conteudo_cfg.replace('"💾 Salvar preferências de estudo"', '"💾 Salvar preferências de estudo"')
conteudo_cfg = conteudo_cfg.replace('"💾 Salvar e aplicar"', '"💾 Salvar e aplicar"')

caminho_cfg.write_text(conteudo_cfg, encoding="utf-8")
print("OK: tela_config.py")

# ============================================================
# 5. tela_progresso.py - refinar
# ============================================================
conteudo = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_progresso import estatisticas_idioma, streak_atual


def render():
    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_prog"):
            voltar()
    with col_b:
        st.markdown("## 📊 Meu Progresso · Visao Geral")

    st.markdown("---")

    streak = streak_atual()
    if streak > 0:
        texto_streak = f"🔥 {streak} dia{'s' if streak != 1 else ''} seguido{'s' if streak != 1 else ''}!"
        html_streak = (
            '<div style="background: linear-gradient(135deg, #ef4444, #f97316); '
            'border-radius: 18px; padding: 24px 28px; margin-bottom: 28px; text-align: center; '
            'box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);">'
            '<div style="font-size: 48px; line-height: 1;">🔥</div>'
            f'<div style="font-size: 26px; font-weight: 800; color: #ffffff; margin-top: 8px;">{texto_streak}</div>'
            '<div style="font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 4px;">Continue assim!</div>'
            '</div>'
        )
        st.markdown(html_streak, unsafe_allow_html=True)
    else:
        st.info("💪 Comece a estudar hoje pra iniciar uma sequencia!")

    col1, col2 = st.columns(2)

    for col, (codigo, info) in zip([col1, col2], IDIOMAS.items()):
        with col:
            stats = estatisticas_idioma(codigo)
            dominadas = stats["dominadas"]
            estudadas = stats["estudadas"]
            total = stats["total_disponivel"]
            pct = int((dominadas / total * 100) if total else 0)
            total_fmt = f"{total:,}".replace(",", ".")

            cor_bandeira = "#34d399" if codigo == "ingles" else "#60a5fa"

            card_html = (
                f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                f'border: 2px solid {cor_bandeira}33; border-radius: 22px; padding: 32px; '
                f'margin-bottom: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">'
                '<div style="text-align: center; margin-bottom: 24px;">'
                f'<div style="font-size: 56px; line-height: 1;">{info["bandeira"]}</div>'
                f'<div style="font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 10px; letter-spacing: 1px;">{info["nome"].upper()}</div>'
                '</div>'
                '<div style="display: flex; justify-content: space-around; margin-bottom: 24px; text-align: center;">'
                '<div>'
                f'<div style="font-size: 32px; font-weight: 800; color: #34d399;">{dominadas}</div>'
                '<div style="font-size: 11px; color: #a8b2c1; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">dominadas</div>'
                '</div>'
                '<div>'
                f'<div style="font-size: 32px; font-weight: 800; color: #60a5fa;">{estudadas}</div>'
                '<div style="font-size: 11px; color: #a8b2c1; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">estudadas</div>'
                '</div>'
                '<div>'
                f'<div style="font-size: 32px; font-weight: 800; color: #a78bfa;">{total_fmt}</div>'
                '<div style="font-size: 11px; color: #a8b2c1; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">disponiveis</div>'
                '</div>'
                '</div>'
                '<div style="margin-bottom: 12px;">'
                '<div style="display: flex; justify-content: space-between; font-size: 13px; color: #a8b2c1; margin-bottom: 6px;">'
                '<span>Progresso</span>'
                f'<span><b style="color: {cor_bandeira}; font-size: 15px;">{pct}%</b></span>'
                '</div>'
                '<div style="height: 12px; background: #0f1419; border-radius: 6px; overflow: hidden;">'
                f'<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #34d399, #60a5fa); transition: width 0.5s ease;"></div>'
                '</div>'
                '</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

            if st.button(f"📖 Ver detalhes de {info['nome']}", use_container_width=True, key=f"det_{codigo}"):
                st.session_state.idioma_progresso = codigo
                ir_para("progresso_idioma")

    st.markdown("---")
    st.markdown("### 📈 Totais gerais")

    stats_en = estatisticas_idioma("ingles")
    stats_ru = estatisticas_idioma("russo")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("📚 Palavras disponiveis", stats_en["total_disponivel"] + stats_ru["total_disponivel"])
    with c2:
        st.metric("✅ Dominadas", stats_en["dominadas"] + stats_ru["dominadas"])
    with c3:
        st.metric("🔥 Dias seguidos", streak)
'''

(BASE / "telas" / "tela_progresso.py").write_text(conteudo, encoding="utf-8")
print("OK: tela_progresso.py")

# ============================================================
# 6. tela_inicial.py - refinar
# ============================================================
conteudo = '''import streamlit as st
from config import IDIOMAS, CORES
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
    .bandeira { font-size: 80px; line-height: 1; }
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
            st.markdown(f"""
            <div class="card-idioma">
                <div class="bandeira">{info['bandeira']} {info.get('bandeira_alt', '')}</div>
                <div class="titulo-idioma">{info['nome'].upper()}</div>
                <div class="subtitulo-idioma">{info['nome_nativo']}</div>
            </div>
            """, unsafe_allow_html=True)
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

(BASE / "telas" / "tela_inicial.py").write_text(conteudo, encoding="utf-8")
print("OK: tela_inicial.py")

# ============================================================
# 7. main.py - CSS global
# ============================================================
conteudo = '''import streamlit as st
from logica.navegacao import init_estado, renderizar_tela_atual
from logica.gerenciador_progresso import init_db
from logica.gerenciador_exercicios import init_db_exercicios
from logica.gerenciador_config import carregar_config

st.set_page_config(
    page_title="Lingua App",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()
init_db_exercicios()
init_estado()

config = carregar_config()
tema = config.get("tema", "escuro")

if tema == "claro":
    bg = "#ffffff"
    texto = "#0f1419"
    texto_sub = "#4b5563"
    card_bg = "#f8fafc"
    card_border = "#e2e8f0"
else:
    bg = "#0f1419"
    texto = "#ffffff"
    texto_sub = "#a8b2c1"
    card_bg = "#1a2332"
    card_border = "#2d3748"

st.markdown(f"""
<style>
    /* Fundo geral */
    .stApp {{
        background-color: {bg} !important;
    }}

    /* Texto de titulos */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {texto} !important;
    }}

    /* Texto geral */
    .stApp p, .stApp label, .stApp .stMarkdown {{
        color: {texto};
    }}

    /* Texto secundario */
    .stApp .stCaption, .stApp small {{
        color: {texto_sub} !important;
    }}

    /* Botoes */
    .stButton > button {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background-color: #253045 !important;
        border-color: #34d399 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(52, 211, 153, 0.2) !important;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #f87171, #ef4444) !important;
        box-shadow: 0 6px 24px rgba(239, 68, 68, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button:disabled {{
        opacity: 0.4 !important;
    }}

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        border-radius: 10px !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: #34d399 !important;
        box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.2) !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        color: {texto} !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        background-color: {card_bg} !important;
        border-radius: 10px !important;
    }}

    /* Metrics */
    .stMetric {{
        background-color: {card_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }}
    .stMetric label {{
        color: {texto_sub} !important;
        font-weight: 600 !important;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {texto} !important;
        font-weight: 800 !important;
    }}

    /* Alerts */
    .stAlert {{
        border-radius: 14px !important;
        border-left-width: 5px !important;
    }}

    /* Divisor */
    hr {{
        border-color: {card_border} !important;
        margin: 24px 0 !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        color: {texto_sub} !important;
        font-weight: 600 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #34d399 !important;
        font-weight: 700 !important;
    }}

    /* Progress bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #34d399, #60a5fa) !important;
    }}

    /* Radio / checkbox */
    .stRadio label, .stCheckbox label {{
        color: {texto} !important;
    }}
</style>
""", unsafe_allow_html=True)

renderizar_tela_atual()
'''

(BASE / "main.py").write_text(conteudo, encoding="utf-8")
print("OK: main.py")

# ============================================================
# 8. tela_exercicio.py - adicionar emojis
# ============================================================
caminho_ex = BASE / "telas" / "tela_exercicio.py"
conteudo_ex = caminho_ex.read_text(encoding="utf-8")

# Trocar botoes por versoes com emoji
conteudo_ex = conteudo_ex.replace('"<- Voltar"', '"⬅️ Voltar"')
conteudo_ex = conteudo_ex.replace('"Proxima questao"', '"➡️ Proxima questao"')
conteudo_ex = conteudo_ex.replace('"Mostrar dica (primeira letra)"', '"💡 Mostrar dica (primeira letra)"')
conteudo_ex = conteudo_ex.replace('"Verificar"', '"✅ Verificar"')
conteudo_ex = conteudo_ex.replace('"Refazer esse modulo"', '"🔁 Refazer esse modulo"')
conteudo_ex = conteudo_ex.replace('"Escolher outro modulo"', '"📚 Escolher outro modulo"')

caminho_ex.write_text(conteudo_ex, encoding="utf-8")
print("OK: tela_exercicio.py")

print()
print("=" * 50)
print("Visual refinado em 8 arquivos!")
print("Agora reinicie o Streamlit.")
print("=" * 50)