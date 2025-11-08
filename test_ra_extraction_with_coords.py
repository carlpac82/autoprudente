#!/usr/bin/env python3
"""
Criar PDF de teste e extrair com coordenadas
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import requests
import os

# Criar PDF de teste com dados nas posições mapeadas
pdf_path = "test_rental_agreement.pdf"

print("\n" + "="*80)
print("📄 CRIANDO PDF DE TESTE")
print("="*80)

c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4

# Escrever dados nas posições aproximadas das coordenadas mapeadas
# (Coordenadas do canvas são bottom-left, precisamos converter)

# contractNumber (14, 97 do topo)
c.drawString(14, height - 97, "06424-09")

# clientName (12, 130 do topo)
c.drawString(12, height - 130, "EIKE BERENS")

# address (293, 96.5 do topo)
c.drawString(293, height - 96.5, "RUA EXEMPLO 123")

# vehicleBrandModel (442, 96.5 do topo)
c.drawString(442, height - 96.5, "FIAT 500")

# vehiclePlate (292, 182.5 do topo)
c.drawString(292, height - 182.5, "AB-12-CD")

# pickupTime (442.5, 182.5 do topo)
c.drawString(442.5, height - 182.5, "10:30")

# pickupLocation (442.5, 210 do topo)
c.drawString(442.5, height - 210, "AUTO PRUDENTE")

# pickupDate (292.6569, 237 do topo)
c.drawString(292.6569, height - 237, "06-11-2025")

# pickupFuel (442, 237 do topo)
c.drawString(442, height - 237, "3/4")

# country (13.5, 271 do topo)
c.drawString(13.5, height - 271, "DE")

# postalCodeCity (13.5, 351.5 do topo)
c.drawString(13.5, height - 351.5, "8000-000 / FARO")

# clientPhone (110, 351.5 do topo)
c.drawString(110, height - 351.5, "+351 912345678")

c.save()
print(f"✅ PDF criado: {pdf_path}")

# Testar extração
print("\n" + "="*80)
print("🚀 TESTANDO EXTRAÇÃO COM COORDENADAS")
print("="*80)

try:
    with open(pdf_path, 'rb') as f:
        files = {'file': (pdf_path, f, 'application/pdf')}
        
        response = requests.post(
            'http://localhost:8000/api/damage-reports/extract-from-ra',
            files=files,
            cookies={'session': 'test'}
        )
        
        print(f"\n📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Extração bem-sucedida!")
            print(f"\n📋 Campos extraídos: {len(data.get('fields', {}))}")
            
            for field, value in data.get('fields', {}).items():
                if value:
                    val_str = str(value)[:60]
                    print(f"   • {field}: {val_str}")
            
            print(f"\n🔧 Método: {data.get('method', 'unknown')}")
        else:
            print(f"❌ Erro: {response.text[:200]}")

except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*80)
print("📝 VER LOGS DETALHADOS:")
print("   tail -100 server.log | grep -E '🚨|📍|✅ MELHOR|TESTANDO CAMPO'")
print("="*80)
