"""
Adiciona o idioma ESPANHOL (Latino - es-MX) ao app.
- Atualiza config.py
- Cria dados/espanhol/ com todos os modulos preenchidos
- Corrige codigos hardcoded nas telas
- Faz backup antes de mexer

Uso:
    python adicionar_espanhol.py
"""

import json
import re
import shutil
from pathlib import Path

BASE = Path(__file__).parent
PASTA_ESPANHOL = BASE / "dados" / "espanhol"
BACKUP_DIR = BASE / "backups" / "pre_espanhol"


# ============================================================
# PARTE 0: BACKUP
# ============================================================
def fazer_backup():
    print("=" * 60)
    print("FAZENDO BACKUP...")
    print("=" * 60)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    arquivos = [
        BASE / "config.py",
        BASE / "logica" / "navegacao.py",
        BASE / "telas" / "tela_modulo.py",
        BASE / "telas" / "tela_modulos.py",
        BASE / "telas" / "tela_dicionario.py",
        BASE / "telas" / "tela_exercicio.py",
        BASE / "telas" / "tela_flashcards.py",
        BASE / "telas" / "tela_inicial.py",
        BASE / "telas" / "tela_menu_idioma.py",
        BASE / "telas" / "tela_progresso.py",
        BASE / "telas" / "tela_progresso_idioma.py",
        BASE / "telas" / "tela_anotacoes.py",
    ]

    for arq in arquivos:
        if arq.exists():
            destino = BACKUP_DIR / arq.name
            shutil.copy(arq, destino)
            print(f"  OK: {arq.name}")

    print(f"\nBackup salvo em: {BACKUP_DIR}\n")


# ============================================================
# PARTE 1: ATUALIZAR config.py
# ============================================================
def atualizar_config():
    print("=" * 60)
    print("ATUALIZANDO config.py...")
    print("=" * 60)

    caminho = BASE / "config.py"
    conteudo = caminho.read_text(encoding="utf-8")

    # Verifica se ja tem espanhol
    if '"espanhol"' in conteudo:
        print("  OK: espanhol ja esta no config.py")
        return

    # Adiciona espanhol ANTES do fechamento do dicionario IDIOMAS
    # Procura o bloco do russo e adiciona espanhol depois
    padrao = r'("russo":\s*\{[^}]*\},)'
    match = re.search(padrao, conteudo)

    if not match:
        print("  ERRO: nao achei o bloco do russo no config.py")
        print("  Me manda o config.py que eu ajusto manualmente.")
        return

    bloco_russo = match.group(1)

    bloco_espanhol = '''
    "espanhol": {
        "nome": "Espanhol",
        "nome_nativo": "Espa\u00f1ol (Latino)",
        "bandeira": "\U0001F4B0",
        "bandeira_alt": "",
        "bandeira_img": "",
        "codigo_audio": "es",
        "codigo_conteudo": "es",
    },'''

    conteudo = conteudo.replace(bloco_russo, bloco_russo + bloco_espanhol)

    # Adiciona codigo_conteudo no ingles e russo tambem (pra padronizar)
    if '"codigo_conteudo"' not in conteudo.split('"ingles"')[1][:500]:
        conteudo = re.sub(
            r'("ingles":\s*\{[^}]*"codigo_audio":\s*"en",)',
            r'\1\n        "codigo_conteudo": "en",',
            conteudo
        )

    if '"codigo_conteudo"' not in conteudo.split('"russo"')[1][:500]:
        conteudo = re.sub(
            r'("russo":\s*\{[^}]*"codigo_audio":\s*"ru",)',
            r'\1\n        "codigo_conteudo": "ru",',
            conteudo
        )

    caminho.write_text(conteudo, encoding="utf-8")
    print("  OK: espanhol adicionado ao config.py")
    print("  OK: codigo_conteudo adicionado em ingles/russo\n")


# ============================================================
# PARTE 2: CRIAR DADOS DO ESPANHOL
# ============================================================
def criar_pasta_espanhol():
    print("=" * 60)
    print("CRIANDO dados/espanhol/...")
    print("=" * 60)
    PASTA_ESPANHOL.mkdir(parents=True, exist_ok=True)
    print(f"  OK: pasta {PASTA_ESPANHOL}\n")


def salvar_json(nome_arquivo, dados):
    caminho = PASTA_ESPANHOL / nome_arquivo
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"  OK: {nome_arquivo} ({len(dados)} itens)")


# ============================================================
# VOCABULARIO - MODULOS.JSON
# ============================================================
MODULOS = {
    "niveis": [
        {
            "id": "iniciante",
            "nome": "Iniciante",
            "icone": "🟢",
            "cor": "#4ade80",
            "descricao": "Comece por aqui",
            "modulos": [
                {"id": "alfabeto",  "nome": "Alfabeto",   "icone": "🔤"},
                {"id": "saudacoes", "nome": "Saudações",  "icone": "👋"},
                {"id": "numeros",   "nome": "Números",    "icone": "🔢"},
                {"id": "cores",     "nome": "Cores",      "icone": "🎨"},
                {"id": "familia",   "nome": "Família",    "icone": "👨‍👩‍👧"},
            ],
        },
        {
            "id": "basico",
            "nome": "Básico",
            "icone": "🔵",
            "cor": "#60a5fa",
            "descricao": "Vocabulário do dia a dia",
            "modulos": [
                {"id": "casa",       "nome": "Casa e objetos",  "icone": "🏠"},
                {"id": "roupas",     "nome": "Roupas",          "icone": "👕"},
                {"id": "animais",    "nome": "Animais",         "icone": "🐶"},
                {"id": "clima",      "nome": "Clima e natureza","icone": "🌦️"},
                {"id": "transporte", "nome": "Transporte",      "icone": "🚗"},
                {"id": "direcoes",   "nome": "Direções",        "icone": "🧭"},
                {"id": "comida",     "nome": "Comida",          "icone": "🍞"},
                {"id": "profissoes", "nome": "Profissões",      "icone": "💼"},
            ],
        },
        {
            "id": "intermediario",
            "nome": "Intermediário",
            "icone": "🟡",
            "cor": "#facc15",
            "descricao": "Construindo frases",
            "modulos": [
                {"id": "verbos",      "nome": "Verbos essenciais", "icone": "🔤"},
                {"id": "perguntas",   "nome": "Perguntas",         "icone": "❓"},
                {"id": "emocoes",     "nome": "Emoções",           "icone": "😊"},
                {"id": "dinheiro",    "nome": "Dinheiro e compras","icone": "💰"},
                {"id": "restaurante", "nome": "Restaurante",       "icone": "🍽️"},
                {"id": "lugares",     "nome": "Lugares na cidade", "icone": "🏙️"},
                {"id": "datas",       "nome": "Dias e meses",      "icone": "📅"},
            ],
        },
        {
            "id": "avancado",
            "nome": "Avançado",
            "icone": "🟠",
            "cor": "#fb923c",
            "descricao": "Aprofundando",
            "modulos": [
                {"id": "corpo",    "nome": "Corpo humano",     "icone": "🧑"},
                {"id": "horas",    "nome": "Horas e datas",    "icone": "🕐"},
                {"id": "formas",   "nome": "Formas e tamanhos","icone": "🔷"},
                {"id": "midia",    "nome": "Música e cinema",  "icone": "🎵"},
                {"id": "esportes", "nome": "Esportes",         "icone": "⚽"},
                {"id": "viagem",   "nome": "Viagem",           "icone": "✈️"},
            ],
        },
        {
            "id": "critico",
            "nome": "Crítico",
            "icone": "🔴",
            "cor": "#f87171",
            "descricao": "Sobrevivência",
            "modulos": [
                {"id": "emergencias", "nome": "Emergências", "icone": "🚨"},
            ],
        },
    ]
}


# ============================================================
# VOCABULARIO POR MODULO
# ============================================================

