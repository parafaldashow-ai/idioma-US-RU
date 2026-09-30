from pathlib import Path
import re

BASE = Path(__file__).parent
PASTA_TELAS = BASE / "telas"

# Lista de telas
telas = [
    "tela_inicial.py",
    "tela_menu_idioma.py",
    "tela_modulos.py",
    "tela_modulo.py",
    "tela_exercicio.py",
    "tela_dicionario.py",
    "tela_progresso.py",
    "tela_progresso_idioma.py",
    "tela_anotacoes.py",
    "tela_config.py",
    "tela_flashcards.py",
]

print("Adicionando st.stop() em todas as telas...")
print()

for tela in telas:
    caminho = PASTA_TELAS / tela
    if not caminho.exists():
        print(f"SKIP: {tela} nao existe")
        continue

    conteudo = caminho.read_text(encoding="utf-8")

    # Se ja tem st.stop() no final, pula
    if conteudo.rstrip().endswith("st.stop()"):
        print(f"OK: {tela} ja tinha st.stop()")
        continue

    # Encontra a funcao render() e adiciona st.stop() no final dela
    # Estrategia: pega a ultima linha nao vazia e adiciona st.stop() com indentacao 4
    linhas = conteudo.rstrip().split("\n")

    # Remove linhas vazias do final
    while linhas and not linhas[-1].strip():
        linhas.pop()

    # Adiciona st.stop() com indentacao de 4 espacos
    linhas.append("")
    linhas.append("    st.stop()")

    conteudo_novo = "\n".join(linhas) + "\n"
    caminho.write_text(conteudo_novo, encoding="utf-8")
    print(f"OK: {tela} atualizada")

print()
print("=" * 50)
print("Todas as telas atualizadas!")
print()
print("IMPORTANTE: o st.stop() foi adicionado no FINAL do arquivo,")
print("nao necessariamente dentro da funcao render().")
print("Se der erro, me avisa.")
print()
print("Agora reinicie o Streamlit.")
print("=" * 50)