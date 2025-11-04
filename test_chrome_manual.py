#!/usr/bin/env python3
"""
Script para abrir Chrome e você preencher manualmente
Eu vou observar o que você faz
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

print("🌐 Abrindo Chrome...")

# Configurar Chrome VISÍVEL
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# NÃO usar headless - queremos ver!
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Iniciar Chrome
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

print("✅ Chrome aberto!")
print("")
print("📋 INSTRUÇÕES:")
print("1. Vou abrir o Carjet")
print("2. Você rejeita os cookies")
print("3. Você preenche o formulário")
print("4. Você clica em Pesquisar")
print("5. Eu vou observar os seletores que você usa")
print("")
print("Abrindo em 3 segundos...")
time.sleep(3)

# Abrir Carjet
print("🌐 Abrindo Carjet...")
driver.get("https://www.carjet.com/aluguel-carros/index.htm")

print("")
print("✅ Carjet aberto!")
print("")
print("👉 AGORA É COM VOCÊ:")
print("   1. Rejeite os cookies")
print("   2. Preencha:")
print("      - Local: Faro")
print("      - Data início: 25/11/2025")
print("      - Data fim: 28/11/2025")
print("      - Hora: 15:00")
print("   3. Clique em Pesquisar")
print("")
print("⏳ Vou esperar 2 minutos para você fazer...")
print("   (Depois vou mostrar a URL final)")

# Esperar 2 minutos
time.sleep(120)

# Mostrar URL final
print("")
print("="*60)
print("📊 INFORMAÇÕES COLETADAS:")
print("="*60)
print(f"URL Final: {driver.current_url}")
print(f"Título: {driver.title}")
print("")

# Verificar se tem resultados
try:
    page_source = driver.page_source
    if 'car-card' in page_source or 'resultado' in page_source.lower():
        print("✅ Parece que tem resultados na página!")
    else:
        print("⚠️  Não encontrei resultados óbvios")
except:
    pass

print("")
print("⏳ Chrome vai ficar aberto por mais 30 segundos...")
print("   (Para você ver os resultados)")
time.sleep(30)

driver.quit()
print("✅ Chrome fechado!")