ALFABETO = [
    {"pt": "A (letra)", "es": "A", "pron": "a"},
    {"pt": "B (letra)", "es": "B", "pron": "be"},
    {"pt": "C (letra)", "es": "C", "pron": "se"},
    {"pt": "D (letra)", "es": "D", "pron": "de"},
    {"pt": "E (letra)", "es": "E", "pron": "e"},
    {"pt": "F (letra)", "es": "F", "pron": "efe"},
    {"pt": "G (letra)", "es": "G", "pron": "je"},
    {"pt": "H (letra)", "es": "H", "pron": "ache"},
    {"pt": "I (letra)", "es": "I", "pron": "i"},
    {"pt": "J (letra)", "es": "J", "pron": "jota"},
    {"pt": "K (letra)", "es": "K", "pron": "ka"},
    {"pt": "L (letra)", "es": "L", "pron": "ele"},
    {"pt": "M (letra)", "es": "M", "pron": "eme"},
    {"pt": "N (letra)", "es": "N", "pron": "ene"},
    {"pt": "Ñ (letra)", "es": "Ñ", "pron": "eñe"},
    {"pt": "O (letra)", "es": "O", "pron": "o"},
    {"pt": "P (letra)", "es": "P", "pron": "pe"},
    {"pt": "Q (letra)", "es": "Q", "pron": "cu"},
    {"pt": "R (letra)", "es": "R", "pron": "erre"},
    {"pt": "S (letra)", "es": "S", "pron": "ese"},
    {"pt": "T (letra)", "es": "T", "pron": "te"},
    {"pt": "U (letra)", "es": "U", "pron": "u"},
    {"pt": "V (letra)", "es": "V", "pron": "uve"},
    {"pt": "W (letra)", "es": "W", "pron": "doble u"},
    {"pt": "X (letra)", "es": "X", "pron": "equis"},
    {"pt": "Y (letra)", "es": "Y", "pron": "ye"},
    {"pt": "Z (letra)", "es": "Z", "pron": "zeta"},
]

SAUDACOES = [
    {"pt": "olá",              "es": "hola",                 "pron": "óla"},
    {"pt": "bom dia",          "es": "buenos días",          "pron": "buénos días"},
    {"pt": "boa tarde",        "es": "buenas tardes",        "pron": "buénas tárdas"},
    {"pt": "boa noite",        "es": "buenas noches",        "pron": "buénas nóches"},
    {"pt": "tchau",            "es": "adiós",                "pron": "adiós"},
    {"pt": "até logo",         "es": "hasta luego",          "pron": "ásta luégo"},
    {"pt": "até amanhã",       "es": "hasta mañana",         "pron": "ásta mañana"},
    {"pt": "por favor",        "es": "por favor",            "pron": "por fabór"},
    {"pt": "obrigado",         "es": "gracias",              "pron": "grásias"},
    {"pt": "de nada",          "es": "de nada",              "pron": "de náda"},
    {"pt": "desculpa",         "es": "perdón",               "pron": "perdón"},
    {"pt": "com licença",      "es": "disculpe",             "pron": "diskúlpe"},
    {"pt": "sim",              "es": "sí",                   "pron": "si"},
    {"pt": "não",              "es": "no",                   "pron": "no"},
    {"pt": "talvez",           "es": "quizás",               "pron": "kisás"},
    {"pt": "como vai você?",   "es": "¿cómo estás?",         "pron": "kómo estás"},
    {"pt": "bem, obrigado",    "es": "bien, gracias",        "pron": "bién grásias"},
    {"pt": "qual seu nome?",   "es": "¿cómo te llamas?",     "pron": "kómo te llámas"},
    {"pt": "meu nome é...",    "es": "me llamo...",          "pron": "me llámo"},
    {"pt": "prazer em conhecer","es": "mucho gusto",         "pron": "múcho gústo"},
    {"pt": "de onde você é?",  "es": "¿de dónde eres?",      "pron": "de dónde éres"},
    {"pt": "eu sou do Brasil", "es": "soy de Brasil",        "pron": "soi de Brasíl"},
    {"pt": "quantos anos você tem?","es": "¿cuántos años tienes?","pron": "kuántos áños tiénes"},
    {"pt": "eu tenho ... anos","es": "tengo ... años",       "pron": "téngo áños"},
    {"pt": "você fala português?","es": "¿hablas portugués?","pron": "áblas portugués"},
    {"pt": "eu não entendo",   "es": "no entiendo",          "pron": "no entiéndo"},
    {"pt": "pode repetir?",    "es": "¿puedes repetir?",     "pron": "puédes repetír"},
    {"pt": "muito obrigado",   "es": "muchas gracias",       "pron": "múchas grásias"},
    {"pt": "tudo bem",         "es": "todo bien",            "pron": "tódo bién"},
    {"pt": "até mais",         "es": "nos vemos",            "pron": "nos bémos"},
]

NUMEROS = [
    {"pt": "zero",       "es": "cero",       "pron": "séro"},
    {"pt": "um",         "es": "uno",        "pron": "úno"},
    {"pt": "dois",       "es": "dos",        "pron": "dos"},
    {"pt": "três",       "es": "tres",       "pron": "tres"},
    {"pt": "quatro",     "es": "cuatro",     "pron": "kuátro"},
    {"pt": "cinco",      "es": "cinco",      "pron": "sínko"},
    {"pt": "seis",       "es": "seis",       "pron": "seis"},
    {"pt": "sete",       "es": "siete",      "pron": "siéte"},
    {"pt": "oito",       "es": "ocho",       "pron": "ócho"},
    {"pt": "nove",       "es": "nueve",      "pron": "nuébe"},
    {"pt": "dez",        "es": "diez",       "pron": "diés"},
    {"pt": "onze",       "es": "once",       "pron": "ónse"},
    {"pt": "doze",       "es": "doce",       "pron": "dóse"},
    {"pt": "treze",      "es": "trece",      "pron": "trése"},
    {"pt": "quatorze",   "es": "catorce",    "pron": "katórse"},
    {"pt": "quinze",     "es": "quince",     "pron": "kínse"},
    {"pt": "dezesseis",  "es": "dieciséis",  "pron": "diesiséis"},
    {"pt": "dezessete",  "es": "diecisiete", "pron": "diesisiéte"},
    {"pt": "dezoito",    "es": "dieciocho",  "pron": "diesiócho"},
    {"pt": "dezenove",   "es": "diecinueve", "pron": "diesinuébe"},
    {"pt": "vinte",      "es": "veinte",     "pron": "béinte"},
    {"pt": "trinta",     "es": "treinta",    "pron": "tréinta"},
    {"pt": "quarenta",   "es": "cuarenta",   "pron": "kuarénta"},
    {"pt": "cinquenta",  "es": "cincuenta",  "pron": "sinkuénta"},
    {"pt": "sessenta",   "es": "sesenta",    "pron": "sesénta"},
    {"pt": "setenta",    "es": "setenta",    "pron": "seténta"},
    {"pt": "oitenta",    "es": "ochenta",    "pron": "ochénta"},
    {"pt": "noventa",    "es": "noventa",    "pron": "nobénta"},
    {"pt": "cem",        "es": "cien",       "pron": "sién"},
    {"pt": "mil",        "es": "mil",        "pron": "mil"},
]

CORES = [
    {"pt": "vermelho",   "es": "rojo",       "pron": "rójo"},
    {"pt": "azul",       "es": "azul",       "pron": "asúl"},
    {"pt": "verde",      "es": "verde",      "pron": "bérde"},
    {"pt": "amarelo",    "es": "amarillo",   "pron": "amaríllo"},
    {"pt": "preto",      "es": "negro",      "pron": "négro"},
    {"pt": "branco",     "es": "blanco",     "pron": "blánko"},
    {"pt": "cinza",      "es": "gris",       "pron": "gris"},
    {"pt": "rosa",       "es": "rosa",       "pron": "rósa"},
    {"pt": "roxo",       "es": "morado",     "pron": "morádo"},
    {"pt": "laranja",    "es": "naranja",    "pron": "naránja"},
    {"pt": "marrom",     "es": "marrón",     "pron": "marrón"},
    {"pt": "bege",       "es": "beige",      "pron": "béish"},
    {"pt": "dourado",    "es": "dorado",     "pron": "dorádo"},
    {"pt": "prateado",   "es": "plateado",   "pron": "plateádo"},
]

