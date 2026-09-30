from pathlib import Path

caminho = Path(__file__).parent / "logica" / "gerenciador_flashcards.py"
conteudo = caminho.read_text(encoding="utf-8")

# Muda o SQL de "erros > 0" pra "erros > acertos"
antigo = '''    c.execute("SELECT modulo, item, SUM(acertos) as ta, SUM(erros) as te FROM progresso_exercicios WHERE idioma = ? AND erros > 0 GROUP BY modulo, item ORDER BY te DESC", (idioma,))'''

novo = '''    c.execute("SELECT modulo, item, SUM(acertos) as ta, SUM(erros) as te FROM progresso_exercicios WHERE idioma = ? GROUP BY modulo, item HAVING te > ta ORDER BY te DESC", (idioma,))'''

if antigo in conteudo:
    conteudo = conteudo.replace(antigo, novo)
    caminho.write_text(conteudo, encoding="utf-8")
    print("OK: criterio mudado para 'erros > acertos'")
    print()
    print("Agora uma palavra sai da lista quando voce acertar mais do que errar.")
    print("Reinicie o Streamlit.")
else:
    print("AVISO: nao achei o bloco exato. Tentando variante...")
    
    # Tenta variante com aspas simples
    antigo2 = """c.execute("SELECT modulo, item, SUM(acertos) as ta, SUM(erros) as te FROM progresso_exercicios WHERE idioma = ? AND erros > 0 GROUP BY modulo, item ORDER BY te DESC", (idioma,))"""
    
    if antigo2 in conteudo:
        conteudo = conteudo.replace(antigo2, novo)
        caminho.write_text(conteudo, encoding="utf-8")
        print("OK: criterio mudado (variante)")
    else:
        print("ERRO: nao achei o bloco. Me manda o arquivo.")
