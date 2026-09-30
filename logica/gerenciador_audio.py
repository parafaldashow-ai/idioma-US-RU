import io
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
