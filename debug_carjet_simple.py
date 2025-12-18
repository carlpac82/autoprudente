#!/usr/bin/env python3
"""
Debug script simples usando Selenium para analisar estrutura HTML do CarJet
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys
import time
from datetime import datetime, timedelta

def analyze_carjet_html():
    """Captura e analisa HTML do CarJet"""
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("📱 Acessando CarJet...", file=sys.stderr)
        driver.get('https://www.carjet.com/aluguel-carros/index.htm')
        time.sleep(2)
        
        # Rejeita cookies
        try:
            reject_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Rejeitar')]")
            reject_btn.click()
            print("✅ Cookies rejeitados", file=sys.stderr)
            time.sleep(1)
        except:
            print("⚠️  Sem popup de cookies", file=sys.stderr)
        
        # Preenche formulário
        location_input = driver.find_element(By.NAME, 'txt-rent-pickup')
        location_input.clear()
        location_input.send_keys('Albufeira')
        time.sleep(1)
        
        # Clica no dropdown
        driver.execute_script("document.querySelector('.uiListTxt').click();")
        time.sleep(1)
        
        # Datas
        start_date = datetime.now() + timedelta(days=2)
        end_date = start_date + timedelta(days=2)
        
        pickup_date = driver.find_element(By.NAME, 'pickUpDate')
        pickup_date.clear()
        pickup_date.send_keys(start_date.strftime('%d/%m/%Y'))
        
        dropoff_date = driver.find_element(By.NAME, 'dropOffDate')
        dropoff_date.clear()
        dropoff_date.send_keys(end_date.strftime('%d/%m/%Y'))
        
        Select(driver.find_element(By.NAME, 'pickUpTime')).select_by_value('15:00')
        Select(driver.find_element(By.NAME, 'dropOffTime')).select_by_value('15:00')
        
        print("📝 Formulário preenchido", file=sys.stderr)
        
        # Submete
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_btn.click()
            print("🔄 Formulário submetido", file=sys.stderr)
        except:
            print("⚠️  Submit via JS", file=sys.stderr)
            driver.execute_script("document.querySelector('form').submit();")
        
        # Aguarda página carregar
        time.sleep(8)
        
        current_url = driver.current_url
        print(f"🌐 URL atual: {current_url}", file=sys.stderr)
        
        # Captura HTML
        html = driver.page_source
        print(f"📄 HTML capturado: {len(html)} bytes", file=sys.stderr)
        
        # Salva HTML
        with open('carjet_debug_structure.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("💾 HTML salvo: carjet_debug_structure.html", file=sys.stderr)
        
        # Analisa estrutura
        soup = BeautifulSoup(html, 'html.parser')
        
        print("\n" + "="*80, file=sys.stderr)
        print("🔍 ANÁLISE DA ESTRUTURA", file=sys.stderr)
        print("="*80, file=sys.stderr)
        
        # Procura por diferentes seletores de cards
        selectors = [
            ("article", None),
            ("article.car", None),
            ("li.result", None),
            ("li.car", None),
            (".car-item", None),
            (".result-row", None),
            ("section.newcarlist article", None),
            (".newcarlist article", None),
            ("div[class*='car']", "div com 'car' na classe"),
            ("div[class*='result']", "div com 'result' na classe"),
            ("div[class*='vehicle']", "div com 'vehicle' na classe"),
        ]
        
        for selector, desc in selectors:
            elements = soup.select(selector)
            if elements:
                label = desc or selector
                print(f"\n✅ {label}: {len(elements)} elementos", file=sys.stderr)
                
                # Analisa primeiro elemento
                first = elements[0]
                print(f"   Classes do elemento: {first.get('class')}", file=sys.stderr)
                
                # Mostra estrutura interna
                print(f"   Tags internas: {[tag.name for tag in first.find_all(recursive=False)]}", file=sys.stderr)
                
                # Procura preços
                price_selectors = [
                    ".price.pr-euros",
                    ".pr-euros",
                    ".price",
                    "span[class*='price']",
                    "span[class*='Price']",
                    "div[class*='price']",
                    "div[class*='Price']",
                ]
                
                for ps in price_selectors:
                    prices = first.select(ps)
                    if prices:
                        print(f"   💰 {ps}: {len(prices)} encontrados", file=sys.stderr)
                        for i, p in enumerate(prices[:3]):
                            print(f"      [{i}] classes={p.get('class')} text='{p.get_text(strip=True)[:50]}'", file=sys.stderr)
                
                # Procura todos os spans no primeiro elemento
                spans = first.find_all('span')
                print(f"   📊 Total de spans: {len(spans)}", file=sys.stderr)
                if spans:
                    print(f"   📊 Primeiros 10 spans:", file=sys.stderr)
                    for i, sp in enumerate(spans[:10]):
                        classes = sp.get('class', [])
                        text = sp.get_text(strip=True)[:50]
                        print(f"      [{i}] classes={classes} text='{text}'", file=sys.stderr)
                
                break  # Só analisa o primeiro seletor que encontrar resultados
        
        # Se não encontrou nada, mostra estrutura geral
        if not any(soup.select(sel[0]) for sel in selectors):
            print("\n⚠️  NENHUM SELETOR ENCONTROU RESULTADOS", file=sys.stderr)
            print("\n📋 Estrutura geral do body:", file=sys.stderr)
            body = soup.find('body')
            if body:
                for child in body.children:
                    if hasattr(child, 'name') and child.name:
                        classes = child.get('class', [])
                        print(f"   - {child.name}: {classes}", file=sys.stderr)
        
        driver.quit()
        print("\n✅ Análise completa!", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        driver.quit()
        raise

if __name__ == '__main__':
    analyze_carjet_html()
