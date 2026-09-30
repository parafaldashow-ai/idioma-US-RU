import sqlite3

conn = sqlite3.connect("banco/progresso.db")
cur = conn.cursor()

# Lista todas as tabelas
print("=" * 50)
print("TABELAS DO BANCO:")
print("=" * 50)
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = [t[0] for t in cur.fetchall()]
for t in tabelas:
    print(f"  - {t}")

# Mostra estrutura de cada tabela
for tabela in tabelas:
    print()
    print("=" * 50)
    print(f"ESTRUTURA DA TABELA '{tabela}':")
    print("=" * 50)
    cur.execute(f"PRAGMA table_info({tabela})")
    for col in cur.fetchall():
        # col = (cid, name, type, notnull, default, pk)
        print(f"  [{col[0]}] {col[1]} ({col[2]}) | default={col[4]} | pk={col[5]}")

conn.close()