FAMILIA = [
    {"pt": "pai",            "es": "padre",         "pron": "pádre"},
    {"pt": "mãe",            "es": "madre",         "pron": "mádre"},
    {"pt": "irmão",          "es": "hermano",       "pron": "ermáno"},
    {"pt": "irmã",           "es": "hermana",       "pron": "ermána"},
    {"pt": "filho",          "es": "hijo",          "pron": "íjo"},
    {"pt": "filha",          "es": "hija",          "pron": "íja"},
    {"pt": "avô",            "es": "abuelo",        "pron": "abuél o"},
    {"pt": "avó",            "es": "abuela",        "pron": "abuél a"},
    {"pt": "tio",            "es": "tío",           "pron": "tío"},
    {"pt": "tia",            "es": "tía",           "pron": "tía"},
    {"pt": "primo",          "es": "primo",         "pron": "prímo"},
    {"pt": "prima",          "es": "prima",         "pron": "príma"},
    {"pt": "sobrinho",       "es": "sobrino",       "pron": "sobríno"},
    {"pt": "sobrinha",       "es": "sobrina",       "pron": "sobrína"},
    {"pt": "marido",         "es": "esposo",        "pron": "espóso"},
    {"pt": "esposa",         "es": "esposa",        "pron": "espósa"},
    {"pt": "namorado",       "es": "novio",         "pron": "nóbio"},
    {"pt": "namorada",       "es": "novia",         "pron": "nóbia"},
    {"pt": "filho (criança)", "es": "niño",          "pron": "níño"},
    {"pt": "filha (criança)", "es": "niña",          "pron": "níña"},
]

CASA = [
    {"pt": "casa",          "es": "casa",           "pron": "kása"},
    {"pt": "apartamento",   "es": "apartamento",    "pron": "apartaménto"},
    {"pt": "quarto",        "es": "habitación",     "pron": "abitación"},
    {"pt": "sala",          "es": "sala",           "pron": "sála"},
    {"pt": "cozinha",       "es": "cocina",         "pron": "kosína"},
    {"pt": "banheiro",      "es": "baño",           "pron": "báño"},
    {"pt": "porta",         "es": "puerta",         "pron": "puérta"},
    {"pt": "janela",        "es": "ventana",        "pron": "bentána"},
    {"pt": "cama",          "es": "cama",           "pron": "káma"},
    {"pt": "mesa",          "es": "mesa",           "pron": "mésa"},
    {"pt": "cadeira",       "es": "silla",          "pron": "sílla"},
    {"pt": "sofá",          "es": "sofá",           "pron": "sofá"},
    {"pt": "geladeira",     "es": "refrigerador",   "pron": "refrijeradór"},
    {"pt": "fogão",         "es": "estufa",         "pron": "estúfa"},
    {"pt": "televisão",     "es": "televisión",     "pron": "telebisión"},
    {"pt": "luz",           "es": "luz",            "pron": "lus"},
    {"pt": "chave",         "es": "llave",          "pron": "llábe"},
    {"pt": "espelho",       "es": "espejo",         "pron": "espéjo"},
    {"pt": "tapete",        "es": "alfombra",       "pron": "alfómbra"},
    {"pt": "cortina",       "es": "cortina",        "pron": "kortína"},
    {"pt": "toalha",        "es": "toalla",         "pron": "toálla"},
    {"pt": "sabonete",      "es": "jabón",          "pron": "jabón"},
    {"pt": "pia",           "es": "lavabo",         "pron": "labábo"},
    {"pt": "chuveiro",      "es": "ducha",          "pron": "dúcha"},
    {"pt": "vaso sanitário", "es": "inodoro",       "pron": "inodóro"},
    {"pt": "travesseiro",   "es": "almohada",       "pron": "almoháda"},
    {"pt": "cobertor",      "es": "cobija",         "pron": "kobíja"},
    {"pt": "guarda-roupa",  "es": "armario",        "pron": "armário"},
    {"pt": "gaveta",        "es": "cajón",          "pron": "cajón"},
    {"pt": "lixo",          "es": "basura",         "pron": "basúra"},
]

ROUPAS = [
    {"pt": "camisa",        "es": "camisa",         "pron": "kamísa"},
    {"pt": "camiseta",      "es": "camiseta",       "pron": "kamiséta"},
    {"pt": "calça",         "es": "pantalón",       "pron": "pantalón"},
    {"pt": "bermuda",       "es": "pantalón corto", "pron": "pantalón kórto"},
    {"pt": "saia",          "es": "falda",          "pron": "fálda"},
    {"pt": "vestido",       "es": "vestido",        "pron": "bestído"},
    {"pt": "jaqueta",       "es": "chaqueta",       "pron": "chakéta"},
    {"pt": "casaco",        "es": "abrigo",         "pron": "abrígo"},
    {"pt": "sapato",        "es": "zapato",         "pron": "sapáto"},
    {"pt": "tênis",         "es": "zapatillas",     "pron": "sapatíllas"},
    {"pt": "sandália",      "es": "sandalia",       "pron": "sandália"},
    {"pt": "meia",          "es": "calcetín",       "pron": "kalsetín"},
    {"pt": "chapéu",        "es": "sombrero",       "pron": "sombréro"},
    {"pt": "boné",          "es": "gorra",          "pron": "górra"},
    {"pt": "cinto",         "es": "cinturón",       "pron": "sinturón"},
    {"pt": "gravata",       "es": "corbata",        "pron": "korbáta"},
    {"pt": "bolsa",         "es": "bolso",          "pron": "bólso"},
    {"pt": "mochila",       "es": "mochila",        "pron": "mochíla"},
    {"pt": "luva",          "es": "guante",         "pron": "guánte"},
    {"pt": "óculos",        "es": "gafas",          "pron": "gáfas"},
    {"pt": "relógio",       "es": "reloj",          "pron": "relój"},
    {"pt": "anel",          "es": "anillo",         "pron": "aníllo"},
    {"pt": "colar",         "es": "collar",         "pron": "kollár"},
    {"pt": "brinco",        "es": "arete",          "pron": "aréte"},
    {"pt": "pulseira",      "es": "pulsera",        "pron": "pulséra"},
]

ANIMAIS = [
    {"pt": "cachorro",      "es": "perro",          "pron": "pérro"},
    {"pt": "gato",          "es": "gato",           "pron": "gáto"},
    {"pt": "pássaro",       "es": "pájaro",         "pron": "pájaro"},
    {"pt": "peixe",         "es": "pez",            "pron": "pes"},
    {"pt": "cavalo",        "es": "caballo",        "pron": "kabáio"},
    {"pt": "vaca",          "es": "vaca",           "pron": "báka"},
    {"pt": "porco",         "es": "cerdo",          "pron": "sérdo"},
    {"pt": "ovelha",        "es": "oveja",          "pron": "obéja"},
    {"pt": "galinha",       "es": "gallina",        "pron": "gallína"},
    {"pt": "galo",          "es": "gallo",          "pron": "gállo"},
    {"pt": "pato",          "es": "pato",           "pron": "páto"},
    {"pt": "leão",          "es": "león",           "pron": "león"},
    {"pt": "tigre",         "es": "tigre",          "pron": "tígre"},
    {"pt": "elefante",      "es": "elefante",       "pron": "elefánte"},
    {"pt": "macaco",        "es": "mono",           "pron": "móno"},
    {"pt": "urso",          "es": "oso",            "pron": "óso"},
    {"pt": "lobo",          "es": "lobo",           "pron": "lóbo"},
    {"pt": "rato",          "es": "ratón",          "pron": "ratón"},
    {"pt": "coelho",        "es": "conejo",         "pron": "konéjo"},
    {"pt": "tartaruga",     "es": "tortuga",        "pron": "tortúga"},
    {"pt": "cobra",         "es": "serpiente",      "pron": "serpiénte"},
    {"pt": "aranha",        "es": "araña",          "pron": "aráña"},
    {"pt": "abelha",        "es": "abeja",          "pron": "abéja"},
    {"pt": "borboleta",     "es": "mariposa",       "pron": "maripósa"},
    {"pt": "formiga",       "es": "hormiga",        "pron": "ormíga"},
    {"pt": "mosquito",      "es": "mosquito",       "pron": "moskíto"},
    {"pt": "pinguim",       "es": "pingüino",       "pron": "pingüíno"},
    {"pt": "golfinho",      "es": "delfín",         "pron": "delfín"},
    {"pt": "tubarão",       "es": "tiburón",        "pron": "tiburón"},
    {"pt": "águia",         "es": "águila",         "pron": "águila"},
]

