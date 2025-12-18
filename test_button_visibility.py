#!/usr/bin/env python3
"""
Debug: Verificar se botão sendForm está visível
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://www.carjet.com/aluguel-carros/index.htm')
    time.sleep(3)
    
    # Verificar todos os botões
    result = driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        const forms = document.querySelectorAll('form');
        
        return {
            totalButtons: buttons.length,
            totalForms: forms.length,
            sendForm: {
                exists: !!document.getElementById('sendForm'),
                visible: document.getElementById('sendForm')?.offsetParent !== null,
                type: document.getElementById('sendForm')?.type,
                text: document.getElementById('sendForm')?.textContent.trim()
            },
            allButtons: Array.from(buttons).slice(0, 5).map(b => ({
                id: b.id,
                type: b.type,
                visible: b.offsetParent !== null,
                text: b.textContent.trim().slice(0, 30)
            })),
            formButtons: Array.from(forms[0]?.querySelectorAll('button') || []).map(b => ({
                id: b.id,
                type: b.type,
                visible: b.offsetParent !== null,
                text: b.textContent.trim()
            }))
        };
    """)
    
    print("="*80)
    print("RESULTADO DA ANÁLISE")
    print("="*80)
    print(f"\nTotal de botões: {result['totalButtons']}")
    print(f"Total de forms: {result['totalForms']}")
    
    print(f"\n#sendForm:")
    print(f"  Existe: {result['sendForm']['exists']}")
    print(f"  Visível: {result['sendForm']['visible']}")
    print(f"  Type: {result['sendForm']['type']}")
    print(f"  Texto: {result['sendForm']['text']}")
    
    print(f"\nPrimeiros 5 botões:")
    for i, btn in enumerate(result['allButtons']):
        print(f"  {i+1}. id={btn['id']}, type={btn['type']}, visible={btn['visible']}, text='{btn['text']}'")
    
    print(f"\nBotões dentro do form:")
    for btn in result['formButtons']:
        print(f"  - id={btn['id']}, type={btn['type']}, visible={btn['visible']}, text='{btn['text']}'")
    
    # Tentar diferentes estratégias de clique
    print(f"\n{'='*80}")
    print("TESTANDO CLIQUES")
    print("="*80)
    
    strategies = [
        ("Selenium By.ID", lambda: driver.find_element(By.ID, 'sendForm').click()),
        ("JS getElementById", lambda: driver.execute_script("document.getElementById('sendForm').click();")),
        ("JS querySelector", lambda: driver.execute_script("document.querySelector('button[type=\"submit\"]').click();")),
        ("JS form submit", lambda: driver.execute_script("document.querySelector('form').submit();")),
    ]
    
    for name, action in strategies:
        try:
            print(f"\n✓ Tentando: {name}")
            action()
            print(f"  ✅ SUCESSO!")
            break
        except Exception as e:
            print(f"  ❌ Falhou: {str(e)[:100]}")
    
finally:
    driver.quit()
