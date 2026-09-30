from pathlib import Path
import json

BASE = Path(__file__).parent

# ============================================================
# PARTE 1: Criar o modulo Alfabeto
# ============================================================
print("Criando modulo Alfabeto...")

alfabeto = [
    {"pt": "A (letra)", "en": "A", "pron": "êi"},
    {"pt": "B (letra)", "en": "B", "pron": "bí"},
    {"pt": "C (letra)", "en": "C", "pron": "sí"},
    {"pt": "D (letra)", "en": "D", "pron": "dí"},
    {"pt": "E (letra)", "en": "E", "pron": "í"},
    {"pt": "F (letra)", "en": "F", "pron": "éf"},
    {"pt": "G (letra)", "en": "G", "pron": "djí"},
    {"pt": "H (letra)", "en": "H", "pron": "êitch"},
    {"pt": "I (letra)", "en": "I", "pron": "ái"},
    {"pt": "J (letra)", "en": "J", "pron": "djêi"},
    {"pt": "K (letra)", "en": "K", "pron": "kêi"},
    {"pt": "L (letra)", "en": "L", "pron": "él"},
    {"pt": "M (letra)", "en": "M", "pron": "ém"},
    {"pt": "N (letra)", "en": "N", "pron": "én"},
    {"pt": "O (letra)", "en": "O", "pron": "ôu"},
    {"pt": "P (letra)", "en": "P", "pron": "pí"},
    {"pt": "Q (letra)", "en": "Q", "pron": "kiú"},
    {"pt": "R (letra)", "en": "R", "pron": "ár"},
    {"pt": "S (letra)", "en": "S", "pron": "és"},
    {"pt": "T (letra)", "en": "T", "pron": "tí"},
    {"pt": "U (letra)", "en": "U", "pron": "iú"},
    {"pt": "V (letra)", "en": "V", "pron": "ví"},
    {"pt": "W (letra)", "en": "W", "pron": "dábliu"},
    {"pt": "X (letra)", "en": "X", "pron": "éks"},
    {"pt": "Y (letra)", "en": "Y", "pron": "uái"},
    {"pt": "Z (letra)", "en": "Z", "pron": "zí"},

    # Bonus: como soletrar palavras
    {"pt": "Como soletrar 'hello'", "en": "H-E-L-L-O", "pron": "eitch-i-él-él-ôu"},
    {"pt": "Como soletrar 'name'",  "en": "N-A-M-E",   "pron": "en-êi-em-í"},
    {"pt": "Como soletrar 'Brazil'","en": "B-R-A-Z-I-L","pron": "bí-ár-êi-zí-ái-él"},
    {"pt": "Como soletrar 'English'","en": "E-N-G-L-I-S-H","pron": "í-en-djí-él-ái-és-eitch"},
]

