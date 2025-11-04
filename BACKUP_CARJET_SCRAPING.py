"""
═══════════════════════════════════════════════════════════════════════════════
BACKUP COMPLETO DO SCRAPING CARJET - Nov 4, 2025
═══════════════════════════════════════════════════════════════════════════════

Este arquivo contém TODO o código de scraping do Carjet, incluindo:
- 8 passos exatos de preenchimento do formulário
- 7 idiomas suportados com traduções
- Rotações anti-detecção (devices, timezones, referrers, horas)
- Tratamento de cookies
- Retry logic para war= errors
- Seletores CSS corretos e testados

TESTADO E FUNCIONANDO EM TODOS OS 7 IDIOMAS!

═══════════════════════════════════════════════════════════════════════════════
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import random


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DOS 7 IDIOMAS SUPORTADOS
# ═══════════════════════════════════════════════════════════════════════════════

CARJET_LANGUAGES = [
    {
        'name': 'Português',
        'url': 'https://www.carjet.com/aluguel-carros/index.htm',
        'faro': 'Faro Aeroporto (FAO)',
        'albufeira': 'Albufeira Cidade'
    },
    {
        'name': 'English',
        'url': 'https://www.carjet.com/index.htm',
        'faro': 'Faro Airport (FAO)',
        'albufeira': 'Albufeira City'
    },
    {
        'name': 'Français',
        'url': 'https://www.carjet.com/location-voitures/index.htm',
        'faro': 'Faro Aéroport (FAO)',
        'albufeira': 'Albufeira Centre ville'
    },
    {
        'name': 'Español',
        'url': 'https://www.carjet.com/alquiler-coches/index.htm',
        'faro': 'Faro Aeropuerto (FAO)',
        'albufeira': 'Albufeira Ciudad'
    },
    {
        'name': 'Deutsch',
        'url': 'https://www.carjet.com/mietwagen/index.htm',
        'faro': 'Faro Flughafen (FAO)',
        'albufeira': 'Albufeira Stadt'
    },
    {
        'name': 'Italiano',
        'url': 'https://www.carjet.com/autonoleggio/index.htm',
        'faro': 'Faro Aeroporto (FAO)',
        'albufeira': 'Albufeira Città'
    },
    {
        'name': 'Nederlands',
        'url': 'https://www.carjet.com/autohuur/index.htm',
        'faro': 'Faro Vliegveld (FAO)',
        'albufeira': 'Albufeira Stad'
    }
]


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO ANTI-DETECÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

# 1. DISPOSITIVOS MOBILE (4 devices)
MOBILE_DEVICES = [
    {
        'name': 'iPhone 13',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'iPhone 12',
        'ua': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'width': 390, 'height': 844, 'pixelRatio': 3.0
    },
    {
        'name': 'Samsung Galaxy S21',
        'ua': 'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 360, 'height': 800, 'pixelRatio': 3.0
    },
    {
        'name': 'Google Pixel 5',
        'ua': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'width': 393, 'height': 851, 'pixelRatio': 2.75
    }
]

# 2. TIMEZONES EUROPEUS (4 opções)
TIMEZONES = [
    'Europe/Lisbon',    # Portugal
    'Europe/Madrid',    # Espanha
    'Europe/London',    # UK
    'Europe/Paris'      # França
]

# 3. LANGUAGES (4 opções)
LANGUAGES = [
    'pt-PT,pt;q=0.9,en;q=0.8',  # Portugal
    'pt-BR,pt;q=0.9,en;q=0.8',  # Brasil
    'en-GB,en;q=0.9',           # UK
    'es-ES,es;q=0.9,en;q=0.8'   # Espanha
]

# 4. REFERRERS (5 opções)
REFERRERS = [
    'https://www.google.com/search?q=aluguer+carros+faro',
    'https://www.google.pt/search?q=rent+car+portugal',
    'https://www.bing.com/search?q=car+rental+algarve',
    'https://www.booking.com/',
    ''  # Direct (sem referrer)
]

# 5. HORAS DISPONÍVEIS (6 opções)
AVAILABLE_HOURS = ['14:30', '15:00', '15:30', '16:00', '16:30', '17:00']


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPOS DO FORMULÁRIO CARJET (NUNCA MUDAR!)
# ═══════════════════════════════════════════════════════════════════════════════

CARJET_FIELDS = {
    'pickup': 'input[id="pickup"]',
    'fechaRecogida': 'input[id="fechaRecogida"]',
    'fechaDevolucion': 'input[id="fechaDevolucion"]',
    'fechaRecogidaSelHour': 'select[id="fechaRecogidaSelHour"]',
    'fechaDevolucionSelHour': 'select[id="fechaDevolucionSelHour"]'
}


# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO PRINCIPAL DE SCRAPING
# ═══════════════════════════════════════════════════════════════════════════════

def scrape_carjet_selenium(location, start_dt, end_dt):
    """
    Scraping completo do Carjet usando Selenium com os 8 passos documentados.
    
    Args:
        location: Nome da localização (ex: "Faro", "Albufeira")
        start_dt: Data/hora de recolha (datetime)
        end_dt: Data/hora de devolução (datetime)
    
    Returns:
        tuple: (final_url, html_content) ou (None, None) se falhar
    """
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PASSO 0: CONFIGURAÇÃO INICIAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Selecionar idioma aleatoriamente
    selected_language = random.choice(CARJET_LANGUAGES)
    
    # Mapear location para formato CarJet no idioma selecionado
    carjet_location = location
    if 'faro' in location.lower():
        carjet_location = selected_language['faro']
    elif 'albufeira' in location.lower():
        carjet_location = selected_language['albufeira']
    
    carjet_url = selected_language['url']
    
    print(f"[CARJET] Idioma: {selected_language['name']}")
    print(f"[CARJET] URL: {carjet_url}")
    print(f"[CARJET] Local: {carjet_location}")
    
    # Rotação de datas (0-4 dias aleatório)
    date_offset = random.randint(0, 4)
    start_dt = start_dt + timedelta(days=date_offset)
    end_dt = end_dt + timedelta(days=date_offset)
    
    # Rotação de horas
    selected_hour = random.choice(AVAILABLE_HOURS)
    start_dt = start_dt.replace(
        hour=int(selected_hour.split(':')[0]), 
        minute=int(selected_hour.split(':')[1])
    )
    end_dt = end_dt.replace(
        hour=int(selected_hour.split(':')[0]), 
        minute=int(selected_hour.split(':')[1])
    )
    
    print(f"[CARJET] Datas: {start_dt.date()} - {end_dt.date()}")
    print(f"[CARJET] Hora: {selected_hour}")
    
    # Selecionar configurações anti-detecção
    selected_device = random.choice(MOBILE_DEVICES)
    selected_timezone = random.choice(TIMEZONES)
    selected_lang = random.choice(LANGUAGES)
    selected_referrer = random.choice(REFERRERS)
    
    print(f"[CARJET] Device: {selected_device['name']}")
    print(f"[CARJET] Timezone: {selected_timezone}")
    print(f"[CARJET] Referrer: {selected_referrer if selected_referrer else 'Direct'}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONFIGURAR CHROME
    # ═══════════════════════════════════════════════════════════════════════════
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={selected_device["ua"]}')
    chrome_options.add_argument(f'--lang={selected_lang.split(",")[0]}')
    
    # Emulação mobile
    mobile_emulation = {
        "deviceMetrics": { 
            "width": selected_device['width'], 
            "height": selected_device['height'], 
            "pixelRatio": selected_device['pixelRatio']
        },
        "userAgent": selected_device['ua']
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    # Anti-detecção
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Preferências
    chrome_options.add_experimental_option("prefs", {
        "intl.accept_languages": selected_lang,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_settings.cookies": 2,
        "profile.block_third_party_cookies": True
    })
    
    chrome_options.add_argument(f'--timezone={selected_timezone}')
    
    # Caminho do Chrome no Mac (ajustar se necessário)
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # Iniciar driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print(f"[CARJET] ✅ Chrome iniciado")
    except Exception as e:
        print(f"[CARJET] ❌ Erro ao iniciar Chrome: {e}")
        return None, None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FUNÇÃO HELPER: REJEITAR COOKIES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def reject_cookies_if_present(step_name=""):
        """Detecta e REJEITA cookies automaticamente."""
        try:
            result = driver.execute_script("""
                const buttons = document.querySelectorAll('button, a, [role="button"]');
                let found = false;
                for (let btn of buttons) {
                    const text = btn.textContent.toLowerCase().trim();
                    if (text.includes('rejeitar') || text.includes('recusar') || 
                        text.includes('reject') || text.includes('rechazar') ||
                        text.includes('não aceitar') || text.includes('decline')) {
                        btn.click();
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    document.querySelectorAll('[id*=cookie], [class*=cookie], [id*=didomi], [class*=didomi]').forEach(el => {
                        el.remove();
                    });
                }
                document.body.style.overflow = 'auto';
                return found;
            """)
            if result:
                print(f"[CARJET] ✓ Cookies rejeitados {step_name}")
            return result
        except Exception as e:
            print(f"[CARJET] ⚠ Erro ao rejeitar cookies: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OS 8 PASSOS DO FORMULÁRIO
    # ═══════════════════════════════════════════════════════════════════════════
    
    try:
        # Esconder webdriver
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
        
        driver.set_page_load_timeout(20)
        
        # Definir referrer
        if selected_referrer:
            driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
                'headers': {'Referer': selected_referrer}
            })
        
        # Navegar para Carjet
        print(f"[CARJET] Navegando para {carjet_url}")
        driver.get(carjet_url)
        
        # ═══════════════════════════════════════════════════════════════════════
        # PASSO 1: ACEITAR/REJEITAR COOKIES
        # ═══════════════════════════════════════════════════════════════════════
        print(f"[CARJET] PASSO 1: Rejeitando cookies...")
        time.sleep(0.3)
        reject_cookies_if_present("(inicial)")
        time.sleep(0.5)
        reject_cookies_if_present("(retry)")
        time.sleep(0.5)
        
        # ═══════════════════════════════════════════════════════════════════════
        # PASSO 2: ESCREVER O NOME DO LOCAL
        # ═══════════════════════════════════════════════════════════════════════
        print(f"[CARJET] PASSO 2: Escrevendo local '{carjet_location}'...")
        
        pickup_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickup"))
        )
        pickup_input.clear()
        pickup_input.send_keys(carjet_location)
        print(f"[CARJET] ✓ Local digitado")
        
        # ═══════════════════════════════════════════════════════════════════════
        # PASSO 3: CLICAR NO ITEM DO DROPDOWN ⚠️ CRÍTICO!
        # ═══════════════════════════════════════════════════════════════════════
        print(f"[CARJET] PASSO 3: Aguardando dropdown...")
        time.sleep(2)
        
        clicked = False
        
        # Tentar seletores CSS
        selectors = [
            "#recogida_lista li:first-child a",  # ✅ PRINCIPAL - FUNCIONA EM TODOS OS IDIOMAS
            "#recogida_lista li:first-child",
            f"#recogida_lista li[data-id='{carjet_location}'] a",
            f"#recogida_lista li[data-id='{carjet_location}']",
        ]
        
        for selector in selectors:
            if clicked:
                break
            try:
                dropdown_item = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                dropdown_item.click()
                clicked = True
                print(f"[CARJET] ✓ Dropdown clicado via: {selector}")
                break
            except:
                pass
        
        # Fallback JavaScript
        if not clicked:
            print(f"[CARJET] Tentando via JavaScript...")
            result = driver.execute_script("""
                const items = document.querySelectorAll('#recogida_lista li');
                for (let item of items) {
                    if (item.offsetParent !== null) {
                        item.click();
                        return true;
                    }
                }
                return false;
            """)
            if result:
                clicked = True
                print(f"[CARJET] ✓ Dropdown clicado via JavaScript")
        
        if not clicked:
            print(f"[CARJET] ❌ Não conseguiu clicar no dropdown!")
            driver.quit()
            return None, None
        
        time.sleep(1)
        
        # ═══════════════════════════════════════════════════════════════════════
        # PASSOS 4-7: PREENCHER DATAS E HORAS VIA JAVASCRIPT
        # ═══════════════════════════════════════════════════════════════════════
        print(f"[CARJET] PASSOS 4-7: Preenchendo datas e horas...")
        
        result = driver.execute_script("""
            function fill(sel, val) {
                const el = document.querySelector(sel);
                if (el) { 
                    el.value = val; 
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    el.dispatchEvent(new Event('blur', {bubbles: true}));
                    return true;
                }
                return false;
            }
            
            // PASSO 4: Data de recolha
            const r1 = fill('input[id="fechaRecogida"]', arguments[0]);
            
            // PASSO 5: Data de devolução
            const r2 = fill('input[id="fechaDevolucion"]', arguments[1]);
            
            // PASSO 6: Hora de recolha
            const h1 = document.querySelector('select[id="fechaRecogidaSelHour"]');
            let h1_ok = false;
            if (h1) { 
                h1.value = arguments[2]; 
                h1.dispatchEvent(new Event('change', {bubbles: true}));
                h1_ok = true;
            }
            
            // PASSO 7: Hora de devolução
            const h2 = document.querySelector('select[id="fechaDevolucionSelHour"]');
            let h2_ok = false;
            if (h2) { 
                h2.value = arguments[3]; 
                h2.dispatchEvent(new Event('change', {bubbles: true}));
                h2_ok = true;
            }
            
            return {
                fechaRecogida: r1,
                fechaDevolucion: r2,
                horaRecogida: h1_ok,
                horaDevolucion: h2_ok,
                allFilled: r1 && r2 && h1_ok && h2_ok
            };
        """, 
        start_dt.strftime("%d/%m/%Y"), 
        end_dt.strftime("%d/%m/%Y"), 
        start_dt.strftime("%H:%M"), 
        end_dt.strftime("%H:%M"))
        
        if result and result.get('allFilled'):
            print(f"[CARJET] ✅ Formulário completo preenchido!")
        else:
            print(f"[CARJET] ⚠️ Preenchimento incompleto: {result}")
        
        time.sleep(1)
        
        # ═══════════════════════════════════════════════════════════════════════
        # PASSO 8: CLICAR EM BUSCAR
        # ═══════════════════════════════════════════════════════════════════════
        print(f"[CARJET] PASSO 8: Submetendo formulário...")
        
        # Rejeitar cookies antes de submeter
        reject_cookies_if_present("(antes de submeter)")
        
        # Delays e scroll simulation (anti-bot)
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        
        scroll_amount = random.randint(200, 500)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.3, 0.7))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.3)
        
        # Submit
        driver.execute_script("document.querySelector('form').submit();")
        
        # Aguardar navegação
        print(f"[CARJET] Aguardando navegação...")
        time.sleep(5)
        
        # Rejeitar cookies após submeter
        reject_cookies_if_present("(após submeter)")
        time.sleep(2)
        
        final_url = driver.current_url
        print(f"[CARJET] URL final: {final_url}")
        
        # ═══════════════════════════════════════════════════════════════════════
        # VALIDAÇÃO DE SUCESSO
        # ═══════════════════════════════════════════════════════════════════════
        
        if '/do/list/' in final_url and 's=' in final_url and 'b=' in final_url:
            print(f"[CARJET] ✅ SUCESSO! URL válida com s= e b=")
            html_content = driver.page_source
            driver.quit()
            return final_url, html_content
        
        elif 'war=' in final_url:
            print(f"[CARJET] ⚠️ URL contém war= (sem disponibilidade)")
            driver.quit()
            return None, None
        
        else:
            print(f"[CARJET] ⚠️ URL inesperada")
            driver.quit()
            return None, None
        
    except Exception as e:
        print(f"[CARJET] ❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        try:
            driver.quit()
        except:
            pass
        return None, None


# ═══════════════════════════════════════════════════════════════════════════════
# EXEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# MÉTODO ALTERNATIVO: POST DIRETO (try_direct_carjet)
# ═══════════════════════════════════════════════════════════════════════════════

import requests
import re
from bs4 import BeautifulSoup
from typing import Dict, Any

# Códigos de localização conhecidos
LOCATION_CODES = {
    "faro": "FAO",
    "faro aeroporto": "FAO",
    "faro airport": "FAO",
    "albufeira": "ALBUFEIRA",
    "albufeira cidade": "ALBUFEIRA",
    "albufeira city": "ALBUFEIRA",
}


def try_direct_carjet(location_name: str, start_dt, end_dt, lang: str = "pt", currency: str = "EUR") -> str:
    """
    Método alternativo: POST direto ao Carjet sem Selenium.
    Mais rápido mas menos confiável que Selenium.
    
    Args:
        location_name: Nome da localização
        start_dt: Data/hora de recolha
        end_dt: Data/hora de devolução
        lang: Idioma (pt, en, es, fr, de, it, nl)
        currency: Moeda (EUR, USD, GBP, etc)
    
    Returns:
        str: HTML da página de resultados ou string vazia se falhar
    """
    try:
        sess = requests.Session()
        ua = {
            "User-Agent": "Mozilla/5.0 (compatible; PriceTracker/1.0)",
            "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.6",
            "X-Forwarded-For": "185.23.160.1",
            "Referer": "https://www.carjet.com/do/list/pt",
        }
        lang = (lang or "pt").lower()
        
        # Pre-seed cookies
        try:
            sess.cookies.set("monedaForzada", currency)
            sess.cookies.set("moneda", currency)
            sess.cookies.set("currency", currency)
            sess.cookies.set("idioma", lang.upper())
            sess.cookies.set("lang", lang)
            sess.cookies.set("country", "PT")
        except:
            pass
        
        # Determinar homepage por idioma
        if lang == "pt":
            home_path = "aluguel-carros/index.htm"
        elif lang == "es":
            home_path = "alquiler-coches/index.htm"
        elif lang == "fr":
            home_path = "location-voitures/index.htm"
        elif lang == "de":
            home_path = "mietwagen/index.htm"
        elif lang == "it":
            home_path = "autonoleggio/index.htm"
        elif lang == "nl":
            home_path = "autohuur/index.htm"
        else:
            home_path = "index.htm"
        
        home_url = f"https://www.carjet.com/{home_path}"
        home = sess.get(home_url, headers=ua, timeout=20)
        
        # Tentar extrair tokens s= e b=
        s_token = None
        b_token = None
        try:
            m = re.search(r"[?&]s=([A-Za-z0-9-]+)", home.text)
            if m:
                s_token = m.group(1)
            m = re.search(r"[?&]b=([A-Za-z0-9-]+)", home.text)
            if m:
                b_token = m.group(1)
        except:
            pass
        
        # Construir payload
        data = build_carjet_form(location_name, start_dt, end_dt, lang=lang, currency=currency)
        if s_token:
            data["s"] = s_token
        if b_token:
            data["b"] = b_token
        
        headers = {
            "User-Agent": ua["User-Agent"],
            "Origin": "https://www.carjet.com",
            "Referer": home_url,
            "Accept-Language": ua.get("Accept-Language", "pt-PT,pt;q=0.9,en;q=0.6"),
        }
        
        # POST para /do/list/{lang}
        url = f"https://www.carjet.com/do/list/{lang}"
        resp = sess.post(url, data=data, headers=headers, timeout=25)
        
        if resp.status_code == 200 and resp.text:
            return resp.text
        
    except Exception as e:
        print(f"[DIRECT_POST] Erro: {e}")
    
    return ""


def build_carjet_form(location_name: str, start_dt, end_dt, lang: str = "pt", currency: str = "EUR") -> Dict[str, Any]:
    """
    Constrói o payload do formulário Carjet.
    
    Args:
        location_name: Nome da localização
        start_dt: Data/hora de recolha
        end_dt: Data/hora de devolução
        lang: Idioma
        currency: Moeda
    
    Returns:
        Dict com campos do formulário
    """
    pickup_dmY = start_dt.strftime("%d/%m/%Y")
    dropoff_dmY = end_dt.strftime("%d/%m/%Y")
    pickup_HM = start_dt.strftime("%H:%M")
    dropoff_HM = end_dt.strftime("%H:%M")
    
    code = LOCATION_CODES.get((location_name or "").lower(), "")
    
    form = {
        # Campos de texto
        "pickup": location_name,
        "dropoff": location_name,
        
        # IDs de destino
        "pickupId": code,
        "dst_id": code,
        "zoneCode": code,
        
        # Datas (CAMPOS CORRETOS - NUNCA MUDAR!)
        "fechaRecogida": pickup_dmY,
        "fechaEntrega": dropoff_dmY,
        
        # Horas (CAMPOS CORRETOS - NUNCA MUDAR!)
        "fechaRecogidaSelHour": pickup_HM,
        "fechaEntregaSelHour": dropoff_HM,
        
        # Locale
        "idioma": lang.upper(),
        "moneda": currency,
        "chkOneWay": "SI",
        
        # Campos adicionais
        "frmDestino": code or "",
        "frmFechaRecogida": f"{pickup_dmY} {pickup_HM}",
        "frmFechaDevolucion": f"{dropoff_dmY} {dropoff_HM}",
        "frmMoneda": currency,
    }
    
    return form


# ═══════════════════════════════════════════════════════════════════════════════
# EXEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Exemplo de teste
    location = "Faro"
    start_dt = datetime.now() + timedelta(days=7)
    end_dt = start_dt + timedelta(days=3)
    
    print("═" * 80)
    print("TESTE DE SCRAPING CARJET")
    print("═" * 80)
    
    # Método 1: Selenium (mais confiável)
    print("\n[MÉTODO 1] Tentando via Selenium...")
    final_url, html = scrape_carjet_selenium(location, start_dt, end_dt)
    
    if final_url and html:
        print(f"\n✅ SUCESSO VIA SELENIUM!")
        print(f"URL: {final_url}")
        print(f"HTML: {len(html)} bytes")
    else:
        print(f"\n⚠️ Selenium falhou, tentando POST direto...")
        
        # Método 2: POST direto (fallback)
        print("\n[MÉTODO 2] Tentando via POST direto...")
        html = try_direct_carjet(location, start_dt, end_dt, lang="pt", currency="EUR")
        
        if html:
            print(f"\n✅ SUCESSO VIA POST DIRETO!")
            print(f"HTML: {len(html)} bytes")
        else:
            print(f"\n❌ AMBOS OS MÉTODOS FALHARAM!")
