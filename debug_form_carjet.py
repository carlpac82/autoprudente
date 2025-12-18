#!/usr/bin/env python3
"""
Debug - extrair estrutura do formulário CarJet
"""

import requests
from bs4 import BeautifulSoup

def debug_form():
    print("=" * 60)
    print("DEBUG FORMULÁRIO CARJET")
    print("=" * 60)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-PT,pt;q=0.9',
    })
    
    print("\n[1] Obtendo homepage...")
    resp = session.get('https://www.carjet.com/aluguel-carros/index.htm', timeout=15)
    print(f"    Status: {resp.status_code}")
    print(f"    Cookies: {dict(session.cookies)}")
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # Encontrar todos os forms
    forms = soup.find_all('form')
    print(f"\n[2] Forms encontrados: {len(forms)}")
    
    for i, form in enumerate(forms):
        print(f"\n--- FORM {i+1} ---")
        print(f"    Name: {form.get('name')}")
        print(f"    Action: {form.get('action')}")
        print(f"    Method: {form.get('method')}")
        
        # Encontrar todos os inputs
        inputs = form.find_all(['input', 'select', 'textarea'])
        print(f"    Campos ({len(inputs)}):")
        
        for inp in inputs:
            inp_type = inp.get('type', inp.name)
            inp_name = inp.get('name', inp.get('id', 'N/A'))
            inp_value = inp.get('value', '')[:30] if inp.get('value') else ''
            print(f"      - {inp_name} ({inp_type}): '{inp_value}'")
    
    # Procurar especificamente pelo campo pickup
    print("\n[3] Campo pickup:")
    pickup = soup.find(id='pickup')
    if pickup:
        print(f"    ID: {pickup.get('id')}")
        print(f"    Name: {pickup.get('name')}")
        print(f"    Type: {pickup.get('type')}")
    
    # Procurar campos de data
    print("\n[4] Campos de data:")
    for field_id in ['fechaRecogida', 'fechaDevolucion', 'fechaEntrega']:
        field = soup.find(id=field_id)
        if field:
            print(f"    {field_id}: name={field.get('name')}, type={field.get('type')}")
    
    # Procurar campos hidden importantes
    print("\n[5] Campos hidden:")
    hiddens = soup.find_all('input', {'type': 'hidden'})
    for h in hiddens:
        name = h.get('name', 'N/A')
        value = h.get('value', '')[:50]
        print(f"    {name}: '{value}'")
    
    # Salvar HTML para análise manual
    with open('carjet_homepage.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    print("\n[6] HTML salvo em carjet_homepage.html")

if __name__ == "__main__":
    debug_form()
