"""
Teste do urllib COM polling
"""
from datetime import datetime, timedelta
from carjet_direct import scrape_carjet_direct

# Datas de teste
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=1)

print("=" * 80)
print("🧪 TESTE urllib COM POLLING")
print("=" * 80)
print(f"📅 Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
print(f"📍 Local: Albufeira")
print()

results = scrape_carjet_direct('Albufeira', start_dt, end_dt, quick=0)

print()
print("=" * 80)
print(f"✅ RESULTADO: {len(results)} carros encontrados")
print("=" * 80)

if results:
    print("\n📊 PRIMEIROS 5 CARROS:")
    for i, car in enumerate(results[:5]):
        print(f"\n{i+1}. {car['car']}")
        print(f"   Supplier: {car['supplier']}")
        print(f"   Preço: {car['price']}")
        print(f"   Categoria: {car.get('category', 'N/A')}")
        print(f"   Grupo: {car.get('group', 'N/A')}")
        print(f"   Transmissão: {car.get('transmission', 'N/A')}")
else:
    print("\n⚠️ Nenhum carro encontrado - verificar logs acima")
