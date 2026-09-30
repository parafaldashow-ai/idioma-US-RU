"""
Script que cria TODA a estrutura do app e cola o conteúdo nos arquivos.
Roda uma vez só.
"""
import os
import json
from pathlib import Path

BASE = Path(__file__).parent

# ============ ESTRUTURA DE PASTAS ============
pastas = [
    "assets/images",
    "dados/ingles",
    "dados/russo",
    "telas",
    "componentes",
    "logica",
    "banco",
]
for p in pastas:
    (BASE / p).mkdir(parents=True, exist_ok=True)

# ============ ARQUIVOS PYTHON ============
arquivos = {}

arquivos["main.py"] = '''import streamlit as st
from logica.navegacao import init_estado, renderizar_tela_atual
from logica.gerenciador_progresso import init_db

st.set_page_config(
    page_title="Lingua App",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()
init_estado()
renderizar_tela_atual()
'''

arquivos["logica/__init__.py"] = ""
arquivos["telas/__init__.py"] = ""
arquivos["componentes/__init__.py"] = ""

arquivos["logica/gerenciador_progresso.py"] = '''import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS progresso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT NOT NULL,
            modulo TEXT NOT NULL,
            item TEXT NOT NULL,
            acertos INTEGER DEFAULT 0,
            erros INTEGER DEFAULT 0,
            dominado INTEGER DEFAULT 0,
            ultima_revisao TEXT,
            UNIQUE(idioma, modulo, item)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS anotacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idioma TEXT,
            titulo TEXT,
            conteudo TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            data TEXT PRIMARY KEY,
            revisoes INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def registrar(idioma, modulo, item, acertou: bool):
    from datetime import datetime
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    agora = datetime.now().isoformat()
    c.execute("""
        INSERT INTO progresso (idioma, modulo, item, acertos, erros, ultima_revisao)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(idioma, modulo, item) DO UPDATE SET
            acertos = acertos + ?,
            erros = erros + ?,
            ultima_revisao = ?,
            dominado = CASE WHEN acertos + ? >= 3 THEN 1 ELSE dominado END
    """, (
        idioma, modulo, item,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
        1 if acertou else 0,
        0 if acertou else 1,
        agora,
        1 if acertou else 0,
    ))
    hoje = agora[:10]
    c.execute("""
        INSERT INTO streak (data, revisoes) VALUES (?, 1)
        ON CONFLICT(data) DO UPDATE SET revisoes = revisoes + 1
    """, (hoje,))
    conn.commit()
    conn.close()

def progresso_modulo(idioma, modulo):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM progresso WHERE idioma=? AND modulo=?", (idioma, modulo))
    linhas = [dict(r) for r in c.fetchall()]
    conn.close()
    return linhas

def resumo_geral(idioma):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(dominado) FROM progresso WHERE idioma=?", (idioma,))
    total, dominados = c.fetchone()
    conn.close()
    return {"total_estudado": total or 0, "dominados": dominados or 0}

def streak_atual():
    from datetime import date, timedelta
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM streak ORDER BY data DESC")
    datas = [r[0] for r in c.fetchall()]
    conn.close()
    if not datas:
        return 0
    hoje = date.today()
    streak = 0
    dia = hoje
    for d in datas:
        if d == dia.isoformat():
            streak += 1
            dia -= timedelta(days=1)
        elif d < dia.isoformat():
            break
    return streak
'''

arquivos["logica/gerenciador_dados.py"] = '''import json
from config import DADOS_DIR

def carregar_indice_modulos(idioma: str):
    caminho = DADOS_DIR / idioma / "modulos.json"
    if not caminho.exists():
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_modulo(idioma: str, modulo_id: str):
    caminho = DADOS_DIR / idioma / f"{modulo_id}.json"
    if not caminho.exists():
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def listar_todos_vocabulos(idioma: str):
    tudo = []
    for mod in carregar_indice_modulos(idioma):
        itens = carregar_modulo(idioma, mod["id"])
        for item in itens:
            item["_modulo"] = mod["nome"]
            tudo.append(item)
    return tudo

def buscar_palavra(idioma: str, termo: str):
    termo = termo.lower().strip()
    if not termo:
        return []
    resultados = []
    for item in listar_todos_vocabulos(idioma):
        pt = item.get("pt", "").lower()
        estrangeiro = item.get(idioma, "").lower()
        if termo in pt or termo in estrangeiro:
            resultados.append(item)
    return resultados
'''

