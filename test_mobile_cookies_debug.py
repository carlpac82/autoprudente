#!/usr/bin/env python3
"""
Debug: Ver EXATAMENTE que botões existem na página mobile
"""
import sys
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

print("=" * 80, flush=True)
print("DEBUG - BOTÕES DE COOKIES NO MOBILE", flush=True)
print("=" * 80, flush=True)

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')

mobile_emulation = {
    "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    "userAgent": mobile_ua
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

print("\n🚀 Iniciando Chrome MOBILE...", flush=True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("\n1️⃣  Abrindo página...", flush=True)
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    
    print("\n⏳ Aguardando 2 segundos...", flush=True)
    time.sleep(2)
    
    print("\n🔍 Procurando TODOS os botões...", flush=True)
    buttons_info = driver.execute_script("""
        const buttons = document.querySelectorAll('button');
        return Array.from(buttons).map((btn, i) => ({
            index: i,
            text: btn.textContent.trim().substring(0, 100),
            visible: btn.offsetParent !== null,
            id: btn.id,
            class: btn.className
        }));
    """)
    
    print(f"\n📋 Total de botões: {len(buttons_info)}", flush=True)
    
    for btn in buttons_info:
        if btn['visible']:
            print(f"\n   Botão #{btn['index']}:", flush=True)
            print(f"      Texto: '{btn['text']}'", flush=True)
            print(f"      ID: '{btn['id']}'", flush=True)
            print(f"      Class: '{btn['class']}'", flush=True)
            
            # Verificar se é botão de cookies
            text_lower = btn['text'].lower()
            if 'aceitar' in text_lower or 'accept' in text_lower or 'cookie' in text_lower:
                print(f"      🍪 POSSÍVEL BOTÃO DE COOKIES!", flush=True)
    
    print("\n\n🔍 Procurando elementos com 'cookie' no ID ou classe...", flush=True)
    cookie_elements = driver.execute_script("""
        const all = document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi], [id*=consent], [class*=consent]');
        return Array.from(all).map(el => ({
            tag: el.tagName,
            id: el.id,
            class: el.className,
            visible: el.offsetParent !== null
        }));
    """)
    
    print(f"\n📋 Elementos com 'cookie': {len(cookie_elements)}", flush=True)
    for el in cookie_elements[:10]:  # Mostrar só os primeiros 10
        if el['visible']:
            print(f"   {el['tag']} - ID: '{el['id']}' - Class: '{el['class']}'", flush=True)
    
    print("\n\n🍪 Tentando aceitar cookies...", flush=True)
    result = driver.execute_script("""
        // Tentar vários seletores
        const selectors = [
            'button:contains("Aceitar")',
            'button:contains("Accept")',
            '[id*=accept]',
            '[class*=accept]',
            'button[id*=cookie]',
            'button[class*=cookie]'
        ];
        
        const buttons = document.querySelectorAll('button');
        for (let btn of buttons) {
            const text = btn.textContent.toLowerCase().trim();
            if (text.includes('aceitar') || text.includes('accept') || 
                text.includes('concordo') || text.includes('agree')) {
                btn.click();
                return {success: true, text: btn.textContent.trim()};
            }
        }
        return {success: false, text: 'Não encontrado'};
    """)
    
    print(f"\n   Resultado: {result}", flush=True)
    
    print("\n\n⏱️  Chrome aberto 60 segundos para inspecionar", flush=True)
    time.sleep(60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}", flush=True)
    import traceback
    traceback.print_exc()
    time.sleep(30)
finally:
    driver.quit()
    print("\n👋 Fechado", flush=True)
