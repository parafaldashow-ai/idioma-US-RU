import streamlit as st
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
    if "as_rodada_atual" not in st.session_state:
        st.session_state.as_rodada_atual = []
    if "as_selecionado_pt" not in st.session_state:
        st.session_state.as_selecionado_pt = None
    if "as_pares_feitos" not in st.session_state:
        st.session_state.as_pares_feitos = []
    if "as_erros_rodada" not in st.session_state:
        st.session_state.as_erros_rodada = 0
    if "as_rodada_num" not in st.session_state:
        st.session_state.as_rodada_num = 1
    if "as_total_rodadas" not in st.session_state:
        st.session_state.as_total_rodadas = 5
    if "as_acertos_total" not in st.session_state:
        st.session_state.as_acertos_total = 0
    if "as_erros_total" not in st.session_state:
        st.session_state.as_erros_total = 0
    if "as_pares_embaralhados" not in st.session_state:
        st.session_state.as_pares_embaralhados = []

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_ex"):
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
    elif st.session_state.ex_tipo == "ouvir":
        render_ouvir(idioma, codigo)
    elif st.session_state.ex_tipo == "associar":
        render_associar(idioma, codigo)


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

    # Inicializa o modo selecionado
    if "ex_modo_selecionado" not in st.session_state:
        st.session_state.ex_modo_selecionado = "multipla_escolha"

    # Define os modos com suas cores e icones
    modos = [
        ("multipla_escolha", "🎯", "Multipla", "#34d399"),
        ("digitar",          "⌨️", "Digitar",  "#60a5fa"),
        ("ouvir",            "🔊", "Ouvir",    "#a78bfa"),
        ("associar",         "🧩", "Associar", "#fbbf24"),
    ]

    cols = st.columns(4)
    for col, (modo_id, icone, nome, cor) in zip(cols, modos):
        with col:
            ativo = st.session_state.ex_modo_selecionado == modo_id
            border_cor = cor if ativo else "#2d3748"
            bg_cor = f"{cor}22" if ativo else "#1a2332"

            st.markdown(
                f'<div style="background: {bg_cor}; '
                f'border: 2px solid {border_cor}; '
                f'border-radius: 14px; padding: 16px 8px; text-align: center; '
                f'margin-bottom: 8px; transition: all 0.2s;">'
                f'<div style="font-size: 32px; line-height: 1;">{icone}</div>'
                f'<div style="font-size: 13px; font-weight: 700; color: {cor}; margin-top: 6px;">{nome}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if st.button(
                "Selecionar" if not ativo else "Ativo",
                use_container_width=True,
                key=f"modo_{modo_id}",
                type="primary" if ativo else "secondary",
            ):
                if not ativo:
                    st.session_state.ex_modo_selecionado = modo_id
                    st.rerun()

    tipo = st.session_state.ex_modo_selecionado

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
            st.markdown(
                f'<div style="background: rgba(96, 165, 250, 0.15); '
                f'border: 2px solid #60a5fa; border-radius: 14px; '
                f'padding: 14px 20px; margin-top: 12px; text-align: center;">'
                f'<span style="font-size: 24px; color: #60a5fa; font-weight: 700;">'
                f'🔊 {pron}'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"Audio indisponivel: {e}")

        if st.button("➡️ Proxima questao", use_container_width=True, type="primary", key="prox_q_mc"):
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
            if st.button("💡 Mostrar dica (primeira letra)", key="btn_dica"):
                st.session_state.ex_dica_mostrada = True
                st.rerun()
        else:
            primeira_letra = trad_certa[0].upper() if trad_certa else "?"
            st.info(f"Dica: a primeira letra e {primeira_letra}")

        with st.form("form_digitar"):
            resposta = st.text_input("Sua resposta:", placeholder="Digite aqui...", key=f"input_dig_{idx}")
            verificar = st.form_submit_button("✅ Verificar", use_container_width=True, type="primary")

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
            st.markdown(
                f'<div style="background: rgba(96, 165, 250, 0.15); '
                f'border: 2px solid #60a5fa; border-radius: 14px; '
                f'padding: 14px 20px; margin-top: 12px; text-align: center;">'
                f'<span style="font-size: 24px; color: #60a5fa; font-weight: 700;">'
                f'🔊 {pron}'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"Audio indisponivel: {e}")

        if st.button("➡️ Proxima questao", use_container_width=True, type="primary", key="prox_q_dig"):
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
        if st.button("🔁 Refazer esse modulo", use_container_width=True, type="primary"):
            iniciar_sessao(
                idioma,
                st.session_state.ex_modulo,
                st.session_state.ex_modulo_nome,
                total,
                IDIOMAS[idioma]["codigo_audio"],
                tipo,
            )
    with col_b:
        if st.button("📚 Escolher outro modulo", use_container_width=True):
            resetar_sessao()
            st.rerun()



