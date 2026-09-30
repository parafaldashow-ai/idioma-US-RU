from pathlib import Path

conteudo = '''import streamlit as st
import random
import unicodedata
import re
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dados import carregar_modulo, listar_modulos_flat
from logica.gerenciador_exercicios import registrar_exercicio, registrar_sessao
from logica.gerenciador_audio import gerar_audio


def normalizar(texto):
    """Normaliza texto pra comparacao tolerante."""
    if not texto:
        return ""

    # Remove acentos
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))

    # Minusculo
    texto_limpo = sem_acento.lower()

    # Remove pontuacao
    for char in "!?.,;:()[]{}":
        texto_limpo = texto_limpo.replace(char, "")

    # Colapsa espacos
    texto_limpo = " ".join(texto_limpo.split())

    # Remove palavras extras comuns do final
    extras = [" voce", " vc", " tu", " a", " o", " de", " da", " do"]
    mudou = True
    while mudou:
        mudou = False
        for extra in extras:
            if texto_limpo.endswith(extra):
                texto_limpo = texto_limpo[:-len(extra)].strip()
                mudou = True

    return texto_limpo


def render():
    idioma = st.session_state.get("idioma") or "ingles"
    info = IDIOMAS.get(idioma, {"bandeira": "?", "nome": "?"})
    codigo = info["codigo_audio"]

    if "ex_modulo" not in st.session_state:
        st.session_state.ex_modulo = None
    if "ex_tipo" not in st.session_state:
        st.session_state.ex_tipo = None
    if "ex_questoes" not in st.session_state:
        st.session_state.ex_questoes = []
    if "ex_idx" not in st.session_state:
        st.session_state.ex_idx = 0
    if "ex_respostas" not in st.session_state:
        st.session_state.ex_respostas = []
    if "ex_respondido" not in st.session_state:
        st.session_state.ex_respondido = False
    if "ex_finalizado" not in st.session_state:
        st.session_state.ex_finalizado = False
    if "ex_dica_mostrada" not in st.session_state:
        st.session_state.ex_dica_mostrada = False

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_ex"):
            if st.session_state.ex_modulo and not st.session_state.ex_finalizado:
                resetar_sessao()
                st.rerun()
            else:
                voltar()
    with col_b:
        st.markdown(f"## Exercicios · {info['bandeira']} {info['nome']}")

    st.markdown("---")

    if not st.session_state.ex_modulo:
        render_menu(idioma, info, codigo)
        return

    if st.session_state.ex_finalizado:
        render_resultado(idioma)
        return

    if st.session_state.ex_tipo == "multipla_escolha":
        render_mc(idioma, codigo)
    elif st.session_state.ex_tipo == "digitar":
        render_digitar(idioma, codigo)


def resetar_sessao():
    st.session_state.ex_modulo = None
    st.session_state.ex_tipo = None
    st.session_state.ex_questoes = []
    st.session_state.ex_idx = 0
    st.session_state.ex_respostas = []
    st.session_state.ex_respondido = False
    st.session_state.ex_finalizado = False
    st.session_state.ex_dica_mostrada = False


def render_menu(idioma, info, codigo):
    st.markdown("### 1. Escolha o modo de exercicio")

    modo = st.radio(
        "Modo:",
        ["Multipla escolha", "Digitar", "Ouvir (em breve)"],
        horizontal=True,
        key="ex_modo_radio",
        label_visibility="collapsed",
    )

    if "Ouvir" in modo:
        st.info("O modo Ouvir sera implementado na proxima fase.")
        return

    tipo = "multipla_escolha" if "Multipla" in modo else "digitar"

    st.markdown("---")
    st.markdown(f"### 2. Escolha o modulo")

    modulos = listar_modulos_flat(idioma)

    modulos_com_conteudo = []
    for mod in modulos:
        itens = carregar_modulo(idioma, mod["id"])
        if itens:
            modulos_com_conteudo.append({**mod, "total_itens": len(itens)})

    if not modulos_com_conteudo:
        st.warning("Nenhum modulo com conteudo.")
        return

    for i in range(0, len(modulos_com_conteudo), 3):
        cols = st.columns(3)
        for col, mod in zip(cols, modulos_com_conteudo[i:i+3]):
            with col:
                if st.button(
                    f"{mod['icone']} {mod['nome']} ({mod['total_itens']})",
                    use_container_width=True,
                    key=f"ex_mod_{tipo}_{mod['id']}",
                ):
                    iniciar_sessao(idioma, mod["id"], mod["nome"], mod["total_itens"], codigo, tipo)


def iniciar_sessao(idioma, modulo_id, modulo_nome, total, codigo, tipo):
    itens = carregar_modulo(idioma, modulo_id)

    if not itens:
        st.error("Modulo vazio.")
        return

    itens_emb = itens.copy()
    random.shuffle(itens_emb)

    questoes = []
    for item in itens_emb:
        if tipo == "multipla_escolha":
            opcoes = gerar_opcoes(idioma, item, itens, codigo)
            questoes.append({"item": item, "opcoes": opcoes})
        else:
            questoes.append({"item": item})

    st.session_state.ex_modulo = modulo_id
    st.session_state.ex_modulo_nome = modulo_nome
    st.session_state.ex_tipo = tipo
    st.session_state.ex_questoes = questoes
    st.session_state.ex_idx = 0
    st.session_state.ex_respostas = []
    st.session_state.ex_respondido = False
    st.session_state.ex_finalizado = False
    st.session_state.ex_dica_mostrada = False
    st.rerun()


def gerar_opcoes(idioma, item_correto, itens_modulo, codigo, n_opcoes=4):
    correta_texto = item_correto.get("pt", "?")

    candidatos = [i for i in itens_modulo if i.get("pt") != correta_texto and i.get("pt", "").strip()]

    if len(candidatos) < n_opcoes - 1:
        todos_modulos = listar_modulos_flat(idioma)
        for mod in todos_modulos:
            extras = carregar_modulo(idioma, mod["id"])
            candidatos.extend(extras)
            if len(candidatos) >= n_opcoes * 2:
                break

    vistos = {correta_texto.lower().strip()}
    unicos = []
    for c in candidatos:
        trad = c.get("pt", "").strip()
        if trad and trad.lower() not in vistos:
            vistos.add(trad.lower())
            unicos.append(c)

    n_distratores = min(n_opcoes - 1, len(unicos))
    distratores = random.sample(unicos, n_distratores) if unicos else []

    opcoes = [(correta_texto, True)] + [(d.get("pt", "?"), False) for d in distratores]
    random.shuffle(opcoes)
    return opcoes


def render_mc(idioma, codigo):
    questoes = st.session_state.ex_questoes
    idx = st.session_state.ex_idx
    total = len(questoes)

    if idx >= total:
        st.session_state.ex_finalizado = True
        st.rerun()
        return

    questao = questoes[idx]
    item = questao["item"]
    opcoes = questao["opcoes"]

    st.progress((idx + 1) / total)
    st.caption(f"Questao {idx + 1} de {total} - Modulo: {st.session_state.ex_modulo_nome}")

    palavra = item.get(codigo, "?")

    pergunta_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 40px 32px; '
        'text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">Traduza para portugues</div>'
        f'<div style="font-size: 42px; font-weight: bold; color: #ffffff; margin: 16px 0;">{palavra}</div>'
        '</div>'
    )
    st.markdown(pergunta_html, unsafe_allow_html=True)

    st.markdown("### Escolha a traducao correta:")

    if not st.session_state.ex_respondido:
        for i, (texto, correta) in enumerate(opcoes):
            if st.button(texto, use_container_width=True, key=f"op_{idx}_{i}"):
                st.session_state.ex_respondido = True
                st.session_state.ex_resposta_dada = texto
                st.session_state.ex_resposta_correta = correta
                st.session_state.ex_resposta_certa = item.get("pt", "?")

                registrar_exercicio(
                    idioma, st.session_state.ex_modulo, item["pt"],
                    "multipla_escolha", correta
                )
                st.session_state.ex_respostas.append(correta)
                st.rerun()
    else:
        resp_correta = st.session_state.ex_resposta_correta
        resp_dada = st.session_state.ex_resposta_dada
        trad_certa = st.session_state.ex_resposta_certa

        if resp_correta:
            st.success(f"Correto! {palavra} = {trad_certa}")
        else:
            st.error(f"Errou. Voce marcou {resp_dada}, mas a resposta era {trad_certa}")

        pron = item.get("pron", "")
        if pron:
            st.caption(f"Pronuncia: {pron}")

        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"Audio indisponivel: {e}")

        if st.button("Proxima questao", use_container_width=True, type="primary", key="prox_q_mc"):
            st.session_state.ex_idx += 1
            st.session_state.ex_respondido = False
            st.session_state.ex_dica_mostrada = False
            st.rerun()


def render_digitar(idioma, codigo):
    questoes = st.session_state.ex_questoes
    idx = st.session_state.ex_idx
    total = len(questoes)

    if idx >= total:
        st.session_state.ex_finalizado = True
        st.rerun()
        return

    questao = questoes[idx]
    item = questao["item"]

    st.progress((idx + 1) / total)
    st.caption(f"Questao {idx + 1} de {total} - Modulo: {st.session_state.ex_modulo_nome}")

    palavra = item.get(codigo, "?")
    trad_certa = item.get("pt", "?")

    pergunta_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 40px 32px; '
        'text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">Traduza para portugues</div>'
        f'<div style="font-size: 42px; font-weight: bold; color: #ffffff; margin: 16px 0;">{palavra}</div>'
        '</div>'
    )
    st.markdown(pergunta_html, unsafe_allow_html=True)

    if not st.session_state.ex_respondido:
        st.markdown("### Digite a traducao:")

        if not st.session_state.ex_dica_mostrada:
            if st.button("Mostrar dica (primeira letra)", key="btn_dica"):
                st.session_state.ex_dica_mostrada = True
                st.rerun()
        else:
            primeira_letra = trad_certa[0].upper() if trad_certa else "?"
            st.info(f"Dica: a primeira letra e {primeira_letra}")

        with st.form("form_digitar"):
            resposta = st.text_input("Sua resposta:", placeholder="Digite aqui...", key=f"input_dig_{idx}")
            verificar = st.form_submit_button("Verificar", use_container_width=True, type="primary")

            if verificar:
                resposta_norm = normalizar(resposta)
                certa_norm = normalizar(trad_certa)
                acertou = (resposta_norm == certa_norm)

                st.session_state.ex_respondido = True
                st.session_state.ex_resposta_dada = resposta
                st.session_state.ex_resposta_correta = acertou
                st.session_state.ex_resposta_certa = trad_certa

                registrar_exercicio(
                    idioma, st.session_state.ex_modulo, item["pt"],
                    "digitar", acertou
                )
                st.session_state.ex_respostas.append(acertou)
                st.rerun()
    else:
        resp_correta = st.session_state.ex_resposta_correta
        resp_dada = st.session_state.ex_resposta_dada

        if resp_correta:
            st.success(f"Correto! {palavra} = {trad_certa}")
        else:
            st.error(f"Errou. Voce digitou '{resp_dada}', mas era '{trad_certa}'")

        pron = item.get("pron", "")
        if pron:
            st.caption(f"Pronuncia: {pron}")

        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"Audio indisponivel: {e}")

        if st.button("Proxima questao", use_container_width=True, type="primary", key="prox_q_dig"):
            st.session_state.ex_idx += 1
            st.session_state.ex_respondido = False
            st.session_state.ex_dica_mostrada = False
            st.rerun()


def render_resultado(idioma):
    questoes = st.session_state.ex_questoes
    respostas = st.session_state.ex_respostas

    total = len(questoes)
    acertos = sum(1 for r in respostas if r)
    erros = total - acertos
    pct = int((acertos / total * 100) if total else 0)

    tipo = st.session_state.ex_tipo

    registrar_sessao(
        idioma,
        st.session_state.ex_modulo,
        tipo,
        total, acertos, erros,
    )

    nome_tipo = "Multipla escolha" if tipo == "multipla_escolha" else "Digitar"

    st.markdown(f"## Sessao finalizada - {nome_tipo}")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Acertos", acertos)
    with col2:
        st.metric("Erros", erros)
    with col3:
        st.metric("Taxa", f"{pct}%")

    st.progress(pct / 100)

    st.markdown("---")

    if pct >= 80:
        st.success("Excelente! Voce dominou esse modulo!")
    elif pct >= 60:
        st.info("Bom trabalho! Continue praticando.")
    else:
        st.warning("Continue! A pratica leva a perfeicao.")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Refazer esse modulo", use_container_width=True, type="primary"):
            iniciar_sessao(
                idioma,
                st.session_state.ex_modulo,
                st.session_state.ex_modulo_nome,
                total,
                IDIOMAS[idioma]["codigo_audio"],
                tipo,
            )
    with col_b:
        if st.button("Escolher outro modulo", use_container_width=True):
            resetar_sessao()
            st.rerun()
'''

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho} reescrito")
print("Reinicie o Streamlit.")