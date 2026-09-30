import sqlite3
from config import DB_PATH
from logica.gerenciador_dados import listar_modulos_flat, carregar_modulo
from logica.identidade import obter_usuario_id


def _carregar_item_completo(idioma, modulo, item_pt):
    itens = carregar_modulo(idioma, modulo)
    for item in itens:
        if item.get("pt") == item_pt:
            return item
    return None


def _info_modulo(idioma, modulo_id):
    for mod in listar_modulos_flat(idioma):
        if mod["id"] == modulo_id:
            return mod
    return None


def pegar_nao_dominadas(idioma, limite=None):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT modulo, item, visualizacoes FROM progresso WHERE usuario_id=? AND idioma=? AND visualizacoes > 0",
        (uid, idioma),
    )
    vistos = [dict(r) for r in c.fetchall()]
    c.execute(
        "SELECT modulo, item, acertos FROM progresso_exercicios WHERE usuario_id=? AND idioma=?",
        (uid, idioma),
    )
    acertos = {}
    for row in c.fetchall():
        k = (row["modulo"], row["item"])
        acertos[k] = acertos.get(k, 0) + row["acertos"]
    conn.close()
    resultado = []
    for v in vistos:
        k = (v["modulo"], v["item"])
        if acertos.get(k, 0) < 3:
            item = _carregar_item_completo(idioma, v["modulo"], v["item"])
            if item:
                mi = _info_modulo(idioma, v["modulo"])
                if mi:
                    item["_modulo"] = mi["nome"]
                    item["_modulo_id"] = v["modulo"]
                    item["_icone"] = mi["icone"]
                    item["_nivel"] = mi["nivel_nome"]
                    item["_nivel_cor"] = mi["nivel_cor"]
                    item["_acertos"] = acertos.get(k, 0)
                    item["_erros"] = 0
                    resultado.append(item)
    if limite:
        resultado = resultado[:limite]
    return resultado


def pegar_erradas(idioma, limite=None):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT modulo, item, SUM(acertos) as ta, SUM(erros) as te FROM progresso_exercicios WHERE usuario_id=? AND idioma=? GROUP BY modulo, item HAVING te > ta ORDER BY te DESC",
        (uid, idioma),
    )
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    resultado = []
    for l in linhas:
        item = _carregar_item_completo(idioma, l["modulo"], l["item"])
        if item:
            mi = _info_modulo(idioma, l["modulo"])
            if mi:
                item["_modulo"] = mi["nome"]
                item["_modulo_id"] = l["modulo"]
                item["_icone"] = mi["icone"]
                item["_nivel"] = mi["nivel_nome"]
                item["_nivel_cor"] = mi["nivel_cor"]
                item["_acertos"] = l["ta"]
                item["_erros"] = l["te"]
                resultado.append(item)
    if limite:
        resultado = resultado[:limite]
    return resultado


def pegar_aleatorias(idioma, quantidade=20):
    import random
    todos = []
    for mod in listar_modulos_flat(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            ic = dict(item)
            ic["_modulo"] = mod["nome"]
            ic["_modulo_id"] = mod["id"]
            ic["_icone"] = mod["icone"]
            ic["_nivel"] = mod["nivel_nome"]
            ic["_nivel_cor"] = mod["nivel_cor"]
            ic["_acertos"] = 0
            ic["_erros"] = 0
            todos.append(ic)
    random.shuffle(todos)
    return todos[:quantidade]


def contar_nao_dominadas(idioma):
    return len(pegar_nao_dominadas(idioma))


def contar_erradas(idioma):
    return len(pegar_erradas(idioma))