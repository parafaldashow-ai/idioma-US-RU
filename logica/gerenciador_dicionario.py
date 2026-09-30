import json
from collections import Counter
from config import DADOS_DIR
from logica.gerenciador_dados import listar_modulos_flat, carregar_modulo


def buscar_palavra(idioma, termo):
    termo = termo.lower().strip()
    if not termo:
        return []
    codigo_idioma = "en" if idioma == "ingles" else "ru"
    resultados = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            pt = item.get("pt", "").lower()
            estrangeiro = item.get(codigo_idioma, "").lower()
            if termo in pt or termo in estrangeiro:
                item_copia = dict(item)
                item_copia["_modulo"] = mod["nome"]
                item_copia["_icone"] = mod["icone"]
                item_copia["_nivel"] = mod["nivel_nome"]
                item_copia["_nivel_cor"] = mod["nivel_cor"]
                resultados.append(item_copia)
    return resultados


def listar_palavras_por_letra(idioma, letra, campo="pt"):
    letra = letra.upper()
    codigo_idioma = "en" if idioma == "ingles" else "ru"
    if campo == "estrangeiro":
        campo = codigo_idioma
    resultados = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            texto = item.get(campo, "")
            if texto and texto.upper().startswith(letra):
                item_copia = dict(item)
                item_copia["_modulo"] = mod["nome"]
                item_copia["_icone"] = mod["icone"]
                item_copia["_nivel"] = mod["nivel_nome"]
                item_copia["_nivel_cor"] = mod["nivel_cor"]
                resultados.append(item_copia)
    resultados.sort(key=lambda x: x.get(campo, "").lower())
    return resultados


def contar_por_letra(idioma, campo="pt"):
    codigo_idioma = "en" if idioma == "ingles" else "ru"
    if campo == "estrangeiro":
        campo = codigo_idioma
    todas_letras = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            texto = item.get(campo, "")
            if texto:
                todas_letras.append(texto[0].upper())
    return dict(Counter(todas_letras))


def estatisticas_gerais(idioma):
    total = 0
    por_modulo = []
    por_nivel = {}
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        qtd = len(itens)
        total += qtd
        por_modulo.append({
            "nome": mod["nome"],
            "icone": mod["icone"],
            "total": qtd,
            "nivel": mod["nivel_nome"],
            "nivel_cor": mod["nivel_cor"],
        })
        nivel = mod["nivel_nome"]
        if nivel not in por_nivel:
            por_nivel[nivel] = {"cor": mod["nivel_cor"], "icone": mod["nivel_icone"], "total": 0}
        por_nivel[nivel]["total"] += qtd
    por_modulo.sort(key=lambda x: x["total"], reverse=True)
    return {"total": total, "por_modulo": por_modulo, "por_nivel": por_nivel}
