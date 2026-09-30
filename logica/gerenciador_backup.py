import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from config import BASE_DIR, DB_PATH, DADOS_DIR


BACKUP_DIR = BASE_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


def tamanho_banco():
    """Retorna tamanho do banco em KB."""
    if not DB_PATH.exists():
        return 0
    return DB_PATH.stat().st_size / 1024


def contar_registros():
    """Conta registros em cada tabela."""
    if not DB_PATH.exists():
        return {"progresso": 0, "anotacoes": 0, "streak": 0}
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM progresso")
    progresso = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM anotacoes")
    anotacoes = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM streak")
    streak = c.fetchone()[0]
    conn.close()
    return {"progresso": progresso, "anotacoes": anotacoes, "streak": streak}


def exportar_progresso():
    """Exporta tudo (progresso + anotações + streak) para JSON."""
    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM progresso")
    progresso = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM anotacoes")
    anotacoes = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM streak")
    streak = [dict(r) for r in c.fetchall()]

    conn.close()

    dados = {
        "exportado_em": datetime.now().isoformat(),
        "versao": "1.0",
        "progresso": progresso,
        "anotacoes": anotacoes,
        "streak": streak,
    }

    return json.dumps(dados, ensure_ascii=False, indent=2)


def importar_progresso(json_str):
    """Importa de um JSON. Sobrescreve tudo."""
    try:
        dados = json.loads(json_str)
    except Exception as e:
        return False, f"JSON inválido: {e}"

    if "progresso" not in dados:
        return False, "JSON não tem o campo 'progresso'."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Limpa tabelas
    c.execute("DELETE FROM progresso")
    c.execute("DELETE FROM anotacoes")
    c.execute("DELETE FROM streak")

    # Insere progresso
    for p in dados.get("progresso", []):
        c.execute("""
            INSERT INTO progresso (idioma, modulo, item, acertos, erros, dominado, ultima_revisao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            p.get("idioma"), p.get("modulo"), p.get("item"),
            p.get("acertos", 0), p.get("erros", 0),
            p.get("dominado", 0), p.get("ultima_revisao"),
        ))

    # Insere anotações
    for a in dados.get("anotacoes", []):
        c.execute("""
            INSERT INTO anotacoes (idioma, titulo, conteudo, favorita, modulo, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            a.get("idioma"), a.get("titulo"), a.get("conteudo"),
            a.get("favorita", 0), a.get("modulo", ""),
            a.get("criado_em"), a.get("atualizado_em"),
        ))

    # Insere streak
    for s in dados.get("streak", []):
        c.execute("INSERT INTO streak (data, revisoes) VALUES (?, ?)",
                  (s.get("data"), s.get("revisoes", 0)))

    conn.commit()
    conn.close()
    return True, "Progresso importado com sucesso!"


def backup_banco():
    """Copia o progresso.db pra pasta backups/."""
    if not DB_PATH.exists():
        return None
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = BACKUP_DIR / f"progresso_{agora}.db"
    shutil.copy(DB_PATH, destino)
    return destino


def listar_backups():
    """Lista backups disponíveis, ordenados do mais novo."""
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
    """Apaga o progresso de um idioma específico."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM progresso WHERE idioma = ?", (idioma,))
    conn.commit()
    conn.close()


def resetar_tudo():
    """Apaga todo o progresso, anotações e streak."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM progresso")
    c.execute("DELETE FROM anotacoes")
    c.execute("DELETE FROM streak")
    conn.commit()
    conn.close()


def contar_palavras_por_idioma():
    """Conta quantas palavras tem em cada idioma."""
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