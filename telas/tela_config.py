import streamlit as st
from config import IDIOMAS
from logica.navegacao import ir_para, voltar
from logica.gerenciador_config import carregar_config, atualizar_config, resetar_config
from logica.gerenciador_backup import (
    tamanho_banco,
    contar_registros,
    exportar_progresso,
    importar_progresso,
    backup_banco,
    listar_backups,
    resetar_progresso_idioma,
    resetar_tudo,
    contar_palavras_por_idioma,
)


def render():
    config = carregar_config()

    # ---------- HEADER ----------
    col_a, col_b = st.columns([1, 8])
    with col_a:
      if st.button("⬅️ Voltar", key="voltar_config"):
        st.write("🔥🔥🔥 BOTÃO CLICADO! 🔥🔥🔥")
        st.write(f"Tela atual ANTES: `{st.session_state.get('tela')}`")
        st.write(f"Histórico ANTES: `{st.session_state.get('historico', [])}`")
        st.write("---")
        st.write("Chamando `voltar()`...")
        voltar()
        st.write("⚠️ Se você tá vendo isso, o `voltar()` NÃO parou a execução.")
    with col_b:
        st.markdown("## ⚙️ Configurações")

    # ---------- MENSAGEM DE STATUS ----------
    if "msg_config" in st.session_state:
        st.success(st.session_state.msg_config)
        del st.session_state.msg_config

    if config.get("ultima_atualizacao"):
        st.caption(f"🕐 Última alteração: {config['ultima_atualizacao']}")

    st.markdown("---")

    # ============================================
    # 🎯 ESTUDO
    # ============================================
    with st.expander("🎯 Estudo", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            idioma_padrao = st.selectbox(
                "Idioma padrão ao abrir o app",
                ["ingles", "russo"],
                index=["ingles", "russo"].index(config["idioma_padrao"]),
                format_func=lambda x: "🇺🇸 Inglês" if x == "ingles" else "🇷🇺 Russo",
                key="cfg_idioma_padrao",
            )

            ordem_cards = st.selectbox(
                "Ordem dos cards",
                ["sequencial", "aleatorio"],
                index=["sequencial", "aleatorio"].index(config["ordem_cards"]),
                format_func=lambda x: "📋 Sequencial" if x == "sequencial" else "🔀 Aleatório",
                key="cfg_ordem",
            )

        with col2:
            repeticoes = st.slider(
                "Acertos para considerar uma palavra dominada",
                min_value=1, max_value=10,
                value=config["repeticoes_dominar"],
                key="cfg_repet",
            )

            mostrar_emoji = st.checkbox(
                "Mostrar emoji nos cards e módulos",
                value=config["mostrar_emoji"],
                key="cfg_emoji",
            )

        if st.button("💾 Salvar preferências de estudo", use_container_width=True, key="salvar_estudo"):
            atualizar_config(
                idioma_padrao=idioma_padrao,
                ordem_cards=ordem_cards,
                repeticoes_dominar=repeticoes,
                mostrar_emoji=mostrar_emoji,
            )
            st.session_state.msg_config = "✅ Preferências de estudo salvas!"
            st.rerun()

    # ============================================
    # 🎨 APARÊNCIA
    # ============================================
    with st.expander("🎨 Aparência", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            tema = st.radio(
                "Tema",
                ["escuro", "claro"],
                index=["escuro", "claro"].index(config["tema"]),
                horizontal=True,
                key="cfg_tema",
            )

        with col2:
            tamanho_fonte = st.radio(
                "Tamanho da fonte dos cards",
                ["pequeno", "medio", "grande"],
                index=["pequeno", "medio", "grande"].index(config["tamanho_fonte"]),
                horizontal=True,
                key="cfg_fonte",
            )

        st.info("💡 Ao salvar, o tema é aplicado **imediatamente** — a página recarrega.")

        if st.button("💾 Salvar e aplicar", use_container_width=True, type="primary", key="salvar_aparencia"):
            atualizar_config(tema=tema, tamanho_fonte=tamanho_fonte)
            st.session_state.msg_config = f"✅ Aparência salva! Tema: {tema}"
            st.rerun()

    # ============================================
    # 🔊 ÁUDIO
    # ============================================
    with st.expander("🔊 Áudio", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            audio_auto = st.checkbox(
                "Tocar áudio automaticamente ao revelar",
                value=config["audio_auto"],
                key="cfg_audio_auto",
            )
        with col2:
            audio_vel = st.radio(
                "Velocidade da fala",
                ["normal", "lenta"],
                index=["normal", "lenta"].index(config["audio_velocidade"]),
                horizontal=True,
                key="cfg_audio_vel",
            )

        if st.button("💾 Salvar áudio", use_container_width=True, key="salvar_audio"):
            atualizar_config(audio_auto=audio_auto, audio_velocidade=audio_vel)
            st.session_state.msg_config = "✅ Configurações de áudio salvas!"
            st.rerun()

    # ============================================
    # 💾 DADOS
    # ============================================
    with st.expander("💾 Dados e backup", expanded=False):
        st.markdown("### 📊 Estatísticas do banco")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tamanho", f"{tamanho_banco():.1f} KB")
        with col2:
            reg = contar_registros()
            st.metric("Progresso", reg["progresso"])
        with col3:
            st.metric("Anotações", reg["anotacoes"])
        with col4:
            st.metric("Dias (streak)", reg["streak"])

        st.markdown("---")
        st.markdown("### 📤 Exportar progresso")
        st.caption("Gera um arquivo JSON com todo o seu progresso, anotações e streak.")

        dados = exportar_progresso()
        if dados:
            from datetime import datetime
            st.download_button(
                label="💾 Baixar arquivo JSON",
                data=dados,
                file_name=f"progresso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                key="download_json",
            )
        else:
            st.info("Nada pra exportar ainda.")

        st.markdown("---")
        st.markdown("### 📥 Importar progresso")
        st.caption("⚠️ Substitui TODO o progresso atual. Faça backup antes.")

        arquivo = st.file_uploader("Escolha um arquivo JSON", type=["json"], key="upload_json")
        if arquivo:
            conteudo = arquivo.read().decode("utf-8")
            if st.button("⚠️ Importar e substituir tudo", type="primary", use_container_width=True, key="importar"):
                ok, msg = importar_progresso(conteudo)
                if ok:
                    st.session_state.msg_config = f"✅ {msg}"
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

        st.markdown("---")
        st.markdown("### 💾 Backup do banco")
        col_bkp1, col_bkp2 = st.columns(2)
        with col_bkp1:
            if st.button("📦 Criar backup agora", use_container_width=True, key="criar_backup"):
                destino = backup_banco()
                if destino:
                    st.session_state.msg_config = f"✅ Backup criado: {destino.name}"
                    st.rerun()
                else:
                    st.warning("Banco não existe ainda.")
        with col_bkp2:
            if st.button("📂 Ver últimos backups", use_container_width=True, key="ver_backups"):
                st.session_state.mostrar_backups = not st.session_state.get("mostrar_backups", False)

        if st.session_state.get("mostrar_backups", False):
            backups = listar_backups()
            if not backups:
                st.info("Nenhum backup ainda.")
            else:
                for b in backups[:10]:
                    st.caption(f"📦 {b['nome']} — {b['tamanho_kb']:.1f} KB")

        st.markdown("---")
        st.markdown("### 🗑️ Resetar dados")

        with st.expander("🚨 Zona de perigo", expanded=False):
            col_r1, col_r2 = st.columns(2)

            with col_r1:
                st.markdown("**Resetar progresso de um idioma**")
                idioma_reset = st.selectbox(
                    "Escolha",
                    ["ingles", "russo"],
                    format_func=lambda x: "🇺🇸 Inglês" if x == "ingles" else "🇷🇺 Russo",
                    key="reset_idioma",
                )
                if st.button(f"🗑️ Apagar progresso de {idioma_reset}", use_container_width=True, key="reset_idioma_btn"):
                    resetar_progresso_idioma(idioma_reset)
                    st.session_state.msg_config = f"✅ Progresso de {idioma_reset} apagado."
                    st.rerun()

            with col_r2:
                st.markdown("**Resetar TUDO**")
                st.caption("Apaga progresso, anotações e streak")
                confirmar = st.text_input("Digite **RESETAR** pra confirmar", key="confirma_reset")
                if st.button("🗑️ Apagar TUDO", use_container_width=True, type="primary", key="reset_tudo_btn"):
                    if confirmar.strip().upper() == "RESETAR":
                        resetar_tudo()
                        st.session_state.msg_config = "✅ Tudo apagado."
                        st.rerun()
                    else:
                        st.error("Digite RESETAR (tudo maiúsculo) pra confirmar.")

    # ============================================
    # ℹ️ SOBRE
    # ============================================
    with st.expander("ℹ️ Sobre", expanded=False):
        st.markdown("### 🌍 Língua App")
        st.caption("Versão 1.0 · Uso pessoal")

        st.markdown("---")
        st.markdown("### 📚 Total de palavras por idioma")

        palavras = contar_palavras_por_idioma()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🇺🇸 Inglês", palavras.get("ingles", 0))
        with col2:
            st.metric("🇷🇺 Russo", palavras.get("russo", 0))

        st.markdown("---")
        st.markdown("### 🛠️ Tecnologias")
        st.markdown("""
        - **Python** + **Streamlit** (interface)
        - **SQLite** (banco local)
        - **gTTS** (áudio)
        - **JSON** (conteúdo dos módulos)
        """)

        st.markdown("---")
        if st.button("🔄 Restaurar configurações padrão", use_container_width=True, key="reset_config"):
            resetar_config()
            st.session_state.msg_config = "✅ Configurações restauradas pro padrão!"
            st.rerun()

    st.stop()
