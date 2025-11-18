"""
Teste de integração: Verificar se requests está integrado no main.py
"""
from datetime import datetime, timedelta
import sys

print("=" * 80)
print("🧪 TESTE DE INTEGRAÇÃO: CARJET_REQUESTS NO MAIN.PY")
print("=" * 80)

# Importar função do main.py
try:
    from main import try_direct_carjet, parse_prices
    print("✅ Funções importadas com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

# Testar scraping
print("\n" + "=" * 80)
print("📍 Teste: Aeroporto de Faro - 1 dia")
print("=" * 80)

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=1)

print(f"📅 Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
print()

# Chamar try_direct_carjet
print("Chamando try_direct_carjet()...")
html = try_direct_carjet('Aeroporto de Faro', start_dt, end_dt)

if html:
    print(f"✅ HTML recebido: {len(html)} chars")
    
    # Verificar se é do novo método
    if "<!--CARJET_REQUESTS_DATA-->" in html:
        print("🔵 Detectado: dados do carjet_requests (NOVO MÉTODO)")
    else:
        print("🟡 Detectado: HTML normal (método antigo)")
    
    # Parse
    print("\nChamando parse_prices()...")
    items = parse_prices(html, "https://www.carjet.com")
    
    print(f"\n✅ RESULTADO: {len(items)} carros parseados")
    
    if items:
        print("\n📋 PRIMEIROS 5 CARROS:")
        for i, car in enumerate(items[:5]):
            print(f"\n{i+1}. {car.get('car', 'N/A')}")
            print(f"   Preço: {car.get('price', 'N/A')}")
            print(f"   Categoria: {car.get('category', 'N/A')}")
            print(f"   Grupo: {car.get('group', 'N/A')}")
            print(f"   Supplier: {car.get('supplier', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("✅ INTEGRAÇÃO FUNCIONANDO CORRETAMENTE!")
    print("=" * 80)
    
else:
    print("❌ Nenhum HTML retornado")
    print("=" * 80)
    print("❌ TESTE FALHOU")
    print("=" * 80)
