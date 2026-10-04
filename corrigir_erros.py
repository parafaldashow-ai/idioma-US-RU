import json

def corrigir(arquivo, idx, pt=None, en=None, ru=None, pron=None):
    with open(arquivo, encoding='utf-8') as f:
        data = json.load(f)
    
    card = data[idx]
    print(f'ANTES:  {card}')
    
    if pt: card['pt'] = pt
    if en: card['en'] = en
    if ru: card['ru'] = ru
    if pron: card['pron'] = pron
    
    print(f'DEPOIS: {card}\n')
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


print('=== INGLÊS ===')
# 1. transporte.json[21]: fogão/rocket → foguete/rocket
corrigir('dados/ingles/transporte.json', 21, pt='foguete')

# 2. formas.json[47]: médio-grande/large → médio-grande/medium-large
corrigir('dados/ingles/formas.json', 47, en='medium-large', pron='mídium lárj')

# 3. restaurante.json[67]: batida/milkshake → batida/batida
corrigir('dados/ingles/restaurante.json', 67, en='batida', pron='batída')

# 4. lugares.json[26]: dentista/dentist's office → consultório do dentista/dentist's office
corrigir('dados/ingles/lugares.json', 26, pt='consultório do dentista')


print('=== RUSSO ===')
# 1. transporte.json[21]: fogão/ракета → foguete/ракета
corrigir('dados/russo/transporte.json', 21, pt='foguete')

# 2. formas.json[47]: médio-grande/крупный → médio-grande/средне-крупный
corrigir('dados/russo/formas.json', 47, ru='средне-крупный', pron='sryédne krúpniy')

# 3. restaurante.json[67]: batida/молочный коктейль → batida/батида
corrigir('dados/russo/restaurante.json', 67, ru='батида', pron='batída')

# 4. lugares.json[26]: dentista/стоматология → consultório do dentista/стоматология
corrigir('dados/russo/lugares.json', 26, pt='consultório do dentista')

print('✅ Correções concluídas!')