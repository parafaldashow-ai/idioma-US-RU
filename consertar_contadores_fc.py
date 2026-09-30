from pathlib import Path

caminho = Path(__file__).parent / "telas" / "tela_flashcards.py"
conteudo = caminho.read_text(encoding="utf-8")

# Adiciona a funcao de limpar cache no inicio do render_menu
antigo = '''def render_menu(idioma, info):
    st.markdown("### Escolha um modo de revisao:")

    qtd_nao_dom = contar_nao_dominadas(idioma)
    qtd_err = contar_erradas(idioma)'''

novo = '''def render_menu(idioma, info):
    st.markdown("### Escolha um modo de revisao:")

    # Limpa cache pra forcar recalculo
    st.cache_data.clear()

    qtd_nao_dom = contar_nao_dominadas(idioma)
    qtd_err = contar_erradas(idioma)'''

if antigo in conteudo:
    conteudo = conteudo.replace(antigo, novo)
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: contadores agora atualizam sempre")
    print()
    print("Reinicie o Streamlit.")
else:
    print("AVISO: nao achei o bloco. Tentando variante...")
    
    antigo2 = '''def render_menu(idioma, info):
    st.markdown("### Escolha um modo de revisao:")
    qtd_nao_dom = contar_nao_dominadas(idioma)
    qtd_err = contar_erradas(idioma)'''
    
    if antigo2 in conteudo:
        conteudo = conteudo.replace(antigo2, novo)
        caminho.write_text(conteudo, encoding="utf-8")
        print("OK: contadores atualizados (variante)")
    else:
        print("ERRO: nao consegui. Me manda o arquivo.")