arquivos["logica/gerenciador_audio.py"] = '''import io
import hashlib
from pathlib import Path
from gtts import gTTS
from config import ASSETS_DIR

AUDIO_CACHE = ASSETS_DIR / "audio_cache"
AUDIO_CACHE.mkdir(parents=True, exist_ok=True)

def gerar_audio(texto: str, idioma_codigo: str) -> bytes:
    chave = hashlib.md5(f"{idioma_codigo}:{texto}".encode("utf-8")).hexdigest()
    arquivo = AUDIO_CACHE / f"{chave}.mp3"
    if arquivo.exists():
        return arquivo.read_bytes()
    tts = gTTS(text=texto, lang=idioma_codigo, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    dados = buf.getvalue()
    arquivo.write_bytes(dados)
    return dados
'''

arquivos["logica/navegacao.py"] = '''import streamlit as st
import importlib

TELAS = {
    "inicio":     "telas.tela_inicial",
    "menu":       "telas.tela_menu_idioma",
    "modulos":    "telas.tela_modulos",
    "modulo":     "telas.tela_modulo",
    "flashcards": "telas.tela_flashcards",
    "exercicio":  "telas.tela_exercicio",
    "dicionario": "telas.tela_dicionario",
    "progresso":  "telas.tela_progresso",
    "anotacoes":  "telas.tela_anotacoes",
    "config":     "telas.tela_config",
}

def init_estado():
    if "tela" not in st.session_state:
        st.session_state.tela = "inicio"
    if "idioma" not in st.session_state:
        st.session_state.idioma = None
    if "modulo_atual" not in st.session_state:
        st.session_state.modulo_atual = None

def ir_para(tela: str):
    if tela not in TELAS:
        st.error(f"Tela desconhecida: {tela}")
        return
    st.session_state.tela = tela
    st.rerun()

def renderizar_tela_atual():
    tela = st.session_state.tela
    modulo_path = TELAS.get(tela, "telas.tela_inicial")
    mod = importlib.import_module(modulo_path)
    mod.render()
'''

arquivos["telas/tela_inicial.py"] = '''import streamlit as st
from config import IDIOMAS, CORES
from logica.navegacao import ir_para

def render():
    st.markdown(f"""
    <style>
    .card-idioma {{
        background: linear-gradient(135deg, {CORES['card_bg']}, #2a2a3e);
        border: 2px solid {CORES['card_border']};
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
    }}
    .bandeira {{ font-size: 72px; line-height: 1; }}
    .titulo-idioma {{ font-size: 28px; font-weight: bold; color: {CORES['texto']}; margin-top: 16px; }}
    .subtitulo-idioma {{ font-size: 16px; color: {CORES['texto_sub']}; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("# 🌍 Lingua App")
    st.markdown("#### Aprenda ingles e russo do seu jeito")
    st.markdown("")
    st.markdown("### Qual idioma voce quer estudar?")
    st.markdown("")

    col1, col2 = st.columns(2)
    for col, (codigo, info) in zip([col1, col2], IDIOMAS.items()):
        with col:
            st.markdown(f"""
            <div class="card-idioma">
                <div class="bandeira">{info['bandeira']} {info.get('bandeira_alt', '')}</div>
                <div class="titulo-idioma">{info['nome'].upper()}</div>
                <div class="subtitulo-idioma">{info['nome_nativo']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Estudar {info['nome']}", key=f"btn_{codigo}", use_container_width=True):
                st.session_state.idioma = codigo
                ir_para("menu")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 Meu Progresso", use_container_width=True):
            ir_para("progresso")
    with c2:
        if st.button("⚙️ Configuracoes", use_container_width=True):
            ir_para("config")
'''

arquivos["telas/tela_menu_idioma.py"] = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para

