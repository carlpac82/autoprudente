#!/usr/bin/env python3
"""
Debug script - Ver HTML do CarJet e identificar problema de parsing
"""
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import uuid
from bs4 import BeautifulSoup

# Pesquisa de teste
location = "Aeroporto de Faro"
start_dt = datetime.now() + timedelta(days=2)
end_dt = start_dt + timedelta(days=7)

print(f"🔍 DEBUG CARJET HTML")
print(f"Location: {location}")
print(f"Dates: {start_dt.strftime('%d/%m/%Y')} - {end_dt.strftime('%d/%m/%Y')}")
print("=" * 80)

# Form data
form_data = {
    'frmPkupDT': start_dt.strftime('%d/%m/%Y %H:%M'),
    'frmRetDT': end_dt.strftime('%d/%m/%Y %H:%M'),
    'frmPkupLoc': 'FAO02',
    'frmRetLoc': 'FAO02',
    'frmPkupType': 'APT',
    'frmRetType': 'APT',
    'frmCurrency': 'EUR',
    's': str(uuid.uuid4())[:8],
}

url = 'https://www.carjet.com/do/list/pt'
data = urllib.parse.urlencode(form_data).encode('utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
}

print(f"📤 POST → {url}")

req = urllib.request.Request(url, data=data, headers=headers)
with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode('utf-8')

print(f"✅ HTML recebido: {len(html)} bytes")
print("=" * 80)

# Parse com BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

# Procurar blocos de carros
car_blocks = (
    soup.find_all('article') or
    soup.find_all('div', class_=lambda x: x and ('car' in x or 'auto' in x or 'result' in x) if x else False)
)

print(f"🚗 Blocos encontrados: {len(car_blocks)}")
print("=" * 80)

if len(car_blocks) == 0:
    print("❌ NENHUM BLOCO ENCONTRADO!")
    print("\n📄 PRIMEIROS 2000 CARACTERES DO HTML:")
    print(html[:2000])
    print("\n...")
    exit(1)

# Analisar primeiro bloco
print(f"\n🔍 ANALISANDO PRIMEIRO BLOCO:")
print("=" * 80)

block = car_blocks[0]

# Ver estrutura completa do bloco
print("\n📦 ESTRUTURA DO BLOCO:")
print(block.prettify()[:1500])
print("\n...")

# Procurar nome do carro
print("\n🚗 PROCURANDO NOME DO CARRO:")
for tag in block.find_all(['h3', 'h4', 'h5', 'span', 'div', 'p']):
    text = tag.get_text(strip=True)
    if text and len(text) > 3:
        print(f"  {tag.name}.{tag.get('class', [])[0] if tag.get('class') else 'no-class'}: {text[:60]}")

# Procurar preço
print("\n💰 PROCURANDO PREÇOS:")
for tag in block.find_all(['span', 'div'], class_=lambda x: x and ('price' in str(x) or 'euro' in str(x)) if x else False):
    text = tag.get_text(strip=True)
    classes = tag.get('class', [])
    print(f"  {tag.name}.{'.'.join(classes)}: {text}")

# Procurar supplier
print("\n🏢 PROCURANDO SUPPLIER:")
data_prv = block.get('data-prv', '')
if data_prv:
    print(f"  data-prv: {data_prv}")

for img in block.find_all('img'):
    src = img.get('src', '')
    alt = img.get('alt', '')
    if '/logo' in src.lower() or 'logo_' in src.lower():
        print(f"  Logo: {src} (alt: {alt})")

# Procurar transmissão
print("\n⚙️ PROCURANDO TRANSMISSÃO:")
for icon in block.find_all('i', class_='icon'):
    classes = icon.get('class', [])
    print(f"  Icon classes: {classes}")

print("\n" + "=" * 80)
print("✅ Debug completo!")
