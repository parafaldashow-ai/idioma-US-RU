from pathlib import Path

BASE = Path(__file__).parent
caminho = BASE / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# 1. Adicionar "Associar pares" no radio do menu
# ============================================================
conteudo = conteudo.replace(
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
        tipo = "ouvir"''',
    '''    modo = st.radio(
        "Modo:",
        ["Multipla escolha", "Digitar", "Ouvir", "Associar pares"],
        horizontal=True,
        key="ex_modo_radio",
        label_visibility="collapsed",
    )

    if "Multipla" in modo:
        tipo = "multipla_escolha"
    elif "Digitar" in modo:
        tipo = "digitar"
    elif "Ouvir" in modo:
        tipo = "ouvir"
    else:
        tipo = "associar"'''
)

# ============================================================
# 2. Adicionar chamada pra render_associar
# ============================================================
conteudo = conteudo.replace(
    '''    if st.session_state.ex_tipo == "multipla_escolha":
        render_mc(idioma, codigo)
    elif st.session_state.ex_tipo == "digitar":
        render_digitar(idioma, codigo)
    elif st.session_state.ex_tipo == "ouvir":
        render_ouvir(idioma, codigo)''',
    '''    if st.session_state.ex_tipo == "multipla_escolha":
        render_mc(idioma, codigo)
    elif st.session_state.ex_tipo == "digitar":
        render_digitar(idioma, codigo)
    elif st.session_state.ex_tipo == "ouvir":
        render_ouvir(idioma, codigo)
    elif st.session_state.ex_tipo == "associar":
        render_associar(idioma, codigo)'''
)

# ============================================================
# 3. Adicionar o estado de associar no inicio
# ============================================================
conteudo = conteudo.replace(
    '''    if "ex_dica_mostrada" not in st.session_state:
        st.session_state.ex_dica_mostrada = False''',
    '''    if "ex_dica_mostrada" not in st.session_state:
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
        st.session_state.as_pares_embaralhados = []'''
)

# ============================================================
# 4. Adicionar funcao render_associar no final
# ============================================================
funcao_associar = '''


def render_associar(idioma, codigo):
    """Modo Associar Pares - 4 pares por rodada, 5 rodadas."""
    import random

    questoes = st.session_state.ex_questoes
    total_pares = len(questoes)

    PAres_POR_RODADA = 4
    TOTAL_RODADAS = 5

    # ============================================
    # INICIALIZA RODADA (na primeira vez)
    # ============================================
    if not st.session_state.as_rodada_atual:
        # Pega 4 pares aleatorios
        pares_disponiveis = questoes.copy()
        random.shuffle(pares_disponiveis)
        rodada = pares_disponiveis[:min(PAres_POR_RODADA, len(pares_disponiveis))]

        st.session_state.as_rodada_atual = rodada
        st.session_state.as_pares_feitos = []
        st.session_state.as_selecionado_pt = None
        st.session_state.as_erros_rodada = 0
        st.session_state.as_pares_embaralhados = rodada.copy()
        random.shuffle(st.session_state.as_pares_embaralhados)

    rodada = st.session_state.as_rodada_atual
    pares_feitos = st.session_state.as_pares_feitos
    selecionado_pt = st.session_state.as_selecionado_pt
    rodada_num = st.session_state.as_rodada_num
    total_rodadas = st.session_state.as_total_rodadas

    # ============================================
    # HEADER
    # ============================================
    st.progress(rodada_num / total_rodadas)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas} · Modulo: {st.session_state.ex_modulo_nome}")

    st.markdown(f"### Associe as palavras ({len(rodada)} pares)")

    # ============================================
    # VERIFICA SE A RODADA ACABOU
    # ============================================
    if len(pares_feitos) >= len(rodada):
        st.success(f"🎉 Rodada {rodada_num} completa!")
        st.markdown(f"**Acertos:** {len(rodada) - st.session_state.as_erros_rodada} · **Erros:** {st.session_state.as_erros_rodada}")

        # Acumula
        st.session_state.as_acertos_total += (len(rodada) - st.session_state.as_erros_rodada)
        st.session_state.as_erros_total += st.session_state.as_erros_rodada

        if rodada_num >= total_rodadas:
            st.markdown("---")
            st.markdown(f"## 🏁 Sessao completa!")
            st.metric("Total de acertos", st.session_state.as_acertos_total)
            st.metric("Total de erros", st.session_state.as_erros_total)

            if st.button("🔄 Nova sessao", use_container_width=True, type="primary", key="nova_sessao_assoc"):
                resetar_associar()
                st.rerun()

            if st.button("📚 Escolher outro modulo", use_container_width=True, key="outro_mod_assoc"):
                resetar_sessao()
                st.rerun()
        else:
            if st.button("➡️ Proxima rodada", use_container_width=True, type="primary", key="prox_rodada_assoc"):
                # Nova rodada
                pares_disponiveis = questoes.copy()
                random.shuffle(pares_disponiveis)
                nova_rodada = pares_disponiveis[:min(PAres_POR_RODADA, len(pares_disponiveis))]

                st.session_state.as_rodada_atual = nova_rodada
                st.session_state.as_pares_feitos = []
                st.session_state.as_selecionado_pt = None
                st.session_state.as_erros_rodada = 0
                st.session_state.as_pares_embaralhados = nova_rodada.copy()
                random.shuffle(st.session_state.as_pares_embaralhados)
                st.session_state.as_rodada_num += 1
                st.rerun()

        return

    # ============================================
    # MOSTRA AS DUAS COLUNAS
    # ============================================
    col_pt, col_en = st.columns(2)

    # Coluna PT (nao mostra os ja feitos)
    with col_pt:
        st.markdown("#### 🇧🇷 Portugues")
        for i, item in enumerate(rodada):
            if item["pt"] in pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {item["pt"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                selecionado = selecionado_pt == item["pt"]
                if selecionado:
                    tipo_btn = "primary"
                else:
                    tipo_btn = "secondary"

                if st.button(item["pt"], use_container_width=True, key=f"pt_{i}_{item['pt']}", type=tipo_btn):
                    st.session_state.as_selecionado_pt = item["pt"]
                    st.rerun()

    # Coluna EN
    with col_en:
        st.markdown(f"#### {IDIOMAS[idioma]['nome']}")
        for i, item in enumerate(st.session_state.as_pares_embaralhados):
            traducao = item.get(codigo, "?")
            if item["pt"] in pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {traducao}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                # Verifica se ta selecionado
                selecionado = (selecionado_pt == item["pt"])
                if selecionado:
                    tipo_btn = "primary"
                else:
                    tipo_btn = "secondary"

                if st.button(traducao, use_container_width=True, key=f"en_{i}_{item['pt']}", type=tipo_btn):
                    # Verifica se tem algo selecionado na esquerda
                    if st.session_state.as_selecionado_pt is None:
                        st.warning("Primeiro escolhe uma palavra em portugues!")
                    else:
                        # Verifica se acertou
                        if st.session_state.as_selecionado_pt == item["pt"]:
                            # ACERTOU
                            st.session_state.as_pares_feitos.append(item["pt"])

                            # Registra acerto pra palavra
                            from logica.gerenciador_exercicios import registrar_exercicio
                            registrar_exercicio(
                                idioma, st.session_state.ex_modulo, item["pt"],
                                "associar", True
                            )

                            st.session_state.as_selecionado_pt = None
                            st.rerun()
                        else:
                            # ERROU
                            st.session_state.as_erros_rodada += 1
                            st.session_state.as_selecionado_pt = None

                            from logica.gerenciador_exercicios import registrar_exercicio
                            registrar_exercicio(
                                idioma, st.session_state.ex_modulo, item["pt"],
                                "associar", False
                            )

                            st.error(f"❌ Errou! Tenta de novo.")
                            st.rerun()

    # ============================================
    # FEEDBACK
    # ============================================
    if st.session_state.as_selecionado_pt:
        st.info(f"👆 Agora escolhe a traducao de **{st.session_state.as_selecionado_pt}**")
    else:
        st.caption("👈 Escolhe uma palavra em portugues pra comecar")


def resetar_associar():
    st.session_state.as_rodada_atual = []
    st.session_state.as_selecionado_pt = None
    st.session_state.as_pares_feitos = []
    st.session_state.as_erros_rodada = 0
    st.session_state.as_rodada_num = 1
    st.session_state.as_acertos_total = 0
    st.session_state.as_erros_total = 0
    st.session_state.as_pares_embaralhados = []
'''

# Adiciona a funcao no final do arquivo
conteudo = conteudo + funcao_associar

caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho}")
print()
print("Modo Associar pares adicionado!")
print("Reinicie o Streamlit.")