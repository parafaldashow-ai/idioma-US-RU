import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_dados import carregar_indice_modulos, carregar_modulo
from logica.gerenciador_progresso import contar_visualizacoes_modulo


def render():
    idioma = st.session_state.idioma
    info = IDIOMAS[idioma]

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_modulos"):
            voltar()
    with col_b:
        st.markdown(f"## 📖 Modulos · {info['bandeira']} {info['nome']}")

    st.markdown("---")

    indice = carregar_indice_modulos(idioma)
    niveis = indice.get("niveis", [])

    if not niveis:
        st.warning("Nenhum modulo encontrado.")
        return

    for nivel in niveis:
        st.markdown(
            f'<div style="'
            f'background: linear-gradient(90deg, {nivel["cor"]}22, transparent); '
            f'border-left: 5px solid {nivel["cor"]}; '
            f'padding: 16px 20px; '
            f'border-radius: 10px; '
            f'margin: 32px 0 20px 0; '
            f'box-shadow: 0 4px 16px rgba(0,0,0,0.2);">'
            f'<div style="font-size: 24px; font-weight: 800; color: {nivel["cor"]}; letter-spacing: 1px;">'
            f'{nivel["icone"]} {nivel["nome"].upper()}'
            f'</div>'
            f'<div style="font-size: 14px; color: #a8b2c1; margin-top: 4px;">{nivel.get("descricao", "")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        modulos = nivel.get("modulos", [])

        for i in range(0, len(modulos), 3):
            cols = st.columns(3)
            for col, mod in zip(cols, modulos[i:i+3]):
                with col:
                    itens = carregar_modulo(idioma, mod["id"])
                    total = len(itens)

                    # Usa VISUALIZACOES em vez de dominados
                    vistos = contar_visualizacoes_modulo(idioma, mod["id"])
                    pct = int((vistos / total * 100) if total else 0)

                    if total == 0:
                        contador = "vazio"
                        cor_contador = "#666"
                    else:
                        contador = f"👁️ {vistos}/{total} · {pct}%"
                        cor_contador = "#a8b2c1"

                    card_html = (
                        f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                        f'border: 2px solid {nivel["cor"]}33; '
                        f'border-radius: 18px; padding: 28px 20px; text-align: center; '
                        f'margin-bottom: 12px; min-height: 180px; '
                        f'box-shadow: 0 4px 16px rgba(0,0,0,0.2);">'
                        f'<div style="font-size: 48px; line-height: 1;">{mod["icone"]}</div>'
                        f'<div style="font-size: 17px; font-weight: 700; color: #ffffff; margin: 12px 0;">{mod["nome"]}</div>'
                        f'<div style="font-size: 13px; color: {cor_contador};">{contador}</div>'
                        f'<div style="height: 8px; background: #0f1419; border-radius: 4px; margin-top: 12px; overflow: hidden;">'
                        f'<div style="width: {pct}%; height: 100%; background: {nivel["cor"]}; transition: width 0.5s ease;"></div>'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

                    if st.button(
                        "📖 Abrir",
                        key=f'abrir_{mod["id"]}',
                        use_container_width=True,
                        disabled=(total == 0),
                    ):
                        st.session_state.modulo_atual = mod["id"]
                        st.session_state.idx_modulo = 0
                        ir_para("modulo")

    st.stop()
