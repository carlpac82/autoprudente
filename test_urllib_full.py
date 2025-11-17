#!/usr/bin/env python3
"""
Teste completo do urllib - ver todos os redirects
"""
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import uuid
import time

location = "Albufeira"
start_dt = datetime.now() + timedelta(days=2)
end_dt = start_dt + timedelta(days=7)

pickup_code = 'ABF01'
pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
return_date = end_dt.strftime('%d/%m/%Y %H:%M')
session_id = str(uuid.uuid4())

form_data = {
    'frmDestino': pickup_code,
    'frmDestinoFinal': '',
    'frmFechaRecogida': pickup_date,
    'frmFechaDevolucion': return_date,
    'frmHasAge': 'False',
    'frmEdad': '35',
    'frmPrvNo': '',
    'frmMoneda': 'EUR',
    'frmMonedaForzada': '',
    'frmJsonFilterInfo': '',
    'frmTipoVeh': 'CAR',
    'idioma': 'PT',
    'frmSession': session_id,
    'frmDetailCode': ''
}

encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
url = 'https://www.carjet.com/do/list/pt'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-PT,pt;q=0.9',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
    'Referer': 'https://www.carjet.com/aluguel-carros/index.htm',
    'Origin': 'https://www.carjet.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

print(f"🔍 TESTE COMPLETO URLLIB")
print(f"Location: {location}")
print(f"Dates: {pickup_date} - {return_date}")
print("=" * 80)

# POST inicial
print(f"📤 STEP 1: POST → {url}")
req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')

with urllib.request.urlopen(req, timeout=30) as response:
    html1 = response.read().decode('utf-8')

print(f"✅ HTML recebido: {len(html1)} bytes")

# Verificar redirect
if 'window.location.replace' in html1:
    print("✅ Encontrou redirect no HTML")
    
    import re
    pattern = r"window\.location\.replace\('([^']+)'\)"
    match = re.search(pattern, html1)
    
    if match:
        redirect_url = match.group(1)
        print(f"🔗 Redirect URL: {redirect_url}")
        
        # Aguardar
        print("⏳ Aguardando 5 segundos...")
        time.sleep(5)
        
        # GET do redirect
        full_url = f'https://www.carjet.com{redirect_url}'
        print(f"\n📤 STEP 2: GET → {full_url[:100]}...")
        
        headers2 = dict(headers)
        headers2['Cookie'] = 'monedaForzada=EUR; moneda=EUR; currency=EUR; country=PT; idioma=PT; lang=pt'
        del headers2['Content-Type']  # GET não tem Content-Type
        
        req2 = urllib.request.Request(full_url, headers=headers2, method='GET')
        
        with urllib.request.urlopen(req2, timeout=30) as response2:
            html2 = response2.read().decode('utf-8')
        
        print(f"✅ HTML recebido: {len(html2)} bytes")
        
        # Verificar se tem OUTRO redirect
        if 'window.location.replace' in html2:
            print("⚠️ HTML ainda tem redirect - precisa de mais um GET")
            
            match2 = re.search(pattern, html2)
            if match2:
                redirect_url2 = match2.group(1)
                print(f"🔗 Segundo redirect: {redirect_url2}")
                
                print("⏳ Aguardando 5 segundos...")
                time.sleep(5)
                
                full_url2 = f'https://www.carjet.com{redirect_url2}'
                print(f"\n📤 STEP 3: GET → {full_url2[:100]}...")
                
                req3 = urllib.request.Request(full_url2, headers=headers2, method='GET')
                
                with urllib.request.urlopen(req3, timeout=30) as response3:
                    html3 = response3.read().decode('utf-8')
                
                print(f"✅ HTML recebido: {len(html3)} bytes")
                html_final = html3
            else:
                html_final = html2
        else:
            print("✅ HTML final (sem mais redirects)")
            html_final = html2
    else:
        print("❌ Não conseguiu extrair redirect")
        html_final = html1
else:
    print("❌ Sem redirect no HTML")
    html_final = html1

print("\n" + "=" * 80)
print(f"📄 HTML FINAL: {len(html_final)} bytes")

# Verificar conteúdo
if 'window.location.replace' in html_final:
    print("⚠️ AINDA TEM REDIRECT - não esperou o suficiente")
else:
    print("✅ Sem redirects - HTML final")

# Tentar parsear
from carjet_direct import parse_carjet_html_complete
items = parse_carjet_html_complete(html_final)

print(f"🚗 Carros parseados: {len(items)}")

if len(items) == 0:
    print("\n❌ NENHUM CARRO ENCONTRADO")
    print("Primeiros 1000 chars do HTML final:")
    print(html_final[:1000])
else:
    print(f"\n✅ {len(items)} CARROS ENCONTRADOS!")
    print("\nPrimeiros 3:")
    for i, item in enumerate(items[:3], 1):
        print(f"{i}. {item.get('car_name')} - {item.get('price')} EUR")
