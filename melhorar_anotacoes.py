import sqlite3
from pathlib import Path
from config import DB_PATH

# ============================================================
# PARTE 1: Atualizar banco (adicionar categoria)
# ============================================================
print("Atualizando banco...")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("PRAGMA table_info(anotacoes)")
colunas = [row[1] for row in c.fetchall()]

if "categoria" not in colunas:
    c.execute("ALTER TABLE anotacoes ADD COLUMN categoria TEXT DEFAULT 'outros'")
    conn.commit()
    print("OK: coluna 'categoria' adicionada")
else:
    print("OK: coluna 'categoria' ja existe")

conn.close()

# ============================================================
# PARTE 2: Reescrever tela_anotacoes.py
# ============================================================
print()
print("Reescrevendo tela_anotacoes.py...")

conteudo = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_anotacoes import (
    criar_anotacao,
    atualizar_anotacao,
    excluir_anotacao,
    listar_anotacoes,
    obter_anotacao,
)
from logica.gerenciador_dados import listar_modulos_flat


# Categorias com icone + cor
CATEGORIAS = {
    "vocabulario": {"nome": "Vocabulario", "icone": "📖", "cor": "#34d399"},
    "gramatica":   {"nome": "Gramatica",   "icone": "🧠", "cor": "#60a5fa"},
    "frases":      {"nome": "Frases",      "icone": "✍️", "cor": "#a78bfa"},
    "metas":       {"nome": "Metas",       "icone": "🎯", "cor": "#ef4444"},
    "midia":       {"nome": "Musica/Filme","icone": "🎵", "cor": "#fbbf24"},
    "outros":      {"nome": "Outros",      "icone": "📌", "cor": "#a8b2c1"},
}


def render():
    idioma_atual = st.session_state.get("idioma") or "ingles"
    info = IDIOMAS.get(idioma_atual, {"bandeira": "🌍", "nome": "Geral"})

    if "anotacao_aberta" not in st.session_state:
        st.session_state.anotacao_aberta = None
    if "modo_nova_anotacao" not in st.session_state:
        st.session_state.modo_nova_anotacao = False

    # ============================================
    # HEADER
    # ============================================
    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_anotacoes"):
            voltar()
    with col_b:
        st.markdown(f"## 📝 Anotacoes · {info['bandeira']} {info['nome']}")

    st.markdown("---")

    # ============================================
    # LAYOUT 2 COLUNAS
    # ============================================
    col_lista, col_editor = st.columns([1, 2])

    # ============ COLUNA ESQUERDA: LISTA ============
    with col_lista:
        # Botao Nova
        if st.button("➕ Nova anotacao", use_container_width=True, type="primary", key="nova_anot"):
            st.session_state.modo_nova_anotacao = True
            st.session_state.anotacao_aberta = None
            st.rerun()

        st.markdown("")

        # Filtros
        busca = st.text_input("🔍 Buscar...", key="busca_anot", placeholder="Titulo ou conteudo")

        # Filtro por categoria
        categorias_disponiveis = ["todas"] + list(CATEGORIAS.keys())
        filtro_cat = st.selectbox(
            "📂 Categoria",
            categorias_disponiveis,
            format_func=lambda x: "📚 Todas" if x == "todas" else f"{CATEGORIAS[x]['icone']} {CATEGORIAS[x]['nome']}",
            key="filtro_cat_anot",
        )

        # Filtro por favoritas
        somente_fav = st.checkbox("⭐ So favoritas", key="fav_anot")

        st.markdown("---")

        # Busca
        cat_filtro = None if filtro_cat == "todas" else filtro_cat
        anotacoes = listar_anotacoes(
            idioma=None,
            somente_favoritas=somente_fav,
            busca=busca,
        )

        # Filtra por categoria (manual, porque a funcao nao suporta ainda)
        if cat_filtro:
            anotacoes = [a for a in anotacoes if a.get("categoria", "outros") == cat_filtro]

        # Contadores
        total = len(anotacoes)
        favoritas = sum(1 for a in anotacoes if a["favorita"])

        st.caption(f"📚 {total} anotacao(oes) · ⭐ {favoritas} favoritas")

        if not anotacoes:
            st.info("Nenhuma anotacao ainda. Cria a primeira! ✍️")
        else:
            for anot in anotacoes:
                esta_aberta = st.session_state.anotacao_aberta == anot["id"]
                fav = "⭐ " if anot["favorita"] else ""
                titulo = anot["titulo"] or "(sem titulo)"

                cat = anot.get("categoria", "outros")
                cat_info = CATEGORIAS.get(cat, CATEGORIAS["outros"])
                cor = cat_info["cor"]
                icone = cat_info["icone"]

                # Card com cor da categoria
                card_html = (
                    f'<div style="background: {cor}11; '
                    f'border-left: 4px solid {cor}; '
                    f'border-radius: 10px; padding: 12px 14px; '
                    f'margin-bottom: 8px;">'
                    f'<div style="font-size: 13px; color: {cor}; font-weight: 700;">'
                    f'{fav}{icone} {cat_info["nome"]}'
                    f'</div>'
                    f'<div style="font-size: 14px; color: #ffffff; margin-top: 4px; '
                    f'overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">'
                    f'{titulo[:40]}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                if st.button(
                    "Abrir" if not esta_aberta else "Aberta",
                    use_container_width=True,
                    key=f"abrir_anot_{anot['id']}",
                    type="primary" if esta_aberta else "secondary",
                ):
                    st.session_state.anotacao_aberta = anot["id"]
                    st.session_state.modo_nova_anotacao = False
                    st.rerun()

    # ============ COLUNA DIREITA: EDITOR ============
    with col_editor:
        if st.session_state.modo_nova_anotacao:
            render_nova_anotacao(idioma_atual)
        elif st.session_state.anotacao_aberta:
            render_editar_anotacao(idioma_atual)
        else:
            render_boas_vindas()


