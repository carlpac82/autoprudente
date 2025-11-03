#!/usr/bin/env python3
"""
Teste para preencher local e clicar no dropdown
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
print("TESTE - PREENCHER LOCAL E DROPDOWN")
print("=" * 80)

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
    
    # 2. Aceitar cookies
    print("\n🍪 Aceitando cookies...")
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
    
    # 3. Preencher campo pickup
    print("\n📝 Preenchendo campo pickup...")
    try:
        pickup = driver.find_element(By.ID, "pickup")
        print(f"✅ Campo encontrado")
        
        # Limpar e digitar
        pickup.clear()
        pickup.send_keys("Albufeira Cidade")
        print(f"✅ Digitado: 'Albufeira Cidade'")
        
        # Aguardar dropdown aparecer
        print("\n⏳ Aguardando dropdown aparecer...")
        time.sleep(2)
        
        # Verificar se dropdown apareceu
        try:
            dropdown = driver.find_element(By.ID, "recogida_lista")
            if dropdown.is_displayed():
                print("✅ Dropdown visível!")
                
                # Listar opções do dropdown
                items = dropdown.find_elements(By.TAG_NAME, "li")
                print(f"   Total de opções: {len(items)}")
                
                for i, item in enumerate(items[:5], 1):
                    try:
                        text = item.text
                        data_id = item.get_attribute("data-id")
                        print(f"   {i}. '{text}' (data-id: '{data_id}')")
                    except:
                        pass
                
                # Tentar clicar na opção "Albufeira Cidade"
                print("\n👆 Tentando clicar em 'Albufeira Cidade'...")
                
                # Método 1: Via Selenium
                try:
                    item = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
                    )
                    item.click()
                    print("✅ Clicado via Selenium!")
                except Exception as e:
                    print(f"⚠️  Selenium falhou: {e}")
                    
                    # Método 2: Via JavaScript
                    try:
                        driver.execute_script("""
                            const item = document.querySelector('#recogida_lista li[data-id="Albufeira Cidade"]');
                            if (item) {
                                item.click();
                                console.log('Clicado via JS');
                            }
                        """)
                        print("✅ Clicado via JavaScript!")
                    except Exception as e2:
                        print(f"❌ JavaScript também falhou: {e2}")
                
                time.sleep(1)
                
                # Verificar se foi selecionado
                pickup_value = pickup.get_attribute("value")
                print(f"\n📄 Valor final do campo: '{pickup_value}'")
                
            else:
                print("❌ Dropdown não está visível")
        except Exception as e:
            print(f"❌ Dropdown não encontrado: {e}")
            
            # Tentar com Keys
            print("\n⚠️  Tentando com teclas de navegação...")
            pickup.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            pickup.send_keys(Keys.ENTER)
            print("✅ Tentou com ARROW_DOWN + ENTER")
            time.sleep(1)
            
            pickup_value = pickup.get_attribute("value")
            print(f"📄 Valor final: '{pickup_value}'")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Chrome ficará aberto por 60 segundos para você inspecionar")
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
