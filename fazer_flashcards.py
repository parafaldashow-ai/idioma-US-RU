from pathlib import Path

BASE = Path(__file__).parent

# PARTE 1: gerenciador_flashcards.py
print("Criando gerenciador_flashcards.py...")

conteudo_ger = """import sqlite3
from config import DB_PATH
from logica.gerenciador_dados import listar_modulos_flat, carregar_modulo


def _carregar_item_completo(idioma, modulo, item_pt):
    itens = carregar_modulo(idioma, modulo)
    for item in itens:
        if item.get("pt") == item_pt:
            return item
    return None


def _info_modulo(idioma, modulo_id):
    for mod in listar_modulos_flat(idioma):
        if mod["id"] == modulo_id:
            return mod
    return None


def pegar_nao_dominadas(idioma, limite=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT modulo, item, visualizacoes FROM progresso WHERE idioma = ? AND visualizacoes > 0", (idioma,))
    vistos = [dict(r) for r in c.fetchall()]
    c.execute("SELECT modulo, item, acertos FROM progresso_exercicios WHERE idioma = ?", (idioma,))
    acertos = {}
    for row in c.fetchall():
        k = (row["modulo"], row["item"])
        acertos[k] = acertos.get(k, 0) + row["acertos"]
    conn.close()
    resultado = []
    for v in vistos:
        k = (v["modulo"], v["item"])
        if acertos.get(k, 0) < 3:
            item = _carregar_item_completo(idioma, v["modulo"], v["item"])
            if item:
                mi = _info_modulo(idioma, v["modulo"])
                if mi:
                    item["_modulo"] = mi["nome"]
                    item["_modulo_id"] = v["modulo"]
                    item["_icone"] = mi["icone"]
                    item["_nivel"] = mi["nivel_nome"]
                    item["_nivel_cor"] = mi["nivel_cor"]
                    item["_acertos"] = acertos.get(k, 0)
                    item["_erros"] = 0
                    resultado.append(item)
    if limite:
        resultado = resultado[:limite]
    return resultado


def pegar_erradas(idioma, limite=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT modulo, item, SUM(acertos) as ta, SUM(erros) as te FROM progresso_exercicios WHERE idioma = ? AND erros > 0 GROUP BY modulo, item ORDER BY te DESC", (idioma,))
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    resultado = []
    for l in linhas:
        item = _carregar_item_completo(idioma, l["modulo"], l["item"])
        if item:
            mi = _info_modulo(idioma, l["modulo"])
            if mi:
                item["_modulo"] = mi["nome"]
                item["_modulo_id"] = l["modulo"]
                item["_icone"] = mi["icone"]
                item["_nivel"] = mi["nivel_nome"]
                item["_nivel_cor"] = mi["nivel_cor"]
                item["_acertos"] = l["ta"]
                item["_erros"] = l["te"]
                resultado.append(item)
    if limite:
        resultado = resultado[:limite]
    return resultado


def pegar_aleatorias(idioma, quantidade=20):
    import random
    todos = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            ic = dict(item)
            ic["_modulo"] = mod["nome"]
            ic["_modulo_id"] = mod["id"]
            ic["_icone"] = mod["icone"]
            ic["_nivel"] = mod["nivel_nome"]
            ic["_nivel_cor"] = mod["nivel_cor"]
            ic["_acertos"] = 0
            ic["_erros"] = 0
            todos.append(ic)
    random.shuffle(todos)
    return todos[:quantidade]


def contar_nao_dominadas(idioma):
    return len(pegar_nao_dominadas(idioma))


def contar_erradas(idioma):
    return len(pegar_erradas(idioma))
"""

caminho = BASE / "logica" / "gerenciador_flashcards.py"
caminho.write_text(conteudo_ger, encoding="utf-8")
print("OK: gerenciador_flashcards.py criado")