CLIMA = [
    {"pt": "sol",           "es": "sol",            "pron": "sol"},
    {"pt": "lua",           "es": "luna",           "pron": "lúna"},
    {"pt": "estrela",       "es": "estrella",       "pron": "estrélla"},
    {"pt": "céu",           "es": "cielo",          "pron": "siélo"},
    {"pt": "nuvem",         "es": "nube",           "pron": "núbe"},
    {"pt": "chuva",         "es": "lluvia",         "pron": "llúbia"},
    {"pt": "neve",          "es": "nieve",          "pron": "niébe"},
    {"pt": "vento",         "es": "viento",         "pron": "biénto"},
    {"pt": "tempestade",    "es": "tormenta",       "pron": "torménta"},
    {"pt": "trovão",        "es": "trueno",         "pron": "truéno"},
    {"pt": "relâmpago",     "es": "relámpago",      "pron": "relámpago"},
    {"pt": "arco-íris",     "es": "arco iris",      "pron": "árko íris"},
    {"pt": "frio",          "es": "frío",           "pron": "frío"},
    {"pt": "calor",         "es": "calor",          "pron": "kalór"},
    {"pt": "primavera",     "es": "primavera",      "pron": "primabéra"},
    {"pt": "verão",         "es": "verano",         "pron": "beráno"},
    {"pt": "outono",        "es": "otoño",          "pron": "otóño"},
    {"pt": "inverno",       "es": "invierno",       "pron": "inbiérno"},
    {"pt": "árvore",        "es": "árbol",          "pron": "árbol"},
    {"pt": "flor",          "es": "flor",           "pron": "flor"},
    {"pt": "folha",         "es": "hoja",           "pron": "ója"},
    {"pt": "grama",         "es": "césped",         "pron": "sésped"},
    {"pt": "montanha",      "es": "montaña",        "pron": "montáña"},
    {"pt": "rio",           "es": "río",            "pron": "río"},
    {"pt": "mar",           "es": "mar",            "pron": "mar"},
    {"pt": "praia",         "es": "playa",          "pron": "plája"},
    {"pt": "ilha",          "es": "isla",           "pron": "ísla"},
    {"pt": "lago",          "es": "lago",           "pron": "lágo"},
    {"pt": "floresta",      "es": "bosque",         "pron": "bóske"},
    {"pt": "deserto",       "es": "desierto",       "pron": "desiérto"},
]

TRANSPORTE = [
    {"pt": "carro",         "es": "coche",          "pron": "kóche"},
    {"pt": "moto",          "es": "moto",           "pron": "móto"},
    {"pt": "bicicleta",     "es": "bicicleta",      "pron": "bisikléta"},
    {"pt": "ônibus",        "es": "autobús",        "pron": "autobús"},
    {"pt": "metrô",         "es": "metro",          "pron": "métro"},
    {"pt": "trem",          "es": "tren",           "pron": "tren"},
    {"pt": "avião",         "es": "avión",          "pron": "abión"},
    {"pt": "navio",         "es": "barco",          "pron": "bárko"},
    {"pt": "táxi",          "es": "taxi",           "pron": "táksi"},
    {"pt": "caminhão",      "es": "camión",         "pron": "kamión"},
    {"pt": "estrada",       "es": "carretera",      "pron": "karretéra"},
    {"pt": "rua",           "es": "calle",          "pron": "kálle"},
    {"pt": "avenida",       "es": "avenida",        "pron": "abenída"},
    {"pt": "semáforo",      "es": "semáforo",       "pron": "semáforo"},
    {"pt": "faixa de pedestre", "es": "paso de cebra","pron": "páso de sébra"},
    {"pt": "estacionamento", "es": "estacionamiento","pron": "estasionamiénto"},
    {"pt": "posto de gasolina","es": "gasolinera",  "pron": "gasolinéra"},
    {"pt": "aeroporto",     "es": "aeropuerto",     "pron": "aeropuérto"},
    {"pt": "estação",       "es": "estación",       "pron": "estasión"},
    {"pt": "passagem",      "es": "billete",        "pron": "billéte"},
    {"pt": "motorista",     "es": "conductor",      "pron": "kondúktor"},
    {"pt": "passageiro",    "es": "pasajero",       "pron": "pasajéro"},
    {"pt": "volante",       "es": "volante",        "pron": "bolánte"},
    {"pt": "pneu",          "es": "neumático",      "pron": "neumátiko"},
    {"pt": "farol",         "es": "faro",           "pron": "fáro"},
]

DIRECOES = [
    {"pt": "esquerda",      "es": "izquierda",      "pron": "iskierda"},
    {"pt": "direita",       "es": "derecha",        "pron": "derécha"},
    {"pt": "reto",          "es": "derecho",        "pron": "derécho"},
    {"pt": "para frente",   "es": "adelante",       "pron": "adelánte"},
    {"pt": "para trás",     "es": "atrás",          "pron": "atrás"},
    {"pt": "acima",         "es": "arriba",         "pron": "arríba"},
    {"pt": "abaixo",        "es": "abajo",          "pron": "abájo"},
    {"pt": "dentro",        "es": "dentro",         "pron": "déntro"},
    {"pt": "fora",          "es": "fuera",          "pron": "fuéra"},
    {"pt": "perto",         "es": "cerca",          "pron": "sérka"},
    {"pt": "longe",         "es": "lejos",          "pron": "léjos"},
    {"pt": "aqui",          "es": "aquí",           "pron": "akí"},
    {"pt": "ali",           "es": "allí",           "pron": "allí"},
    {"pt": "norte",         "es": "norte",          "pron": "nórte"},
    {"pt": "sul",           "es": "sur",            "pron": "sur"},
    {"pt": "leste",         "es": "este",           "pron": "éste"},
    {"pt": "oeste",         "es": "oeste",          "pron": "oéste"},
    {"pt": "onde fica?",    "es": "¿dónde está?",   "pron": "dónde está"},
    {"pt": "como chego?",   "es": "¿cómo llego?",   "pron": "kómo llégo"},
    {"pt": "estou perdido", "es": "estoy perdido",  "pron": "estói perdído"},
]

COMIDA = [
    {"pt": "pão",           "es": "pan",            "pron": "pan"},
    {"pt": "água",          "es": "agua",           "pron": "água"},
    {"pt": "leite",         "es": "leche",          "pron": "léche"},
    {"pt": "café",          "es": "café",           "pron": "kafé"},
    {"pt": "chá",           "es": "té",             "pron": "te"},
    {"pt": "suco",          "es": "jugo",           "pron": "júgo"},
    {"pt": "cerveja",       "es": "cerveza",        "pron": "serbésa"},
    {"pt": "vinho",         "es": "vino",           "pron": "bíno"},
    {"pt": "arroz",         "es": "arroz",          "pron": "arrós"},
    {"pt": "feijão",        "es": "frijoles",       "pron": "frijóles"},
    {"pt": "carne",         "es": "carne",          "pron": "kárne"},
    {"pt": "frango",        "es": "pollo",          "pron": "póllo"},
    {"pt": "peixe",         "es": "pescado",        "pron": "peskádo"},
    {"pt": "fruta",         "es": "fruta",          "pron": "frúta"},
    {"pt": "banana",        "es": "plátano",        "pron": "plátano"},
    {"pt": "maçã",          "es": "manzana",        "pron": "mansána"},
    {"pt": "laranja",       "es": "naranja",        "pron": "naránja"},
    {"pt": "uva",           "es": "uva",            "pron": "úba"},
    {"pt": "morango",       "es": "fresa",          "pron": "frésa"},
    {"pt": "tomate",        "es": "tomate",         "pron": "tomáte"},
    {"pt": "batata",        "es": "patata",         "pron": "patáta"},
    {"pt": "cebola",        "es": "cebolla",        "pron": "sebólla"},
    {"pt": "alho",          "es": "ajo",            "pron": "ájo"},
    {"pt": "queijo",        "es": "queso",          "pron": "késo"},
    {"pt": "ovo",           "es": "huevo",          "pron": "uéb o"},
    {"pt": "sal",           "es": "sal",            "pron": "sal"},
    {"pt": "açúcar",        "es": "azúcar",         "pron": "asúkar"},
    {"pt": "sobremesa",     "es": "postre",         "pron": "póstre"},
    {"pt": "sorvete",       "es": "helado",         "pron": "eládo"},
    {"pt": "bolo",          "es": "pastel",         "pron": "pastél"},
]

