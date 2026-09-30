from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# SUBSTITUI A FUNCAO render_associar INTEIRA
# ============================================================
import re

# Encontra a funcao render_associar atual
padrao = r'def render_associar\(idioma, codigo\):.*?(?=\ndef resetar_associar\(\))'
match = re.search(padrao, conteudo, re.DOTALL)

if not match:
    print("ERRO: nao achei a funcao render_associar")
    print("Verifica se o arquivo ta correto.")
else:
    nova_funcao = '''def render_associar(idioma, codigo):
    """Modo Associar Pares - palavras unicas por sessao."""
    import random

    questoes = st.session_state.ex_questoes
    total_palavras = len(questoes)

    PARES_POR_RODADA = 4
    TOTAL_RODADAS = 5

    # ============================================
    # INICIALIZA SESSAO (na primeira vez)
    # ============================================
    if "as_lista_embaralhada" not in st.session_state or not st.session_state.as_lista_embaralhada:
        # Embaralha TODAS as palavras UMA VEZ
        lista = questoes.copy()
        random.shuffle(lista)
        st.session_state.as_lista_embaralhada = lista
        st.session_state.as_rodada_num = 1
        st.session_state.as_acertos_total = 0
        st.session_state.as_erros_total = 0
        st.session_state.as_pares_feitos = []
        st.session_state.as_selecionado_pt = None
        st.session_state.as_erros_rodada = 0
        st.session_state.as_pares_embaralhados = []

    lista_embaralhada = st.session_state.as_lista_embaralhada
    rodada_num = st.session_state.as_rodada_num

    # Calcula quantas rodadas da pra fazer
    total_rodadas_possiveis = (total_palavras + PARES_POR_RODADA - 1) // PARES_POR_RODADA
    total_rodadas_possiveis = min(total_rodadas_possiveis, TOTAL_RODADAS)

    # ============================================
    # PEGA A RODADA ATUAL
    # ============================================
    inicio = (rodada_num - 1) * PARES_POR_RODADA
    fim = inicio + PARES_POR_RODADA
    rodada = lista_embaralhada[inicio:fim]

    # Se nao tem palavras, acabou
    if not rodada:
        st.session_state.as_sessao_completa = True

    # Inicializa embaralhamento da coluna EN (so uma vez por rodada)
    if not st.session_state.as_pares_embaralhados or len(st.session_state.as_pares_embaralhados) != len(rodada):
        embaralhado = rodada.copy()
        random.shuffle(embaralhado)
        st.session_state.as_pares_embaralhados = embaralhado

    # ============================================
    # HEADER
    # ============================================
    st.progress(rodada_num / total_rodadas_possiveis)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")

    # ============================================
    # VERIFICA SE ACABOU A SESSAO
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
    # MOSTRA O TITULO DA RODADA
    # ============================================
    st.markdown(f"### Associe as palavras ({len(rodada)} pares)")

    # ============================================
    # VERIFICA SE A RODADA ACABOU
    # ============================================
    if len(st.session_state.as_pares_feitos) >= len(rodada):
        st.success(f"🎉 Rodada {rodada_num} completa!")
        st.markdown(f"**Acertos:** {len(rodada) - st.session_state.as_erros_rodada} · **Erros:** {st.session_state.as_erros_rodada}")

        # Acumula
        st.session_state.as_acertos_total += (len(rodada) - st.session_state.as_erros_rodada)
        st.session_state.as_erros_total += st.session_state.as_erros_rodada

        if st.button("➡️ Proxima rodada", use_container_width=True, type="primary", key="prox_rodada_assoc"):
            st.session_state.as_rodada_num += 1
            st.session_state.as_pares_feitos = []
            st.session_state.as_selecionado_pt = None
            st.session_state.as_erros_rodada = 0
            st.session_state.as_pares_embaralhados = []
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
            if item["pt"] in st.session_state.as_pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {item["pt"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                selecionado = st.session_state.as_selecionado_pt == item["pt"]
                tipo_btn = "primary" if selecionado else "secondary"

                if st.button(item["pt"], use_container_width=True, key=f"pt_{rodada_num}_{i}_{item['pt']}", type=tipo_btn):
                    st.session_state.as_selecionado_pt = item["pt"]
                    st.rerun()

    # Coluna EN
    with col_en:
        st.markdown(f"#### {IDIOMAS[idioma]['nome']}")
        for i, item in enumerate(st.session_state.as_pares_embaralhados):
            traducao = item.get(codigo, "?")
            if item["pt"] in st.session_state.as_pares_feitos:
                st.markdown(
                    f'<div style="background: #34d39933; border: 2px solid #34d399; '
                    f'border-radius: 12px; padding: 14px; margin-bottom: 8px; '
                    f'text-align: center; color: #34d399; font-weight: 700;">'
                    f'✅ {traducao}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                selecionado = (st.session_state.as_selecionado_pt == item["pt"])
                tipo_btn = "primary" if selecionado else "secondary"

                if st.button(traducao, use_container_width=True, key=f"en_{rodada_num}_{i}_{item['pt']}", type=tipo_btn):
                    if st.session_state.as_selecionado_pt is None:
                        st.warning("Primeiro escolhe uma palavra em portugues!")
                    else:
                        if st.session_state.as_selecionado_pt == item["pt"]:
                            # ACERTOU
                            st.session_state.as_pares_feitos.append(item["pt"])

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

                            from logica.gerenciador_exercicios import registrar_exercicio
                            registrar_exercicio(
                                idioma, st.session_state.ex_modulo, item["pt"],
                                "associar", False
                            )

                            palavra_errada = st.session_state.as_selecionado_pt
                            st.session_state.as_selecionado_pt = None
                            st.error(f"❌ Errou! **{palavra_errada}** nao e **{traducao}**")
                            st.rerun()

    # ============================================
    # FEEDBACK
    # ============================================
    if st.session_state.as_selecionado_pt:
        st.info(f"👆 Agora escolhe a traducao de **{st.session_state.as_selecionado_pt}**")
    else:
        st.caption("👈 Escolhe uma palavra em portugues pra comecar")

    # ============================================
    # BOTAO PRA REINICIAR SESSAO
    # ============================================
    st.markdown("---")
    if st.button("🔄 Reiniciar sessao", use_container_width=True, key="reiniciar_assoc"):
        resetar_associar()
        st.rerun()


'''
    
    conteudo = conteudo[:match.start()] + nova_funcao + conteudo[match.end():]
    
    # Adiciona a variavel as_lista_embaralhada no resetar_associar
    if "as_lista_embaralhada" not in conteudo.split("def resetar_associar")[1][:500]:
        conteudo = conteudo.replace(
            "def resetar_associar():",
            '''def resetar_associar():
    st.session_state.as_lista_embaralhada = []'''
        )
    
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: render_associar atualizada com palavras unicas")
    print()
    print("Reinicie o Streamlit.")