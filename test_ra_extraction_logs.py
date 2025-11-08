#!/usr/bin/env python3
"""
Teste da extração de campos do Rental Agreement PDF
Para verificar se os logs aparecem corretamente
"""
import requests
import os

# URL do servidor local
BASE_URL = "http://localhost:8000"

# Caminho do PDF de teste (usar o que já existe)
PDF_PATH = "uploaded/rental_agreements/06424-09_rental_agreement.pdf"

def test_extraction():
    print("\n" + "="*80)
    print("🧪 TESTE DE EXTRAÇÃO DO RENTAL AGREEMENT")
    print("="*80)
    
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF não encontrado: {PDF_PATH}")
        print("📂 PDFs disponíveis:")
        if os.path.exists("uploaded/rental_agreements"):
            for f in os.listdir("uploaded/rental_agreements"):
                if f.endswith('.pdf'):
                    print(f"   - {f}")
        return
    
    print(f"📄 PDF: {PDF_PATH}")
    print(f"📏 Tamanho: {os.path.getsize(PDF_PATH)} bytes")
    
    # Fazer upload e extração
    print("\n🚀 Enviando para extração...")
    
    with open(PDF_PATH, 'rb') as f:
        files = {'file': (os.path.basename(PDF_PATH), f, 'application/pdf')}
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/damage-reports/extract-from-ra",
                files=files,
                cookies={'session': 'test_session'}  # Simular autenticação
            )
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sucesso!")
                print(f"\n📋 Campos extraídos ({len(data.get('fields', {}))} campos):")
                
                for field_name, value in data.get('fields', {}).items():
                    if value:
                        print(f"   • {field_name}: {value[:50]}..." if len(str(value)) > 50 else f"   • {field_name}: {value}")
                
                print(f"\n🔧 Método usado: {data.get('method', 'unknown')}")
                
            else:
                print(f"❌ Erro: {response.status_code}")
                print(f"📄 Resposta: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
    
    print("\n" + "="*80)
    print("📝 VERIFICAR LOGS DO SERVIDOR:")
    print("   tail -100 server.log | grep -A 5 -B 5 'COORDENADAS\\|TESTANDO CAMPO\\|MELHOR'")
    print("="*80)

if __name__ == "__main__":
    test_extraction()
