import sqlite3
from datetime import datetime
from config import DB_PATH


def criar_anotacao(idioma, titulo, conteudo, modulo="", favorita=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        INSERT INTO anotacoes (idioma, titulo, conteudo, modulo, favorita, criado_em, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (idioma, titulo, conteudo, modulo, 1 if favorita else 0, agora, agora))
    novo_id = c.lastrowid
    conn.commit()
    conn.close()
    return novo_id


def atualizar_anotacao(anot_id, titulo, conteudo, modulo, favorita):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        UPDATE anotacoes
        SET titulo = ?, conteudo = ?, modulo = ?, favorita = ?, atualizado_em = ?
        WHERE id = ?
    """, (titulo, conteudo, modulo, 1 if favorita else 0, agora, anot_id))
    conn.commit()
    conn.close()


def excluir_anotacao(anot_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM anotacoes WHERE id = ?", (anot_id,))
    conn.commit()
    conn.close()


def listar_anotacoes(idioma=None, somente_favoritas=False, busca=""):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM anotacoes WHERE 1=1"
    params = []

    if idioma:
        query += " AND (idioma = ? OR idioma = 'geral')"
        params.append(idioma)

    if somente_favoritas:
        query += " AND favorita = 1"

    if busca:
        query += " AND (titulo LIKE ? OR conteudo LIKE ?)"
        params.append(f"%{busca}%")
        params.append(f"%{busca}%")

    query += " ORDER BY favorita DESC, atualizado_em DESC, criado_em DESC"

    c.execute(query, params)
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    return linhas


def obter_anotacao(anot_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM anotacoes WHERE id = ?", (anot_id,))
    linha = c.fetchone()
    conn.close()
    return dict(linha) if linha else None


def contar_anotacoes(idioma=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if idioma:
        c.execute("SELECT COUNT(*) FROM anotacoes WHERE idioma = ? OR idioma = 'geral'", (idioma,))
    else:
        c.execute("SELECT COUNT(*) FROM anotacoes")
    total = c.fetchone()[0]
    conn.close()
    return total