from pathlib import Path

BASE = Path(__file__).parent
PASTA_RUSSO = BASE / "dados" / "russo"

print("Verificando arquivos com problema...")
print()

# Lista os arquivos problematicos
arquivos = ["alfabeto.json", "animais.json", "casa.json"]

for nome in arquivos:
    caminho = PASTA_RUSSO / nome
    if not caminho.exists():
        print(f"NAO EXISTE: {nome}")
        continue

    tamanho = caminho.stat().st_size
    print(f"{nome}: {tamanho} bytes")

    # Le o conteudo removendo BOM se existir
    try:
        with open(caminho, "r", encoding="utf-8-sig") as f:
            conteudo = f.read()

        if not conteudo.strip():
            print(f"  AVISO: arquivo VAZIO")
            continue

        # Verifica se eh JSON valido
        import json
        try:
            dados = json.loads(conteudo)
            print(f"  OK: {len(dados)} itens")
        except Exception as e:
            print(f"  ERRO JSON: {e}")
            continue

        # Reescreve SEM BOM
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"  OK: reescrito sem BOM")

    except Exception as e:
        print(f"  ERRO ao ler: {e}")

print()
print("Pronto!")