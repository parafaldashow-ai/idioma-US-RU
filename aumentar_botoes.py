from pathlib import Path

caminho = Path(__file__).parent / "main.py"
conteudo = caminho.read_text(encoding="utf-8")

# Adiciona/atualiza o bloco de botões no CSS
# Procura pelo bloco atual e substitui
bloco_botoes_antigo = """    /* Botoes */
    .stButton > button {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }}"""

bloco_botoes_novo = """    /* Botoes - maiores e mais confortaveis */
    .stButton > button {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        padding: 16px 28px !important;
        min-height: 54px !important;
        transition: all 0.2s ease !important;
    }}"""

if bloco_botoes_antigo in conteudo:
    conteudo = conteudo.replace(bloco_botoes_antigo, bloco_botoes_novo)
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: botoes aumentados no main.py")
else:
    # Procura por versoes alternativas
    bloco_alt = """    .stButton > button {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }}"""
    
    if bloco_alt in conteudo:
        conteudo = conteudo.replace(bloco_alt, bloco_botoes_novo)
        caminho.write_text(conteudo, encoding="utf-8")
        print("OK: botoes aumentados (variante)")
    else:
        print("AVISO: nao achei o bloco de botoes no main.py")
        print("Vou adicionar no final do CSS existente...")
        
        # Fallback: adiciona no final do st.markdown de CSS
        # Procura por </style>
        if "</style>" in conteudo:
            css_extra = """
    /* Botoes maiores */
    .stButton > button {
        font-size: 16px !important;
        padding: 16px 28px !important;
        min-height: 54px !important;
        border-radius: 14px !important;
    }
"""
            conteudo = conteudo.replace("</style>", css_extra + "</style>")
            caminho.write_text(conteudo, encoding="utf-8")
            print("OK: CSS de botoes adicionado")
        else:
            print("ERRO: nao consegui adicionar. Me manda o main.py")

print()
print("Reinicie o Streamlit.")