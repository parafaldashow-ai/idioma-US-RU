from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_exercicio.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# SUBSTITUI O RADIO POR BOTOES
# ============================================================
antigo = '''    modo = st.radio(
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

novo = '''    # Inicializa o modo selecionado
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

    tipo = st.session_state.ex_modo_selecionado'''

if antigo in conteudo:
    conteudo = conteudo.replace(antigo, novo)
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: radio substituido por botoes coloridos")
    print()
    print("Reinicie o Streamlit.")
else:
    print("ERRO: nao achei o bloco do radio. Me manda o arquivo.")