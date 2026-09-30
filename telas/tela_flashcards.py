import streamlit as st
import random
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_audio import gerar_audio
from logica.gerenciador_exercicios import registrar_exercicio
from logica.gerenciador_flashcards import (
    pegar_nao_dominadas,
    pegar_erradas,
    pegar_aleatorias,
    contar_nao_dominadas,
    contar_erradas,
)


def render():
    idioma = st.session_state.get("idioma") or "ingles"
    info = IDIOMAS.get(idioma, {"bandeira": "?", "nome": "?"})
    codigo = info["codigo_audio"]

    # Estado
    if "fc_modo" not in st.session_state:
        st.session_state.fc_modo = None
    if "fc_cards" not in st.session_state:
        st.session_state.fc_cards = []
    if "fc_idx" not in st.session_state:
        st.session_state.fc_idx = 0
    if "fc_mostrar" not in st.session_state:
        st.session_state.fc_mostrar = False
    if "fc_acertos" not in st.session_state:
        st.session_state.fc_acertos = 0
    if "fc_erros" not in st.session_state:
        st.session_state.fc_erros = 0

    # Header
    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_fc"):
            if st.session_state.fc_modo:
                st.session_state.fc_modo = None
                st.session_state.fc_cards = []
                st.session_state.fc_idx = 0
                st.session_state.fc_mostrar = False
                st.session_state.fc_acertos = 0
                st.session_state.fc_erros = 0
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

    # Limpa cache pra forcar recalculo
    st.cache_data.clear()

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
    st.session_state.fc_mostrar = False
    st.session_state.fc_acertos = 0
    st.session_state.fc_erros = 0


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
        st.session_state.fc_mostrar = False

    card = cards[idx]
    mostrar = st.session_state.fc_mostrar

    nomes = {"nao_dominadas": "🔥 Nao dominadas", "erradas": "❌ As que errei", "aleatorias": "🎲 Aleatorio"}
    nome_modo = nomes.get(st.session_state.fc_modo, "Revisao")

    st.progress((idx + 1) / total)
    col_info1, col_info2, col_info3 = st.columns([2, 1, 1])
    with col_info1:
        st.caption(f"{nome_modo} - Card {idx + 1} de {total}")
    with col_info2:
        st.caption(f"✅ {st.session_state.fc_acertos}")
    with col_info3:
        st.caption(f"❌ {st.session_state.fc_erros}")

    traducao = card.get(codigo, "?")
    pron = card.get("pron", "")
    pt = card.get("pt", "?")
    modulo = card.get("_modulo", "")
    icone = card.get("_icone", "?")
    nivel = card.get("_nivel", "")
    nivel_cor = card.get("_nivel_cor", "#34d399")

    # Bloco da traducao (escondido ou visivel)
    if mostrar:
        bloco_traducao = (
            f'<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; '
            f'text-transform: uppercase; margin-top: 24px;">{IDIOMAS[idioma]["nome"]}</div>'
            f'<div style="font-size: 38px; font-weight: 800; color: {nivel_cor}; '
            f'margin: 12px 0 4px 0;">{traducao}</div>'
        )

        if pron:
            bloco_traducao += (
                f'<div style="background: rgba(96, 165, 250, 0.15); '
                f'border: 2px solid #60a5fa; border-radius: 14px; '
                f'padding: 12px 24px; margin-top: 16px; display: inline-block;">'
                f'<span style="font-size: 22px; color: #60a5fa; font-weight: 700;">'
                f'Pron: {pron}</span></div>'
            )
    else:
        bloco_traducao = (
            f'<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; '
            f'text-transform: uppercase; margin-top: 24px;">{IDIOMAS[idioma]["nome"]}</div>'
            f'<div style="font-size: 38px; font-weight: 800; color: #2d3748; '
            f'margin: 12px 0 4px 0;">?????</div>'
            f'<div style="color: #a8b2c1; font-size: 14px; margin-top: 16px;">'
            f'Tente lembrar antes de revelar</div>'
        )

    card_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; '
        'padding: 48px 32px; text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 12px; letter-spacing: 3px; text-transform: uppercase;">Portugues</div>'
        f'<div style="font-size: 42px; font-weight: 800; color: #ffffff; margin: 12px 0 4px 0;">{pt}</div>'
        f'{bloco_traducao}'
        '</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    # Audio (so se mostrou)
    if mostrar:
        try:
            audio_bytes = gerar_audio(traducao, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception:
            pass

        st.caption(f"{icone} {modulo} - {nivel}")

    # Botoes de acao
    if not mostrar:
        if st.button("Mostrar resposta", use_container_width=True, type="primary", key="fc_mostrar_btn"):
            st.session_state.fc_mostrar = True
            st.rerun()
    else:
        st.markdown("##### Voce lembrou?")
        col_erro, col_acerto = st.columns(2)

        with col_erro:
            if st.button("Errei", use_container_width=True, key="fc_errei"):
                registrar_exercicio(
                    idioma, card.get("_modulo_id", ""), pt,
                    "flashcard", False
                )
                st.session_state.fc_erros += 1
                st.session_state.fc_idx = (idx + 1) % total
                st.session_state.fc_mostrar = False
                st.rerun()

        with col_acerto:
            if st.button("Acertei", use_container_width=True, type="primary", key="fc_acertei"):
                registrar_exercicio(
                    idioma, card.get("_modulo_id", ""), pt,
                    "flashcard", True
                )
                st.session_state.fc_acertos += 1
                st.session_state.fc_idx = (idx + 1) % total
                st.session_state.fc_mostrar = False
                st.rerun()

    # Navegacao
    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("Anterior", use_container_width=True, key="fc_ant"):
            st.session_state.fc_idx = (idx - 1) % total
            st.session_state.fc_mostrar = False
            st.rerun()

    with nav2:
        if st.button("Aleatorio", use_container_width=True, key="fc_rand"):
            novo = random.randrange(total)
            if novo == idx and total > 1:
                novo = (novo + 1) % total
            st.session_state.fc_idx = novo
            st.session_state.fc_mostrar = False
            st.rerun()

    with nav3:
        if st.button("Proximo", use_container_width=True, key="fc_prox"):
            st.session_state.fc_idx = (idx + 1) % total
            st.session_state.fc_mostrar = False
            st.rerun()
