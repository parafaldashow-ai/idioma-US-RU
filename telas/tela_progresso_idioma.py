import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_progresso import (
    estatisticas_idioma,
    estatisticas_por_nivel,
    top_modulos,
    palavras_mais_erradas,
    dias_estudados,
)


def render():
    idioma = st.session_state.get("idioma_progresso")
    if not idioma:
        ir_para("progresso")
        return

    info = IDIOMAS[idioma]

    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_prog_idioma"):
            voltar()
    with col_b:
        st.markdown(f"## 📊 Progresso · {info['bandeira']} {info['nome']}")

    st.markdown("---")

    # RESUMO
    stats = estatisticas_idioma(idioma)
    dominadas = stats["dominadas"]
    em_andamento = stats["em_andamento"]
    total = stats["total_disponivel"]
    pct = int((dominadas / total * 100) if total else 0)

    # Card principal de dominadas
    card_dominadas = (
        '<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        'border: 2px solid #34d39933; border-radius: 22px; padding: 36px; '
        'text-align: center; margin-bottom: 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">'
        '<div style="font-size: 64px; font-weight: 800; color: #34d399;">'
        f'{dominadas}'
        '</div>'
        '<div style="font-size: 16px; color: #a8b2c1; text-transform: uppercase; letter-spacing: 2px; margin-top: 8px;">'
        'dominadas'
        '</div>'
        f'<div style="font-size: 14px; color: #a8b2c1; margin-top: 12px;">de {total:,} palavras</div>'.replace(",", ".")
        +
        '<div style="height: 12px; background: #0f1419; border-radius: 6px; overflow: hidden; margin-top: 20px;">'
        f'<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #34d399, #60a5fa);"></div>'
        '</div>'
        f'<div style="text-align: right; font-size: 16px; color: #34d399; font-weight: 800; margin-top: 8px;">{pct}%</div>'
        '</div>'
    )
    st.markdown(card_dominadas, unsafe_allow_html=True)

    # Metricas extras
    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔥 Em andamento", em_andamento)
    with c2:
        st.metric("📚 Total disponivel", total)

    st.markdown("---")

    # PROGRESSO POR NIVEL
    st.markdown("### 🎯 Progresso por nivel")

    niveis = estatisticas_por_nivel(idioma)

    for nivel in niveis:
        pct_n = nivel["pct"]
        cor = nivel["cor"]

        html_nivel = (
            f'<div style="background: #1a2332; border-left: 4px solid {cor}; '
            'border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;">'
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
            f'<div style="font-size: 16px; font-weight: bold; color: #ffffff;">{nivel["icone"]} {nivel["nome"]}</div>'
            f'<div style="font-size: 14px; color: #a8b2c1;"><b style="color: {cor};">{nivel["dominadas"]}</b> / {nivel["total"]} · <b>{pct_n}%</b></div>'
            '</div>'
            '<div style="height: 8px; background: #0f1419; border-radius: 4px; overflow: hidden;">'
            f'<div style="width: {pct_n}%; height: 100%; background: {cor};"></div>'
            '</div>'
            '</div>'
        )
        st.markdown(html_nivel, unsafe_allow_html=True)

    st.markdown("---")

    # TOP MODULOS
    st.markdown("### 🏆 Top 5 modulos mais estudados")

    tops = top_modulos(idioma, limite=5)

    if not tops:
        st.info("Voce ainda nao estudou nenhum modulo desse idioma.")
    else:
        for i, mod in enumerate(tops, 1):
            medalha = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i - 1]

            col_num, col_info, col_pct = st.columns([1, 4, 2])
            with col_num:
                st.markdown(f"### {medalha}")
            with col_info:
                st.markdown(f"**{mod['icone']} {mod['nome']}**")
                st.caption(f"{mod['dominadas']} dominadas · {mod['estudadas']} estudadas")
            with col_pct:
                st.markdown(f"<div style='text-align: right;'><b style='color: #34d399;'>{mod['pct']}%</b></div>", unsafe_allow_html=True)

    st.markdown("---")

    # CALENDARIO
    st.markdown("### 📅 Ultimos 30 dias")

    dias = dias_estudados(ultimos_dias=30)
    total_estudados = sum(1 for d in dias if d["estudou"])

    st.caption(f"Voce estudou **{total_estudados} de 30 dias** ({int(total_estudados/30*100)}%)")

    html_cal = '<div style="display: grid; grid-template-columns: repeat(10, 1fr); gap: 6px; max-width: 500px;">'
    for d in dias:
        if d["estudou"]:
            cor = "#34d399"
            title = f"{d['data']} · {d['revisoes']} revisoes"
        else:
            cor = "#2d3748"
            title = f"{d['data']} · nao estudou"

        html_cal += f'<div title="{title}" style="aspect-ratio: 1; background: {cor}; border-radius: 4px;"></div>'

    html_cal += '</div>'
    st.markdown(html_cal, unsafe_allow_html=True)

    st.caption("🟢 Verde = estudou · ⚫ Cinza = nao estudou")

    st.markdown("---")

    # PALAVRAS MAIS ERRADAS
    st.markdown("### ❌ Palavras que voce mais erra")

    erradas = palavras_mais_erradas(idioma, limite=10)

    if not erradas:
        st.success("🎉 Voce nao tem erros registrados! Continue assim.")
    else:
        for i, palavra in enumerate(erradas, 1):
            col_pt, col_trad, col_stats = st.columns([2, 2, 1])
            with col_pt:
                st.markdown(f"**{i}. {palavra['pt']}**")
            with col_trad:
                st.markdown(f"→ **{palavra['traducao']}**")
                if palavra["pron"]:
                    st.caption(f"_{palavra['pron']}_")
            with col_stats:
                st.markdown(f"<div style='text-align: right;'><span style='color: #ef4444;'>❌ {palavra['erros']}</span> · <span style='color: #34d399;'>✅ {palavra['acertos']}</span></div>", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("📚 Ir estudar esse idioma", use_container_width=True, type="primary", key="estudar_agora"):
        st.session_state.idioma = idioma
        ir_para("menu")

    st.stop()
