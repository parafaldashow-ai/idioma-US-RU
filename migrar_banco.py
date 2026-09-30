import sqlite3

conn = sqlite3.connect("banco/progresso.db")
cursor = conn.cursor()

# Verifica se a coluna já existe
cursor.execute("PRAGMA table_info(progresso)")
colunas = [col[1] for col in cursor.fetchall()]

if "usuario_id" not in colunas:
    print("Adicionando coluna usuario_id...")
    cursor.execute("ALTER TABLE progresso ADD COLUMN usuario_id TEXT DEFAULT 'default'")
    conn.commit()
    print("Coluna adicionada com sucesso!")
else:
    print("Coluna usuario_id já existe.")

conn.close()