def render_boas_vindas():
    """Tela de boas-vindas com cards coloridos."""
    st.markdown("### 👋 Bem-vindo as suas anotacoes")
    st.markdown("Aqui voce guarda tudo que quer lembrar sobre seus estudos:")

    st.markdown("")

    # Cards coloridos das categorias
    cats_mostrar = [
        ("vocabulario", "Palavras novas que voce ouviu em musica/filme"),
        ("gramatica",   "Duvidas tipo qual a diferenca entre X e Y"),
        ("frases",      "Frases que voce escreveu e quer revisar"),
        ("metas",       "Metas e reflexoes sobre o aprendizado"),
    ]

    for cat_id, descricao in cats_mostrar:
        cat = CATEGORIAS[cat_id]
        st.markdown(
            f'<div style="background: {cat["cor"]}11; '
            f'border-left: 4px solid {cat["cor"]}; '
            f'border-radius: 12px; padding: 16px 20px; margin-bottom: 10px;">'
            f'<div style="font-size: 16px; font-weight: 700; color: {cat["cor"]};">'
            f'{cat["icone"]} {cat["nome"]}'
            f'</div>'
            f'<div style="font-size: 14px; color: #a8b2c1; margin-top: 4px;">{descricao}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📌 Como usar")

    st.markdown("""
    1. Clica em **➕ Nova anotacao** na coluna esquerda
    2. Escreve o titulo e o conteudo (Markdown funciona!)
    3. Escolhe uma **categoria** (pra organizar)
    4. Salva
    5. Aparece na lista da esquerda pra clicar e ver
    """)

    st.markdown("---")
    st.info("💡 **Dica:** voce pode escrever em **Markdown** — `**negrito**`, `*italico*`, `# titulo`, `- lista`, `> citacao`")


def render_nova_anotacao(idioma_atual):
    """Formulario de nova anotacao."""
    st.markdown("### ✍️ Nova anotacao")

    with st.form("form_nova_anotacao", clear_on_submit=False):
        titulo = st.text_input("📝 Titulo", placeholder="Ex: Diferenca entre make e do")

        col1, col2 = st.columns(2)
        with col1:
            idioma_anot = st.selectbox(
                "🌍 Idioma",
                ["ingles", "russo", "geral"],
                format_func=lambda x: {
                    "ingles": "🗽 Ingles",
                    "russo": "🐻 Russo",
                    "geral": "🌍 Geral",
                }[x],
            )
        with col2:
            categoria = st.selectbox(
                "📂 Categoria",
                list(CATEGORIAS.keys()),
                format_func=lambda x: f"{CATEGORIAS[x]['icone']} {CATEGORIAS[x]['nome']}",
            )

        modulo_vinculado = st.selectbox(
            "🔗 Vincular a modulo (opcional)",
            ["(nenhum)"] + [m["id"] for m in listar_modulos_flat(idioma_atual)],
            format_func=lambda x: "(nenhum)" if x == "(nenhum)" else next(
                (f"{m['icone']} {m['nome']}" for m in listar_modulos_flat(idioma_atual) if m["id"] == x),
                x,
            ),
        )

        favorita = st.checkbox("⭐ Marcar como favorita")

        conteudo = st.text_area(
            "📖 Conteudo",
            height=300,
            placeholder="Escreve aqui... Markdown funciona! **negrito**, *italico*, listas...",
        )

        col_salvar, col_cancelar = st.columns(2)
        with col_salvar:
            salvar = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col_cancelar:
            cancelar = st.form_submit_button("Cancelar", use_container_width=True)

        if salvar:
            if not titulo.strip() and not conteudo.strip():
                st.error("⚠️ Preenche pelo menos titulo ou conteudo!")
            else:
                mod_final = "" if modulo_vinculado == "(nenhum)" else modulo_vinculado
                novo_id = criar_anotacao(
                    idioma=idioma_anot,
                    titulo=titulo or "(sem titulo)",
                    conteudo=conteudo,
                    modulo=mod_final,
                    favorita=favorita,
                )

                # Salva a categoria manualmente
                import sqlite3
                from config import DB_PATH
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("UPDATE anotacoes SET categoria = ? WHERE id = ?", (categoria, novo_id))
                conn.commit()
                conn.close()

                st.session_state.modo_nova_anotacao = False
                st.session_state.anotacao_aberta = novo_id
                st.success("✅ Anotacao criada!")
                st.rerun()

        if cancelar:
            st.session_state.modo_nova_anotacao = False
            st.rerun()


def render_editar_anotacao(idioma_atual):
    """Visualiza / edita anotacao existente."""
    anot = obter_anotacao(st.session_state.anotacao_aberta)

    if not anot:
        st.error("Anotacao nao encontrada.")
        st.session_state.anotacao_aberta = None
        st.rerun()

    cat = anot.get("categoria", "outros")
    cat_info = CATEGORIAS.get(cat, CATEGORIAS["outros"])
    cor = cat_info["cor"]

    # Titulo com cor da categoria
    st.markdown(
        f'<h3 style="color: {cor};">{cat_info["icone"]} {anot["titulo"]}</h3>',
        unsafe_allow_html=True,
    )

    # Info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 Criada: {anot['criado_em'][:10]}")
    with col2:
        st.caption(f"✏️ Atualizada: {(anot['atualizado_em'] or anot['criado_em'])[:10]}")
    with col3:
        if anot["favorita"]:
            st.caption("⭐ Favorita")

    st.markdown("---")

    if "editando" not in st.session_state:
        st.session_state.editando = False

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        if st.button("✏️ Editar", use_container_width=True, key="btn_editar_anot"):
            st.session_state.editando = not st.session_state.editando
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Excluir", use_container_width=True, key="btn_excluir_anot"):
            excluir_anotacao(anot["id"])
            st.session_state.anotacao_aberta = None
            st.session_state.editando = False
            st.success("Anotacao excluida.")
            st.rerun()

    st.markdown("")

    if st.session_state.editando:
        with st.form("form_editar_anotacao"):
            novo_titulo = st.text_input("Titulo", value=anot["titulo"])
            novo_idioma = st.selectbox(
                "Idioma",
                ["ingles", "russo", "geral"],
                index=["ingles", "russo", "geral"].index(anot["idioma"] or "geral"),
                format_func=lambda x: {
                    "ingles": "🗽 Ingles",
                    "russo": "🐻 Russo",
                    "geral": "🌍 Geral",
                }[x],
            )
            novo_conteudo = st.text_area("Conteudo", value=anot["conteudo"], height=300)
            nova_fav = st.checkbox("⭐ Favorita", value=bool(anot["favorita"]))

            col_s, col_c = st.columns(2)
            with col_s:
                salvar = st.form_submit_button("💾 Salvar alteracoes", use_container_width=True, type="primary")
            with col_c:
                cancelar = st.form_submit_button("Cancelar", use_container_width=True)

            if salvar:
                atualizar_anotacao(
                    anot_id=anot["id"],
                    titulo=novo_titulo,
                    conteudo=novo_conteudo,
                    modulo=anot["modulo"] or "",
                    favorita=nova_fav,
                )
                st.session_state.editando = False
                st.success("✅ Salvo!")
                st.rerun()

            if cancelar:
                st.session_state.editando = False
                st.rerun()
    else:
        # Visualizacao com Markdown
        st.markdown(anot["conteudo"] or "_vazio_")
'''

caminho = Path(__file__).parent / "telas" / "tela_anotacoes.py"
caminho.write_text(conteudo, encoding="utf-8")
print("OK: tela_anotacoes.py reescrita")

print()
print("=" * 50)
print("Anotacoes melhoradas!")
print("Reinicie o Streamlit.")
print("=" * 50)