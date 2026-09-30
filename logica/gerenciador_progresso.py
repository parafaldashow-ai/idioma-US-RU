import sqlite3
from datetime import datetime, timedelta, date
from config import DB_PATH, DADOS_DIR
import json
from logica.identidade import obter_usuario_id


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL DEFAULT 'default',
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            item TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            dominado INTEGER DEFAULT 0,
            ultima_revisao TEXT,
            visualizacoes INTEGER DEFAULT 0,
            UNIQUE(usuario_id, idioma, modulo, item)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS anotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL DEFAULT 'default',
            idioma TEXT,
            titulo TEXT,
            conteudo TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
            favorita INTEGER DEFAULT 0,
            modulo TEXT DEFAULT '',
            atualizado_em TEXT,
            categoria TEXT DEFAULT 'outros'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            usuario_id TEXT NOT NULL DEFAULT 'default',
            data TEXT NOT NULL,
            revisoes INTEGER DEFAULT 0,
            PRIMARY KEY (usuario_id, data)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso_exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL DEFAULT 'default',
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            item TEXT NOT NULL,
            tipo_exercicio TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            ultima_pratica TEXT,
            UNIQUE(usuario_id, idioma, modulo, item, tipo_exercicio)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT NOT NULL DEFAULT 'default',
            idioma TEXT,
            modulo TEXT,
            tipo_exercicio TEXT,
            total_questoes INTEGER,
            acertos INTEGER,
            erros INTEGER,
            data TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def registrar(idioma, modulo, item, acertou: bool):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        INSERT INTO progresso (usuario_id, idioma, modulo, item, acertos, erros, ultima_revisao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(usuario_id, idioma, modulo, item) DO UPDATE SET
            acertos = acertos + ?,
            erros = erros + ?,
            ultima_revisao = ?,
            dominado = CASE WHEN acertos + ? >= 3 THEN 1 ELSE dominado END
    """, (
        uid, idioma, modulo, item,
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
        INSERT INTO streak (usuario_id, data, revisoes) VALUES (?, ?, 1)
        ON CONFLICT(usuario_id, data) DO UPDATE SET revisoes = revisoes + 1
    """, (uid, hoje))
    conn.commit()
    conn.close()


def progresso_modulo(idioma, modulo):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(
        "SELECT * FROM progresso WHERE usuario_id=? AND idioma=? AND modulo=?",
        (uid, idioma, modulo),
    )
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    return linhas


def resumo_geral(idioma):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*), SUM(dominado) FROM progresso WHERE usuario_id=? AND idioma=?",
        (uid, idioma),
    )
    total, dominados = c.fetchone()
    conn.close()
    return {
        "total_estudado": total or 0,
        "dominados": dominados or 0,
    }


def streak_atual():
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM streak WHERE usuario_id=? ORDER BY data DESC", (uid,))
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


def _total_palavras_idioma(idioma):
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
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE usuario_id=? AND idioma=? AND acertos >= 3
    """, (uid, idioma))
    dominadas = c.fetchone()[0] or 0
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE usuario_id=? AND idioma=? AND acertos < 3 AND (acertos + erros) > 0
    """, (uid, idioma))
    em_andamento = c.fetchone()[0] or 0
    c.execute("""
        SELECT COUNT(*) FROM progresso_exercicios
        WHERE usuario_id=? AND idioma=?
    """, (uid, idioma))
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
    uid = obter_usuario_id()
    modulos = _modulos_do_idioma(idioma)
    if not modulos:
        return []
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
        placeholders = ",".join("?" * len(info["modulos_ids"]))
        c.execute(
            f"SELECT COUNT(*) FROM progresso WHERE usuario_id=? AND idioma=? AND modulo IN ({placeholders}) AND dominado=1",
            [uid, idioma] + info["modulos_ids"],
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
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT modulo,
               COUNT(*) as estudadas,
               SUM(dominado) as dominadas
        FROM progresso
        WHERE usuario_id=? AND idioma=?
        GROUP BY modulo
        ORDER BY estudadas DESC
        LIMIT ?
    """, (uid, idioma, limite))
    linhas = c.fetchall()
    conn.close()
    modulos_info = {m["id"]: m for m in _modulos_do_idioma(idioma)}
    resultado = []
    for mod_id, estudadas, dominadas in linhas:
        info = modulos_info.get(mod_id, {})
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
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT modulo, item, acertos, erros
        FROM progresso
        WHERE usuario_id=? AND idioma=? AND erros > 0
        ORDER BY erros DESC
        LIMIT ?
    """, (uid, idioma, limite))
    linhas = c.fetchall()
    conn.close()
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
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT data, revisoes FROM streak WHERE usuario_id=? ORDER BY data DESC LIMIT ?",
        (uid, ultimos_dias),
    )
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


def registrar_visualizacao(idioma, modulo, item):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO progresso (usuario_id, idioma, modulo, item, visualizacoes)
        VALUES (?, ?, ?, ?, 1)
        ON CONFLICT(usuario_id, idioma, modulo, item) DO UPDATE SET
            visualizacoes = visualizacoes + 1
    """, (uid, idioma, modulo, item))
    conn.commit()
    conn.close()


def contar_visualizacoes_modulo(idioma, modulo):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*) FROM progresso
        WHERE usuario_id=? AND idioma=? AND modulo=? AND visualizacoes > 0
    """, (uid, idioma, modulo))
    total = c.fetchone()[0]
    conn.close()
    return total or 0