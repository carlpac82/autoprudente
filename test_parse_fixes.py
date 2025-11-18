"""
Teste rápido: Verificar se os ajustes de parse funcionam
"""
from datetime import datetime, timedelta
from carjet_requests import scrape_carjet_requests

print("=" * 80)
print("🧪 TESTE: AJUSTES DE PARSE")
print("=" * 80)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=1)

print(f"📍 Local: Albufeira")
print(f"📅 Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
print()

results = scrape_carjet_requests('Albufeira', start_dt, end_dt)

if results:
    print(f"\n✅ {len(results)} carros encontrados\n")
    print("=" * 80)
    print("📋 PRIMEIROS 5 CARROS (VERIFICAR LIMPEZA):")
    print("=" * 80)
    
    for i, car in enumerate(results[:5]):
        print(f"\n{i+1}. Nome: '{car.get('car', 'N/A')}'")
        print(f"   Supplier: {car.get('supplier', 'N/A')}")
        print(f"   Preço: {car.get('price', 'N/A')}")
        
        # Verificar se nome está limpo
        name = car.get('car', '')
        problems = []
        if 'ou similar' in name.lower():
            problems.append("❌ Contém 'ou similar'")
        if 'pequeno' in name.lower() or 'medio' in name.lower() or 'grande' in name.lower():
            problems.append("❌ Contém tamanho (pequeno/medio/grande)")
        if 'suvs' in name.lower():
            problems.append("❌ Contém 'SUVs'")
        if '  ' in name:
            problems.append("❌ Tem espaços duplos")
        
        if problems:
            print(f"   ⚠️  PROBLEMAS: {', '.join(problems)}")
        else:
            print(f"   ✅ Nome limpo!")
    
    # Estatísticas de suppliers
    print("\n" + "=" * 80)
    print("📊 SUPPLIERS ENCONTRADOS:")
    print("=" * 80)
    suppliers = {}
    for car in results:
        sup = car.get('supplier', 'N/A')
        suppliers[sup] = suppliers.get(sup, 0) + 1
    
    for sup, count in sorted(suppliers.items(), key=lambda x: -x[1])[:10]:
        print(f"   {sup}: {count} carros")
    
    if len(suppliers) == 1 and 'CarJet' in suppliers:
        print("\n   ⚠️  ATENÇÃO: Todos os suppliers são 'CarJet'")
        print("   Pode indicar que data-prv não está sendo extraído")
    else:
        print(f"\n   ✅ {len(suppliers)} suppliers diferentes detectados")
    
    print("\n" + "=" * 80)
    print("✅ TESTE COMPLETO")
    print("=" * 80)
else:
    print("\n❌ Nenhum carro encontrado")