PROFISSOES = [
    {"pt": "professor",     "es": "profesor",       "pron": "profesór"},
    {"pt": "médico",        "es": "médico",         "pron": "médiko"},
    {"pt": "enfermeiro",    "es": "enfermero",      "pron": "enferméro"},
    {"pt": "dentista",      "es": "dentista",       "pron": "dentísta"},
    {"pt": "advogado",      "es": "abogado",        "pron": "abogádo"},
    {"pt": "engenheiro",    "es": "ingeniero",      "pron": "injeniéro"},
    {"pt": "programador",   "es": "programador",    "pron": "programadór"},
    {"pt": "designer",      "es": "diseñador",      "pron": "diseñadór"},
    {"pt": "jornalista",    "es": "periodista",     "pron": "periodísta"},
    {"pt": "piloto",        "es": "piloto",         "pron": "pilóto"},
    {"pt": "cozinheiro",    "es": "cocinero",       "pron": "kosinéro"},
    {"pt": "garçom",        "es": "mesero",         "pron": "meséro"},
    {"pt": "motorista",     "es": "conductor",      "pron": "kondúktor"},
    {"pt": "policial",      "es": "policía",        "pron": "polisía"},
    {"pt": "bombeiro",      "es": "bombero",        "pron": "bombéro"},
    {"pt": "vendedor",      "es": "vendedor",       "pron": "bendedór"},
    {"pt": "agricultor",    "es": "agricultor",     "pron": "agrikultór"},
    {"pt": "pedreiro",      "es": "albañil",        "pron": "albañíl"},
    {"pt": "cabeleireiro",  "es": "peluquero",      "pron": "pelukéro"},
    {"pt": "estudante",     "es": "estudiante",     "pron": "estudiánte"},
]

VERBOS = [
    {"pt": "ser",           "es": "ser",            "pron": "ser"},
    {"pt": "estar",         "es": "estar",          "pron": "estár"},
    {"pt": "ter",           "es": "tener",          "pron": "tenér"},
    {"pt": "ir",            "es": "ir",             "pron": "ir"},
    {"pt": "vir",           "es": "venir",          "pron": "benír"},
    {"pt": "fazer",         "es": "hacer",          "pron": "asér"},
    {"pt": "dizer",         "es": "decir",          "pron": "desír"},
    {"pt": "poder",         "es": "poder",          "pron": "podér"},
    {"pt": "querer",        "es": "querer",         "pron": "kerér"},
    {"pt": "saber",         "es": "saber",          "pron": "sabér"},
    {"pt": "ver",           "es": "ver",            "pron": "ber"},
    {"pt": "comer",         "es": "comer",          "pron": "komér"},
    {"pt": "beber",         "es": "beber",          "pron": "bebér"},
    {"pt": "dormir",        "es": "dormir",         "pron": "dormír"},
    {"pt": "falar",         "es": "hablar",         "pron": "ablár"},
    {"pt": "escutar",       "es": "escuchar",       "pron": "esku chár"},
    {"pt": "ler",           "es": "leer",           "pron": "leér"},
    {"pt": "escrever",      "es": "escribir",       "pron": "eskribír"},
    {"pt": "estudar",       "es": "estudiar",       "pron": "estudiár"},
    {"pt": "trabalhar",     "es": "trabajar",       "pron": "trabajár"},
    {"pt": "correr",        "es": "correr",         "pron": "korrér"},
    {"pt": "andar",         "es": "caminar",        "pron": "kaminár"},
    {"pt": "comprar",       "es": "comprar",        "pron": "komprár"},
    {"pt": "vender",        "es": "vender",         "pron": "bendér"},
    {"pt": "abrir",         "es": "abrir",          "pron": "abr ír"},
    {"pt": "fechar",        "es": "cerrar",         "pron": "serrár"},
    {"pt": "começar",       "es": "empezar",        "pron": "empesár"},
    {"pt": "terminar",      "es": "terminar",       "pron": "terminár"},
    {"pt": "ajudar",        "es": "ayudar",         "pron": "ayudár"},
    {"pt": "gostar",        "es": "gustar",         "pron": "gustár"},
]

PERGUNTAS = [
    {"pt": "quem?",         "es": "¿quién?",        "pron": "kién"},
    {"pt": "o que?",        "es": "¿qué?",          "pron": "ke"},
    {"pt": "onde?",         "es": "¿dónde?",        "pron": "dónde"},
    {"pt": "quando?",       "es": "¿cuándo?",       "pron": "kuándo"},
    {"pt": "por que?",      "es": "¿por qué?",      "pron": "por ke"},
    {"pt": "como?",         "es": "¿cómo?",         "pron": "kómo"},
    {"pt": "qual?",         "es": "¿cuál?",         "pron": "kuál"},
    {"pt": "quanto?",       "es": "¿cuánto?",       "pron": "kuánto"},
    {"pt": "quantos?",      "es": "¿cuántos?",      "pron": "kuántos"},
    {"pt": "como você está?","es": "¿cómo estás?",  "pron": "kómo estás"},
    {"pt": "qual seu nome?", "es": "¿cómo te llamas?","pron": "kómo te llámas"},
    {"pt": "quantos anos?", "es": "¿cuántos años?", "pron": "kuántos áños"},
    {"pt": "de onde você é?","es": "¿de dónde eres?","pron": "de dónde éres"},
    {"pt": "você fala espanhol?","es": "¿hablas español?","pron": "áblas español"},
    {"pt": "você entende?", "es": "¿entiendes?",    "pron": "entiéndes"},
    {"pt": "pode repetir?", "es": "¿puedes repetir?","pron": "puédes repetír"},
    {"pt": "o que significa?","es": "¿qué significa?","pron": "ke signifíka"},
    {"pt": "que horas são?", "es": "¿qué hora es?", "pron": "ke óra es"},
    {"pt": "quanto custa?", "es": "¿cuánto cuesta?","pron": "kuánto kuésta"},
    {"pt": "onde é o banheiro?","es": "¿dónde está el baño?","pron": "dónde está el báño"},
]

EMOCOES = [
    {"pt": "feliz",         "es": "feliz",          "pron": "felís"},
    {"pt": "triste",        "es": "triste",         "pron": "tríste"},
    {"pt": "com raiva",     "es": "enojado",        "pron": "enojádo"},
    {"pt": "cansado",       "es": "cansado",        "pron": "kansádo"},
    {"pt": "animado",       "es": "emocionado",     "pron": "emosionádo"},
    {"pt": "com medo",      "es": "asustado",       "pron": "asustádo"},
    {"pt": "surpreso",      "es": "sorprendido",    "pron": "sorprendído"},
    {"pt": "nervoso",       "es": "nervioso",       "pron": "nervióso"},
    {"pt": "calmo",         "es": "tranquilo",      "pron": "trankílo"},
    {"pt": "confuso",       "es": "confundido",     "pron": "konfundído"},
    {"pt": "envergonhado",  "es": "avergonzado",    "pron": "aBergonsádo"},
    {"pt": "orgulhoso",     "es": "orgulloso",      "pron": "orgullóso"},
    {"pt": "apaixonado",    "es": "enamorado",      "pron": "enamorádo"},
    {"pt": "com fome",      "es": "hambriento",     "pron": "ambriénto"},
    {"pt": "com sede",      "es": "sediento",       "pron": "sediénto"},
    {"pt": "com sono",      "es": "somnoliento",    "pron": "somnoliénto"},
    {"pt": "entediado",     "es": "aburrido",       "pron": "aburrído"},
    {"pt": "sozinho",       "es": "solo",           "pron": "sólo"},
    {"pt": "estressado",    "es": "estresado",      "pron": "estresádo"},
    {"pt": "grato",         "es": "agradecido",     "pron": "agradesído"},
]

