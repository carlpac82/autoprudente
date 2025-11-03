#!/usr/bin/env python3
"""
TESTE 2: Observar você REJEITANDO cookies
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80)
print("TESTE 2 - REJEITAR COOKIES")
print("=" * 80)
print("\n📋 Desta vez:")
print("   ✅ REJEITE os cookies (não aceite!)")
print("   ✅ Preencha o formulário")
print("   ✅ Clique em Pesquisar")
print("\n⏳ Vou observar e registar tudo...")
print("=" * 80)

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')

mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": mobile_ua
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Abrindo Chrome MOBILE...\n")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("✅ Chrome aberto!")
    print("\n👉 PASSOS:")
    print("   1. ❌ REJEITE os cookies (botão de rejeitar)")
    print("   2. 📍 Preencha: Albufeira Cidade")
    print("   3. 📅 Preencha datas (qualquer data futura)")
    print("   4. ⏰ Preencha horas")
    print("   5. 🔍 Clique em Pesquisar")
    print("\n⏳ Aguardando 5 minutos...\n")
    
    # Aguardar 5 minutos
    for i in range(300, 0, -30):
        print(f"⏱️  {i} segundos restantes...", flush=True)
        time.sleep(30)
    
    print("\n📊 Capturando resultado...")
    
    url = driver.current_url
    print(f"\n📄 URL final: {url}")
    
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'N/A',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'N/A',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'N/A',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'N/A',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'N/A'
        };
    """)
    
    print("\n📋 Valores do formulário:")
    for key, val in values.items():
        status = "✅" if val != 'N/A' else "❌"
        print(f"   {status} {key}: {val}")
    
    if "/do/list/" in url:
        print("\n🎉 SUCESSO! Chegou nos resultados!")
        try:
            from selenium.webdriver.common.by import By
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"🚗 {len(articles)} carros encontrados")
        except:
            pass
    elif "war=" in url:
        war = url.split("war=")[1].split("&")[0]
        print(f"\n❌ ERRO: war={war}")
        print("   Possíveis causas:")
        print("   - Campos não preenchidos")
        print("   - Datas inválidas")
        print("   - Cookies bloquearam")
    else:
        print(f"\n⚠️  URL inesperada")
    
    print("\n" + "=" * 80)
    print("OBSERVAÇÃO CONCLUÍDA!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("\n👋 Fechando em 10 segundos...")
    time.sleep(10)
    driver.quit()
    print("Fechado!")
