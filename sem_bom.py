from pathlib import Path

PASTA = Path(__file__).parent / "dados" / "ingles"

corrigidos = 0
for arquivo in PASTA.glob("*.json"):
    conteudo = arquivo.read_text(encoding="utf-8-sig")  # remove BOM se existir
    if conteudo.strip() == "":
        conteudo = "[]"
    arquivo.write_text(conteudo, encoding="utf-8")  # salva sem BOM
    print(f"OK: {arquivo.name}")
    corrigidos += 1

print(f"\n{corrigidos} arquivo(s) regravado(s) sem BOM.")