from pathlib import Path

conteudo = '''from pathlib import Path

BASE_DIR = Path(__file__).parent

DADOS_DIR = BASE_DIR / "dados"
ASSETS_DIR = BASE_DIR / "assets"
BANCO_DIR = BASE_DIR / "banco"
DB_PATH = BANCO_DIR / "progresso.db"

IDIOMAS = {
    "ingles": {
        "nome": "Inglês",
        "nome_nativo": "English",
        "bandeira": "🇺🇸",
        "bandeira_alt": "🇬🇧",
        "codigo_audio": "en",
    },
    "russo": {
        "nome": "Russo",
        "nome_nativo": "Русский",
        "bandeira": "🇷🇺",
        "bandeira_alt": "",
        "codigo_audio": "ru",
    },
}

CORES = {
    "bg": "#0e1117",
    "card_bg": "#1e1e2e",
    "card_border": "#333",
    "texto": "#fafafa",
    "texto_sub": "#888",
    "primaria": "#4ade80",
    "secundaria": "#60a5fa",
    "erro": "#f87171",
}

BANCO_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
'''

caminho = Path(__file__).parent / "config.py"
caminho.write_text(conteudo, encoding="utf-8")
print(f"OK: {caminho} sobrescrito")