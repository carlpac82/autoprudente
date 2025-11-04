#!/usr/bin/env python3
"""
Teste para verificar extração de nome do carro do atributo alt
"""

from bs4 import BeautifulSoup

# HTML de exemplo do CarJet
html_sample = '''
<div class="car-card">
    <img class="cl--car-img" 
         src="/cdn/img/cars/M/car_C166.jpg" 
         data-original="" 
         alt="Skoda Scala ou similar ">
</div>
'''

soup = BeautifulSoup(html_sample, 'html.parser')
card = soup.select_one('.car-card')

# Simular extração
car_img = card.select_one("img.cl--car-img")
if car_img:
    src = (car_img.get("src") or car_img.get("data-src") or car_img.get("data-original") or "").strip()
    alt_text = (car_img.get("alt") or "").strip()
    
    print(f"Imagem encontrada: {src}")
    print(f"Alt text: '{alt_text}'")
    
    if alt_text:
        # "Skoda Scala ou similar " -> "Skoda Scala"
        alt_car_name = alt_text.split('ou similar')[0].split('|')[0].strip()
        print(f"Nome extraído: '{alt_car_name}'")
        
        # Limpar nome
        car_clean = alt_car_name.lower().strip()
        print(f"Nome limpo: '{car_clean}'")
        
        print("\n✅ SUCESSO! Nome do carro extraído corretamente do atributo alt")
    else:
        print("\n❌ ERRO: Atributo alt vazio")
else:
    print("\n❌ ERRO: Imagem cl--car-img não encontrada")