def render_ouvir(idioma, codigo):
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
    st.caption(f"🔊 Questao {idx + 1} de {total} · Modulo: {st.session_state.ex_modulo_nome}")

    palavra = item.get(codigo, "?")
    trad_certa = item.get("pt", "?")

    # Card da pergunta (sem mostrar o texto!)
    pergunta_html = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 1px solid #2d3748; border-radius: 24px; padding: 40px 32px; '
        'text-align: center; margin: 24px 0;">'
        '<div style="color: #a8b2c1; font-size: 13px; letter-spacing: 3px; text-transform: uppercase;">🔉 Ouça e traduza</div>'
        '<div style="font-size: 72px; margin: 20px 0; line-height: 1;">🔊</div>'
        '<div style="color: #a8b2c1; font-size: 15px;">Ouça o audio e digite a traducao em portugues</div>'
        '</div>'
    )
    st.markdown(pergunta_html, unsafe_allow_html=True)

    if not st.session_state.ex_respondido:
        # Toca o audio automaticamente na primeira vez
        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.caption(f"🔇 Audio indisponivel: {e}")

        st.caption("🔁 Pode ouvir quantas vezes quiser antes de responder.")

        st.markdown("### Digite o que voce ouviu:")

        if not st.session_state.ex_dica_mostrada:
            if st.button("💡 Mostrar dica (primeira letra)", key="btn_dica_ouvir"):
                st.session_state.ex_dica_mostrada = True
                st.rerun()
        else:
            primeira_letra = trad_certa[0].upper() if trad_certa else "?"
            st.info(f"💡 A primeira letra e: **{primeira_letra}**")

        with st.form("form_ouvir"):
            resposta = st.text_input("Sua resposta:", placeholder="Digite aqui...", key=f"input_ouvir_{idx}")
            verificar = st.form_submit_button("✅ Verificar", use_container_width=True, type="primary")

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
                    "ouvir", acertou
                )
                st.session_state.ex_respostas.append(acertou)
                st.rerun()
    else:
        resp_correta = st.session_state.ex_resposta_correta
        resp_dada = st.session_state.ex_resposta_dada

        if resp_correta:
            st.success(f"🎉 Correto! Voce ouviu **{palavra}** = **{trad_certa}**")
        else:
            st.error(f"❌ Errou. Voce digitou '{resp_dada}', mas era '{trad_certa}' (audio: {palavra})")

        pron = item.get("pron", "")
        if pron:
            st.markdown(
                f'<div style="background: rgba(96, 165, 250, 0.15); '
                f'border: 2px solid #60a5fa; border-radius: 14px; '
                f'padding: 16px 24px; margin-top: 16px; text-align: center;">'
                f'<span style="font-size: 24px; color: #60a5fa; font-weight: 700;">'
                f'🔊 {pron}'
                f'</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Toca o audio de novo pra comparar
        try:
            audio_bytes = gerar_audio(palavra, codigo)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.caption(f"🔇 Audio indisponivel: {e}")

        if st.button("➡️ Proxima questao", use_container_width=True, type="primary", key="prox_q_ouvir"):
            st.session_state.ex_idx += 1
            st.session_state.ex_respondido = False
            st.session_state.ex_dica_mostrada = False
            st.rerun()



def render_associar(idioma, codigo):
    """Modo Associar Pares - versao corrigida."""
    import random

    questoes_raw = st.session_state.ex_questoes
    questoes = []
    for q in questoes_raw:
        if isinstance(q, dict) and "item" in q:
            item = q["item"]
            if isinstance(item, dict) and "pt" in item:
                questoes.append(item)
        elif isinstance(q, dict) and "pt" in q:
            questoes.append(q)

    total_palavras = len(questoes)
    PARES_POR_RODADA = 4
    TOTAL_RODADAS = 5

    # ============================================
    # INICIALIZA ESTADO
    # ============================================
    if "as_lista_embaralhada" not in st.session_state or not st.session_state.as_lista_embaralhada:
        lista = questoes.copy()
        random.shuffle(lista)
        st.session_state.as_lista_embaralhada = lista
        st.session_state.as_rodada_num = 1
        st.session_state.as_acertos_total = 0
        st.session_state.as_erros_total = 0
        st.session_state.as_pares_feitos = []
        st.session_state.as_selecionado_pt = None
        st.session_state.as_erros_rodada = 0

    # Mensagem de feedback persistente
    if "as_msg_feedback" not in st.session_state:
        st.session_state.as_msg_feedback = None

    lista_embaralhada = st.session_state.as_lista_embaralhada
    rodada_num = st.session_state.as_rodada_num

    total_rodadas_possiveis = (total_palavras + PARES_POR_RODADA - 1) // PARES_POR_RODADA
    total_rodadas_possiveis = min(total_rodadas_possiveis, TOTAL_RODADAS)

    inicio = (rodada_num - 1) * PARES_POR_RODADA
    fim = inicio + PARES_POR_RODADA
    rodada = lista_embaralhada[inicio:fim]

    # Embaralha coluna EN (com ID unico por item pra garantir par certo)
    chave_rodada = f"as_en_rodada_{rodada_num}"
    if chave_rodada not in st.session_state:
        en_embaralhada = []
        for idx, item in enumerate(rodada):
            item_copia = dict(item)
            item_copia["_id_temp"] = idx  # ID unico pra rastrear
            en_embaralhada.append(item_copia)
        random.shuffle(en_embaralhada)
        st.session_state[chave_rodada] = en_embaralhada

    en_embaralhada = st.session_state[chave_rodada]

    # ============================================
    # SESSAO COMPLETA (verifica ANTES de mostrar progresso)
    # ============================================
    if rodada_num > total_rodadas_possiveis:
        st.markdown("## 🏁 Sessao completa!")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Acertos", st.session_state.as_acertos_total)
        with col2:
            st.metric("❌ Erros", st.session_state.as_erros_total)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Nova sessao", use_container_width=True, type="primary", key="nova_sessao_assoc"):
                resetar_associar()
                st.rerun()
        with col_b:
            if st.button("📚 Escolher outro modulo", use_container_width=True, key="outro_mod_assoc"):
                resetar_sessao()
                st.rerun()
        return

    # ============================================
    # HEADER (so aparece se ainda nao acabou)
    # ============================================
    pct_progresso = min(rodada_num / total_rodadas_possiveis, 1.0) if total_rodadas_possiveis > 0 else 0.0
    st.progress(pct_progresso)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")

    # ============================================
    # MOSTRA FEEDBACK PENDENTE
    # ============================================
    if st.session_state.as_msg_feedback:
        tipo, texto = st.session_state.as_msg_feedback
        if tipo == "erro":
            st.error(texto)
        elif tipo == "acerto":
            st.success(texto)
        # Limpa depois de mostrar
        st.session_state.as_msg_feedback = None

    # ============================================
    # SESSAO COMPLETA
    # ============================================
    if rodada_num > total_rodadas_possiveis:
        st.markdown("## 🏁 Sessao completa!")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Acertos", st.session_state.as_acertos_total)
        with col2:
            st.metric("❌ Erros", st.session_state.as_erros_total)

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Nova sessao", use_container_width=True, type="primary", key="nova_sessao_assoc"):
                resetar_associar()
                st.rerun()
        with col_b:
            if st.button("📚 Escolher outro modulo", use_container_width=True, key="outro_mod_assoc"):
                resetar_sessao()
                st.rerun()
        return

    # ============================================
    # RODADA COMPLETA
    # ============================================
    if len(st.session_state.as_pares_feitos) >= len(rodada):
        st.success(f"🎉 Rodada {rodada_num} completa!")
        acertos_r = len(rodada) - st.session_state.as_erros_rodada
        st.markdown(f"**Acertos:** {acertos_r} · **Erros:** {st.session_state.as_erros_rodada}")

        st.session_state.as_acertos_total += acertos_r
        st.session_state.as_erros_total += st.session_state.as_erros_rodada

        if st.button("➡️ Proxima rodada", use_container_width=True, type="primary", key="prox_rodada_assoc"):
            st.session_state.as_rodada_num += 1
            st.session_state.as_pares_feitos = []
            st.session_state.as_selecionado_pt = None
            st.session_state.as_erros_rodada = 0
            st.session_state.as_msg_feedback = None
            chave_antiga = f"as_en_rodada_{rodada_num}"
            if chave_antiga in st.session_state:
                del st.session_state[chave_antiga]
            st.rerun()
        return

    # ============================================
    # MOSTRA AS DUAS COLUNAS
    # ============================================
    col_pt, col_en = st.columns(2)

    # Coluna PT
    with col_pt:
        st.markdown("#### 🇧🇷 Portugues")
        for i, item in enumerate(rodada):
            pt_texto = item.get("pt", "?")
            item_id = item.get("_id_temp", i)

            if pt_texto in st.session_state.as_pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {pt_texto}</div>',
                    unsafe_allow_html=True,
                )
            else:
                selecionado = st.session_state.as_selecionado_pt == pt_texto
                tipo_btn = "primary" if selecionado else "secondary"

                if st.button(pt_texto, use_container_width=True, key=f"pt_btn_{rodada_num}_{i}", type=tipo_btn):
                    st.session_state.as_selecionado_pt = pt_texto
                    st.session_state.as_msg_feedback = None
                    st.rerun()

    # Coluna EN
    with col_en:
        st.markdown(f"#### {IDIOMAS[idioma]['nome']}")
        for i, item in enumerate(en_embaralhada):
            pt_item = item.get("pt", "")
            traducao = item.get(codigo, "?")

            if pt_item in st.session_state.as_pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {traducao}</div>',
                    unsafe_allow_html=True,
                )
            else:
                if st.button(traducao, use_container_width=True, key=f"en_btn_{rodada_num}_{i}"):
                    if st.session_state.as_selecionado_pt is None:
                        st.session_state.as_msg_feedback = ("erro", "⚠️ Primeiro escolhe uma palavra em portugues!")
                        st.rerun()
                    else:
                        if st.session_state.as_selecionado_pt == pt_item:
                            # ACERTOU
                            st.session_state.as_pares_feitos.append(pt_item)

                            from logica.gerenciador_exercicios import registrar_exercicio
                            registrar_exercicio(
                                idioma, st.session_state.ex_modulo, pt_item,
                                "associar", True
                            )

                            st.session_state.as_selecionado_pt = None
                            st.session_state.as_msg_feedback = ("acerto", f"✅ Acertou! {pt_item} = {traducao}")
                            st.rerun()
                        else:
                            # ERROU - mostra feedback e MANTEM o PT selecionado
                            st.session_state.as_erros_rodada += 1
                            palavra_errada = st.session_state.as_selecionado_pt

                            from logica.gerenciador_exercicios import registrar_exercicio
                            registrar_exercicio(
                                idioma, st.session_state.ex_modulo, pt_item,
                                "associar", False
                            )

                            # MANTEM o PT selecionado pra pessoa tentar de novo
                            st.session_state.as_msg_feedback = ("erro", f"❌ Errou! **{palavra_errada}** nao combina com **{traducao}**. Tenta de novo!")
                            st.rerun()

    # ============================================
    # FEEDBACK
    # ============================================
    if st.session_state.as_selecionado_pt:
        st.info(f"👆 Agora escolhe a traducao de **{st.session_state.as_selecionado_pt}**")
    else:
        st.caption("👈 Escolhe uma palavra em portugues pra comecar")

    # ============================================
    # BOTAO REINICIAR
    # ============================================
    st.markdown("---")
    if st.button("🔄 Reiniciar sessao", use_container_width=True, key="reiniciar_assoc"):
        resetar_associar()
        st.rerun()



def resetar_associar():
    st.session_state.as_lista_embaralhada = []
    st.session_state.as_rodada_num = 1
    st.session_state.as_acertos_total = 0
    st.session_state.as_erros_total = 0
    st.session_state.as_pares_feitos = []
    st.session_state.as_selecionado_pt = None
    st.session_state.as_erros_rodada = 0
    st.session_state.as_msg_feedback = None
    # Limpa todas as rodadas antigas
    chaves = [k for k in st.session_state.keys() if k.startswith("as_en_rodada_")]
    for k in chaves:
        del st.session_state[k]

    st.stop()
