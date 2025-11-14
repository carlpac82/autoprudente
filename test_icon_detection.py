#!/usr/bin/env python3
"""
Teste direto de detecção de ícone de transmissão
"""
from bs4 import BeautifulSoup

# HTML de exemplo do CarJet (simplificado)
html_auto = """
<div class="card">
    <h3>Toyota Aygo</h3>
    <div class="specs">
        <i class="icon icon-transm-auto size-24"></i>
        <span>5 passageiros</span>
    </div>
    <span class="price">25.50€</span>
</div>
"""

html_manual = """
<div class="card">
    <h3>Volkswagen Sharan</h3>
    <div class="specs">
        <i class="icon icon-transm size-24"></i>
        <span>Manual</span>
        <span>7 passageiros</span>
    </div>
    <span class="price">45.00€</span>
</div>
"""

def test_detection(html, expected):
    soup = BeautifulSoup(html, "lxml")
    card = soup.find("div", class_="card")
    
    # MESMA LÓGICA DO MAIN.PY
    card_transmission = ""
    
    # Procurar ícone de transmissão no card
    trans_icon = card.select_one("i.icon-transm-auto, i.icon.icon-transm-auto")
    if trans_icon:
        card_transmission = "Automatic"
        print(f"✅ Detectado: AUTOMATIC (icon-transm-auto encontrado)")
    else:
        # Verificar se tem ícone manual (icon-transm SEM auto)
        trans_icon_manual = card.select_one("i.icon-transm:not(.icon-transm-auto), i.icon.icon-transm:not(.icon-transm-auto)")
        if trans_icon_manual:
            card_transmission = "Manual"
            print(f"✅ Detectado: MANUAL (icon-transm sem auto encontrado)")
        else:
            print(f"❌ Nenhum ícone encontrado!")
    
    # Verificar resultado
    car_name = card.find("h3").text
    if card_transmission == expected:
        print(f"✅ CORRETO: {car_name} → {card_transmission}")
    else:
        print(f"❌ ERRADO: {car_name} → {card_transmission} (esperado: {expected})")
    
    print()
    return card_transmission == expected

print("=" * 80)
print("🔧 TESTE DE DETECÇÃO DE ÍCONE DE TRANSMISSÃO")
print("=" * 80)
print()

print("TESTE 1: Toyota Aygo (AUTOMÁTICO)")
print("-" * 80)
test1 = test_detection(html_auto, "Automatic")

print("TESTE 2: Volkswagen Sharan (MANUAL)")
print("-" * 80)
test2 = test_detection(html_manual, "Manual")

print("=" * 80)
if test1 and test2:
    print("✅ TODOS OS TESTES PASSARAM!")
else:
    print("❌ ALGUNS TESTES FALHARAM!")
print("=" * 80)
