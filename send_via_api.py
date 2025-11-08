#!/usr/bin/env python3
"""
Enviar email de teste via API
"""

import requests
import json
import base64

API_URL = "https://carrental-api-5f8q.onrender.com"

def read_template():
    """Ler template PT"""
    with open('email_template_pt_complete.html', 'r', encoding='utf-8') as f:
        return f.read()

def send_email_via_api():
    """Enviar email via API"""
    
    print("="*60)
    print("📧 ENVIAR EMAIL VIA API")
    print("="*60)
    
    # Ler e preparar template
    template = read_template()
    
    # Substituir placeholders
    email_body = template.replace('{drNumber}', 'DR 39/2025')
    email_body = email_body.replace('{raNumber}', '06424-09')
    email_body = email_body.replace('{firstName}', 'FILIPE')
    email_body = email_body.replace('{contractNumber}', '06424-09')
    email_body = email_body.replace('{vehiclePlate}', '30-XQ-97')
    email_body = email_body.replace('{date}', '08/11/2025')
    
    # Dados do email
    email_data = {
        'to_email': 'carlpac82@hotmail.com',
        'subject': 'Relatório de Danos DR 39/2025 - Auto Prudente',
        'body': email_body,
        'dr_number': 'DR 39/2025',
        'client_name': 'Filipe Pacheco',
        'language': 'pt',
        # Se tiveres o PDF em base64, adiciona aqui:
        # 'pdf_attachment': base64_pdf_data
    }
    
    print(f"\n📤 Enviando para: {email_data['to_email']}")
    print(f"   Assunto: {email_data['subject']}")
    print(f"   Tamanho: {len(email_body):,} caracteres")
    
    print("\n📡 Enviando via API...")
    
    try:
        response = requests.post(
            f"{API_URL}/api/damage-reports/send-email",
            json=email_data,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ EMAIL ENVIADO COM SUCESSO!")
            print(f"   {result}")
            print("\n📥 Verifica o inbox: carlpac82@hotmail.com")
            print("   (Pode demorar 1-2 minutos)")
        else:
            print(f"\n❌ Erro: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"\n❌ Erro na conexão: {e}")
        print("\n⚠️  ALTERNATIVA: Enviar pela Interface Web")
        print("1. https://carrental-api-5f8q.onrender.com/damage-report")
        print("2. Tab 'Histórico' → Ícone ✉️")
        print("3. Email: carlpac82@hotmail.com")

if __name__ == '__main__':
    send_email_via_api()