# PARTE 2: tela_flashcards.py
conteudo_tela = """import streamlit as st
import random
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_audio import gerar_audio
from logica.gerenciador_flashcards import (
    pegar_nao_dominadas,
    pegar_erradas,
    pegar_aleatorias,
    contar_nao_dominadas,
    contar_erradas,
)


def idioma_emoji(i):
    return {"ingles": "US", "russo": "RU"}.get(i, "??")


def render():
    idioma = st.session_state.get("idioma") or "ingles"
    info = IDIOMAS.get(idioma, {"bandeira": "?", "nome": "?"})
    codigo = info["codigo_audio"]

    if "fc_modo" not in st.session_state:
        st.session_state.fc_modo = None
    if "fc_cards" not in st.session_state:
        st.session_state.fc_cards = []
    if "fc_idx" not in st.session_state:
        st.session_state.fc_idx = 0

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_fc"):
            if st.session_state.fc_modo:
                st.session_state.fc_modo = None
                st.session_state.fc_cards = []
                st.session_state.fc_idx = 0
                st.rerun()
            else:
                voltar()
                return
    with col_b:
        st.markdown(f"## 🎴 Flashcards - {info['nome']}")

    st.markdown("---")

    if not st.session_state.fc_modo:
        render_menu(idioma, info)
    else:
        render_revisao(idioma, codigo)


def render_menu(idioma, info):
    st.markdown("### Escolha um modo de revisao:")

    qtd_nao_dom = contar_nao_dominadas(idioma)
    qtd_err = contar_erradas(idioma)

    modos = [
        ("nao_dominadas", "🔥", "Nao dominadas", qtd_nao_dom, "#ef4444"),
        ("erradas", "❌", "As que errei", qtd_err, "#f97316"),
        ("aleatorias", "🎲", "Aleatorio", 20, "#a78bfa"),
    ]

    cols = st.columns(3)
    for col, (modo_id, icone, nome, qtd, cor) in zip(cols, modos):
        with col:
            card_html = (
                f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                f'border: 2px solid {cor}44; border-radius: 18px; '
                f'padding: 24px 16px; text-align: center; margin-bottom: 8px; min-height: 180px;">'
                f'<div style="font-size: 52px; line-height: 1;">{icone}</div>'
                f'<div style="font-size: 18px; font-weight: 800; color: {cor}; margin-top: 12px;">{nome}</div>'
                f'<div style="font-size: 28px; font-weight: 800; color: #ffffff; margin-top: 8px;">{qtd}</div>'
                f'<div style="font-size: 12px; color: #a8b2c1; margin-top: 8px;">palavras</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

            if st.button("Abrir", use_container_width=True, key=f"fc_modo_{modo_id}", type="primary"):
                iniciar_revisao(idioma, modo_id)
                st.rerun()

    st.markdown("---")
    st.caption("🔥 Nao dominadas: palavras que voce ja viu mas acertou menos de 3 vezes em exercicios")
    st.caption("❌ Errei: palavras que voce errou em algum exercicio")
    st.caption("🎲 Aleatorio: 20 palavras sorteadas de TODOS os modulos")


def iniciar_revisao(idioma, modo_id):
    if modo_id == "nao_dominadas":
        cards = pegar_nao_dominadas(idioma)
    elif modo_id == "erradas":
        cards = pegar_erradas(idioma)
    else:
        cards = pegar_aleatorias(idioma, quantidade=20)

    if not cards:
        st.warning("Nenhuma palavra nesse modo. Faz mais exercicios primeiro!")
        return

    random.shuffle(cards)
    st.session_state.fc_modo = modo_id
    st.session_state.fc_cards = cards
    st.session_state.fc_idx = 0


def render_revisao(idioma, codigo):
    cards = st.session_state.fc_cards
    idx = st.session_state.fc_idx
    total = len(cards)

    if not cards:
        st.warning("Nenhuma palavra.")
        st.session_state.fc_modo = None
        return

    if idx >= total:
        st.session_state.fc_idx = 0
        idx = 0

    card = cards[idx]

    nomes = {"nao_dominadas": "🔥 Nao dominadas", "erradas": "❌ As que errei", "aleatorias": "🎲 Aleatorio"}
    nome_modo = nomes.get(st.session_state.fc_modo, "Revisao")

    st.progress((idx + 1) / total)
    st.caption(f"{nome_modo} - Card {idx + 1} de {total}")

    traducao = card.get(codigo, "?")
    pron = card.get("pron", "")
    pt = card.get("pt", "?")
    modulo = card.get("_modulo", "")
    icone = card.get("_icone", "?")
    nivel = card.get("_nivel", "")
    nivel_cor = card.get("_nivel_cor", "#34d399")

    if pron:
        bloco_pron = (
            f'<div style="background: rgba(96, 165, 250, 0.15); '
            f'border: 2px solid #60a5fa; border-radius: 14px; '
            f'padding: 12px 24px; margin-top: 20px; display: inline-block;">'
            f'<span style="font-size: 22px; color: #60a5fa; font-weight: 700;">'
            f'Pron: {pron}</span></div>'
        )
    else:
        bloco_pron = ""

    card_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; '
        'padding: 48px 32px; text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; text-transform: uppercase;">Portugues</div>'
        f'<div style="font-size: 38px; font-weight: 800; color: #ffffff; margin: 12px 0 28px 0;">{pt}</div>'
        f'<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; text-transform: uppercase;">{info_nome(idioma)}</div>'
        f'<div style="font-size: 38px; font-weight: 800; color: {nivel_cor}; margin: 12px 0 4px 0;">{traducao}</div>'
        f'{bloco_pron}'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    try:
        audio_bytes = gerar_audio(traducao, codigo)
        st.audio(audio_bytes, format="audio/mp3")
    except Exception:
        pass

    st.caption(f"{icone} {modulo} - {nivel}")

    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("Anterior", use_container_width=True, key="fc_ant"):
            st.session_state.fc_idx = (idx - 1) % total
            st.rerun()

    with nav2:
        if st.button("Aleatorio", use_container_width=True, key="fc_rand"):
            novo = random.randrange(total)
            if novo == idx and total > 1:
                novo = (novo + 1) % total
            st.session_state.fc_idx = novo
            st.rerun()

    with nav3:
        if st.button("Proximo", use_container_width=True, key="fc_prox"):
            st.session_state.fc_idx = (idx + 1) % total
            st.rerun()


def info_nome(idioma):
    return IDIOMAS.get(idioma, {}).get("nome", "?")
"""

caminho = BASE / "telas" / "tela_flashcards.py"
caminho.write_text(conteudo_tela, encoding="utf-8")
print("OK: tela_flashcards.py criada")
print()
print("Flashcards prontos!")
print("Reinicie o Streamlit: streamlit run main.py")
