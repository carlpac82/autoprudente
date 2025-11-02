#!/usr/bin/env python3
"""
Debug visual do scraping de Albufeira com Chrome visível
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import random

print("=" * 70)
print("DEBUG VISUAL - SCRAPING ALBUFEIRA")
print("=" * 70)

# Datas de teste
start_dt = datetime.now() + timedelta(days=14)
end_dt = start_dt + timedelta(days=2)

# Hora aleatória entre 14:30 e 17:00 (apenas valores que existem no dropdown)
# Opções: 14:30, 15:00, 15:30, 16:00, 16:30, 17:00
possible_times = ["14:30", "15:00", "15:30", "16:00", "16:30", "17:00"]
pickup_time = random.choice(possible_times)
return_time = pickup_time  # Mesma hora para devolução

print(f"\nPickup: {start_dt.strftime('%d/%m/%Y')} às {pickup_time}")
print(f"Return: {end_dt.strftime('%d/%m/%Y')} às {return_time}")
print()

# Configurar Chrome VISÍVEL (sem headless) com anti-deteção
chrome_options = Options()
# chrome_options.add_argument('--headless')  # COMENTADO para ver o browser
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')

# Anti-deteção
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("🌐 Iniciando Chrome visível...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # Esconder webdriver
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        '''
    })
    
    print("✅ Chrome aberto!")
    print("\n📍 Navegando para CarJet...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    
    print(f"📄 URL atual: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    
    # Aceitar cookies se aparecer
    print("\n🍪 Procurando banner de cookies...")
    try:
        cookie_buttons = driver.find_elements(By.CSS_SELECTOR, "button, a")
        for btn in cookie_buttons:
            text = btn.text.lower()
            if any(word in text for word in ['aceitar', 'accept', 'concordo', 'agree']):
                print(f"   ✓ Clicando em: {btn.text}")
                btn.click()
                time.sleep(1)
                break
    except:
        print("   (Sem cookies ou já aceite)")
    
    # Preencher formulário
    print("\n📝 Preenchendo formulário...")
    
    # Campo Pickup
    print("   1. Campo Pickup (Albufeira Cidade)...")
    try:
        pickup_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        pickup_field.clear()
        pickup_field.send_keys("Albufeira Cidade")
        time.sleep(1)
        
        # Esperar dropdown
        print("   2. Aguardando dropdown de sugestões...")
        time.sleep(2)
        
        # Tentar clicar na primeira opção
        try:
            first_option = driver.find_element(By.CSS_SELECTOR, "#recogida_lista li a")
            print(f"   ✓ Clicando em: {first_option.text}")
            first_option.click()
            time.sleep(1)
        except:
            print("   ⚠️  Dropdown não apareceu, continuando...")
        
    except Exception as e:
        print(f"   ❌ Erro no pickup: {e}")
    
    # Data de pickup
    print(f"   3. Data pickup: {start_dt.strftime('%d/%m/%Y')}...")
    try:
        date_field = driver.find_element(By.ID, "fechaRecogida")
        driver.execute_script(f"arguments[0].value = '{start_dt.strftime('%d/%m/%Y')}'", date_field)
        time.sleep(0.5)
    except Exception as e:
        print(f"   ⚠️  Erro na data: {e}")
    
    # Hora de pickup (clicar no dropdown e selecionar)
    print(f"   4. Hora pickup: {pickup_time}...")
    try:
        from selenium.webdriver.support.ui import Select
        # Tentar diferentes seletores
        pickup_hour_select = None
        selectors = [
            (By.NAME, "fechaRecogidaSelHour"),
            (By.ID, "fechaRecogidaSelHour"),
            (By.CSS_SELECTOR, "select[name*='hora']"),
            (By.CSS_SELECTOR, "select[name*='Hour']"),
            (By.CSS_SELECTOR, "select[name*='time']"),
        ]
        for by, selector in selectors:
            try:
                pickup_hour_select = driver.find_element(by, selector)
                print(f"      ✓ Encontrado via: {selector}")
                break
            except:
                continue
        
        if pickup_hour_select:
            select = Select(pickup_hour_select)
            select.select_by_value(pickup_time)
            time.sleep(0.5)
        else:
            print(f"      ⚠️ Campo de hora não encontrado!")
    except Exception as e:
        print(f"   ⚠️  Erro na hora: {e}")
    
    # Data de devolução
    print(f"   5. Data devolução: {end_dt.strftime('%d/%m/%Y')}...")
    try:
        return_date_field = driver.find_element(By.ID, "fechaEntrega")
        driver.execute_script(f"arguments[0].value = '{end_dt.strftime('%d/%m/%Y')}'", return_date_field)
        time.sleep(0.5)
    except Exception as e:
        print(f"   ⚠️  Erro na data devolução: {e}")
    
    # Hora de devolução (clicar no dropdown e selecionar)
    print(f"   6. Hora devolução: {return_time}...")
    try:
        from selenium.webdriver.support.ui import Select
        return_hour_select = driver.find_element(By.NAME, "fechaEntregaSelHour")
        return_hour_select.click()
        time.sleep(0.5)
        
        select = Select(return_hour_select)
        select.select_by_value(return_time)
        time.sleep(0.5)
    except Exception as e:
        print(f"   ⚠️  Erro na hora devolução: {e}")
    
    print("\n🔍 Formulário preenchido! Aguarda 3 segundos para veres...")
    time.sleep(3)
    
    # Submeter formulário
    print("\n🚀 Submetendo formulário...")
    try:
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn-search")
        print(f"   ✓ Botão encontrado: {submit_btn.text}")
        submit_btn.click()
    except Exception as e:
        print(f"   ❌ Erro ao submeter: {e}")
        print("   Tentando submeter via JavaScript...")
        driver.execute_script("document.querySelector('form').submit()")
    
    print("\n⏳ Aguardando resultados (15 segundos)...")
    time.sleep(15)
    
    final_url = driver.current_url
    print(f"\n📍 URL final: {final_url}")
    print(f"📄 Título final: {driver.title}")
    
    # Se deu erro (war=X), alterar horas e clicar pesquisar até 5 vezes
    max_retries = 5
    retry_count = 0
    
    while 'war=' in final_url and retry_count < max_retries:
        retry_count += 1
        print(f"\n⚠️  ERRO DETECTADO (war=X) - Tentativa {retry_count}/{max_retries}")
        
        # Gerar nova hora aleatória (mesma para recolha e entrega)
        new_time = random.choice(possible_times)
        print(f"🔄 Mudando horas para: {new_time}")
        
        try:
            from selenium.webdriver.support.ui import Select
            
            # Alterar hora de RECOLHA
            print("   📝 Alterando hora de recolha...")
            pickup_selectors = [
                (By.NAME, "fechaRecogidaSelHour"),
                (By.ID, "fechaRecogidaSelHour"),
                (By.CSS_SELECTOR, "select[name*='Recogida']"),
            ]
            for by, sel in pickup_selectors:
                try:
                    pickup_select = driver.find_element(by, sel)
                    Select(pickup_select).select_by_value(new_time)
                    print(f"      ✓ Hora recolha alterada para {new_time}")
                    break
                except:
                    continue
            
            time.sleep(0.5)
            
            # Alterar hora de ENTREGA (mesma hora!)
            print("   📝 Alterando hora de entrega...")
            return_selectors = [
                (By.NAME, "fechaEntregaSelHour"),
                (By.ID, "fechaEntregaSelHour"),
                (By.CSS_SELECTOR, "select[name*='Entrega']"),
            ]
            for by, sel in return_selectors:
                try:
                    return_select = driver.find_element(by, sel)
                    Select(return_select).select_by_value(new_time)
                    print(f"      ✓ Hora entrega alterada para {new_time}")
                    break
                except:
                    continue
            
            time.sleep(0.5)
            
            # Clicar pesquisar
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn-search")
            print("   🔍 Clicando em Pesquisar...")
            submit_btn.click()
            
            print("   ⏳ Aguardando resultados...")
            time.sleep(15)
            
            final_url = driver.current_url
            print(f"   📍 Nova URL: {final_url}")
            
        except Exception as e:
            print(f"   ❌ Erro na retry: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # Verificar se tem resultados
    try:
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"\n✅ Encontrados {len(articles)} <article> tags")
        
        prices = driver.find_elements(By.CSS_SELECTOR, ".price, [class*='price']")
        print(f"✅ Encontrados {len(prices)} elementos com 'price'")
        
        if articles and 'war=' not in final_url:
            print("\n📊 Primeiros 3 carros:")
            for i, article in enumerate(articles[:3], 1):
                try:
                    car_name = article.find_element(By.CSS_SELECTOR, "h3, h4, .car-name").text
                    price = article.find_element(By.CSS_SELECTOR, ".price").text
                    print(f"   {i}. {car_name} - {price}")
                except:
                    print(f"   {i}. (Erro ao extrair dados)")
        
    except Exception as e:
        print(f"❌ Erro ao verificar resultados: {e}")
    
    print("\n" + "=" * 70)
    print("🔍 INSPECIONA O BROWSER AGORA!")
    print("   O Chrome vai ficar aberto por 60 segundos.")
    print("   Podes ver o que o CarJet está a mostrar.")
    print("=" * 70)
    
    # Manter browser aberto
    time.sleep(60)
    
except Exception as e:
    print(f"\n❌ ERRO GERAL: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)

finally:
    print("\n🔴 Fechando browser...")
    driver.quit()
    print("✅ Concluído!")
