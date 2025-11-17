#!/usr/bin/env python3
"""
Debug - Verificar se há redirect no HTML do CarJet
"""
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import uuid
import re

location = "Aeroporto de Faro"
start_dt = datetime.now() + timedelta(days=2)
end_dt = start_dt + timedelta(days=7)

pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
return_date = end_dt.strftime('%d/%m/%Y %H:%M')
session_id = str(uuid.uuid4())

form_data = {
    'frmDestino': 'FAO02',
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

print(f"🔍 VERIFICANDO REDIRECT")
print(f"Dates: {pickup_date} - {return_date}")
print("=" * 80)

req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')

print(f"✅ HTML recebido: {len(html)} bytes")
print("=" * 80)

# Procurar por redirect
if 'window.location.replace' in html:
    print("✅ ENCONTROU: window.location.replace")
    pattern = r"window\.location\.replace\('([^']+)'\)"
    match = re.search(pattern, html)
    if match:
        redirect_url = match.group(1)
        print(f"🔗 Redirect URL: {redirect_url}")
    else:
        print("❌ Não conseguiu extrair URL de redirect")
elif 'Waiting Prices' in html:
    print("✅ ENCONTROU: Waiting Prices")
else:
    print("❌ NÃO ENCONTROU redirect!")
    print("\n📄 PRIMEIROS 3000 CARACTERES DO HTML:")
    print(html[:3000])
    print("\n...")
    
    # Procurar por artigos
    import re
    articles = re.findall(r'<article[^>]*>', html)
    print(f"\n📦 Artigos encontrados: {len(articles)}")
    
    if len(articles) > 0:
        print("Primeiro artigo:")
        start = html.find('<article')
        end = html.find('</article>', start) + 10
        print(html[start:end][:500])
