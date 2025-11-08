#!/usr/bin/env python3
"""
Script de teste para enviar email de Damage Report
"""

import requests
import json

API_URL = "https://carrental-api-5f8q.onrender.com"

def send_test_email():
    """Enviar email de teste"""
    
    print("="*60)
    print("📧 ENVIAR EMAIL DE TESTE - DAMAGE REPORT")
    print("="*60)
    
    # Dados do DR de teste (baseado nos logs)
    email_data = {
        'to_email': 'carlpac82@hotmail.com',  # Email de teste
        'client_name': 'EIKE BERENS',
        'dr_number': 'DR 39/2025',  # Exemplo
        'ra_number': '06424-09',
        'vehicle_plate': '30-XQ-97',
        'language': 'de',  # Cliente alemão
        'subject': 'Schadensbericht DR 39/2025 - Auto Prudente',
    }
    
    print(f"\n📤 Enviando para: {email_data['to_email']}")
    print(f"   Cliente: {email_data['client_name']}")
    print(f"   DR: {email_data['dr_number']}")
    print(f"   RA: {email_data['ra_number']}")
    print(f"   Idioma: {email_data['language'].upper()}")
    
    # Nota: Esta API precisa de ser implementada no backend
    # Por agora, vamos apenas mostrar o que seria enviado
    
    print("\n" + "="*60)
    print("⚠️  NOTA: Para enviar o email de verdade:")
    print("="*60)
    print("\n1. Ir para: https://carrental-api-5f8q.onrender.com")
    print("2. Damage Report → Histórico")
    print("3. Clicar no ícone ✉️ (envelope) do DR que criaste")
    print("4. No modal:")
    print("   - Email: carlpac82@hotmail.com")
    print("   - Preview do template aparece automaticamente")
    print("5. Clicar 'Enviar Email'")
    print("\n✅ O email será enviado com o template profissional!")
    print("   (Cabeçalho azul + Logo + Ícone telefone 32px + Rodapé)")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    send_test_email()