def render():
    idioma = st.session_state.idioma
    if not idioma:
        ir_para("inicio")
        return
    info = IDIOMAS[idioma]
    st.markdown(f"## {info['bandeira']} {info['nome'].upper()}")
    st.markdown("---")
    opcoes = [
        ("📖", "Modulos",     "modulos"),
        ("✏️", "Exercicios",  "exercicio"),
        ("🎴", "Flashcards",  "flashcards"),
        ("🔍", "Dicionario",  "dicionario"),
        ("📊", "Progresso",   "progresso"),
        ("📝", "Anotacoes",   "anotacoes"),
    ]
    for i in range(0, len(opcoes), 2):
        cols = st.columns(2)
        for col, (icone, nome, tela) in zip(cols, opcoes[i:i+2]):
            with col:
                if st.button(f"{icone}  {nome}", use_container_width=True, key=f"menu_{tela}"):
                    ir_para(tela)
    st.markdown("---")
    if st.button("<- Voltar", use_container_width=True):
        ir_para("inicio")
'''

arquivos["telas/tela_modulos.py"] = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para
from logica.gerenciador_dados import carregar_indice_modulos, carregar_modulo
from logica.gerenciador_progresso import progresso_modulo

def render():
    idioma = st.session_state.idioma
    info = IDIOMAS[idioma]
    st.markdown(f"## 📖 Modulos · {info['bandeira']} {info['nome']}")
    if st.button("<- Voltar"):
        ir_para("menu")
    st.markdown("---")
    modulos = carregar_indice_modulos(idioma)
    if not modulos:
        st.warning("Nenhum modulo encontrado.")
        return
    for i in range(0, len(modulos), 3):
        cols = st.columns(3)
        for col, mod in zip(cols, modulos[i:i+3]):
            with col:
                itens = carregar_modulo(idioma, mod["id"])
                prog = progresso_modulo(idioma, mod["id"])
                dominados = sum(1 for p in prog if p["dominado"])
                total = len(itens)
                pct = int((dominados / total * 100) if total else 0)
                st.markdown(f"""
                <div style="background: #1e1e2e; border: 1px solid #333; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 8px;">
                    <div style="font-size: 40px;">{mod['icone']}</div>
                    <div style="font-size: 16px; font-weight: bold; color: #fafafa; margin: 8px 0;">{mod['nome']}</div>
                    <div style="font-size: 12px; color: #888;">{dominados}/{total} · {pct}%</div>
                    <div style="height: 6px; background: #333; border-radius: 3px; margin-top: 8px; overflow: hidden;">
                        <div style="width: {pct}%; height: 100%; background: #4ade80;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Abrir", key=f"abrir_{mod['id']}", use_container_width=True):
                    st.session_state.modulo_atual = mod["id"]
                    st.session_state.idx_modulo = 0
                    st.session_state.mostrar = False
                    ir_para("modulo")
'''

arquivos["telas/tela_modulo.py"] = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para
from logica.gerenciador_dados import carregar_modulo, carregar_indice_modulos
from logica.gerenciador_progresso import registrar
from logica.gerenciador_audio import gerar_audio

