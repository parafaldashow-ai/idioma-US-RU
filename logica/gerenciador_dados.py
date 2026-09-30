import json
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
