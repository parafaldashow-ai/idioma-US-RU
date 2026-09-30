import sqlite3

conn = sqlite3.connect("banco/progresso.db")
cur = conn.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='progresso'")
resultado = cur.fetchone()
print(resultado[0] if resultado else "TABELA NAO EXISTE")
conn.close()