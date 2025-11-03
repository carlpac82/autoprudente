#!/usr/bin/env python3
"""
Teste final do scraping com cookies corrigidos
Simula o fluxo completo: aceitar cookies → pesquisar → filtrar AUTOPRUDENTE → extrair resultados
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80)
print("TESTE FINAL - SCRAPING COMPLETO COM COOKIES CORRIGIDOS")
print("=" * 80)

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

print("\n🚀 Iniciando Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Abrir página
    print("\n📍 Abrindo CarJet...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(1)
    
    # 2. Aceitar cookies (MÉTODO QUE FUNCIONA)
    print("\n🍪 Aceitando cookies...")
    time.sleep(0.5)
    driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            const text = btn.textContent.toLowerCase().trim();
            if (text.includes('aceitar todos') || text.includes('aceitar tudo')) {
                btn.click();
                console.log('✓ Cookies aceitos:', btn.textContent);
                break;
            }
        }
        document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
            el.remove();
        });
        document.body.style.overflow = 'auto';
    """)
    print("✅ Cookies aceitos")
    time.sleep(1)
    
    # 3. Preencher formulário
    print("\n📝 Preenchendo formulário...")
    try:
        # Local de recolha
        pickup = driver.find_element(By.ID, "pickup")
        pickup.clear()
        pickup.send_keys("Albufeira")
        time.sleep(2)
        pickup.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        pickup.send_keys(Keys.ENTER)
        print("✅ Local de recolha: Albufeira")
        time.sleep(1)
        
        # Datas (exemplo)
        date_pickup = driver.find_element(By.ID, "fechaRecogida")
        date_pickup.clear()
        date_pickup.send_keys("10/11/2025")
        
        date_dropoff = driver.find_element(By.ID, "fechaEntrega")
        date_dropoff.clear()
        date_dropoff.send_keys("15/11/2025")
        print("✅ Datas preenchidas")
        time.sleep(1)
        
    except Exception as e:
        print(f"⚠️  Erro ao preencher: {e}")
    
    # 4. Submeter formulário
    print("\n🔍 Submetendo pesquisa...")
    try:
        search_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_btn.click()
        print("✅ Pesquisa submetida")
        time.sleep(8)
    except Exception as e:
        print(f"⚠️  Erro ao submeter: {e}")
    
    print(f"\n📄 URL após pesquisa: {driver.current_url}")
    
    # 5. Filtrar por AUTOPRUDENTE
    print("\n🔍 Procurando filtro AUTOPRUDENTE...")
    try:
        # Aguardar checkbox aparecer
        aup_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chkAUP"))
        )
        print("✅ Checkbox AUTOPRUDENTE encontrado")
        
        # Desmarcar todos os suppliers
        print("📋 Desmarcando todos os suppliers...")
        driver.execute_script("""
            document.querySelectorAll('input[name="frmPrv"]:checked').forEach(cb => cb.click());
        """)
        time.sleep(2)
        
        # Marcar apenas AUTOPRUDENTE
        print("✅ Marcando AUTOPRUDENTE...")
        driver.execute_script("document.querySelector('#chkAUP').click();")
        time.sleep(5)
        print("✅ Filtro AUTOPRUDENTE aplicado")
        
    except Exception as e:
        print(f"❌ Erro ao filtrar AUTOPRUDENTE: {e}")
    
    # 6. Extrair resultados
    print("\n🚗 Extraindo resultados...")
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
        print(f"✅ Encontrados {len(articles)} resultados")
        
        if len(articles) > 0:
            print("\n📊 Primeiros 5 resultados:")
            for i, art in enumerate(articles[:5], 1):
                try:
                    car = art.find_element(By.CSS_SELECTOR, "h2").text
                    price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                    
                    # Tentar extrair supplier
                    supplier = ""
                    try:
                        supplier_img = art.find_element(By.CSS_SELECTOR, "img[src*='/prv/']")
                        supplier = supplier_img.get_attribute("alt") or ""
                    except:
                        pass
                    
                    print(f"  {i}. {car}")
                    print(f"     Preço: {price}")
                    if supplier:
                        print(f"     Supplier: {supplier}")
                    print()
                except Exception as e:
                    print(f"  {i}. [Erro ao extrair: {e}]")
        else:
            print("⚠️  Nenhum resultado encontrado!")
            # Screenshot para debug
            driver.save_screenshot("/Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay/debug_no_results.png")
            print("📸 Screenshot salvo: debug_no_results.png")
        
    except Exception as e:
        print(f"❌ Erro ao extrair resultados: {e}")
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO! Chrome ficará aberto por 60 segundos")
    print("=" * 80)
    
    for i in range(60, 0, -10):
        print(f"⏱️  {i} segundos...")
        time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO GERAL: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
