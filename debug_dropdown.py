#!/usr/bin/env python3
"""
Debug script - capturar estrutura HTML do dropdown do CarJet
Abre browser, escreve "Faro" e captura HTML do dropdown para análise
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def debug_dropdown():
    print("=" * 70)
    print("DEBUG DROPDOWN CARJET")
    print("Este script vai capturar a estrutura HTML do dropdown")
    print("=" * 70)
    
    chrome_options = Options()
    # EMULAÇÃO MOBILE iPhone 13 Pro
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # iPhone 13 Pro emulation
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = None
    try:
        print("\n[1] Iniciando Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(60)
        
        print("[2] Abrindo CarJet...")
        driver.get("https://www.carjet.com/aluguel-carros/index.htm")
        time.sleep(3)
        
        # Tratar cookies
        print("[3] Tratando cookies...")
        try:
            driver.execute_script("""
                document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=consent], [id*=didomi]').forEach(el => el.remove());
                document.body.style.overflow = 'auto';
            """)
        except:
            pass
        
        time.sleep(1)
        
        # Encontrar campo de pickup
        print("[4] Procurando campo de pickup...")
        pickup_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        
        # Capturar HTML inicial
        print("[5] Capturando HTML do formulário...")
        form_html = driver.execute_script("""
            const form = document.querySelector('form');
            return form ? form.outerHTML.substring(0, 3000) : 'form não encontrado';
        """)
        print(f"\n--- FORM HTML (primeiros 3000 chars) ---")
        print(form_html[:1500])
        print("...")
        
        # Clicar no campo e digitar
        print("\n[6] Clicando no campo pickup...")
        pickup_input.click()
        time.sleep(0.5)
        
        print("[7] Digitando 'Faro'...")
        pickup_input.clear()
        for char in "Faro":
            pickup_input.send_keys(char)
            time.sleep(0.1)
        
        print("[8] Aguardando dropdown aparecer (5 segundos)...")
        time.sleep(5)
        
        # Capturar TODOS os elementos que podem ser dropdown
        print("\n[9] Capturando elementos dropdown...")
        dropdown_info = driver.execute_script("""
            const results = [];
            
            // Procurar por vários seletores possíveis
            const selectors = [
                '#recogida_lista',
                '.ui-autocomplete',
                '.autocomplete-suggestions',
                '[class*="autocomplete"]',
                '[class*="dropdown"]',
                '[class*="suggestion"]',
                '[id*="lista"]',
                'ul[style*="display: block"]',
                'ul[style*="display:block"]',
                'div[style*="display: block"]'
            ];
            
            for (const sel of selectors) {
                const els = document.querySelectorAll(sel);
                for (const el of els) {
                    const rect = el.getBoundingClientRect();
                    if (rect.height > 0) {  // Só elementos visíveis
                        results.push({
                            selector: sel,
                            id: el.id,
                            className: el.className,
                            tagName: el.tagName,
                            visible: rect.height > 0,
                            childCount: el.children.length,
                            innerHTML: el.innerHTML.substring(0, 500),
                            rect: {width: rect.width, height: rect.height, top: rect.top}
                        });
                    }
                }
            }
            
            // Também procurar LI elements que possam ser opções
            const allLis = document.querySelectorAll('li');
            let visibleLis = [];
            for (const li of allLis) {
                const rect = li.getBoundingClientRect();
                if (rect.height > 20 && rect.top > 100 && rect.top < 500) {
                    visibleLis.push({
                        text: li.textContent?.substring(0, 50),
                        parentId: li.parentElement?.id,
                        parentClass: li.parentElement?.className
                    });
                }
            }
            
            return {elements: results, visibleLis: visibleLis.slice(0, 10)};
        """)
        
        print("\n" + "=" * 70)
        print("ELEMENTOS DROPDOWN ENCONTRADOS:")
        print("=" * 70)
        
        if dropdown_info['elements']:
            for i, el in enumerate(dropdown_info['elements']):
                print(f"\n--- Elemento {i+1} ---")
                print(f"Selector: {el['selector']}")
                print(f"ID: {el['id']}")
                print(f"Class: {el['className']}")
                print(f"Tag: {el['tagName']}")
                print(f"Filhos: {el['childCount']}")
                print(f"Tamanho: {el['rect']}")
                print(f"HTML: {el['innerHTML'][:300]}...")
        else:
            print("NENHUM elemento dropdown encontrado!")
        
        print("\n" + "=" * 70)
        print("LIs VISÍVEIS (possíveis opções):")
        print("=" * 70)
        
        if dropdown_info['visibleLis']:
            for li in dropdown_info['visibleLis']:
                print(f"  - '{li['text']}' (parent: #{li['parentId']} .{li['parentClass']})")
        else:
            print("NENHUM LI visível encontrado!")
        
        # Screenshot
        print("\n[10] Guardando screenshot...")
        driver.save_screenshot("/tmp/carjet_dropdown_debug.png")
        print("Screenshot guardado em /tmp/carjet_dropdown_debug.png")
        
        print("\n" + "=" * 70)
        print("O browser vai ficar aberto. Interaja manualmente se quiser.")
        print("Prima ENTER para fechar...")
        print("=" * 70)
        input()
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        if driver:
            print("\nPrima ENTER para fechar...")
            input()
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    debug_dropdown()
