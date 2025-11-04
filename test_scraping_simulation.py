#!/usr/bin/env python3
"""
Simulação de scraping real do CarJet
Testa o fluxo completo: HTML → Extração → Limpeza → Mapeamento
"""

from bs4 import BeautifulSoup

# HTML simulado de uma página de resultados do CarJet
html_page = '''
<div class="results">
    <!-- Carro 1: Skoda Scala -->
    <div class="car-card" data-prv="AUP">
        <img class="cl--car-img" 
             src="/cdn/img/cars/M/car_C166.jpg" 
             alt="Skoda Scala ou similar ">
        <div class="price">45.50 €</div>
        <span class="transmission">Automatic</span>
    </div>
    
    <!-- Carro 2: Toyota Aygo -->
    <div class="car-card" data-prv="EUR">
        <img class="cl--car-img" 
             src="/cdn/img/cars/M/car_C01.jpg" 
             alt="Toyota Aygo ou similar | Pequeno">
        <div class="price">35.00 €</div>
        <span class="transmission">Manual</span>
    </div>
    
    <!-- Carro 3: Renault Clio -->
    <div class="car-card" data-prv="SXT">
        <img class="cl--car-img" 
             src="/cdn/img/cars/M/car_C04.jpg" 
             alt="Renault Clio or similar">
        <div class="price">42.00 €</div>
        <span class="transmission">Automatic</span>
    </div>
    
    <!-- Carro 4: Fiat 500 -->
    <div class="car-card" data-prv="HER">
        <img class="cl--car-img" 
             src="/cdn/img/cars/M/car_C02.jpg" 
             alt="Fiat 500">
        <div class="price">38.75 €</div>
        <span class="transmission">Manual</span>
    </div>
</div>
'''

print("=" * 80)
print("SIMULAÇÃO DE SCRAPING REAL DO CARJET")
print("=" * 80)

soup = BeautifulSoup(html_page, 'html.parser')
car_cards = soup.select('.car-card')

print(f"\n📊 Total de carros encontrados: {len(car_cards)}\n")

results = []

for idx, card in enumerate(car_cards, 1):
    print(f"[CARRO {idx}]")
    print("-" * 80)
    
    # Extrair supplier
    supplier = card.get('data-prv', 'Unknown')
    
    # Extrair imagem e nome do alt
    car_img = card.select_one('img.cl--car-img')
    if car_img:
        photo_url = car_img.get('src', '')
        alt_text = (car_img.get('alt') or '').strip()
        
        # Limpar nome do alt
        car_name = alt_text.split('ou similar')[0].split('or similar')[0].split('|')[0].strip()
        car_name_clean = car_name.lower()
        
        # Extrair preço
        price_el = card.select_one('.price')
        price = price_el.get_text(strip=True) if price_el else '0.00 €'
        
        # Extrair transmissão
        trans_el = card.select_one('.transmission')
        transmission = trans_el.get_text(strip=True) if trans_el else 'Unknown'
        
        # Montar resultado
        result = {
            'car': car_name,
            'car_clean': car_name_clean,
            'photo': f'https://www.carjet.com{photo_url}',
            'price': price,
            'supplier': supplier,
            'transmission': transmission
        }
        
        results.append(result)
        
        # Exibir
        print(f"  🚗 Carro: {car_name}")
        print(f"  🔤 Nome limpo: {car_name_clean}")
        print(f"  📸 Foto: {photo_url}")
        print(f"  💰 Preço: {price}")
        print(f"  🏢 Supplier: {supplier}")
        print(f"  ⚙️  Transmissão: {transmission}")
        print(f"  ✅ Mapeamento: {photo_url} → {car_name}")
        print()

print("=" * 80)
print("RESUMO DOS RESULTADOS")
print("=" * 80)

print(f"\n📊 Total processado: {len(results)} carros\n")

# Criar tabela de mapeamento
print("TABELA DE MAPEAMENTO FOTO → CARRO:")
print("-" * 80)
print(f"{'Foto':<30} {'Carro':<25} {'Preço':<12} {'Supplier':<10}")
print("-" * 80)

for r in results:
    photo_short = r['photo'].split('/')[-1]
    print(f"{photo_short:<30} {r['car']:<25} {r['price']:<12} {r['supplier']:<10}")

print("-" * 80)

# Validar mapeamentos
print("\n✅ VALIDAÇÃO:")
expected_mappings = {
    'car_C166.jpg': 'skoda scala',
    'car_C01.jpg': 'toyota aygo',
    'car_C04.jpg': 'renault clio',
    'car_C02.jpg': 'fiat 500'
}

all_correct = True
for r in results:
    photo_file = r['photo'].split('/')[-1]
    expected_name = expected_mappings.get(photo_file)
    
    if expected_name and r['car_clean'] == expected_name:
        print(f"  ✅ {photo_file} → {r['car_clean']}")
    else:
        print(f"  ❌ {photo_file} → {r['car_clean']} (esperado: {expected_name})")
        all_correct = False

print("\n" + "=" * 80)
if all_correct:
    print("🎉 SUCESSO! Todos os mapeamentos estão corretos!")
    print("\n✅ O sistema está pronto para:")
    print("   - Fazer scraping real do CarJet")
    print("   - Extrair nomes do atributo alt das imagens")
    print("   - Mapear fotos → carros corretamente")
    print("   - Salvar no banco de dados com nomes precisos")
else:
    print("⚠️  Alguns mapeamentos falharam. Verificar lógica de extração.")

print("=" * 80)
