import sqlite3
from datetime import datetime, timedelta, date
from config import DB_PATH, DADOS_DIR
import json


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            item TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            dominado INTEGER DEFAULT 0,
            ultima_revisao TEXT,
            UNIQUE(idioma, modulo, item)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS anotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT,
            titulo TEXT,
            conteudo TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            data TEXT PRIMARY KEY,
            revisoes INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def registrar(idioma, modulo, item, acertou: bool):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        INSERT INTO progresso (idioma, modulo, item, acertos, erros, ultima_revisao)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(idioma, modulo, item) DO UPDATE SET
            acertos = acertos + ?,
            erros = erros + ?,
            ultima_revisao = ?,
            dominado = CASE WHEN acertos + ? >= 3 THEN 1 ELSE dominado END
    """, (
        idioma, modulo, item,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
        1 if acertou else 0,
    ))
    hoje = agora[:10]
    c.execute("""
        INSERT INTO streak (data, revisoes) VALUES (?, 1)
        ON CONFLICT(data) DO UPDATE SET revisoes = revisoes + 1
    """, (hoje,))
    conn.commit()
    conn.close()


def progresso_modulo(idioma, modulo):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM progresso WHERE idioma=? AND modulo=?", (idioma, modulo))
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    return linhas


def resumo_geral(idioma):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(dominado) FROM progresso WHERE idioma=?", (idioma,))
    total, dominados = c.fetchone()
    conn.close()
    return {
        "total_estudado": total or 0,
        "dominados": dominados or 0,
    }


def streak_atual():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM streak ORDER BY data DESC")
    datas = [r[0] for r in c.fetchall()]
    conn.close()
    if not datas:
        return 0
    hoje = date.today()
    streak = 0
    dia = hoje
    for d in datas:
        if d == dia.isoformat():
            streak += 1
            dia -= timedelta(days=1)
        elif d < dia.isoformat():
            break
    return streak


# ============================================================
# FUNÇÕES NOVAS — ESTATÍSTICAS
# ============================================================

def _total_palavras_idioma(idioma):
    """Conta total de palavras disponíveis num idioma (lendo JSONs)."""
    pasta = DADOS_DIR / idioma
    if not pasta.exists():
        return 0
    total = 0
    for arquivo in pasta.glob("*.json"):
        if arquivo.name == "modulos.json":
            continue
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            if isinstance(dados, list):
                total += len(dados)
        except Exception:
            pass
    return total


def _modulos_do_idioma(idioma):
    """Lê o modulos.json e retorna lista flat com info do nível."""
    caminho = DADOS_DIR / idioma / "modulos.json"
    if not caminho.exists():
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            indice = json.load(f)
    except Exception:
        return []
    modulos = []
    for nivel in indice.get("niveis", []):
        for mod in nivel.get("modulos", []):
            modulos.append({
                "id": mod["id"],
                "nome": mod["nome"],
                "icone": mod.get("icone", "📖"),
                "nivel_id": nivel["id"],
                "nivel_nome": nivel["nome"],
                "nivel_cor": nivel["cor"],
                "nivel_icone": nivel["icone"],
            })
    return modulos


def estatisticas_idioma(idioma):
    """Retorna stats do idioma baseado em EXERCICIOS (nao visualizacoes)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Dominadas: itens do banco de exercicios com 3+ acertos
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE idioma=? AND acertos >= 3
    """, (idioma,))
    dominadas = c.fetchone()[0] or 0

    # Em andamento: itens praticados mas com menos de 3 acertos
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE idioma=? AND acertos < 3 AND (acertos + erros) > 0
    """, (idioma,))
    em_andamento = c.fetchone()[0] or 0

    # Total praticado
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE idioma=?
    """, (idioma,))
    praticadas = c.fetchone()[0] or 0

    conn.close()

    total_disp = _total_palavras_idioma(idioma)

    return {
        "dominadas": dominadas,
        "em_andamento": em_andamento,
        "praticadas": praticadas,
        "total_disponivel": total_disp,
    }


def estatisticas_por_nivel(idioma):
    """Retorna lista de dicts: um por nível, com total e dominadas."""
    modulos = _modulos_do_idioma(idioma)
    if not modulos:
        return []

    # Agrupa módulos por nível
    niveis = {}
    for mod in modulos:
        nid = mod["nivel_id"]
        if nid not in niveis:
            niveis[nid] = {
                "id": nid,
                "nome": mod["nivel_nome"],
                "cor": mod["nivel_cor"],
                "icone": mod["nivel_icone"],
                "modulos_ids": [],
            }
        niveis[nid]["modulos_ids"].append(mod["id"])

    # Conta total de palavras por nível
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    resultado = []
    for nid, info in niveis.items():
        total = 0
        for mid in info["modulos_ids"]:
            caminho = DADOS_DIR / idioma / f"{mid}.json"
            if caminho.exists():
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        dados = json.load(f)
                    if isinstance(dados, list):
                        total += len(dados)
                except Exception:
                    pass

        # Dominadas nesse nível
        placeholders = ",".join("?" * len(info["modulos_ids"]))
        c.execute(
            f"SELECT COUNT(*) FROM progresso WHERE idioma=? AND modulo IN ({placeholders}) AND dominado=1",
            [idioma] + info["modulos_ids"],
        )
        dominadas = c.fetchone()[0]

        resultado.append({
            "id": nid,
            "nome": info["nome"],
            "cor": info["cor"],
            "icone": info["icone"],
            "total": total,
            "dominadas": dominadas,
            "pct": int((dominadas / total * 100) if total else 0),
        })

    conn.close()
    return resultado


def top_modulos(idioma, limite=5):
    """Retorna os módulos mais estudados (por palavras com progresso)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT modulo,
               COUNT(*) as estudadas,
               SUM(dominado) as dominadas
        FROM progresso
        WHERE idioma=?
        GROUP BY modulo
        ORDER BY estudadas DESC
        LIMIT ?
    """, (idioma, limite))
    linhas = c.fetchall()
    conn.close()

    # Anota info do módulo
    modulos_info = {m["id"]: m for m in _modulos_do_idioma(idioma)}

    resultado = []
    for mod_id, estudadas, dominadas in linhas:
        info = modulos_info.get(mod_id, {})
        # Total de palavras no módulo
        caminho = DADOS_DIR / idioma / f"{mod_id}.json"
        total = 0
        if caminho.exists():
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                if isinstance(dados, list):
                    total = len(dados)
            except Exception:
                pass

        resultado.append({
            "id": mod_id,
            "nome": info.get("nome", mod_id),
            "icone": info.get("icone", "📖"),
            "estudadas": estudadas,
            "dominadas": dominadas or 0,
            "total": total,
            "pct": int(((dominadas or 0) / total * 100) if total else 0),
        })

    return resultado


def palavras_mais_erradas(idioma, limite=10):
    """Retorna itens com mais erros."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT modulo, item, acertos, erros
        FROM progresso
        WHERE idioma=? AND erros > 0
        ORDER BY erros DESC
        LIMIT ?
    """, (idioma, limite))
    linhas = c.fetchall()
    conn.close()

    # Pega tradução de cada item
    resultado = []
    for mod_id, item_pt, acertos, erros in linhas:
        caminho = DADOS_DIR / idioma / f"{mod_id}.json"
        traducao = "?"
        pron = ""
        if caminho.exists():
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                for it in dados:
                    if it.get("pt") == item_pt:
                        traducao = it.get(idioma, "?")
                        pron = it.get("pron", "")
                        break
            except Exception:
                pass

        resultado.append({
            "pt": item_pt,
            "traducao": traducao,
            "pron": pron,
            "acertos": acertos,
            "erros": erros,
        })

    return resultado


def dias_estudados(ultimos_dias=30):
    """Retorna lista de dicts: {data, revisoes} dos últimos N dias."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data, revisoes FROM streak ORDER BY data DESC LIMIT ?", (ultimos_dias,))
    linhas = {row[0]: row[1] for row in c.fetchall()}
    conn.close()

    hoje = date.today()
    resultado = []
    for i in range(ultimos_dias - 1, -1, -1):
        dia = hoje - timedelta(days=i)
        data_iso = dia.isoformat()
        resultado.append({
            "data": data_iso,
            "dia_semana": dia.weekday(),
            "revisoes": linhas.get(data_iso, 0),
            "estudou": data_iso in linhas,
        })

    return resultado


# ============================================================
# VISUALIZACOES (progresso dos modulos)
# ============================================================

def registrar_visualizacao(idioma, modulo, item):
    """Registra que o usuario viu o card (sem contar acerto/erro)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO progresso (idioma, modulo, item, visualizacoes)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(idioma, modulo, item) DO UPDATE SET
            visualizacoes = visualizacoes + 1
    """, (idioma, modulo, item))
    conn.commit()
    conn.close()


def contar_visualizacoes_modulo(idioma, modulo):
    """Retorna quantos itens unicos do modulo ja foram vistos."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM progresso
        WHERE idioma=? AND modulo=? AND visualizacoes > 0
    """, (idioma, modulo))
    total = c.fetchone()[0]
    conn.close()
    return total or 0
