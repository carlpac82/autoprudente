#!/usr/bin/env python3
"""
Script para abrir Chrome no CarJet e deixar o usuário preencher manualmente
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🚀 Abrindo Chrome no CarJet...")

# Configurar Chrome (NÃO headless - visível)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')

# Iniciar driver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    print("📍 Acessando CarJet (Português BR)...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("\n" + "="*60)
    print("✅ Chrome aberto!")
    print("👉 Agora VOCÊ preenche o formulário manualmente")
    print("👀 Observe quando o popup de cookies aparece")
    print("⏸️  Quando terminar, pressione ENTER aqui no terminal")
    print("="*60 + "\n")
    
    input("Pressione ENTER quando terminar de testar...")
    
    print("\n📸 Capturando informações finais...")
    print(f"URL final: {driver.current_url}")
    print(f"Título: {driver.title}")
    
    # Tentar capturar HTML da página de resultados (se navegou)
    if '/do/list' in driver.current_url or 'results' in driver.current_url.lower():
        print("\n✅ Você chegou à página de resultados!")
        print("Vou tentar extrair os dados...")
        
        # Salvar HTML para análise
        with open('/tmp/carjet_results.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("💾 HTML salvo em: /tmp/carjet_results.html")
    
    print("\n✅ Teste concluído!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    
finally:
    print("\n🔄 Fechando Chrome em 5 segundos...")
    time.sleep(5)
    driver.quit()
    print("✅ Chrome fechado!")
