#!/usr/bin/env python3
"""
Script para abrir Chrome e testar preenchimento de campos no Carjet mobile
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configuração do Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Mobile emulation - iPhone 13
mobile_emulation = {
    "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Caminho do ChromeDriver (ajuste se necessário)
service = Service()

print("🚀 Abrindo Chrome com emulação mobile...")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # URL do Carjet em português
    url = "https://www.carjet.com/aluguel-carros/index.htm"
    print(f"📱 Navegando para: {url}")
    driver.get(url)
    
    print("\n✅ Chrome aberto!")
    print("📝 Agora você pode me ensinar como preencher os campos.")
    print("⏳ O navegador ficará aberto por 10 minutos...")
    print("🛑 Pressione Ctrl+C para fechar antes disso.\n")
    
    # Aguardar 10 minutos
    time.sleep(600)
    
except KeyboardInterrupt:
    print("\n\n🛑 Fechando Chrome...")
except Exception as e:
    print(f"\n❌ Erro: {e}")
finally:
    driver.quit()
    print("✅ Chrome fechado.")
