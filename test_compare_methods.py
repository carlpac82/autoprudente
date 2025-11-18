"""
Teste comparativo: requests vs Selenium
Pesquisa de 7 dias no Aeroporto de Faro
"""
from datetime import datetime, timedelta
import time
import json

print("=" * 80)
print("🔬 TESTE COMPARATIVO: REQUESTS VS SELENIUM")
print("=" * 80)
print("📍 Local: Aeroporto de Faro")
print("📅 Duração: 7 dias")
print("=" * 80)

# Datas de teste
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=7)

print(f"\n📅 Datas: {start_dt.strftime('%d/%m/%Y')} → {end_dt.strftime('%d/%m/%Y')}")
print()

# =============================================================================
# MÉTODO 1: REQUESTS com sessão
# =============================================================================
print("\n" + "=" * 80)
print("🔵 MÉTODO 1: REQUESTS (urllib com sessão)")
print("=" * 80)

try:
    # Importar função melhorada
    from carjet_requests import scrape_carjet_requests
    
    start_time = time.time()
    results_requests = scrape_carjet_requests('Aeroporto de Faro', start_dt, end_dt)
    elapsed_requests = time.time() - start_time
    
    print(f"\n✅ REQUESTS: {len(results_requests)} carros em {elapsed_requests:.1f}s")
    
    # Salvar resultados
    with open('results_requests.json', 'w', encoding='utf-8') as f:
        json.dump(results_requests, f, indent=2, ensure_ascii=False)
    
except Exception as e:
    print(f"❌ ERRO REQUESTS: {e}")
    import traceback
    traceback.print_exc()
    results_requests = []
    elapsed_requests = 0

# =============================================================================
# MÉTODO 2: SELENIUM/PLAYWRIGHT
# =============================================================================
print("\n" + "=" * 80)
print("🟡 MÉTODO 2: PLAYWRIGHT (browser automation)")
print("=" * 80)

try:
    # Importar função do main.py
    import sys
    sys.path.insert(0, '/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay')
    
    # Importar função de scraping Playwright do main.py
    from main import scrape_carjet_playwright
    
    start_time = time.time()
    results_playwright = scrape_carjet_playwright(
        location='Aeroporto de Faro',
        start_dt=start_dt,
        end_dt=end_dt,
        quick=0
    )
    elapsed_playwright = time.time() - start_time
    
    print(f"\n✅ PLAYWRIGHT: {len(results_playwright)} carros em {elapsed_playwright:.1f}s")
    
    # Salvar resultados
    with open('results_playwright.json', 'w', encoding='utf-8') as f:
        json.dump(results_playwright, f, indent=2, ensure_ascii=False)
    
except Exception as e:
    print(f"❌ ERRO PLAYWRIGHT: {e}")
    import traceback
    traceback.print_exc()
    results_playwright = []
    elapsed_playwright = 0

# =============================================================================
# COMPARAÇÃO DOS RESULTADOS
# =============================================================================
print("\n" + "=" * 80)
print("📊 COMPARAÇÃO DOS RESULTADOS")
print("=" * 80)

print(f"""
┌─────────────────────┬─────────────┬──────────────┐
│ Métrica             │  Requests   │  Playwright  │
├─────────────────────┼─────────────┼──────────────┤
│ Carros encontrados  │ {len(results_requests):>11} │ {len(results_playwright):>12} │
│ Tempo decorrido     │ {elapsed_requests:>9.1f}s │ {elapsed_playwright:>10.1f}s │
│ Velocidade          │ {(len(results_requests)/elapsed_requests if elapsed_requests > 0 else 0):>9.1f}/s │ {(len(results_playwright)/elapsed_playwright if elapsed_playwright > 0 else 0):>10.1f}/s │
└─────────────────────┴─────────────┴──────────────┘
""")

# Comparação detalhada se ambos funcionaram
if results_requests and results_playwright:
    print("\n📋 DETALHES DA COMPARAÇÃO:\n")
    
    # Extrair nomes de carros
    cars_requests = set(r.get('car', '') for r in results_requests if r.get('car'))
    cars_playwright = set(r.get('car', '') for r in results_playwright if r.get('car'))
    
    print(f"🔵 Carros únicos (Requests):   {len(cars_requests)}")
    print(f"🟡 Carros únicos (Playwright): {len(cars_playwright)}")
    
    # Carros em comum
    common_cars = cars_requests & cars_playwright
    print(f"✅ Carros em ambos:            {len(common_cars)}")
    
    # Carros exclusivos
    only_requests = cars_requests - cars_playwright
    only_playwright = cars_playwright - cars_requests
    
    if only_requests:
        print(f"\n🔵 Apenas em Requests ({len(only_requests)}):")
        for car in list(only_requests)[:5]:
            print(f"   - {car}")
        if len(only_requests) > 5:
            print(f"   ... e mais {len(only_requests) - 5}")
    
    if only_playwright:
        print(f"\n🟡 Apenas em Playwright ({len(only_playwright)}):")
        for car in list(only_playwright)[:5]:
            print(f"   - {car}")
        if len(only_playwright) > 5:
            print(f"   ... e mais {len(only_playwright) - 5}")
    
    # Comparar preços dos carros em comum
    if common_cars:
        print(f"\n💰 COMPARAÇÃO DE PREÇOS (primeiros 5 carros em comum):")
        
        # Criar dicionários de preços
        prices_req = {r['car']: r.get('price', 'N/A') for r in results_requests}
        prices_play = {r['car']: r.get('price', 'N/A') for r in results_playwright}
        
        for i, car in enumerate(list(common_cars)[:5]):
            price_req = prices_req.get(car, 'N/A')
            price_play = prices_play.get(car, 'N/A')
            match = "✅" if price_req == price_play else "⚠️"
            print(f"   {match} {car[:50]:<50}")
            print(f"      Requests:   {price_req}")
            print(f"      Playwright: {price_play}")
            print()

# Conclusão
print("=" * 80)
print("🎯 CONCLUSÃO")
print("=" * 80)

if results_requests and results_playwright:
    diff_percent = abs(len(results_requests) - len(results_playwright)) / max(len(results_requests), len(results_playwright)) * 100
    
    if diff_percent < 5:
        print("✅ RESULTADOS EQUIVALENTES (diferença < 5%)")
    elif diff_percent < 15:
        print("⚠️ RESULTADOS SIMILARES (diferença < 15%)")
    else:
        print("❌ RESULTADOS DIFERENTES (diferença > 15%)")
    
    # Performance
    if elapsed_requests > 0 and elapsed_playwright > 0:
        speedup = elapsed_playwright / elapsed_requests
        print(f"⚡ Requests é {speedup:.1f}x mais rápido que Playwright")
    
elif results_requests:
    print("✅ REQUESTS funcionou, Playwright falhou")
elif results_playwright:
    print("⚠️ Playwright funcionou, Requests falhou")
else:
    print("❌ AMBOS OS MÉTODOS FALHARAM")

print("=" * 80)
print("\n📁 Resultados salvos em:")
print("   - results_requests.json")
print("   - results_playwright.json")
