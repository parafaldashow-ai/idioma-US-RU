from pathlib import Path
import re

BASE = Path(__file__).parent
caminho = BASE / "telas" / "tela_dicionario.py"
conteudo = caminho.read_text(encoding="utf-8")

# ============================================================
# 1. Remove TODOS os st.stop() do arquivo
# ============================================================
conteudo = conteudo.replace("    st.stop()\n", "")
conteudo = conteudo.replace("\nst.stop()", "")
conteudo = conteudo.replace("st.stop()", "")

print("OK: removidos todos os st.stop() antigos")

# ============================================================
# 2. Adiciona st.stop() SO no final da funcao render()
# ============================================================
# Encontra o final da funcao render() — antes de "def render_busca"
padrao = r'(        render_estatisticas\(idioma_atual\)\n)(\n*)(def render_busca)'
match = re.search(padrao, conteudo)

if match:
    conteudo = re.sub(
        padrao,
        r'\1\n    st.stop()\n\n\n\3',
        conteudo
    )
    print("OK: st.stop() adicionado no final da funcao render()")
else:
    # Tentativa alternativa
    padrao2 = r'(        render_estatisticas\(idioma_atual\)\n)'
    if re.search(padrao2, conteudo):
        conteudo = re.sub(
            padrao2,
            r'\1\n    st.stop()\n',
            conteudo
        )
        print("OK: st.stop() adicionado (variante)")

caminho.write_text(conteudo, encoding="utf-8")
print()
print("Reinicie o Streamlit.")