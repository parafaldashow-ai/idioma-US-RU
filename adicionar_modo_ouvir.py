from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# 1. Adicionar "Ouvir" no radio do menu
# ============================================================
conteudo = conteudo.replace(
    '''    modo = st.radio(
        "Modo:",
        ["Multipla escolha", "Digitar", "Ouvir (em breve)"],
        horizontal=True,
        key="ex_modo_radio",
        label_visibility="collapsed",
    )

    if "Ouvir" in modo:
        st.info("O modo Ouvir sera implementado na proxima fase.")
        return

    tipo = "multipla_escolha" if "Multipla" in modo else "digitar"''',
    '''    modo = st.radio(
        "Modo:",
        ["Multipla escolha", "Digitar", "Ouvir"],
        horizontal=True,
        key="ex_modo_radio",
        label_visibility="collapsed",
    )

    if "Multipla" in modo:
        tipo = "multipla_escolha"
    elif "Digitar" in modo:
        tipo = "digitar"
    else:
        tipo = "ouvir"'''
)

# ============================================================
# 2. Adicionar chamada pra render_ouvir
# ============================================================
conteudo = conteudo.replace(
    '''    if st.session_state.ex_tipo == "multipla_escolha":
        render_mc(idioma, codigo)
    elif st.session_state.ex_tipo == "digitar":
        render_digitar(idioma, codigo)''',
    '''    if st.session_state.ex_tipo == "multipla_escolha":
        render_mc(idioma, codigo)
    elif st.session_state.ex_tipo == "digitar":
        render_digitar(idioma, codigo)
    elif st.session_state.ex_tipo == "ouvir":
        render_ouvir(idioma, codigo)'''
)

# ============================================================
# 3. Adicionar a função render_ouvir no final do arquivo
# ============================================================
conteudo_ouvir = '''


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
'''

# Adiciona a funcao no final do arquivo
conteudo = conteudo + conteudo_ouvir

caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho}")
print()
print("Modo Ouvir adicionado!")
print("Reinicie o Streamlit.")