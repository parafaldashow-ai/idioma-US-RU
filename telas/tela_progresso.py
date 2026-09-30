import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_progresso import estatisticas_idioma, streak_atual


def render():
    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("⬅️ Voltar", key="voltar_prog"):
            voltar()
    with col_b:
        st.markdown("## 📊 Meu Progresso · Visao Geral")

    st.markdown("---")

    streak = streak_atual()
    if streak > 0:
        texto_streak = f"{streak} dia{'s' if streak != 1 else ''} seguido{'s' if streak != 1 else ''}!"
        html_streak = (
            '<div style="background: linear-gradient(135deg, #ef4444, #f97316); '
            'border-radius: 18px; padding: 24px 28px; margin-bottom: 28px; text-align: center; '
            'box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);">'
            '<div style="font-size: 48px; line-height: 1;">🔥</div>'
            f'<div style="font-size: 26px; font-weight: 800; color: #ffffff; margin-top: 8px;">{texto_streak}</div>'
            '<div style="font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 4px;">Continue assim!</div>'
            '</div>'
        )
        st.markdown(html_streak, unsafe_allow_html=True)
    else:
        st.info("💪 Comece a estudar hoje pra iniciar uma sequencia!")

    col1, col2 = st.columns(2)

    for col, (codigo, info) in zip([col1, col2], IDIOMAS.items()):
        with col:
            stats = estatisticas_idioma(codigo)
            dominadas = stats["dominadas"]
            em_andamento = stats["em_andamento"]
            total = stats["total_disponivel"]
            pct = int((dominadas / total * 100) if total else 0)
            total_fmt = f"{total:,}".replace(",", ".")

            cor_bandeira = "#34d399" if codigo == "ingles" else "#60a5fa"

            card_html = (
                f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
                f'border: 2px solid {cor_bandeira}33; border-radius: 22px; padding: 32px; '
                f'margin-bottom: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">'

                '<div style="text-align: center; margin-bottom: 24px;">'
                f'<div style="font-size: 80px; line-height: 1;">{info["bandeira"]}</div>'
                f'<div style="font-size: 24px; font-weight: 800; color: #ffffff; margin-top: 10px; letter-spacing: 1px;">{info["nome"].upper()}</div>'
                '</div>'

                '<div style="text-align: center; margin-bottom: 20px;">'
                f'<div style="font-size: 48px; font-weight: 800; color: #34d399;">{dominadas}</div>'
                '<div style="font-size: 13px; color: #a8b2c1; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px;">dominadas</div>'
                '</div>'

                f'<div style="text-align: center; font-size: 14px; color: #a8b2c1; margin-bottom: 16px;">'
                f'de {total_fmt} palavras'
                '</div>'

                '<div style="margin-bottom: 12px;">'
                '<div style="height: 12px; background: #0f1419; border-radius: 6px; overflow: hidden;">'
                f'<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, #34d399, #60a5fa); transition: width 0.5s ease;"></div>'
                '</div>'
                f'<div style="text-align: right; font-size: 14px; color: {cor_bandeira}; font-weight: 700; margin-top: 6px;">{pct}%</div>'
                '</div>'

                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

            if st.button(f"📖 Ver detalhes de {info['nome']}", use_container_width=True, key=f"det_{codigo}"):
                st.session_state.idioma_progresso = codigo
                ir_para("progresso_idioma")

    st.markdown("---")
    st.markdown("### 📈 Totais gerais")

    stats_en = estatisticas_idioma("ingles")
    stats_ru = estatisticas_idioma("russo")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("📚 Palavras disponiveis", stats_en["total_disponivel"] + stats_ru["total_disponivel"])
    with c2:
        st.metric("✅ Dominadas", stats_en["dominadas"] + stats_ru["dominadas"])
    with c3:
        st.metric("🔥 Dias seguidos", streak)

    st.stop()
