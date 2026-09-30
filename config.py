from pathlib import Path

BASE_DIR = Path(__file__).parent

DADOS_DIR = BASE_DIR / "dados"
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
BANCO_DIR = BASE_DIR / "banco"
DB_PATH = BANCO_DIR / "progresso.db"

IDIOMAS = {
    "ingles": {
        "nome": "Inglês",
        "nome_nativo": "English",
        "bandeira": "🗽",
        "bandeira_alt": "",
        "bandeira_img": "",
        "codigo_audio": "en",
    },
    "russo": {
        "nome": "Russo",
        "nome_nativo": "Русский",
        "bandeira": "🐻",
        "bandeira_alt": "",
        "bandeira_img": "",
        "codigo_audio": "ru",
    },
}

# Emoji pro português
BANDEIRA_PT = "📖"

CORES = {
    "bg": "#0f1419",
    "bg_alt": "#1a2332",
    "card_bg": "#1a2332",
    "card_border": "#2d3748",
    "texto": "#ffffff",
    "texto_sub": "#a8b2c1",
    "texto_muted": "#6b7280",
    "primaria": "#34d399",
    "secundaria": "#3b82f6",
    "terciaria": "#a78bfa",
    "erro": "#ef4444",
    "aviso": "#fbbf24",
    "sucesso": "#34d399",
}

BANCO_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


def caminho_bandeira(nome_arquivo):
    """Nao usado mais - retorna None."""
    return None