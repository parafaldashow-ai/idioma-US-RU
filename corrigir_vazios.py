import json
from pathlib import Path

BASE = Path(__file__).parent
PASTA_INGLES = BASE / "dados" / "ingles"

# ============ MODULOS.JSON ============
modulos_json = {
    "niveis": [
        {
            "id": "iniciante",
            "nome": "Iniciante",
            "icone": "🟢",
            "cor": "#4ade80",
            "descricao": "Comece por aqui",
            "modulos": [
                {"id": "saudacoes", "nome": "Saudações", "icone": "👋"},
                {"id": "numeros",   "nome": "Números",   "icone": "🔢"},
                {"id": "cores",     "nome": "Cores",     "icone": "🎨"},
                {"id": "familia",   "nome": "Família",   "icone": "👨‍👩‍👧"},
            ],
        },
        {
            "id": "basico",
            "nome": "Básico",
            "icone": "🔵",
            "cor": "#60a5fa",
            "descricao": "Vocabulário do dia a dia",
            "modulos": [
                {"id": "casa",       "nome": "Casa e objetos",   "icone": "🏠"},
                {"id": "roupas",     "nome": "Roupas",           "icone": "👕"},
                {"id": "animais",    "nome": "Animais",          "icone": "🐶"},
                {"id": "clima",      "nome": "Clima e natureza", "icone": "🌦️"},
                {"id": "transporte", "nome": "Transporte",       "icone": "🚗"},
                {"id": "direcoes",   "nome": "Direções",         "icone": "🧭"},
                {"id": "comida",     "nome": "Comida",           "icone": "🍞"},
                {"id": "profissoes", "nome": "Profissões",       "icone": "💼"},
            ],
        },
        {
            "id": "intermediario",
            "nome": "Intermediário",
            "icone": "🟡",
            "cor": "#facc15",
            "descricao": "Construindo frases",
            "modulos": [
                {"id": "verbos",      "nome": "Verbos essenciais",  "icone": "🔤"},
                {"id": "perguntas",   "nome": "Perguntas",          "icone": "❓"},
                {"id": "emocoes",     "nome": "Emoções",            "icone": "😊"},
                {"id": "dinheiro",    "nome": "Dinheiro e compras", "icone": "💰"},
                {"id": "restaurante", "nome": "Restaurante",        "icone": "🍽️"},
                {"id": "lugares",     "nome": "Lugares na cidade",  "icone": "🏙️"},
                {"id": "datas",       "nome": "Dias e meses",       "icone": "📅"},
            ],
        },
        {
            "id": "avancado",
            "nome": "Avançado",
            "icone": "🟠",
            "cor": "#fb923c",
            "descricao": "Aprofundando",
            "modulos": [
                {"id": "corpo",    "nome": "Corpo humano",      "icone": "🧑"},
                {"id": "horas",    "nome": "Horas e datas",     "icone": "🕐"},
                {"id": "formas",   "nome": "Formas e tamanhos", "icone": "🔷"},
                {"id": "midia",    "nome": "Música e cinema",   "icone": "🎵"},
                {"id": "esportes", "nome": "Esportes",          "icone": "⚽"},
                {"id": "viagem",   "nome": "Viagem",            "icone": "✈️"},
            ],
        },
        {
            "id": "critico",
            "nome": "Crítico",
            "icone": "🔴",
            "cor": "#f87171",
            "descricao": "Sobrevivência",
            "modulos": [
                {"id": "emergencias", "nome": "Emergências", "icone": "🚨"},
            ],
        },
    ]
}

caminho_modulos = PASTA_INGLES / "modulos.json"
caminho_modulos.write_text(
    json.dumps(modulos_json, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"OK: {caminho_modulos}")

# ============ GERENCIADOR_DADOS.PY ============
gerenciador = '''import json
from config import DADOS_DIR


def carregar_indice_modulos(idioma: str):
    """Retorna a estrutura de niveis com modulos."""
    caminho = DADOS_DIR / idioma / "modulos.json"
    if not caminho.exists():
        return {"niveis": []}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_modulos_flat(idioma: str):
    """Retorna lista plana de todos os modulos (independente de nivel)."""
    indice = carregar_indice_modulos(idioma)
    modulos = []
    for nivel in indice.get("niveis", []):
        for mod in nivel.get("modulos", []):
            mod_copy = dict(mod)
            mod_copy["nivel_id"] = nivel["id"]
            mod_copy["nivel_nome"] = nivel["nome"]
            mod_copy["nivel_cor"] = nivel["cor"]
            mod_copy["nivel_icone"] = nivel["icone"]
            modulos.append(mod_copy)
    return modulos


def achar_modulo(idioma: str, modulo_id: str):
    """Retorna info de um modulo especifico."""
    for mod in listar_modulos_flat(idioma):
        if mod["id"] == modulo_id:
            return mod
    return None


def carregar_modulo(idioma: str, modulo_id: str):
    """Carrega os itens de um modulo."""
    caminho = DADOS_DIR / idioma / f"{modulo_id}.json"
    if not caminho.exists():
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_todos_vocabulos(idioma: str):
    tudo = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            item["_modulo"] = mod["nome"]
            item["_nivel"] = mod["nivel_nome"]
            tudo.append(item)
    return tudo


def buscar_palavra(idioma: str, termo: str):
    termo = termo.lower().strip()
    if not termo:
        return []
    resultados = []
    for item in listar_todos_vocabulos(idioma):
        pt = item.get("pt", "").lower()
        estrangeiro = item.get(idioma, "").lower()
        if termo in pt or termo in estrangeiro:
            resultados.append(item)
    return resultados
'''

caminho_ger = BASE / "logica" / "gerenciador_dados.py"
caminho_ger.write_text(gerenciador, encoding="utf-8")
print(f"OK: {caminho_ger}")

# ============ JSONs VAZIOS ============
modulos_vazios = [
    "casa", "roupas", "animais", "clima", "transporte",
    "direcoes", "verbos", "perguntas", "emocoes", "dinheiro",
    "restaurante", "lugares", "datas", "corpo", "horas",
    "formas", "midia", "esportes", "viagem",
]

for nome in modulos_vazios:
    caminho = PASTA_INGLES / f"{nome}.json"
    if caminho.exists():
        print(f"JA EXISTE: {nome}.json")
    else:
        caminho.write_text("[]", encoding="utf-8")
        print(f"OK: {nome}.json")

print()
print("=" * 50)
print("Correcao aplicada com sucesso!")
print("Agora reinicia o Streamlit:")
print("  1. Ctrl+C no terminal")
print("  2. streamlit run main.py")
print("  3. Ctrl+Shift+R no navegador")
print("=" * 50)