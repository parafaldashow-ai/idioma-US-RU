from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# 1. Consertar no inicio da render_associar
# ============================================================
conteudo = conteudo.replace(
    '''    questoes = st.session_state.ex_questoes
    total_palavras = len(questoes)''',
    '''    questoes_raw = st.session_state.ex_questoes
    # Extrai os itens reais (que podem estar dentro de {"item": {...}})
    questoes = []
    for q in questoes_raw:
        if isinstance(q, dict) and "item" in q:
            questoes.append(q["item"])
        else:
            questoes.append(q)
    total_palavras = len(questoes)'''
)

# ============================================================
# 2. Consertar a inicializacao da lista embaralhada
# ============================================================
conteudo = conteudo.replace(
    '''    if "as_lista_embaralhada" not in st.session_state or not st.session_state.as_lista_embaralhada:
        # Embaralha TODAS as palavras UMA VEZ
        lista = questoes.copy()
        random.shuffle(lista)
        st.session_state.as_lista_embaralhada = lista''',
    '''    if "as_lista_embaralhada" not in st.session_state or not st.session_state.as_lista_embaralhada:
        # Embaralha TODAS as palavras UMA VEZ
        lista = []
        for item in questoes:
            # Garante que so pega itens com "pt"
            if isinstance(item, dict) and "pt" in item:
                lista.append(item)
        random.shuffle(lista)
        st.session_state.as_lista_embaralhada = lista'''
)

# ============================================================
# 3. Consertar a montagem da rodada
# ============================================================
conteudo = conteudo.replace(
    '''    inicio = (rodada_num - 1) * PARES_POR_RODADA
    fim = inicio + PARES_POR_RODADA
    rodada = lista_embaralhada[inicio:fim]''',
    '''    inicio = (rodada_num - 1) * PARES_POR_RODADA
    fim = inicio + PARES_POR_RODADA
    rodada = []
    for item in lista_embaralhada[inicio:fim]:
        if isinstance(item, dict) and "pt" in item:
            rodada.append(item)'''
)

# ============================================================
# 4. Consertar a coluna PT (protecao contra KeyError)
# ============================================================
conteudo = conteudo.replace(
    '''    with col_pt:
        st.markdown("#### 🇧🇷 Portugues")
        for i, item in enumerate(rodada):
            if item["pt"] in st.session_state.as_pares_feitos:''',
    '''    with col_pt:
        st.markdown("#### 🇧🇷 Portugues")
        for i, item in enumerate(rodada):
            if not isinstance(item, dict) or "pt" not in item:
                continue
            if item["pt"] in st.session_state.as_pares_feitos:'''
)

# ============================================================
# 5. Consertar a coluna EN
# ============================================================
conteudo = conteudo.replace(
    '''    with col_en:
        st.markdown(f"#### {IDIOMAS[idioma]['nome']}")
        for i, item in enumerate(st.session_state.as_pares_embaralhados):
            traducao = item.get(codigo, "?")''',
    '''    with col_en:
        st.markdown(f"#### {IDIOMAS[idioma]['nome']}")
        for i, item in enumerate(st.session_state.as_pares_embaralhados):
            if not isinstance(item, dict) or "pt" not in item:
                continue
            traducao = item.get(codigo, "?")'''
)

caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho} corrigido")
print()
print("Associar pares consertado!")
print("Reinicie o Streamlit.")