import json

# {arquivo: [índices a remover]}
para_remover = {
    'dados/ingles/datas.json': [79],
    'dados/ingles/formas.json': [131],
    'dados/ingles/horas.json': [21],
    'dados/ingles/perguntas.json': [115],
    'dados/ingles/profissoes.json': [41],
    'dados/ingles/verbos.json': [130],
    'dados/ingles/viagem.json': [78, 106, 124],
}

# Versão russa — mesmos índices (mesma estrutura)
para_remover_ru = {
    'dados/russo/datas.json': [79],
    'dados/russo/formas.json': [131],
    'dados/russo/horas.json': [21],
    'dados/russo/perguntas.json': [115],
    'dados/russo/profissoes.json': [41],
    'dados/russo/verbos.json': [130],
    'dados/russo/viagem.json': [78, 106, 124],
}

def limpar(arquivo, indices):
    with open(arquivo, encoding='utf-8') as f:
        data = json.load(f)
    
    # Ordena do maior pro menor pra não deslocar índices
    for i in sorted(indices, reverse=True):
        print(f'  Removendo [{i}] {data[i].get("pt")}')
        del data[i]
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f'✅ {arquivo} limpo. Total: {len(data)} cards.\n')

print('=== INGLÊS ===')
for arq, idx in para_remover.items():
    print(f'{arq}:')
    limpar(arq, idx)

print('=== RUSSO ===')
for arq, idx in para_remover_ru.items():
    print(f'{arq}:')
    limpar(arq, idx)

print('🎉 Limpeza concluída!')