def render():
    idioma = st.session_state.idioma
    modulo_id = st.session_state.modulo_atual
    info = IDIOMAS[idioma]
    if not modulo_id:
        ir_para("modulos")
        return
    modulos = carregar_indice_modulos(idioma)
    nome_modulo = next((m["nome"] for m in modulos if m["id"] == modulo_id), modulo_id)
    itens = carregar_modulo(idioma, modulo_id)
    st.markdown(f"## 📖 {nome_modulo}")
    if st.button("<- Voltar"):
        ir_para("modulos")
    if not itens:
        st.warning("Modulo vazio.")
        return
    if "idx_modulo" not in st.session_state:
        st.session_state.idx_modulo = 0
    if st.session_state.idx_modulo >= len(itens):
        st.session_state.idx_modulo = 0
    item = itens[st.session_state.idx_modulo]
    st.progress((st.session_state.idx_modulo + 1) / len(itens))
    st.caption(f"{st.session_state.idx_modulo + 1} de {len(itens)}")
    mostrar = st.session_state.get("mostrar", False)
    st.markdown(f"""
    <div style="background: #1e1e2e; border-radius: 20px; padding: 40px; text-align: center; margin: 20px 0;">
        <div style="color: #888; font-size: 14px;">Portugues</div>
        <div style="font-size: 36px; font-weight: bold; color: #fafafa; margin: 12px 0;">{item['pt']}</div>
        <div style="color: #888; font-size: 14px;">{info['bandeira']} {info['nome']}</div>
        <div style="font-size: 32px; margin-top: 12px; color: {'#4ade80' if mostrar else 'transparent'};">
            {item[idioma] if mostrar else '•••••'}
        </div>
        <div style="font-size: 18px; color: #60a5fa; font-style: italic; margin-top: 8px;">
            {item.get('pron', '') if mostrar else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if not mostrar:
            if st.button("👁️ Mostrar", use_container_width=True, type="primary"):
                st.session_state.mostrar = True
                st.rerun()
        else:
            try:
                audio = gerar_audio(item[idioma], info["codigo_audio"])
                st.audio(audio, format="audio/mp3")
            except Exception as e:
                st.caption(f"Audio indisponivel: {e}")
    with col2:
        if mostrar:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("OK", use_container_width=True):
                    registrar(idioma, modulo_id, item["pt"], True)
                    st.session_state.idx_modulo = (st.session_state.idx_modulo + 1) % len(itens)
                    st.session_state.mostrar = False
                    st.rerun()
            with c2:
                if st.button("X", use_container_width=True):
                    registrar(idioma, modulo_id, item["pt"], False)
                    st.session_state.idx_modulo = (st.session_state.idx_modulo + 1) % len(itens)
                    st.session_state.mostrar = False
                    st.rerun()
'''

for tela in ["flashcards", "exercicio", "dicionario", "progresso", "anotacoes", "config"]:
    arquivos[f"telas/tela_{tela}.py"] = f'''import streamlit as st
from logica.navegacao import ir_para

def render():
    st.markdown("## {tela.title()}")
    st.info("Em construcao 🚧")
    if st.button("<- Voltar"):
        ir_para("menu" if st.session_state.get("idioma") else "inicio")
'''

# ============ JSONs ============
json_ingles_modulos = [
    {"id": "saudacoes", "nome": "Saudacoes", "icone": "👋"},
    {"id": "numeros", "nome": "Numeros", "icone": "🔢"},
    {"id": "cores", "nome": "Cores", "icone": "🎨"},
    {"id": "familia", "nome": "Familia", "icone": "👨‍👩‍👧"},
    {"id": "comida", "nome": "Comida", "icone": "🍞"},
    {"id": "profissoes", "nome": "Profissoes", "icone": "💼"},
    {"id": "emergencias", "nome": "Emergencias", "icone": "🚨"},
]

json_russo_modulos = [
    {"id": "saudacoes", "nome": "Saudacoes", "icone": "👋"},
    {"id": "numeros", "nome": "Numeros", "icone": "🔢"},
    {"id": "cores", "nome": "Cores", "icone": "🎨"},
    {"id": "familia", "nome": "Familia", "icone": "👨‍👩‍👧"},
    {"id": "comida", "nome": "Comida", "icone": "🍞"},
    {"id": "profissoes", "nome": "Profissoes", "icone": "💼"},
    {"id": "emergencias", "nome": "Emergencias", "icone": "🚨"},
]

# ============ ESCREVER TUDO ============
for caminho, conteudo in arquivos.items():
    p = BASE / caminho
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8")
    print(f"OK: {caminho}")

# JSONs de modulos (só se não existirem)
for idioma, dados in [("ingles", json_ingles_modulos), ("russo", json_russo_modulos)]:
    p = BASE / "dados" / idioma / "modulos.json"
    if not p.exists():
        p.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"OK: dados/{idioma}/modulos.json")
    else:
        print(f"JA EXISTE: dados/{idioma}/modulos.json (nao sobrescrevi)")

print()
print("=" * 50)
print("Estrutura criada com sucesso!")
print("Agora roda: streamlit run main.py")
print("=" * 50)