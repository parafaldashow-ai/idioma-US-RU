import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "banco" / "progresso.db"

conn = sqlite3.connect(DB)
c = conn.cursor()

# Verifica colunas existentes na tabela anotacoes
c.execute("PRAGMA table_info(anotacoes)")
colunas = [row[1] for row in c.fetchall()]
print("Colunas atuais:", colunas)

# Adiciona colunas que faltam
novas = {
    "favorita": "INTEGER DEFAULT 0",
    "modulo": "TEXT DEFAULT ''",
    "atualizado_em": "TEXT",
}

for coluna, tipo in novas.items():
    if coluna not in colunas:
        c.execute(f"ALTER TABLE anotacoes ADD COLUMN {coluna} {tipo}")
        print(f"OK: coluna '{coluna}' adicionada")
    else:
        print(f"JA EXISTE: coluna '{coluna}'")

conn.commit()
conn.close()
print()
print("Banco atualizado com sucesso!")