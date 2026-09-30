import streamlit as st
from logica.navegacao import init_estado, renderizar_tela_atual
from logica.gerenciador_progresso import init_db
from logica.gerenciador_exercicios import init_db_exercicios
from logica.gerenciador_config import carregar_config

st.set_page_config(
    page_title="Lingua App",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_db()
init_db_exercicios()
init_estado()

config = carregar_config()
tema = config.get("tema", "escuro")

if tema == "claro":
    bg = "#ffffff"
    texto = "#0f1419"
    texto_sub = "#4b5563"
    card_bg = "#f8fafc"
    card_border = "#e2e8f0"
else:
    bg = "#0f1419"
    texto = "#ffffff"
    texto_sub = "#a8b2c1"
    card_bg = "#1a2332"
    card_border = "#2d3748"

st.markdown(f"""
<style>
    /* Fundo geral */
    .stApp {{
        background-color: {bg} !important;
    }}

    /* Texto de titulos */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {texto} !important;
    }}

    /* Texto geral */
    .stApp p, .stApp label, .stApp .stMarkdown {{
        color: {texto};
    }}

    /* Texto secundario */
    .stApp .stCaption, .stApp small {{
        color: {texto_sub} !important;
    }}

    /* Botoes - maiores e mais confortaveis */
    .stButton > button {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 14px !important;
        padding: 16px 28px !important;
        min-height: 54px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background-color: #253045 !important;
        border-color: #34d399 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(52, 211, 153, 0.2) !important;
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3) !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #f87171, #ef4444) !important;
        box-shadow: 0 6px 24px rgba(239, 68, 68, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button:disabled {{
        opacity: 0.4 !important;
    }}

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: {card_bg} !important;
        color: {texto} !important;
        border: 2px solid {card_border} !important;
        border-radius: 10px !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: #34d399 !important;
        box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.2) !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        color: {texto} !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        background-color: {card_bg} !important;
        border-radius: 10px !important;
    }}

    /* Metrics */
    .stMetric {{
        background-color: {card_bg} !important;
        border: 2px solid {card_border} !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }}
    .stMetric label {{
        color: {texto_sub} !important;
        font-weight: 600 !important;
    }}
    .stMetric [data-testid="stMetricValue"] {{
        color: {texto} !important;
        font-weight: 800 !important;
    }}

    /* Alerts */
    .stAlert {{
        border-radius: 14px !important;
        border-left-width: 5px !important;
    }}

    /* Divisor */
    hr {{
        border-color: {card_border} !important;
        margin: 24px 0 !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        color: {texto_sub} !important;
        font-weight: 600 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #34d399 !important;
        font-weight: 700 !important;
    }}

    /* Progress bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #34d399, #60a5fa) !important;
    }}

    /* Radio / checkbox */
    .stRadio label, .stCheckbox label {{
        color: {texto} !important;
    }}
</style>
""", unsafe_allow_html=True)

renderizar_tela_atual()
