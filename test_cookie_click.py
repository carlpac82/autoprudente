#!/usr/bin/env python3
"""
Script para testar e capturar o clique no cookie
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configurar Chrome (VISÍVEL)
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("🚀 Abrindo Chrome...")
driver = webdriver.Chrome(options=chrome_options)

# Acessar CarJet
print("📍 Acessando CarJet...")
driver.get("https://www.carjet.com/aluguel-carros/index.htm")
time.sleep(1)

# Aceitar primeiro cookie IMEDIATAMENTE
print("🍪 Aceitando primeiro cookie IMEDIATAMENTE...")
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
    print("✓ Primeiro cookie aceito e removido!")
except Exception as e:
    print(f"⚠ Erro: {e}")

time.sleep(0.5)
print("✅ Continuando...")

# Preencher campo pickup
print("📝 Preenchendo campo pickup...")
try:
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    print("✓ Digitado: Albufeira Cidade")
    
    # Aguardar dropdown aparecer
    print("⏳ Aguardando dropdown aparecer...")
    time.sleep(1.5)
    
    # Clicar no dropdown usando WebDriverWait (método antigo que funcionava)
    print("👆 Clicando no dropdown...")
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        dropdown_item = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#recogida_lista li[data-id='Albufeira Cidade'] a"))
        )
        dropdown_item.click()
        print("✓ Dropdown clicado via Selenium!")
    except:
        # Fallback: tentar via JavaScript
        driver.execute_script("""
            const item = document.querySelector('#recogida_lista li[data-id="Albufeira Cidade"]');
            if (item) item.click();
        """)
        print("✓ Dropdown clicado via JS!")
    
    time.sleep(0.5)
    
except Exception as e:
    print(f"⚠ Erro geral: {e}")

print("\n" + "="*60)
print("⏸️  AGORA É COM VOCÊ!")
print("👉 PREENCHA AS DATAS MANUALMENTE:")
print("   1. Clique no campo de data de recolha")
print("   2. Escolha uma data no calendário")
print("   3. Clique no campo de data de entrega")
print("   4. Escolha uma data no calendário")
print("👉 O 2º popup deve aparecer quando fechares o calendário")
print("👉 CLIQUE em 'Aceitar todos os cookies'")
print("👉 Depois pressione ENTER aqui no terminal")
print("="*60)

input("\nPressione ENTER após clicar no cookie...")

# Capturar qual elemento foi clicado
print("\n🔍 Capturando informações do elemento clicado...")
try:
    info = driver.execute_script("""
        // Procurar todos os botões de cookie
        const buttons = document.querySelectorAll('button');
        const cookieButtons = [];
        
        for (let btn of buttons) {
            const text = btn.textContent.toLowerCase().trim();
            if (text.includes('aceitar') || text.includes('cookie')) {
                cookieButtons.push({
                    text: btn.textContent.trim(),
                    id: btn.id,
                    className: btn.className,
                    visible: btn.offsetParent !== null,
                    outerHTML: btn.outerHTML.substring(0, 300)
                });
            }
        }
        
        return {
            cookieButtons: cookieButtons,
            popupsVisiveis: document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi]').length
        };
    """)
    
    print(f"\n📊 INFORMAÇÕES CAPTURADAS:")
    print(f"Popups visíveis: {info['popupsVisiveis']}")
    print(f"\nBotões de cookie encontrados: {len(info['cookieButtons'])}")
    
    for i, btn in enumerate(info['cookieButtons'], 1):
        print(f"\n--- Botão {i} ---")
        print(f"Texto: {btn['text']}")
        print(f"ID: {btn['id']}")
        print(f"Classes: {btn['className']}")
        print(f"Visível: {btn['visible']}")
        print(f"HTML: {btn['outerHTML'][:200]}...")
    
except Exception as e:
    print(f"⚠ Erro ao capturar: {e}")

print("\n✅ Informações capturadas!")
print("Pressione ENTER para fechar o Chrome...")
input()

driver.quit()
print("✅ Chrome fechado!")
