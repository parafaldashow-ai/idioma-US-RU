from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# CORRIGE O CALCULO DO PROGRESSO
# ============================================================
antigo = '''    st.progress(rodada_num / total_rodadas_possiveis)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")'''

novo = '''    # Proteção contra divisão > 1.0
    pct_progresso = min(rodada_num / total_rodadas_possiveis, 1.0) if total_rodadas_possiveis > 0 else 0.0
    st.progress(pct_progresso)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")'''

if antigo in conteudo:
    conteudo = conteudo.replace(antigo, novo)
    print("OK: progresso do associar corrigido")
else:
    print("AVISO: nao achei o bloco exato. Tentando variante...")
    # Tenta variante sem o emoji
    antigo2 = '''    st.progress(rodada_num / total_rodadas_possiveis)
    st.caption(f"Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")'''
    
    if antigo2 in conteudo:
        conteudo = conteudo.replace(antigo2, novo)
        print("OK: progresso corrigido (variante)")
    else:
        print("ERRO: nao consegui. Me manda o arquivo.")

# ============================================================
# PROTECAO EXTRA: NAO MOSTRAR PROGRESSO QUANDO ACABOU
# ============================================================
# Reorganiza: verifica primeiro se acabou, depois mostra progresso
antigo2 = '''    # ============================================
    # HEADER
    # ============================================
    # Proteção contra divisão > 1.0
    pct_progresso = min(rodada_num / total_rodadas_possiveis, 1.0) if total_rodadas_possiveis > 0 else 0.0
    st.progress(pct_progresso)
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")'''

novo2 = '''    # ============================================
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
    st.caption(f"🧩 Rodada {rodada_num} de {total_rodadas_possiveis} · Modulo: {st.session_state.ex_modulo_nome}")'''

if antigo2 in conteudo:
    conteudo = conteudo.replace(antigo2, novo2)
    print("OK: reorganizado (sessao completa vem antes)")
else:
    print("AVISO: nao reorganizei. Pode ter ficado duplicado.")

# ============================================================
# REMOVE O BLOCO ANTIGO DE SESSAO COMPLETA (duplicado)
# ============================================================
antigo3 = '''    # ============================================
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
        return'''

# Remove só se aparecer 2x
if conteudo.count(antigo3) >= 2:
    # Remove a segunda ocorrencia
    primeiro_idx = conteudo.find(antigo3)
    segundo_idx = conteudo.find(antigo3, primeiro_idx + 1)
    conteudo = conteudo[:segundo_idx] + conteudo[segundo_idx + len(antigo3):]
    print("OK: bloco duplicado removido")

caminho.write_text(conteudo, encoding="utf-8")
print()
print("Reinicie o Streamlit.")