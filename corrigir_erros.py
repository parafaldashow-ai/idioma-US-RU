import json

def corrigir(arquivo, idx, novo_pt=None, novo_en=None, nova_pron=None):
    with open(arquivo, encoding='utf-8') as f:
        data = json.load(f)
    
    card = data[idx]
    print(f'ANTES:  pt="{card["pt"]}" en="{card["en"]}" pron="{card["pron"]}"')
    
    if novo_pt: card['pt'] = novo_pt
    if novo_en: card['en'] = novo_en
    if nova_pron: card['pron'] = nova_pron
    
    print(f'DEPOIS: pt="{card["pt"]}" en="{card["en"]}" pron="{card["pron"]}"\n')
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print('=== INGLÊS ===')
# 1. transporte.json[21]: fogão/rocket → foguete/rocket
corrigir('dados/ingles/transporte.json', 21, novo_pt='foguete')

# 2. formas.json[47]: médio-grande/large → médio-grande/medium-large
corrigir('dados/ingles/formas.json', 47, novo_en='medium-large', nova_pron='mídium lárj')

# 3. restaurante.json[67]: batida/milkshake → batida/batida
corrigir('dados/ingles/restaurante.json', 67, novo_en='batida', nova_pron='batída')

# 4. lugares.json[26]: dentista/dentist's office → consultório do dentista/dentist's office
corrigir('dados/ingles/lugares.json', 26, novo_pt='consultório do dentista')

print('=== RUSSO ===')
# Mesmos índices, mesmas correções (estrutura russa é igual)
corrigir('dados/russo/transporte.json', 21, novo_pt='foguete')
corrigir('dados/russo/formas.json', 47, novo_en='medium-large', nova_pron='mídium lárj')
corrigir('dados/russo/restaurante.json', 67, novo_en='batida', nova_pron='batída')
corrigir('dados/russo/lugares.json', 26, novo_pt='consultório do dentista')

print('✅ Correções concluídas!')