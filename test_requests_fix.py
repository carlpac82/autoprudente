"""
Teste rápido: Verificar se o método requests melhorado funciona
"""
from datetime import datetime, timedelta
import sys

# Importar função melhorada
from carjet_requests import scrape_carjet_requests

print("=" * 80)
print("🧪 TESTE: MÉTODO REQUESTS MELHORADO")
print("=" * 80)

# Configurar datas
start_dt = datetime(2025, 12, 1, 15, 0)
end_dt = datetime(2025, 12, 8, 15, 0)

print(f"\n📍 Local: Albufeira")
print(f"📅 Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
print(f"⏱️  Duração: 7 dias")
print()

try:
    results = scrape_carjet_requests('Albufeira', start_dt, end_dt)
    
    if results:
        print(f"\n✅ SUCESSO: {len(results)} carros encontrados!")
        
        # Mostrar primeiros 3 carros
        for i, car in enumerate(results[:3], 1):
            price_str = car.get('price', '€0.00')
            
            # Extrair número da string '50.35 €'
            import re
            match = re.search(r'([\d.]+)', price_str)
            if match:
                try:
                    price = float(match.group(1))
                except:
                    price = 0.0
            else:
                price = 0.0
            
            print(f"\n{i}. {car.get('car_name', car.get('name', 'N/A'))}")
            print(f"   💰 Preço: {price_str} (€{price:.2f})")
            print(f"   🏢 Fornecedor: {car.get('supplier', 'N/A')}")
            print(f"   🚗 Grupo: {car.get('group', 'N/A')}")
            print(f"   🔧 Transmissão: {car.get('transmission', 'N/A')}")
    else:
        print("\n❌ ERRO: Nenhum carro encontrado")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ Teste concluído")
