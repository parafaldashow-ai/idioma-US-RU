import sqlite3
from datetime import datetime
from config import DB_PATH


def init_db_exercicios():
    """Cria tabelas dos exercícios (separadas do progresso normal)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabela de progresso em exercícios
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso_exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            item TEXT NOT NULL,
            tipo_exercicio TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            ultima_pratica TEXT,
            UNIQUE(idioma, modulo, item, tipo_exercicio)
        )
    """)

    # Tabela de sessões (histórico)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_exercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            tipo_exercicio TEXT NOT NULL,
            total_questoes INTEGER,
            acertos INTEGER,
            erros INTEGER,
            data TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def registrar_exercicio(idioma, modulo, item, tipo_exercicio, acertou: bool):
    """Registra 1 acerto/erro de exercício."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()

    c.execute("""
        INSERT INTO progresso_exercicios (idioma, modulo, item, tipo_exercicio, acertos, erros, ultima_pratica)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(idioma, modulo, item, tipo_exercicio) DO UPDATE SET
            acertos = acertos + ?,
            erros = erros + ?,
            ultima_pratica = ?
    """, (
        idioma, modulo, item, tipo_exercicio,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
    ))

    conn.commit()
    conn.close()


def registrar_sessao(idioma, modulo, tipo_exercicio, total, acertos, erros):
    """Registra uma sessão completa no histórico."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO sessoes_exercicios (idioma, modulo, tipo_exercicio, total_questoes, acertos, erros)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (idioma, modulo, tipo_exercicio, total, acertos, erros))
    conn.commit()
    conn.close()


def progresso_exercicio_item(idioma, modulo, item, tipo_exercicio):
    """Retorna os dados de 1 item específico em 1 tipo de exercício."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT * FROM progresso_exercicios
        WHERE idioma=? AND modulo=? AND item=? AND tipo_exercicio=?
    """, (idioma, modulo, item, tipo_exercicio))
    linha = c.fetchone()
    conn.close()
    return dict(linha) if linha else None


def estatisticas_exercicios_idioma(idioma, tipo_exercicio=None):
    """Retorna estatísticas gerais de exercícios."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if tipo_exercicio:
        c.execute("""
            SELECT COUNT(*), SUM(acertos), SUM(erros)
            FROM progresso_exercicios
            WHERE idioma=? AND tipo_exercicio=?
        """, (idioma, tipo_exercicio))
    else:
        c.execute("""
            SELECT COUNT(*), SUM(acertos), SUM(erros)
            FROM progresso_exercicios
            WHERE idioma=?
        """, (idioma,))

    total, acertos, erros = c.fetchone()
    conn.close()

    return {
        "itens_praticados": total or 0,
        "total_acertos": acertos or 0,
        "total_erros": erros or 0,
        "taxa_acerto": int(((acertos or 0) / ((acertos or 0) + (erros or 0)) * 100)) if (acertos or erros) else 0,
    }


def historico_sessoes(idioma, limite=10):
    """Últimas N sessões de exercício."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT * FROM sessoes_exercicios
        WHERE idioma=?
        ORDER BY data DESC
        LIMIT ?
    """, (idioma, limite))
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    return linhas