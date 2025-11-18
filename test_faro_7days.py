"""
Teste: Pesquisa de 7 dias no Aeroporto de Faro com requests
"""
from datetime import datetime, timedelta
from carjet_requests import scrape_carjet_requests
import json

print("=" * 80)
print("🔬 TESTE: AEROPORTO DE FARO - 7 DIAS")
print("=" * 80)

# Datas: daqui a 7 dias por 7 dias
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=7)

print(f"📍 Local: Aeroporto de Faro")
print(f"📅 Check-in:  {start_dt.strftime('%d/%m/%Y às %H:%M')}")
print(f"📅 Check-out: {end_dt.strftime('%d/%m/%Y às %H:%M')}")
print(f"⏱️  Duração: 7 dias")
print("=" * 80)
print()

# Fazer scraping
results = scrape_carjet_requests('Aeroporto de Faro', start_dt, end_dt)

print()
print("=" * 80)
print(f"✅ RESULTADO: {len(results)} carros encontrados")
print("=" * 80)

if results:
    # Salvar JSON completo
    with open('results_faro_7days.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Resultados completos salvos em: results_faro_7days.json")
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    
    # Por transmissão
    manual = sum(1 for r in results if r.get('transmission') == 'Manual')
    automatic = sum(1 for r in results if r.get('transmission') == 'Automatic')
    print(f"   🔧 Manual: {manual}")
    print(f"   ⚙️  Automático: {automatic}")
    
    # Por categoria
    categories = {}
    for r in results:
        cat = r.get('category', 'N/A')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n   📂 Por categoria:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"      {cat}: {count}")
    
    # Por supplier
    suppliers = {}
    for r in results:
        sup = r.get('supplier', 'N/A')
        suppliers[sup] = suppliers.get(sup, 0) + 1
    
    print(f"\n   🏢 Por fornecedor (Top 10):")
    for sup, count in sorted(suppliers.items(), key=lambda x: -x[1])[:10]:
        print(f"      {sup}: {count}")
    
    # Preços
    prices = []
    for r in results:
        price_str = r.get('price', '')
        if price_str and '€' in price_str:
            try:
                # Extrair número do preço
                price_val = float(price_str.replace('€', '').replace(',', '.').strip())
                prices.append(price_val)
            except:
                pass
    
    if prices:
        print(f"\n   💰 Preços:")
        print(f"      Mínimo: {min(prices):.2f} €")
        print(f"      Máximo: {max(prices):.2f} €")
        print(f"      Médio:  {sum(prices)/len(prices):.2f} €")
    
    # Mostrar primeiros 10 carros
    print(f"\n📋 PRIMEIROS 10 CARROS:")
    print()
    
    for i, car in enumerate(results[:10]):
        print(f"{i+1:2}. {car.get('car', 'N/A'):<45} | {car.get('price', 'N/A'):>12} | {car.get('supplier', 'N/A'):<20}")
        print(f"    Categoria: {car.get('category', 'N/A'):<30} | Transmissão: {car.get('transmission', 'N/A')}")
        print()
    
    if len(results) > 10:
        print(f"    ... e mais {len(results) - 10} carros")
else:
    print("\n⚠️ Nenhum carro encontrado")

print("\n" + "=" * 80)
