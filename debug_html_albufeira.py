#!/usr/bin/env python3
"""
Salvar HTML de Albufeira para debug
"""
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import uuid

start_dt = datetime.now() + timedelta(days=14)
end_dt = start_dt + timedelta(days=2)

pickup_date = start_dt.strftime('%d/%m/%Y %H:%M')
return_date = end_dt.strftime('%d/%m/%Y %H:%M')

form_data = {
    'frmDestino': 'ABF01',
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
    'frmSession': str(uuid.uuid4()),
    'frmDetailCode': ''
}

encoded_data = urllib.parse.urlencode(form_data).encode('utf-8')
url = 'https://www.carjet.com/do/list/pt'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html',
    'Accept-Language': 'pt-PT,pt;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.carjet.com/',
    'Origin': 'https://www.carjet.com',
    'Cookie': 'monedaForzada=EUR; moneda=EUR; currency=EUR; country=PT; idioma=PT; lang=pt'
}

print("Fazendo request...")
req = urllib.request.Request(url, data=encoded_data, headers=headers, method='POST')

with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')

print(f"Recebido: {len(html)} bytes")

# Salvar HTML
with open('albufeira_carjet_debug.html', 'w') as f:
    f.write(html)

print("HTML salvo em: albufeira_carjet_debug.html")

# Mostrar primeiros 2000 caracteres
print("\nPrimeiros 2000 caracteres:")
print("=" * 70)
print(html[:2000])
print("=" * 70)

# Procurar padrões
print("\nPadrões encontrados:")
print(f"  <article>: {html.count('<article')}")
print(f"  data-prv: {html.count('data-prv')}")
price_count = html.count('class="price')
print(f"  class=price: {price_count}")
print(f"  pr-euros: {html.count('pr-euros')}")
euro_count = html.count('€')
print(f"  €: {euro_count}")
