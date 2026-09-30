from pathlib import Path
import re

PASTA = Path(__file__).parent / "telas"

arquivos = [
    "tela_menu_idioma.py",
    "tela_modulos.py",
    "tela_modulo.py",
    "tela_flashcards.py",
    "tela_exercicio.py",
    "tela_dicionario.py",
    "tela_progresso.py",
    "tela_anotacoes.py",
    "tela_config.py",
]

for arquivo in arquivos:
    caminho = PASTA / arquivo
    if not caminho.exists():
        print(f"SKIP: {arquivo}")
        continue

    texto = caminho.read_text(encoding="utf-8")

    # Substitui o bloco de botão voltar
    # Padrão: if st.button("← Voltar"...): ir_para("xxx")
    padrao = r'(if st\.button\("← Voltar"[^:]*:\s*\n\s*)ir_para\([^\)]+\)'
    texto_novo = re.sub(padrao, r'\1voltar()', texto)

    # Se mudou, garante que voltar está importado
    if texto_novo != texto:
        if "from logica.navegacao import" in texto_novo:
            texto_novo = re.sub(
                r'from logica\.navegacao import ir_para(?!, voltar)',
                'from logica.navegacao import ir_para, voltar',
                texto_novo
            )
        caminho.write_text(texto_novo, encoding="utf-8")
        print(f"OK: {arquivo} atualizado")
    else:
        print(f"SEM MUDANÇA: {arquivo}")

print()
print("Pronto! Reinicie o Streamlit.")