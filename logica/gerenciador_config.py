import json
from datetime import datetime
from pathlib import Path
from config import BASE_DIR

CONFIG_PATH = BASE_DIR / "config_usuario.json"

PADRAO = {
    "idioma_padrao": "ingles",
    "tema": "escuro",
    "tamanho_fonte": "medio",
    "ordem_cards": "sequencial",
    "repeticoes_dominar": 3,
    "audio_auto": True,
    "audio_velocidade": "normal",
    "mostrar_emoji": True,
    "ultima_atualizacao": None,
}


def carregar_config():
    if not CONFIG_PATH.exists():
        salvar_config(PADRAO)
        return dict(PADRAO)

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        config = dict(PADRAO)
        config.update(dados)
        return config
    except Exception:
        return dict(PADRAO)


def salvar_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def atualizar_config(**kwargs):
    """Atualiza e registra timestamp da última alteração."""
    config = carregar_config()
    config.update(kwargs)
    config["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    salvar_config(config)
    return config


def resetar_config():
    config = dict(PADRAO)
    config["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    salvar_config(config)
    return config