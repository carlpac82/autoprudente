#!/usr/bin/env python3
"""
Script para testar seletores do formulário CarJet
"""
import requests
from bs4 import BeautifulSoup

# Fazer request para homepage
url = 'https://www.carjet.com/aluguel-carros/index.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15'
}

print("📱 Buscando homepage do CarJet...")
resp = requests.get(url, headers=headers)
print(f"Status: {resp.status_code}")

soup = BeautifulSoup(resp.text, 'html.parser')

print("\n" + "="*80)
print("🔍 SELETORES DE INPUT")
print("="*80)

# Procurar todos os inputs do formulário
form = soup.find('form')
if form:
    print(f"\n✅ Form encontrado: {form.get('id')} / {form.get('name')}")
    
    # Procurar inputs
    inputs = form.find_all('input')
    print(f"\n📝 Inputs encontrados: {len(inputs)}")
    for inp in inputs[:15]:
        inp_id = inp.get('id', '')
        inp_name = inp.get('name', '')
        inp_type = inp.get('type', '')
        inp_placeholder = inp.get('placeholder', '')
        print(f"  - id='{inp_id}' name='{inp_name}' type='{inp_type}' placeholder='{inp_placeholder}'")
    
    # Procurar selects
    selects = form.find_all('select')
    print(f"\n🎛️ Selects encontrados: {len(selects)}")
    for sel in selects[:10]:
        sel_id = sel.get('id', '')
        sel_name = sel.get('name', '')
        print(f"  - id='{sel_id}' name='{sel_name}'")
    
    # Procurar botões
    buttons = form.find_all(['button', 'input'], type='submit')
    print(f"\n🔘 Botões submit: {len(buttons)}")
    for btn in buttons:
        btn_id = btn.get('id', '')
        btn_name = btn.get('name', '')
        btn_class = btn.get('class', [])
        print(f"  - id='{btn_id}' name='{btn_name}' class={btn_class}")
else:
    print("❌ Form não encontrado")

# Verificar se tem o input de local
print("\n" + "="*80)
print("🎯 VERIFICANDO SELETORES ESPECÍFICOS")
print("="*80)

selectors_to_test = [
    ('#pickup', 'pickup por ID'),
    ('input[name="txt-rent-pickup"]', 'txt-rent-pickup'),
    ('input[name="pickUpLocation"]', 'pickUpLocation'),
    ('input[id="fechaRecogida"]', 'fechaRecogida por ID'),
    ('input[name="pickUpDate"]', 'pickUpDate por name'),
    ('select[id="fechaRecogidaSelHour"]', 'hora pickup por ID'),
    ('select[name="pickUpTime"]', 'hora pickup por name'),
]

for selector, desc in selectors_to_test:
    element = soup.select_one(selector)
    if element:
        print(f"✅ {desc}: {selector}")
        print(f"   Atributos: id={element.get('id')}, name={element.get('name')}, type={element.get('type')}")
    else:
        print(f"❌ {desc}: {selector} - NÃO ENCONTRADO")

print("\n✅ Análise completa!")