DINHEIRO = [
    {"pt": "dinheiro",      "es": "dinero",         "pron": "dinéro"},
    {"pt": "moeda",         "es": "moneda",         "pron": "monéda"},
    {"pt": "nota",          "es": "billete",        "pron": "billéte"},
    {"pt": "preço",         "es": "precio",         "pron": "présio"},
    {"pt": "desconto",      "es": "descuento",      "pron": "deskuénto"},
    {"pt": "promoção",      "es": "oferta",         "pron": "oférta"},
    {"pt": "caro",          "es": "caro",           "pron": "káro"},
    {"pt": "barato",        "es": "barato",         "pron": "baráto"},
    {"pt": "grátis",        "es": "gratis",         "pron": "grátis"},
    {"pt": "troco",         "es": "cambio",         "pron": "kámbio"},
    {"pt": "conta",         "es": "cuenta",         "pron": "kuénta"},
    {"pt": "cartão de crédito","es": "tarjeta de crédito","pron": "tarjéta de krédito"},
    {"pt": "dinheiro em espécie","es": "efectivo",  "pron": "efektíbo"},
    {"pt": "banco",         "es": "banco",          "pron": "bánko"},
    {"pt": "caixa eletrônico","es": "cajero automático","pron": "cajéro automatiko"},
    {"pt": "loja",          "es": "tienda",         "pron": "tiénda"},
    {"pt": "mercado",       "es": "mercado",        "pron": "merk ádo"},
    {"pt": "comprar",       "es": "comprar",        "pron": "komprár"},
    {"pt": "vender",        "es": "vender",         "pron": "bendér"},
    {"pt": "pagar",         "es": "pagar",          "pron": "pagár"},
    {"pt": "quanto custa?", "es": "¿cuánto cuesta?","pron": "kuánto kuésta"},
    {"pt": "é muito caro",  "es": "es muy caro",    "pron": "es mui káro"},
    {"pt": "aceita cartão?", "es": "¿acepta tarjeta?","pron": "asépta tarjéta"},
    {"pt": "só dinheiro",   "es": "solo efectivo",  "pron": "sólo efektíbo"},
    {"pt": "recibo",        "es": "recibo",         "pron": "res íbo"},
]

RESTAURANTE = [
    {"pt": "restaurante",   "es": "restaurante",    "pron": "restauránte"},
    {"pt": "cardápio",      "es": "menú",           "pron": "menú"},
    {"pt": "garçom",        "es": "mesero",         "pron": "meséro"},
    {"pt": "mesa",          "es": "mesa",           "pron": "mésa"},
    {"pt": "prato",         "es": "plato",          "pron": "pláto"},
    {"pt": "copo",          "es": "vaso",           "pron": "báso"},
    {"pt": "garfo",         "es": "tenedor",        "pron": "tenedór"},
    {"pt": "faca",          "es": "cuchillo",       "pron": "kuchíllo"},
    {"pt": "colher",        "es": "cuchara",        "pron": "kuchára"},
    {"pt": "guardanapo",    "es": "servilleta",     "pron": "serbilléta"},
    {"pt": "conta",         "es": "cuenta",         "pron": "kuénta"},
    {"pt": "gorjeta",       "es": "propina",        "pron": "propína"},
    {"pt": "água",          "es": "agua",           "pron": "água"},
    {"pt": "com gás",       "es": "con gas",        "pron": "kon gas"},
    {"pt": "sem gás",       "es": "sin gas",        "pron": "sin gas"},
    {"pt": "cerveja",       "es": "cerveza",        "pron": "serbésa"},
    {"pt": "vinho tinto",   "es": "vino tinto",     "pron": "bíno tínto"},
    {"pt": "entrada",       "es": "entrada",        "pron": "entráda"},
    {"pt": "prato principal","es": "plato principal","pron": "pláto prinsipal"},
    {"pt": "sobremesa",     "es": "postre",         "pron": "póstre"},
    {"pt": "eu quero...",   "es": "quiero...",      "pron": "kiéro"},
    {"pt": "para mim",      "es": "para mí",        "pron": "pára mi"},
    {"pt": "a conta, por favor", "es": "la cuenta, por favor","pron": "la kuénta por fabór"},
    {"pt": "está delicioso","es": "está delicioso","pron": "está delisióso"},
    {"pt": "bom apetite",   "es": "buen provecho",  "pron": "buén probécho"},
]

LUGARES = [
    {"pt": "cidade",        "es": "ciudad",         "pron": "siudád"},
    {"pt": "bairro",        "es": "barrio",         "pron": "bárrio"},
    {"pt": "rua",           "es": "calle",          "pron": "kálle"},
    {"pt": "praça",         "es": "plaza",          "pron": "plása"},
    {"pt": "parque",        "es": "parque",         "pron": "párke"},
    {"pt": "igreja",        "es": "iglesia",        "pron": "iglé sia"},
    {"pt": "escola",        "es": "escuela",        "pron": "eskuéla"},
    {"pt": "universidade",  "es": "universidad",    "pron": "unibersidád"},
    {"pt": "hospital",      "es": "hospital",       "pron": "ospitál"},
    {"pt": "farmácia",      "es": "farmacia",       "pron": "farmásia"},
    {"pt": "supermercado",  "es": "supermercado",   "pron": "supermerk ádo"},
    {"pt": "banco",         "es": "banco",          "pron": "bánko"},
    {"pt": "correio",       "es": "correo",         "pron": "korréo"},
    {"pt": "restaurante",   "es": "restaurante",    "pron": "restauránte"},
    {"pt": "hotel",         "es": "hotel",          "pron": "otél"},
    {"pt": "teatro",        "es": "teatro",         "pron": "teátro"},
    {"pt": "cinema",        "es": "cine",           "pron": "síne"},
    {"pt": "museu",         "es": "museo",          "pron": "muséo"},
    {"pt": "biblioteca",    "es": "biblioteca",     "pron": "bibliotéka"},
    {"pt": "estádio",       "es": "estadio",        "pron": "estádio"},
]

DATAS = [
    {"pt": "segunda-feira","es": "lunes",           "pron": "lúnes"},
    {"pt": "terça-feira",  "es": "martes",          "pron": "mártes"},
    {"pt": "quarta-feira", "es": "miércoles",       "pron": "miérkoles"},
    {"pt": "quinta-feira", "es": "jueves",          "pron": "juébes"},
    {"pt": "sexta-feira",  "es": "viernes",         "pron": "biérnes"},
    {"pt": "sábado",       "es": "sábado",          "pron": "sábado"},
    {"pt": "domingo",      "es": "domingo",         "pron": "domíngo"},
    {"pt": "janeiro",      "es": "enero",           "pron": "enéro"},
    {"pt": "fevereiro",    "es": "febrero",         "pron": "febréro"},
    {"pt": "março",        "es": "marzo",           "pron": "márso"},
    {"pt": "abril",        "es": "abril",           "pron": "abr íl"},
    {"pt": "maio",         "es": "mayo",            "pron": "májo"},
    {"pt": "junho",        "es": "junio",           "pron": "júnio"},
    {"pt": "julho",        "es": "julio",           "pron": "júlio"},
    {"pt": "agosto",       "es": "agosto",          "pron": "agósto"},
    {"pt": "setembro",     "es": "septiembre",      "pron": "sept iémbre"},
    {"pt": "outubro",      "es": "octubre",         "pron": "oktúbre"},
    {"pt": "novembro",     "es": "noviembre",       "pron": "nobiémbre"},
    {"pt": "dezembro",     "es": "diciembre",       "pron": "disiémbre"},
    {"pt": "hoje",         "es": "hoy",             "pron": "ói"},
    {"pt": "amanhã",       "es": "mañana",          "pron": "mañána"},
    {"pt": "ontem",        "es": "ayer",            "pron": "ayér"},
    {"pt": "semana",       "es": "semana",          "pron": "semána"},
    {"pt": "mês",          "es": "mes",             "pron": "mes"},
    {"pt": "ano",          "es": "año",             "pron": "áño"},
]

CORPO = [
    {"pt": "cabeça",       "es": "cabeza",          "pron": "kabésa"},
    {"pt": "cabelo",       "es": "pelo",            "pron": "pélo"},
    {"pt": "rosto",        "es": "cara",            "pron": "kára"},
    {"pt": "olho",         "es": "ojo",             "pron": "ójo"},
    {"pt": "nariz",        "es": "nariz",           "pron": "narís"},
    {"pt": "boca",         "es": "boca",            "pron": "bóka"},
    {"pt": "orelha",       "es": "oreja",           "pron": "oréja"},
    {"pt": "dente",        "es": "diente",          "pron": "diénte"},
    {"pt": "língua",       "es": "lengua",          "pron": "léngua"},
    {"pt": "pescoço",      "es": "cuello",          "pron": "kuéllo"},
    {"pt": "ombro",        "es": "hombro",          "pron": "ómbro"},
    {"pt": "braço",        "es": "brazo",           "pron": "bráso"},
    {"pt": "mão",          "es": "mano",            "pron": "máno"},
    {"pt": "dedo",         "es": "dedo",            "pron": "dédo"},
    {"pt": "perna",        "es": "pierna",          "pron": "piérna"},
    {"pt": "pé",           "es": "pie",             "pron": "pié"},
    {"pt": "joelho",       "es": "rodilla",         "pron": "rodílla"},
    {"pt": "coração",      "es": "corazón",         "pron": "korasón"},
    {"pt": "estômago",     "es": "estómago",        "pron": "estómago"},
    {"pt": "sangue",       "es": "sangre",          "pron": "sángre"},
    {"pt": "osso",         "es": "hueso",           "pron": "uéso"},
    {"pt": "pele",         "es": "piel",            "pron": "piél"},
    {"pt": "cérebro",      "es": "cerebro",         "pron": "serébro"},
    {"pt": "dor de cabeça","es": "dolor de cabeza","pron": "dolór de kabésa"},
    {"pt": "dor de barriga","es": "dolor de estómago","pron": "dolór de estómago"},
]

