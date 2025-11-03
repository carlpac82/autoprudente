#!/usr/bin/env python3
"""
Teste do fluxo completo: cookies → local → datas → horas → buscar
"""
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80)
print("TESTE FLUXO COMPLETO - CARJET")
print("=" * 80)

# Datas de teste
start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"\n📅 Datas:")
print(f"   Recolha: {start_dt.strftime('%d/%m/%Y %H:%M')}")
print(f"   Entrega: {end_dt.strftime('%d/%m/%Y %H:%M')}")

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

print("\n🚀 Iniciando Chrome...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Abrir página
    print("\n📍 PASSO 1: Abrindo CarJet...")
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(1)
    print("✅ Página aberta")
    
    # 2. Aceitar cookies
    print("\n🍪 PASSO 2: Aceitando cookies...")
    time.sleep(0.5)
    driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            const text = btn.textContent.toLowerCase().trim();
            if (text.includes('aceitar todos') || text.includes('aceitar tudo')) {
                btn.click();
                console.log('✓ Cookies aceitos');
                break;
            }
        }
        document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
            el.remove();
        });
    """)
    print("✅ Cookies aceitos")
    time.sleep(1)
    
    # 3. Preencher local
    print("\n📍 PASSO 3: Preenchendo local...")
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    print("✅ Digitado: Albufeira Cidade")
    time.sleep(2)
    
    # Clicar no dropdown
    try:
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
        )
        dropdown_item.click()
        print("✅ Dropdown clicado")
    except:
        driver.execute_script("""
            const item = document.querySelector('#recogida_lista li[data-id="Albufeira Cidade"]');
            if (item) item.click();
        """)
        print("✅ Dropdown clicado via JS")
    time.sleep(1)
    
    # 4. Preencher datas e horas via JavaScript
    print("\n📅 PASSO 4: Preenchendo datas e horas...")
    driver.execute_script("""
        function fill(sel, val) {
            const el = document.querySelector(sel);
            if (el) { 
                el.value = val; 
                el.dispatchEvent(new Event('change', {bubbles: true}));
                el.dispatchEvent(new Event('input', {bubbles: true}));
                console.log('Preenchido:', sel, '=', val);
                return true;
            }
            console.log('Não encontrado:', sel);
            return false;
        }
        
        // Preencher local de devolução (mesmo que recolha)
        fill('input[name="dropoff"]', arguments[0]);
        
        // Preencher datas
        fill('input[name="fechaRecogida"]', arguments[1]);
        fill('input[name="fechaEntrega"]', arguments[2]);
        
        // Preencher horas nos dropdowns
        const h1 = document.querySelector('select[name="fechaRecogidaSelHour"]');
        const h2 = document.querySelector('select[name="fechaEntregaSelHour"]');
        if (h1) {
            h1.value = arguments[3] || '10:00';
            console.log('Hora recolha:', h1.value);
        }
        if (h2) {
            h2.value = arguments[4] || '10:00';
            console.log('Hora entrega:', h2.value);
        }
        
        return {
            dropoff: !!document.querySelector('input[name="dropoff"]'),
            fechaRecogida: !!document.querySelector('input[name="fechaRecogida"]'),
            fechaEntrega: !!document.querySelector('input[name="fechaEntrega"]'),
            horaRecogida: !!h1,
            horaEntrega: !!h2
        };
    """, 
    "Albufeira Cidade",  # dropoff
    start_dt.strftime("%d/%m/%Y"),  # data recolha
    end_dt.strftime("%d/%m/%Y"),  # data entrega
    start_dt.strftime("%H:%M"),  # hora recolha
    end_dt.strftime("%H:%M")  # hora entrega
    )
    print("✅ Datas e horas preenchidas")
    time.sleep(1)
    
    # Verificar valores preenchidos
    print("\n🔍 Verificando valores...")
    try:
        fecha_rec = driver.find_element(By.NAME, "fechaRecogida").get_attribute("value")
        fecha_ent = driver.find_element(By.NAME, "fechaEntrega").get_attribute("value")
        print(f"   Data recolha: {fecha_rec}")
        print(f"   Data entrega: {fecha_ent}")
    except:
        print("   ⚠️  Não conseguiu verificar datas")
    
    # 5. Submeter formulário
    print("\n🔍 PASSO 5: Submetendo formulário...")
    try:
        # Tentar clicar no botão de pesquisa
        search_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_btn.click()
        print("✅ Botão 'Pesquisar' clicado")
    except:
        # Fallback: submit via JS
        driver.execute_script("document.querySelector('form').submit();")
        print("✅ Formulário submetido via JS")
    
    # Aguardar navegação
    print("\n⏳ Aguardando resultados (10 segundos)...")
    time.sleep(10)
    
    final_url = driver.current_url
    print(f"\n📄 URL final: {final_url}")
    
    # 6. Verificar se chegou na página de resultados
    if "/do/list/" in final_url or "/search" in final_url:
        print("✅ Chegou na página de resultados!")
        
        # Procurar resultados
        print("\n🚗 Procurando resultados...")
        try:
            articles = driver.find_elements(By.CSS_SELECTOR, "section.newcarlist article")
            print(f"✅ Encontrados {len(articles)} resultados")
            
            if len(articles) > 0:
                print("\n📊 Primeiros 3 resultados:")
                for i, art in enumerate(articles[:3], 1):
                    try:
                        car = art.find_element(By.CSS_SELECTOR, "h2").text
                        price = art.find_element(By.CSS_SELECTOR, ".pr-euros").text
                        print(f"  {i}. {car} - {price}")
                    except:
                        print(f"  {i}. [Erro ao extrair]")
        except Exception as e:
            print(f"⚠️  Erro ao procurar resultados: {e}")
    else:
        print("❌ NÃO chegou na página de resultados!")
        print(f"   URL atual: {final_url}")
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO! Chrome ficará aberto por 60 segundos")
    print("=" * 80)
    
    for i in range(60, 0, -10):
        print(f"⏱️  {i} segundos...")
        time.sleep(10)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Chrome fechado")
