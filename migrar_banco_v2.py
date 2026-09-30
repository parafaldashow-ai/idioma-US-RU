import sqlite3

conn = sqlite3.connect("banco/progresso.db")
c = conn.cursor()

print("Iniciando migração...")

# ==========================================
# 1. Adicionar usuario_id nas tabelas que faltam
# ==========================================
tabelas_para_adicionar = ["anotacoes", "streak", "progresso_exercicios", "sessoes_exercicios"]

for tabela in tabelas_para_adicionar:
    c.execute(f"PRAGMA table_info({tabela})")
    colunas = [col[1] for col in c.fetchall()]
    if "usuario_id" not in colunas:
        print(f"  → Adicionando usuario_id em '{tabela}'...")
        c.execute(f"ALTER TABLE {tabela} ADD COLUMN usuario_id TEXT DEFAULT 'default'")
    else:
        print(f"  → '{tabela}' já tem usuario_id.")

# ==========================================
# 2. Recriar tabela 'progresso' com UNIQUE correto
# ==========================================
print("  → Recriando tabela 'progresso' com UNIQUE(usuario_id, idioma, modulo, item)...")

c.execute("""
    CREATE TABLE progresso_novo (
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
    INSERT INTO progresso_novo
        (id, usuario_id, idioma, modulo, item, acertos, erros, dominado, ultima_revisao, visualizacoes)
    SELECT
        id, usuario_id, idioma, modulo, item, acertos, erros, dominado, ultima_revisao, visualizacoes
    FROM progresso
""")

c.execute("DROP TABLE progresso")
c.execute("ALTER TABLE progresso_novo RENAME TO progresso")

# ==========================================
# 3. Recriar tabela 'progresso_exercicios' com UNIQUE correto
# ==========================================
print("  → Recriando tabela 'progresso_exercicios'...")

# Verifica se existe UNIQUE antes
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='progresso_exercicios'")
sql_atual = c.fetchone()[0]
if "UNIQUE" in sql_atual.upper() or "PRIMARY KEY" in sql_atual.upper():
    print("     (já tem constraint, recriando com usuario_id)")

c.execute("""
    CREATE TABLE progresso_exercicios_novo (
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
    INSERT INTO progresso_exercicios_novo
        (id, usuario_id, idioma, modulo, item, tipo_exercicio, acertos, erros, ultima_pratica)
    SELECT
        id, usuario_id, idioma, modulo, item, tipo_exercicio, acertos, erros, ultima_pratica
    FROM progresso_exercicios
""")

c.execute("DROP TABLE progresso_exercicios")
c.execute("ALTER TABLE progresso_exercicios_novo RENAME TO progresso_exercicios")

# ==========================================
# 4. Recriar tabela 'streak' com PK composta
# ==========================================
print("  → Recriando tabela 'streak'...")

c.execute("""
    CREATE TABLE streak_novo (
        usuario_id TEXT NOT NULL DEFAULT 'default',
        data TEXT NOT NULL,
        revisoes INTEGER DEFAULT 0,
        PRIMARY KEY (usuario_id, data)
    )
""")

c.execute("""
    INSERT INTO streak_novo (usuario_id, data, revisoes)
    SELECT usuario_id, data, revisoes FROM streak
""")

c.execute("DROP TABLE streak")
c.execute("ALTER TABLE streak_novo RENAME TO streak")

conn.commit()
conn.close()

print()
print("✅ Migração concluída com sucesso!")