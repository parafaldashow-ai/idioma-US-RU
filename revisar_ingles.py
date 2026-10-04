import json, glob, re
from collections import defaultdict

# Coletar todos os cards
todos = []
for f in sorted(glob.glob('dados/ingles/*.json')):
    with open(f, encoding='utf-8') as fp:
        data = json.load(fp)
    if isinstance(data, list):
        for i, card in enumerate(data):
            card['_arquivo'] = f
            card['_idx'] = i
            todos.append(card)

print(f'📊 Total de cards: {len(todos)}\n')

# 1. Palavras inglesas com pt diferentes
en_para_pt = defaultdict(set)
for c in todos:
    en_para_pt[c['en']].add(c['pt'])

print('=== 1. Palavras inglesas com traduções diferentes ===')
for en, pts in sorted(en_para_pt.items()):
    if len(pts) > 1:
        print(f'  "{en}": {sorted(pts)}')

# 2. Palavras portuguesas com en diferentes
pt_para_en = defaultdict(set)
for c in todos:
    pt_para_en[c['pt']].add(c['en'])

print('\n=== 2. Palavras portuguesas com traduções diferentes ===')
for pt, ens in sorted(pt_para_en.items()):
    if len(ens) > 1:
        print(f'  "{pt}": {sorted(ens)}')

# 3. pt e en iguais (possível falta de tradução)
print('\n=== 3. Cards com pt e en iguais ===')
for c in todos:
    if c['pt'].lower() == c['en'].lower():
        print(f'  {c["_arquivo"]}[{c["_idx"]}]: {c["pt"]} = {c["en"]}')

# 4. en com acento (não existe em inglês)
print('\n=== 4. Palavras em inglês com acento ===')
for c in todos:
    if re.search(r'[áàâãéêíóôõúç]', c['en'].lower()):
        print(f'  {c["_arquivo"]}[{c["_idx"]}]: pt="{c["pt"]}" en="{c["en"]}"')