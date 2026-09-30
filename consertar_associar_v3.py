from pathlib import Path
import re

BASE = Path(__file__).parent
caminho = BASE / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# Encontra e substitui a funcao render_associar
padrao = r'def render_associar\(idioma, codigo\):.*?(?=\ndef resetar_associar\(\))'
match = re.search(padrao, conteudo, re.DOTALL)

if not match:
    print("ERRO: nao achei render_associar")
else:
    nova_funcao = '''def render_associar(idioma, codigo):
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
    # HEADER
    # ============================================
    st.progress(rodada_num / total_rodadas_possiveis)
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


'''
    
    conteudo = conteudo[:match.start()] + nova_funcao + conteudo[match.end():]
    
    # Corrige resetar_associar
    padrao_reset = r'def resetar_associar\(\):.*?(?=\ndef |\Z)'
    match_reset = re.search(padrao_reset, conteudo, re.DOTALL)
    
    if match_reset:
        novo_reset = '''def resetar_associar():
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
'''
        conteudo = conteudo[:match_reset.start()] + novo_reset + conteudo[match_reset.end():]
    
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: render_associar reescrita (v3)")
    print()
    print("Reinicie o Streamlit.")