import json
from pathlib import Path

BASE = Path(__file__).parent
PASTA_RUSSO = BASE / "dados" / "russo"

alfabeto_correto = [
    {"pt": "А (letra cirílica)", "ru": "А", "pron": "á"},
    {"pt": "Б (letra cirílica)", "ru": "Б", "pron": "bé"},
    {"pt": "В (letra cirílica)", "ru": "В", "pron": "vé"},
    {"pt": "Г (letra cirílica)", "ru": "Г", "pron": "gué"},
    {"pt": "Д (letra cirílica)", "ru": "Д", "pron": "dé"},
    {"pt": "Е (letra cirílica)", "ru": "Е", "pron": "ié"},
    {"pt": "Ё (letra cirílica)", "ru": "Ё", "pron": "ió"},
    {"pt": "Ж (letra cirílica)", "ru": "Ж", "pron": "jé"},
    {"pt": "З (letra cirílica)", "ru": "З", "pron": "zé"},
    {"pt": "И (letra cirílica)", "ru": "И", "pron": "í"},
    {"pt": "Й (letra cirílica)", "ru": "Й", "pron": "í curto"},
    {"pt": "К (letra cirílica)", "ru": "К", "pron": "ká"},
    {"pt": "Л (letra cirílica)", "ru": "Л", "pron": "él"},
    {"pt": "М (letra cirílica)", "ru": "М", "pron": "ém"},
    {"pt": "Н (letra cirílica)", "ru": "Н", "pron": "én"},
    {"pt": "О (letra cirílica)", "ru": "О", "pron": "ó"},
    {"pt": "П (letra cirílica)", "ru": "П", "pron": "pé"},
    {"pt": "Р (letra cirílica)", "ru": "Р", "pron": "ér"},
    {"pt": "С (letra cirílica)", "ru": "С", "pron": "és"},
    {"pt": "Т (letra cirílica)", "ru": "Т", "pron": "té"},
    {"pt": "У (letra cirílica)", "ru": "У", "pron": "ú"},
    {"pt": "Ф (letra cirílica)", "ru": "Ф", "pron": "éf"},
    {"pt": "Х (letra cirílica)", "ru": "Х", "pron": "rá"},
    {"pt": "Ц (letra cirílica)", "ru": "Ц", "pron": "tsé"},
    {"pt": "Ч (letra cirílica)", "ru": "Ч", "pron": "tché"},
    {"pt": "Ш (letra cirílica)", "ru": "Ш", "pron": "shá"},
    {"pt": "Щ (letra cirílica)", "ru": "Щ", "pron": "shchá"},
    {"pt": "Ъ (sinal duro)",     "ru": "Ъ", "pron": "sinal duro"},
    {"pt": "Ы (letra cirílica)", "ru": "Ы", "pron": "i gutural"},
    {"pt": "Ь (sinal suave)",    "ru": "Ь", "pron": "sinal suave"},
    {"pt": "Э (letra cirílica)", "ru": "Э", "pron": "é"},
    {"pt": "Ю (letra cirílica)", "ru": "Ю", "pron": "iú"},
    {"pt": "Я (letra cirílica)", "ru": "Я", "pron": "iá"},
]

caminho = PASTA_RUSSO / "alfabeto.json"
with open(caminho, "w", encoding="utf-8") as f:
    json.dump(alfabeto_correto, f, ensure_ascii=False, indent=2)

print(f"OK: {caminho} reescrito com 33 letras cirilicas")
print()
print("Agora roda:")
print("  python consertar_russo.py")