#!/usr/bin/env python3
"""
Teste SIMPLES: Preencher e mostrar valores
"""
import sys
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

start_dt = datetime.now() + timedelta(days=7)
end_dt = start_dt + timedelta(days=5)

print(f"Datas: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}", flush=True)

mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f'user-agent={mobile_ua}')
mobile_emulation = {"deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0}, "userAgent": mobile_ua}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://www.carjet.com/aluguel-carros/index.htm")
    time.sleep(2)
    
    # Remover cookies
    driver.execute_script("document.querySelectorAll('[id*=cookie]').forEach(el => el.remove());")
    
    # Preencher local
    pickup = driver.find_element(By.ID, "pickup")
    pickup.clear()
    pickup.send_keys("Albufeira Cidade")
    time.sleep(2)
    driver.execute_script("document.querySelector('#recogida_lista li[data-id=\"Albufeira Cidade\"]').click();")
    time.sleep(2)
    
    # Preencher datas e horas SEPARADAMENTE
    print("\nPreenchendo data recolha...", flush=True)
    driver.execute_script("document.querySelector('input[id=\"fechaRecogida\"]').value = arguments[0];", start_dt.strftime("%d/%m/%Y"))
    time.sleep(0.5)
    
    print("Preenchendo data devolução...", flush=True)
    driver.execute_script("document.querySelector('input[id=\"fechaDevolucion\"]').value = arguments[0];", end_dt.strftime("%d/%m/%Y"))
    time.sleep(0.5)
    
    print("Preenchendo horas...", flush=True)
    driver.execute_script("""
        document.querySelector('select[id="fechaRecogidaSelHour"]').value = '10:00';
        document.querySelector('select[id="fechaDevolucionSelHour"]').value = '10:00';
    """)
    time.sleep(1)
    
    # Verificar
    print("\n=== VALORES FINAIS ===", flush=True)
    values = driver.execute_script("""
        return {
            pickup: document.querySelector('input[id="pickup"]')?.value,
            fechaRecogida: document.querySelector('input[id="fechaRecogida"]')?.value,
            fechaDevolucion: document.querySelector('input[id="fechaDevolucion"]')?.value,
            horaRecogida: document.querySelector('select[id="fechaRecogidaSelHour"]')?.value,
            horaDevolucion: document.querySelector('select[id="fechaDevolucionSelHour"]')?.value
        };
    """)
    
    for key, val in values.items():
        print(f"{key}: {val}", flush=True)
    
    print("\nChrome aberto 90 segundos", flush=True)
    time.sleep(90)
    
except Exception as e:
    print(f"ERRO: {e}", flush=True)
    time.sleep(30)
finally:
    driver.quit()
