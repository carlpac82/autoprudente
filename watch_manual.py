#!/usr/bin/env python3
"""
Abrir Chrome VISÍVEL para você fazer manualmente
Eu observo e aprendo
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80)
print("MODO OBSERVAÇÃO - Faça você manualmente")
print("=" * 80)
print("\n📋 Instruções:")
print("1. Vou abrir o Chrome")
print("2. Você preenche o formulário manualmente")
print("3. Eu observo e gravo os passos")
print("\n⏳ Aguardando 5 minutos para você fazer...")
print("=" * 80)

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')

# EMULAÇÃO MOBILE
mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": mobile_ua
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Abrindo Chrome MOBILE visível...\n")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("✅ Chrome aberto!")
    print("\n👉 FAÇA VOCÊ:")
    print("   1. Aceite/Rejeite cookies")
    print("   2. Preencha o local (Albufeira Cidade)")
    print("   3. Clique no dropdown")
    print("   4. Preencha as datas")
    print("   5. Preencha as horas")
    print("   6. Clique em Pesquisar")
    print("\n⏳ Aguardando 5 minutos...\n")
    
    # Aguardar 5 minutos
    for i in range(300, 0, -30):
        print(f"⏱️  {i} segundos restantes...", flush=True)
        time.sleep(30)
    
    print("\n📊 Capturando estado final...")
    
    # Capturar URL final
    url = driver.current_url
    print(f"\n📄 URL final: {url}")
    
    # Capturar valores do formulário
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'N/A',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'N/A',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'N/A',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'N/A',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'N/A'
        };
    """)
    
    print("\n📋 Valores finais do formulário:")
    for key, val in values.items():
        print(f"   {key}: {val}")
    
    if "/do/list/" in url:
        print("\n🎉 SUCESSO! Chegou nos resultados!")
    elif "war=" in url:
        war = url.split("war=")[1].split("&")[0]
        print(f"\n❌ ERRO: war={war}")
    
    print("\n✅ Observação concluída!")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("\n👋 Fechando Chrome em 10 segundos...")
    time.sleep(10)
    driver.quit()
    print("Fechado!")
