from pathlib import Path
import re

BASE = Path(__file__).parent
caminho = BASE / "logica" / "navegacao.py"
conteudo = caminho.read_text(encoding="utf-8")

print("Conteudo atual do TELAS:")
print()

# Mostra as linhas do dicionario TELAS
linhas = conteudo.split("\n")
for i, linha in enumerate(linhas):
    if "TELAS" in linha or (":" in linha and "telas." in linha):
        print(f"  {i+1}: {linha.strip()}")

print()

# Verifica se ja tem "ajuda"
if '"ajuda"' in conteudo:
    print("OK: rota 'ajuda' ja existe")
else:
    print("Adicionando rota 'ajuda'...")
    
    # Estrategia: adiciona depois da ultima linha que tenha "telas.tela_"
    linhas = conteudo.split("\n")
    ultimo_idx = -1
    for i, linha in enumerate(linhas):
        if "telas.tela_" in linha and ":" in linha:
            ultimo_idx = i
    
    if ultimo_idx == -1:
        print("ERRO: nao achei onde adicionar")
    else:
        # Pega a indentacao da linha
        linha_ref = linhas[ultimo_idx]
        indent = linha_ref[:len(linha_ref) - len(linha_ref.lstrip())]
        
        # Verifica se a ultima linha termina com virgula
        if not linha_ref.rstrip().endswith(","):
            linhas[ultimo_idx] = linha_ref.rstrip() + ","
        
        # Adiciona a nova linha
        nova_linha = f'{indent}"ajuda":      "telas.tela_ajuda",'
        linhas.insert(ultimo_idx + 1, nova_linha)
        
        conteudo_novo = "\n".join(linhas)
        caminho.write_text(conteudo_novo, encoding="utf-8")
        print(f"OK: linha adicionada apos a linha {ultimo_idx + 1}")
        print(f"  {nova_linha}")

print()
print("Verificando se ficou certo:")
conteudo = caminho.read_text(encoding="utf-8")
for i, linha in enumerate(conteudo.split("\n")):
    if "telas.tela_" in linha:
        print(f"  {i+1}: {linha.strip()}")

print()
print("Reinicie o Streamlit: streamlit run main.py")
