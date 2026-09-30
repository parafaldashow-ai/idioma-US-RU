import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from config import BASE_DIR, DB_PATH, DADOS_DIR
from logica.identidade import obter_usuario_id


BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


def tamanho_banco():
    if not DB_PATH.exists():
        return 0
    return DB_PATH.stat().st_size / 1024


def contar_registros():
    uid = obter_usuario_id()
    if not DB_PATH.exists():
        return {"progresso": 0, "anotacoes": 0, "streak": 0}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM progresso WHERE usuario_id=?", (uid,))
    progresso = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM anotacoes WHERE usuario_id=?", (uid,))
    anotacoes = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM streak WHERE usuario_id=?", (uid,))
    streak = c.fetchone()[0]
    conn.close()
    return {"progresso": progresso, "anotacoes": anotacoes, "streak": streak}


def exportar_progresso():
    uid = obter_usuario_id()
    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM progresso WHERE usuario_id=?", (uid,))
    progresso = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM anotacoes WHERE usuario_id=?", (uid,))
    anotacoes = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM streak WHERE usuario_id=?", (uid,))
    streak = [dict(r) for r in c.fetchall()]

    conn.close()

    dados = {
        "exportado_em": datetime.now().isoformat(),
        "versao": "1.0",
        "usuario_id": uid,
        "progresso": progresso,
        "anotacoes": anotacoes,
        "streak": streak,
    }

    return json.dumps(dados, ensure_ascii=False, indent=2)


def importar_progresso(json_str):
    uid = obter_usuario_id()
    try:
        dados = json.loads(json_str)
    except Exception as e:
        return False, f"JSON inválido: {e}"

    if "progresso" not in dados:
        return False, "JSON não tem o campo 'progresso'."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Limpa só os dados do usuário atual
    c.execute("DELETE FROM progresso WHERE usuario_id=?", (uid,))
    c.execute("DELETE FROM anotacoes WHERE usuario_id=?", (uid,))
    c.execute("DELETE FROM streak WHERE usuario_id=?", (uid,))

    for p in dados.get("progresso", []):
        c.execute("""
            INSERT INTO progresso (usuario_id, idioma, modulo, item, acertos, erros, dominado, ultima_revisao, visualizacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, p.get("idioma"), p.get("modulo"), p.get("item"),
            p.get("acertos", 0), p.get("erros", 0),
            p.get("dominado", 0), p.get("ultima_revisao"),
            p.get("visualizacoes", 0),
        ))

    for a in dados.get("anotacoes", []):
        c.execute("""
            INSERT INTO anotacoes (usuario_id, idioma, titulo, conteudo, favorita, modulo, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            uid, a.get("idioma"), a.get("titulo"), a.get("conteudo"),
            a.get("favorita", 0), a.get("modulo", ""),
            a.get("criado_em"), a.get("atualizado_em"),
        ))

    for s in dados.get("streak", []):
        c.execute(
            "INSERT OR REPLACE INTO streak (usuario_id, data, revisoes) VALUES (?, ?, ?)",
            (uid, s.get("data"), s.get("revisoes", 0)),
        )

    conn.commit()
    conn.close()
    return True, "Progresso importado com sucesso!"


def backup_banco():
    if not DB_PATH.exists():
        return None
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = BACKUP_DIR / f"progresso_{agora}.db"
    shutil.copy(DB_PATH, destino)
    return destino


def listar_backups():
    arquivos = sorted(BACKUP_DIR.glob("progresso_*.db"), reverse=True)
    return [
        {
            "nome": a.name,
            "tamanho_kb": a.stat().st_size / 1024,
            "caminho": a,
        }
        for a in arquivos
    ]


def resetar_progresso_idioma(idioma):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM progresso WHERE usuario_id=? AND idioma=?", (uid, idioma))
    conn.commit()
    conn.close()


def resetar_tudo():
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM progresso WHERE usuario_id=?", (uid,))
    c.execute("DELETE FROM anotacoes WHERE usuario_id=?", (uid,))
    c.execute("DELETE FROM streak WHERE usuario_id=?", (uid,))
    conn.commit()
    conn.close()


def contar_palavras_por_idioma():
    resultado = {}
    for idioma_dir in DADOS_DIR.iterdir():
        if not idioma_dir.is_dir():
            continue
        idioma = idioma_dir.name
        total = 0
        for arquivo in idioma_dir.glob("*.json"):
            if arquivo.name == "modulos.json":
                continue
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                if isinstance(dados, list):
                    total += len(dados)
            except Exception:
                pass
        resultado[idioma] = total
    return resultado