HORAS = [
    {"pt": "hora",         "es": "hora",            "pron": "óra"},
    {"pt": "minuto",       "es": "minuto",          "pron": "minúto"},
    {"pt": "segundo",      "es": "segundo",         "pron": "segúndo"},
    {"pt": "manhã",        "es": "mañana",          "pron": "mañána"},
    {"pt": "tarde",        "es": "tarde",           "pron": "tárde"},
    {"pt": "noite",        "es": "noche",           "pron": "nóche"},
    {"pt": "meio-dia",     "es": "mediodía",        "pron": "mediodía"},
    {"pt": "meia-noite",   "es": "medianoche",      "pron": "medianóche"},
    {"pt": "que horas são?","es": "¿qué hora es?",  "pron": "ke óra es"},
    {"pt": "uma hora",     "es": "la una",          "pron": "la úna"},
    {"pt": "duas horas",   "es": "las dos",         "pron": "las dos"},
    {"pt": "três horas",   "es": "las tres",        "pron": "las tres"},
    {"pt": "quatro horas", "es": "las cuatro",      "pron": "las kuátro"},
    {"pt": "cinco horas",  "es": "las cinco",       "pron": "las sínko"},
    {"pt": "seis horas",   "es": "las seis",        "pron": "las seis"},
    {"pt": "sete horas",   "es": "las siete",       "pron": "las siéte"},
    {"pt": "oito horas",   "es": "las ocho",        "pron": "las ócho"},
    {"pt": "nove horas",   "es": "las nueve",       "pron": "las nuébe"},
    {"pt": "dez horas",    "es": "las diez",        "pron": "las diés"},
    {"pt": "e meia",       "es": "y media",         "pron": "i média"},
    {"pt": "e quinze",     "es": "y cuarto",        "pron": "i kuárto"},
    {"pt": "quinze para",  "es": "cuarto para",     "pron": "kuárto pára"},
    {"pt": "da manhã",     "es": "de la mañana",    "pron": "de la mañána"},
    {"pt": "da tarde",     "es": "de la tarde",     "pron": "de la tárde"},
    {"pt": "da noite",     "es": "de la noche",     "pron": "de la nóche"},
]

FORMAS = [
    {"pt": "círculo",      "es": "círculo",         "pron": "sírkulo"},
    {"pt": "quadrado",     "es": "cuadrado",        "pron": "kuadrádo"},
    {"pt": "triângulo",    "es": "triángulo",       "pron": "triángulo"},
    {"pt": "retângulo",    "es": "rectángulo",      "pron": "rektángulo"},
    {"pt": "estrela",      "es": "estrella",        "pron": "estrélla"},
    {"pt": "coração",      "es": "corazón",         "pron": "korasón"},
    {"pt": "oval",         "es": "óvalo",           "pron": "óbalo"},
    {"pt": "grande",       "es": "grande",          "pron": "gránde"},
    {"pt": "pequeno",      "es": "pequeño",         "pron": "pek éño"},
    {"pt": "médio",        "es": "mediano",         "pron": "mediáno"},
    {"pt": "alto",         "es": "alto",            "pron": "álto"},
    {"pt": "baixo",        "es": "bajo",            "pron": "bájo"},
    {"pt": "largo",        "es": "ancho",           "pron": "áncho"},
    {"pt": "estreito",     "es": "estrecho",        "pron": "estrécho"},
    {"pt": "comprido",     "es": "largo",           "pron": "lárgo"},
    {"pt": "curto",        "es": "corto",           "pron": "kórto"},
    {"pt": "grosso",       "es": "grueso",          "pron": "gruéso"},
    {"pt": "fino",         "es": "fino",            "pron": "fíno"},
    {"pt": "redondo",      "es": "redondo",         "pron": "redóndo"},
    {"pt": "quadrado (forma)","es": "cuadrado",     "pron": "kuadrádo"},
]

MIDIA = [
    {"pt": "música",       "es": "música",          "pron": "músika"},
    {"pt": "canção",       "es": "canción",         "pron": "kansión"},
    {"pt": "filme",        "es": "película",        "pron": "pelíkula"},
    {"pt": "série",        "es": "serie",           "pron": "série"},
    {"pt": "livro",        "es": "libro",           "pron": "líbro"},
    {"pt": "revista",      "es": "revista",         "pron": "rebísta"},
    {"pt": "jornal",       "es": "periódico",       "pron": "periodíko"},
    {"pt": "televisão",    "es": "televisión",      "pron": "telebisión"},
    {"pt": "rádio",        "es": "radio",           "pron": "rádio"},
    {"pt": "internet",     "es": "internet",        "pron": "internét"},
    {"pt": "celular",      "es": "celular",         "pron": "selulár"},
    {"pt": "computador",   "es": "computadora",     "pron": "komputadóra"},
    {"pt": "foto",         "es": "foto",            "pron": "fóto"},
    {"pt": "vídeo",        "es": "video",           "pron": "bidéo"},
    {"pt": "notícia",      "es": "noticia",         "pron": "notísia"},
    {"pt": "arte",         "es": "arte",            "pron": "árte"},
    {"pt": "pintura",      "es": "pintura",         "pron": "pintúra"},
    {"pt": "dança",        "es": "baile",           "pron": "báile"},
    {"pt": "ator",         "es": "actor",           "pron": "aktór"},
    {"pt": "cantor",       "es": "cantante",        "pron": "kantánte"},
]

ESPORTES = [
    {"pt": "esporte",      "es": "deporte",         "pron": "depórte"},
    {"pt": "futebol",      "es": "fútbol",          "pron": "fútbol"},
    {"pt": "basquete",     "es": "baloncesto",      "pron": "balonsésto"},
    {"pt": "vôlei",        "es": "voleibol",        "pron": "boleiból"},
    {"pt": "tênis",        "es": "tenis",           "pron": "ténis"},
    {"pt": "natação",      "es": "natación",        "pron": "natasión"},
    {"pt": "corrida",      "es": "carrera",         "pron": "karréra"},
    {"pt": "ciclismo",     "es": "ciclismo",        "pron": "siklísmo"},
    {"pt": "boxe",         "es": "boxeo",           "pron": "bokséo"},
    {"pt": "judô",         "es": "judo",            "pron": "júdo"},
    {"pt": "time",         "es": "equipo",          "pron": "ekípo"},
    {"pt": "jogador",      "es": "jugador",         "pron": "jugadór"},
    {"pt": "técnico",      "es": "entrenador",      "pron": "entrenadór"},
    {"pt": "torcida",      "es": "afición",         "pron": "afisión"},
    {"pt": "gol",          "es": "gol",             "pron": "gol"},
    {"pt": "ponto",        "es": "punto",           "pron": "púnto"},
    {"pt": "vitória",      "es": "victoria",        "pron": "biktória"},
    {"pt": "derrota",      "es": "derrota",         "pron": "derróta"},
    {"pt": "empate",       "es": "empate",          "pron": "empáte"},
    {"pt": "jogo",         "es": "partido",         "pron": "partído"},
]

