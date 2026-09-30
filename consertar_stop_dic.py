from pathlib import Path
import re

BASE = Path(__file__).parent
caminho = BASE / "telas" / "tela_dicionario.py"
conteudo = caminho.read_text(encoding="utf-8")

print("Analisando o arquivo...")
print()

# Mostra onde estao os st.stop() atuais
linhas = conteudo.split("\n")
for i, linha in enumerate(linhas, 1):
    if "st.stop()" in linha:
        print(f"  Linha {i}: {linha.strip()}")

print()

# Remove TODOS os st.stop() primeiro
conteudo = conteudo.replace("    st.stop()", "")
conteudo = conteudo.replace("st.stop()", "")

# Limpa linhas vazias duplicadas
while "\n\n\n\n" in conteudo:
    conteudo = conteudo.replace("\n\n\n\n", "\n\n\n")

# Adiciona st.stop() APENAS no final da funcao render()
# Ele deve vir DEPOIS de chamar a ultima aba, antes de "def render_busca"
padrao = r'(    else:\n        render_estatisticas\(idioma_atual\)\n)'
if re.search(padrao, conteudo):
    conteudo = re.sub(
        padrao,
        r'\1\n    st.stop()\n',
        conteudo
    )
    print("OK: st.stop() adicionado APENAS no final do render()")
else:
    print("AVISO: nao achei o padrao esperado")
    print("Vou tentar outra estrategia...")
    
    # Alternativa: adiciona antes do primeiro "def render_"
    padrao2 = r'(\n\ndef render_)'
    if re.search(padrao2, conteudo):
        conteudo = re.sub(
            padrao2,
            r'\n    st.stop()\n\ndef render_',
            conteudo,
            count=1
        )
        print("OK: st.stop() adicionado (variante)")

caminho.write_text(conteudo, encoding="utf-8")

print()
print("Salvo. Vou mostrar as linhas do st.stop() agora:")
print()

linhas = conteudo.split("\n")
for i, linha in enumerate(linhas, 1):
    if "st.stop()" in linha:
        print(f"  Linha {i}: {linha.strip()}")

print()
print("=" * 50)
print("Reinicie o Streamlit.")
print("=" * 50)