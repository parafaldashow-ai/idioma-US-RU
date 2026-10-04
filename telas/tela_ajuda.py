import streamlit as st
from logica.navegacao import ir_para, voltar


def bloco(icone, titulo, conteudo, cor="#34d399"):
    """Renderiza um bloco de ajuda estilizado."""
    html = (
        f'<div style="background: linear-gradient(135deg, #1a2332, #253045); '
        f'border-left: 5px solid {cor}; border-radius: 14px; '
        f'padding: 20px 24px; margin-bottom: 16px;">'
        f'<div style="font-size: 20px; font-weight: 800; color: {cor}; margin-bottom: 12px;">'
        f'{icone} {titulo}</div>'
        f'<div style="font-size: 15px; color: #e0e6ed; line-height: 1.7;">'
        f'{conteudo}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render():
    col_a, col_b = st.columns([1, 8])
    with col_a:
        if st.button("<- Voltar", key="voltar_ajuda"):
            voltar()
            return
    with col_b:
        st.markdown("## Ajuda - Como usar o app")

    st.markdown("---")

    # Bloco 1: Boas-vindas
    bloco(
        "🎯",
        "Bem-vindo ao Lingua App!",
        "Este app te ajuda a estudar <b>ingles</b> e <b>russo</b> de forma organizada.<br><br>"
        "O conteudo esta dividido em <b>5 niveis</b> (Iniciante, Basico, Intermediario, "
        "Avancado e Critico), com varios modulos cada.<br><br>"
        "Cada modulo tem <b>cards de estudo</b> (com audio e pronuncia), "
        "<b>exercicios</b> (4 modos diferentes) e <b>flashcards</b> (revisao ativa).",
        "#34d399"
    )

    # Bloco 2: O que e DOMINADA (destaque)
    bloco(
        "✅",
        "O que e uma palavra DOMINADA?",
        "Uma palavra vira <b>dominada</b> quando voce <b>acerta ela 3 vezes</b> "
        "em exercicios ou flashcards.<br><br>"
        "⚠️ <b>Atencao:</b> 1 acerto NAO basta. Precisa 3+ acertos em momentos diferentes "
        "(3 sessoes, 3 dias, etc).<br><br>"
        "🎯 <b>Para que serve?</b> Saber o que voce <b>REALMENTE sabe</b>, "
        "nao so o que viu uma vez.",
        "#34d399"
    )

    # Bloco 3: Onde ver o progresso
    bloco(
        "📊",
        "Onde vejo meu progresso?",
        "No menu <b>Progresso</b>, cada nivel mostra:<br><br>"
        "<code>🟢 Iniciante: 25/119 - 21%</code><br><br>"
        "Isso significa <b>25 palavras dominadas</b> de 119 totais do nivel.<br><br>"
        "Tambem tem o <b>streak</b> (dias seguidos estudando).",
        "#60a5fa"
    )

    # Bloco 4: Diferenca entre as telas
    bloco(
        "📚",
        "Diferenca entre as telas",
        "<b>📖 Modulos</b> - onde voce <b>ESTUDA</b> (ve os cards pela primeira vez)<br>"
        "<b>✏️ Exercicios</b> - onde voce <b>TESTA</b> (responde perguntas)<br>"
        "<b>🎴 Flashcards</b> - onde voce <b>REVISA</b> (foca no que falta)<br>"
        "<b>📊 Progresso</b> - onde voce <b>VE o avanco</b><br>"
        "<b>🔍 Dicionario</b> - onde voce <b>CONSULTA</b> (busca palavras)<br>"
        "<b>📝 Anotacoes</b> - onde voce <b>ANOTA</b> (caderno pessoal)",
        "#a78bfa"
    )

    # Bloco 5: Modos de exercicio
    bloco(
        "✏️",
        "Os 4 modos de exercicio",
        "<b>🎯 Multipla escolha</b> - escolhe entre 4 opcoes<br>"
        "<b>⌨️ Digitar</b> - escreve a resposta<br>"
        "<b>🔊 Ouça e Traduza</b> - ouve o audio e digita<br>"
        "<b>🧩 Associar pares</b> - liga PT com EN (jogo de memoria)",
        "#fbbf24"
    )

    # Bloco 6: Modos de flashcard
    bloco(
        "🎴",
        "Os 3 modos de flashcard",
        "<b>🔥 Nao dominadas</b> - revisa o que voce viu mas nao dominou<br>"
        "<b>❌ As que errei</b> - foca nas palavras que voce errou<br>"
        "<b>🎲 Aleatorio</b> - 20 palavras aleatorias de tudo",
        "#ec4899"
    )

    # Bloco 7: Como estudar
    bloco(
        "💡",
        "Como estudar de forma eficiente",
        "<b>1.</b> Escolha um modulo no nivel Iniciante<br>"
        "<b>2.</b> Passe pelos cards (veja + ouca)<br>"
        "<b>3.</b> Faca exercicios (multipla escolha)<br>"
        "<b>4.</b> Errou? Vai no <b>❌ As que errei</b> e revisa<br>"
        "<b>5.</b> Volte pros exercicios<br>"
        "<b>6.</b> Revise no <b>🔥 Nao dominadas</b><br>"
        "<b>7.</b> So domina quem acerta 3x em momentos diferentes<br><br>"
        "Nao tenha pressa. Aprender lingua leva tempo.",
        "#f97316"
    )

    # Bloco 8: Sobre a pronuncia
    bloco(
        "🔊",
        "Sobre a pronuncia",
        "A pronuncia esta entre colchetes azuis. Exemplo:<br><br>"
        "<code>hello -> [rélou]</code><br><br>"
        "Significa que <b>hello</b> se pronuncia <b>relou</b>.<br><br>"
        "⚠️ Nao e perfeita - serve como <b>guia</b>.<br><br>"
        "O melhor jeito de aprender pronuncia e <b>ouvir o audio</b> "
        "varias vezes e imitar.",
        "#60a5fa"
    )

    # Bloco 9: Dicas
    bloco(
        "🎓",
        "Dicas para aprender mais rapido",
        "• <b>Estude todos os dias</b> - 15 min por dia vale mais que 2h no domingo<br>"
        "• <b>Ouca o audio</b> - nao confie so na leitura<br>"
        "• <b>Fale em voz alta</b> - repita as palavras<br>"
        "• <b>Revise sempre</b> - Flashcards sao seus amigos<br>"
        "• <b>Nao pule etapas</b> - domine o Iniciante antes de ir pro Basico<br>"
        "• <b>Use o streak</b> - mantenha a sequencia de dias",
        "#34d399"
    )

    st.markdown("---")
    st.caption("Se tiver duvidas, use o Dicionario ou as Anotacoes pra registrar o que aprendeu.")
    st.stop()
