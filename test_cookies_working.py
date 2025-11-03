#!/usr/bin/env python3
"""
Teste com a função de cookies que FUNCIONA
Baseado em test_cookie_click.py linhas 30-47
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80)
print("TESTE COM FUNÇÃO DE COOKIES QUE FUNCIONA")
print("=" * 80)

# Configurar Chrome (VISÍVEL)
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("\n🚀 Abrindo Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acessar CarJet
    print("📍 Acessando CarJet...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(1)
    
    # FUNÇÃO QUE FUNCIONA - Aceitar cookie IMEDIATAMENTE
    print("\n🍪 Aceitando cookies com JavaScript...")
    time.sleep(0.5)  # Aguardar só 0.5 segundos
    try:
        driver.execute_script("""
            // Clicar E remover imediatamente
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                const text = btn.textContent.toLowerCase().trim();
                if (text.includes('aceitar todos') || text.includes('aceitar tudo')) {
                    btn.click();
                    console.log('✓ Clicou em:', btn.textContent);
                    break;
                }
            }
            
            // Remover TUDO via JS também
            document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                el.remove();
            });
            document.body.style.overflow = 'auto';
        """)
        print("✅ Cookies aceitos e banner removido!")
    except Exception as e:
        print(f"❌ Erro ao aceitar cookies: {e}")
    
    time.sleep(1)
    
    # Verificar se página está OK
    print(f"\n📄 URL atual: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    
    # Procurar campo de pesquisa
    print("\n🔍 Procurando campo de pesquisa...")
    try:
        pickup = driver.find_element(By.ID, "pickup")
        print(f"✅ Campo 'pickup' encontrado!")
    except:
        print(f"❌ Campo 'pickup' NÃO encontrado")
    
    print("\n" + "=" * 80)
    print("✅ SUCESSO! Chrome ficará aberto por 60 segundos")
    print("   Você pode inspecionar a página manualmente")
    print("=" * 80)
    
    for i in range(60, 0, -10):
        print(f"⏱️  Fechando em {i} segundos...")
        time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