caminho_alfabeto = BASE / "dados" / "ingles" / "alfabeto.json"
caminho_alfabeto.write_text(
    json.dumps(alfabeto, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"OK: {caminho_alfabeto} ({len(alfabeto)} itens)")

# ============================================================
# PARTE 2: Adicionar Alfabeto no modulos.json
# ============================================================
print()
print("Adicionando Alfabeto no modulos.json...")

caminho_modulos = BASE / "dados" / "ingles" / "modulos.json"
with open(caminho_modulos, "r", encoding="utf-8") as f:
    modulos = json.load(f)

# Procura o nivel iniciante
for nivel in modulos.get("niveis", []):
    if nivel["id"] == "iniciante":
        # Verifica se ja tem alfabeto
        ids_existentes = [m["id"] for m in nivel["modulos"]]
        if "alfabeto" not in ids_existentes:
            nivel["modulos"].append({
                "id": "alfabeto",
                "nome": "Alfabeto",
                "icone": "🔤"
            })
            print("OK: Alfabeto adicionado no nivel Iniciante")
        else:
            print("OK: Alfabeto ja existia")
        break

with open(caminho_modulos, "w", encoding="utf-8") as f:
    json.dump(modulos, f, ensure_ascii=False, indent=2)

print(f"OK: {caminho_modulos} atualizado")

# ============================================================
# PARTE 3: Melhorar abas do Dicionario
# ============================================================
print()
print("Melhorando abas do Dicionario...")

conteudo_tela = '''import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dicionario import (
    buscar_palavra,
    listar_palavras_por_letra,
    contar_por_letra,
    estatisticas_gerais,
)
from logica.gerenciador_audio import gerar_audio


ALFABETO = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def render():
    idioma_atual = st.session_state.get("idioma") or "ingles"
    info = IDIOMAS.get(idioma_atual, {"bandeira": "?", "nome": "?"})

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_dic"):
            voltar()
    with col_b:
        st.markdown(f"## Dicionario - {info['bandeira']} {info['nome']}")

    st.markdown("---")

    # Inicializa a aba
    if "dic_aba" not in st.session_state:
        st.session_state.dic_aba = "busca"

    # Abas em caixas
    abas = [
        ("busca",       "🔍", "Busca",        "#34d399"),
        ("abecedario",  "🔤", "Abecedario",   "#60a5fa"),
        ("estatisticas","📊", "Estatisticas", "#fbbf24"),
    ]

    cols = st.columns(3)
    for col, (aba_id, icone, nome, cor) in zip(cols, abas):
        with col:
            ativo = st.session_state.dic_aba == aba_id
            border_cor = cor if ativo else "#2d3748"
            bg_cor = f"{cor}22" if ativo else "#1a2332"

            st.markdown(
                f'<div style="background: {bg_cor}; '
                f'border: 2px solid {border_cor}; '
                f'border-radius: 14px; padding: 14px 8px; text-align: center; '
                f'margin-bottom: 8px;">'
                f'<div style="font-size: 28px; line-height: 1;">{icone}</div>'
                f'<div style="font-size: 14px; font-weight: 700; color: {cor}; margin-top: 6px;">{nome}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            if st.button(
                "Ativo" if ativo else "Abrir",
                use_container_width=True,
                key=f"aba_{aba_id}",
                type="primary" if ativo else "secondary",
            ):
                if not ativo:
                    st.session_state.dic_aba = aba_id
                    st.rerun()

    st.markdown("---")

    # Renderiza a aba ativa
    aba = st.session_state.dic_aba
    if aba == "busca":
        render_busca(idioma_atual)
    elif aba == "abecedario":
        render_abecedario(idioma_atual)
    else:
        render_estatisticas(idioma_atual)


def render_busca(idioma_atual):
    termo = st.text_input(
        "Buscar",
        placeholder="Digite em portugues ou ingles...",
        key="dic_busca",
        label_visibility="collapsed",
    )

    if not termo or len(termo) < 2:
        st.info("Digite pelo menos 2 caracteres. Funciona em portugues e ingles.")
        return

    resultados = buscar_palavra(idioma_atual, termo)

    if not resultados:
        st.warning(f"Nenhum resultado para {termo}")
        return

    st.success(f"{len(resultados)} resultado(s)")

    for item in resultados:
        render_card_palavra(item, idioma_atual)


def render_abecedario(idioma_atual):
    col_radio = st.columns([2])[0]
    with col_radio:
        campo_busca = st.radio(
            "Buscar por:",
            ["Portugues", "Ingles"],
            horizontal=True,
            key="dic_campo_abc",
        )

    campo = "pt" if campo_busca == "Portugues" else "estrangeiro"
    contagem = contar_por_letra(idioma_atual, campo=campo)

    if "dic_letra_sel" not in st.session_state:
        st.session_state.dic_letra_sel = "A"

    st.markdown("#### Escolha uma letra:")

    linha1 = st.columns(13)
    linha2 = st.columns(13)

    for i, letra in enumerate(ALFABETO):
        col = linha1[i] if i < 13 else linha2[i - 13]
        with col:
            total = contagem.get(letra, 0)
            ativo = st.session_state.dic_letra_sel == letra
            tipo = "primary" if ativo else "secondary"

            if st.button(
                letra,
                key=f"dic_letra_{letra}",
                use_container_width=True,
                type=tipo,
                disabled=(total == 0),
            ):
                st.session_state.dic_letra_sel = letra
                st.rerun()

    st.markdown("---")

    letra = st.session_state.dic_letra_sel
    palavras = listar_palavras_por_letra(idioma_atual, letra, campo=campo)

    st.markdown(f"### Letra {letra} - {len(palavras)} palavra(s)")

    if not palavras:
        st.info(f"Nenhuma palavra comecando com {letra}.")
    else:
        for item in palavras:
            render_card_palavra(item, idioma_atual)


def render_estatisticas(idioma_atual):
    stats = estatisticas_gerais(idioma_atual)
    total_fmt = f"{stats['total']:,}".replace(",", ".")

    st.markdown(
        f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        f'border: 2px solid #34d39933; border-radius: 18px; padding: 24px; '
        f'text-align: center; margin-bottom: 24px;">'
        f'<div style="font-size: 42px; font-weight: 800; color: #34d399;">{total_fmt}</div>'
        f'<div style="font-size: 13px; color: #a8b2c1; text-transform: uppercase; '
        f'letter-spacing: 2px; margin-top: 4px;">palavras disponiveis</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Por nivel")
    for nivel, dados in stats["por_nivel"].items():
        st.markdown(
            f'<div style="background: {dados["cor"]}11; '
            f'border-left: 4px solid {dados["cor"]}; '
            f'border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; '
            f'display: flex; justify-content: space-between;">'
            f'<span style="color: {dados["cor"]}; font-weight: 700;">'
            f'{dados["icone"]} {nivel}</span>'
            f'<span style="color: #ffffff; font-weight: 700;">{dados["total"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Top 10 modulos")

    for i, mod in enumerate(stats["por_modulo"][:10]):
        st.markdown(
            f'<div style="background: #1a2332; '
            f'border-left: 4px solid {mod["nivel_cor"]}; '
            f'border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; '
            f'display: flex; justify-content: space-between; align-items: center;">'
            f'<span style="color: #ffffff;">'
            f'<b>{i+1}.</b> {mod["icone"]} {mod["nome"]}'
            f'</span>'
            f'<span style="color: {mod["nivel_cor"]}; font-weight: 700;">{mod["total"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_card_palavra(item, idioma):
    codigo = "en" if idioma == "ingles" else "ru"
    info = IDIOMAS[idioma]

    traducao = item.get(codigo, "?")
    pron = item.get("pron", "")
    pt = item.get("pt", "?")
    modulo = item.get("_modulo", "")
    icone = item.get("_icone", "?")
    nivel = item.get("_nivel", "")
    nivel_cor = item.get("_nivel_cor", "#34d399")

    if pron:
        bloco_pron = (
            f'<div style="background: rgba(96, 165, 250, 0.15); '
            f'border: 2px solid #60a5fa; border-radius: 10px; '
            f'padding: 6px 14px; margin-top: 8px; display: inline-block;">'
            f'<span style="font-size: 16px; color: #60a5fa; font-weight: 700;">'
            f'{pron}</span></div>'
        )
    else:
        bloco_pron = ""

    card_html = (
        f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        f'border: 1px solid #2d3748; border-left: 5px solid {nivel_cor}; '
        f'border-radius: 14px; padding: 20px; margin-bottom: 10px;">'
        f'<div style="display: flex; justify-content: space-between; align-items: center;">'
        f'<div style="flex: 1;">'
        f'<div style="font-size: 11px; color: #a8b2c1; text-transform: uppercase; '
        f'letter-spacing: 2px;">PT Portugues</div>'
        f'<div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">{pt}</div>'
        f'</div>'
        f'<div style="color: #a8b2c1; font-size: 24px; margin: 0 20px;">-></div>'
        f'<div style="flex: 1; text-align: right;">'
        f'<div style="font-size: 11px; color: #a8b2c1; text-transform: uppercase; '
        f'letter-spacing: 2px;">{info["bandeira"]} {info["nome"]}</div>'
        f'<div style="font-size: 22px; font-weight: 800; color: {nivel_cor}; margin-top: 4px;">{traducao}</div>'
        f'</div>'
        f'</div>'
        f'{bloco_pron}'
        f'<div style="margin-top: 12px; font-size: 12px; color: #a8b2c1;">'
        f'{icone} {modulo} - {nivel}'
        f'</div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

    try:
        audio_bytes = gerar_audio(traducao, codigo)
        st.audio(audio_bytes, format="audio/mp3")
    except Exception:
        pass
'''

caminho_tela = BASE / "telas" / "tela_dicionario.py"
caminho_tela.write_text(conteudo_tela, encoding="utf-8")
print(f"OK: {caminho_tela} atualizada")

print()
print("=" * 50)
print("Tudo pronto!")
print()
print("1. Alfabeto criado como novo modulo")
print("2. Abas do Dicionario em caixas")
print()
print("Reinicie o Streamlit.")
print("=" * 50)