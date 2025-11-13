#!/usr/bin/env python3
"""
Teste do scraping direto (urllib) - Mais rápido que Selenium
"""
from carjet_direct import scrape_carjet_direct
from datetime import datetime, timedelta

# Datas de teste - próximos 30 dias para garantir disponibilidade
start_dt = datetime.now() + timedelta(days=30)
end_dt = start_dt + timedelta(days=7)

print(f"🔍 Testando scraping direto...")
print(f"📅 Datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
print(f"📍 Local: Faro\n")

# Fazer scraping
items = scrape_carjet_direct('faro', start_dt, end_dt, quick=1)

if items:
    print(f"\n✅ SUCESSO! {len(items)} carros encontrados\n")
    print("="*80)
    
    # Mostrar primeiros 5 carros
    for idx, item in enumerate(items[:5], 1):
        print(f"\n{idx}. {item.get('car_name', 'N/A')}")
        print(f"   💰 Preço: {item.get('price', 'N/A')}")
        print(f"   🚗 Transmissão: {item.get('transmission', 'N/A')}")
        print(f"   🏢 Fornecedor: {item.get('supplier', 'N/A')}")
        print(f"   📦 Categoria: {item.get('category', 'N/A')}")
        if item.get('photo'):
            print(f"   📸 Foto: {item['photo'][:80]}...")
    
    print("\n" + "="*80)
    print(f"\n📊 ESTATÍSTICAS:")
    
    # Contar transmissões
    auto_count = sum(1 for item in items if item.get('transmission') == 'Automatic')
    manual_count = sum(1 for item in items if item.get('transmission') == 'Manual')
    unknown_count = len(items) - auto_count - manual_count
    
    print(f"   🔧 Automáticos: {auto_count}")
    print(f"   ⚙️  Manuais: {manual_count}")
    print(f"   ❓ Desconhecidos: {unknown_count}")
    
    # Contar fotos
    photos_count = sum(1 for item in items if item.get('photo'))
    print(f"   📸 Com fotos: {photos_count}/{len(items)} ({(photos_count/len(items)*100):.1f}%)")
    
else:
    print("\n❌ ERRO: Nenhum carro encontrado!")