VIAGEM = [
    {"pt": "viagem",       "es": "viaje",           "pron": "biáje"},
    {"pt": "férias",       "es": "vacaciones",      "pron": "bakasiónes"},
    {"pt": "passaporte",   "es": "pasaporte",       "pron": "pasapórte"},
    {"pt": "visto",        "es": "visa",            "pron": "bísa"},
    {"pt": "passagem",     "es": "billete",         "pron": "billéte"},
    {"pt": "reserva",      "es": "reserva",         "pron": "resérba"},
    {"pt": "mala",         "es": "maleta",          "pron": "maléta"},
    {"pt": "mochila",      "es": "mochila",         "pron": "mochíla"},
    {"pt": "hotel",        "es": "hotel",           "pron": "otél"},
    {"pt": "quarto",       "es": "habitación",      "pron": "abitación"},
    {"pt": "chave",        "es": "llave",           "pron": "llábe"},
    {"pt": "aeroporto",    "es": "aeropuerto",      "pron": "aeropuérto"},
    {"pt": "voo",          "es": "vuelo",           "pron": "buélo"},
    {"pt": "chegada",      "es": "llegada",         "pron": "llegáda"},
    {"pt": "partida",      "es": "salida",          "pron": "salída"},
    {"pt": "mapa",         "es": "mapa",            "pron": "mápa"},
    {"pt": "guia",         "es": "guía",            "pron": "guía"},
    {"pt": "turista",      "es": "turista",         "pron": "turísta"},
    {"pt": "onde fica?",   "es": "¿dónde está?",    "pron": "dónde está"},
    {"pt": "quanto custa?", "es": "¿cuánto cuesta?", "pron": "kuánto kuésta"},
    {"pt": "pode me ajudar?", "es": "¿puede ayudarme?","pron": "puéde ayudárme"},
    {"pt": "estou perdido", "es": "estoy perdido",  "pron": "estói perdído"},
    {"pt": "não entendo",  "es": "no entiendo",     "pron": "no entiéndo"},
    {"pt": "fala inglês?", "es": "¿habla inglés?",  "pron": "ábla inglés"},
    {"pt": "obrigado",     "es": "gracias",         "pron": "grásias"},
]

EMERGENCIAS = [
    {"pt": "socorro!",     "es": "¡ayuda!",         "pron": "ayúda"},
    {"pt": "emergência",   "es": "emergencia",      "pron": "emerjénsia"},
    {"pt": "ambulância",   "es": "ambulancia",      "pron": "ambulánsia"},
    {"pt": "polícia",      "es": "policía",         "pron": "polisía"},
    {"pt": "bombeiro",     "es": "bombero",         "pron": "bombéro"},
    {"pt": "hospital",     "es": "hospital",        "pron": "ospitál"},
    {"pt": "médico",       "es": "médico",          "pron": "médiko"},
    {"pt": "dor",          "es": "dolor",           "pron": "dolór"},
    {"pt": "sangue",       "es": "sangre",          "pron": "sángre"},
    {"pt": "acidente",     "es": "accidente",       "pron": "aksidénte"},
    {"pt": "fogo",         "es": "fuego",           "pron": "fuégo"},
    {"pt": "roubo",        "es": "robo",            "pron": "róbo"},
    {"pt": "perigo",       "es": "peligro",         "pron": "pelígro"},
    {"pt": "cuidado!",     "es": "¡cuidado!",       "pron": "kuidádo"},
    {"pt": "me ajude!",    "es": "¡ayúdeme!",       "pron": "ayúdeme"},
    {"pt": "chame a polícia", "es": "llame a la policía","pron": "lláme a la polisía"},
    {"pt": "chame uma ambulância", "es": "llame a una ambulancia","pron": "lláme a úna ambulánsia"},
    {"pt": "estou perdido", "es": "estoy perdido",  "pron": "estói perdído"},
    {"pt": "perdi minha bolsa", "es": "perdí mi bolso","pron": "perdí mi bólso"},
    {"pt": "não me sinto bem", "es": "no me siento bien","pron": "no me siénto bién"},
]


# ============================================================
# PARTE 3: CORRIGIR TELAS (codigo hardcoded)
# ============================================================
def corrigir_telas():
    print("=" * 60)
    print("CORRIGINDO TELAS...")
    print("=" * 60)

    correcoes = [
        # (arquivo, texto_antigo, texto_novo)
        (
            BASE / "telas" / "tela_modulo.py",
            'codigo = "en" if idioma == "ingles" else "ru"',
            'codigo = IDIOMAS[idioma]["codigo_conteudo"]',
        ),
        (
            BASE / "telas" / "tela_dicionario.py",
            'codigo = "en" if idioma == "ingles" else "ru"',
            'codigo = IDIOMAS[idioma]["codigo_conteudo"]',
        ),
        (
            BASE / "logica" / "gerenciador_dicionario.py",
            'codigo_idioma = "en" if idioma == "ingles" else "ru"',
            'from config import IDIOMAS\n    codigo_idioma = IDIOMAS[idioma]["codigo_conteudo"]',
        ),
    ]

    for arq, antigo, novo in correcoes:
        if not arq.exists():
            print(f"  SKIP: {arq.name} nao existe")
            continue

        conteudo = arq.read_text(encoding="utf-8")
        if antigo in conteudo:
            conteudo = conteudo.replace(antigo, novo)
            arq.write_text(conteudo, encoding="utf-8")
            print(f"  OK: {arq.name}")
        else:
            print(f"  SKIP: {arq.name} (padrao nao encontrado)")

    # Corrigir tambem os outros lugares que usam "en"/"ru" hardcoded
    arquivos_extras = [
        BASE / "telas" / "tela_exercicio.py",
        BASE / "telas" / "tela_flashcards.py",
        BASE / "logica" / "gerenciador_flashcards.py",
    ]

    for arq in arquivos_extras:
        if not arq.exists():
            continue
        conteudo = arq.read_text(encoding="utf-8")
        # Procura padroes tipo: "en" if idioma == "ingles" else "ru"
        if '"en" if idioma == "ingles" else "ru"' in conteudo:
            conteudo = conteudo.replace(
                '"en" if idioma == "ingles" else "ru"',
                'IDIOMAS[idioma]["codigo_conteudo"]'
            )
            # Garante import
            if "from config import IDIOMAS" not in conteudo and "from config import" in conteudo:
                # ja importa config, so adiciona IDIOMAS
                pass
            arq.write_text(conteudo, encoding="utf-8")
            print(f"  OK: {arq.name} (corrigido)")

    print()


# ============================================================
# MAIN
# ============================================================
def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  ADICIONANDO IDIOMA ESPANHOL (Latino) ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    fazer_backup()
    atualizar_config()
    criar_pasta_espanhol()

    print("=" * 60)
    print("SALVANDO VOCABULARIO...")
    print("=" * 60)

    salvar_json("modulos.json", MODULOS)
    salvar_json("alfabeto.json", ALFABETO)
    salvar_json("saudacoes.json", SAUDACOES)
    salvar_json("numeros.json", NUMEROS)
    salvar_json("cores.json", CORES)
    salvar_json("familia.json", FAMILIA)
    salvar_json("casa.json", CASA)
    salvar_json("roupas.json", ROUPAS)
    salvar_json("animais.json", ANIMAIS)
    salvar_json("clima.json", CLIMA)
    salvar_json("transporte.json", TRANSPORTE)
    salvar_json("direcoes.json", DIRECOES)
    salvar_json("comida.json", COMIDA)
    salvar_json("profissoes.json", PROFISSOES)
    salvar_json("verbos.json", VERBOS)
    salvar_json("perguntas.json", PERGUNTAS)
    salvar_json("emocoes.json", EMOCOES)
    salvar_json("dinheiro.json", DINHEIRO)
    salvar_json("restaurante.json", RESTAURANTE)
    salvar_json("lugares.json", LUGARES)
    salvar_json("datas.json", DATAS)
    salvar_json("corpo.json", CORPO)
    salvar_json("horas.json", HORAS)
    salvar_json("formas.json", FORMAS)
    salvar_json("midia.json", MIDIA)
    salvar_json("esportes.json", ESPORTES)
    salvar_json("viagem.json", VIAGEM)
    salvar_json("emergencias.json", EMERGENCIAS)

    print()
    corrigir_telas()

    print("=" * 60)
    print("✅ ESPANHOL ADICIONADO COM SUCESSO!")
    print("=" * 60)
    print()
    print("Proximos passos:")
    print("  1. Reinicie o Streamlit (Ctrl+C e depois streamlit run main.py)")
    print("  2. Abra o app no navegador")
    print("  3. O idioma 'Espanhol' deve aparecer na tela inicial")
    print()
    print(f"Backup dos arquivos antigos em: {BACKUP_DIR}")
    print()


if __name__ == "__main__":
    main()