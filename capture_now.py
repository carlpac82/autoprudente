#!/usr/bin/env python3
"""
Capturar estado AGORA do Chrome que está aberto
"""
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')
mobile_emulation = {"deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0}, "userAgent": mobile_ua}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Conectar à sessão existente ou abrir nova
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("\n📊 Capturando estado...")
    
    url = driver.current_url
    print(f"\n📄 URL: {url}")
    
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value || 'N/A',
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value || 'N/A',
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value || 'N/A',
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value || 'N/A',
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value || 'N/A'
        };
    """)
    
    print("\n📋 Valores:")
    for key, val in values.items():
        print(f"   {key}: {val}")
    
    if "/do/list/" in url:
        print("\n🎉 SUCESSO!")
        # Contar carros
        articles = driver.find_elements("css selector", "section.newcarlist article")
        print(f"🚗 {len(articles)} carros")
    elif "war=" in url:
        war = url.split("war=")[1].split("&")[0]
        print(f"\n❌ ERRO: war={war}")
    
    input("\nPressione ENTER para fechar...")
    
except Exception as e:
    print(f"ERRO: {e}")
finally:
    driver.quit()
