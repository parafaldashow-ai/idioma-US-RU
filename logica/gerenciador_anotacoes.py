import sqlite3
from datetime import datetime
from config import DB_PATH
from logica.identidade import obter_usuario_id


def criar_anotacao(idioma, titulo, conteudo, modulo="", favorita=False):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        INSERT INTO anotacoes (usuario_id, idioma, titulo, conteudo, modulo, favorita, criado_em, atualizado_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (uid, idioma, titulo, conteudo, modulo, 1 if favorita else 0, agora, agora))
    novo_id = c.lastrowid
    conn.commit()
    conn.close()
    return novo_id


def atualizar_anotacao(anot_id, titulo, conteudo, modulo, favorita):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        UPDATE anotacoes
        SET titulo = ?, conteudo = ?, modulo = ?, favorita = ?, atualizado_em = ?
        WHERE id = ? AND usuario_id = ?
    """, (titulo, conteudo, modulo, 1 if favorita else 0, agora, anot_id, uid))
    conn.commit()
    conn.close()


def excluir_anotacao(anot_id):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM anotacoes WHERE id = ? AND usuario_id = ?", (anot_id, uid))
    conn.commit()
    conn.close()


def listar_anotacoes(idioma=None, somente_favoritas=False, busca=""):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM anotacoes WHERE usuario_id = ?"
    params = [uid]

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
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM anotacoes WHERE id = ? AND usuario_id = ?", (anot_id, uid))
    linha = c.fetchone()
    conn.close()
    return dict(linha) if linha else None


def contar_anotacoes(idioma=None):
    uid = obter_usuario_id()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if idioma:
        c.execute(
            "SELECT COUNT(*) FROM anotacoes WHERE usuario_id = ? AND (idioma = ? OR idioma = 'geral')",
            (uid, idioma),
        )
    else:
        c.execute("SELECT COUNT(*) FROM anotacoes WHERE usuario_id = ?", (uid,))
    total = c.fetchone()[0]
    conn.close()
    return total