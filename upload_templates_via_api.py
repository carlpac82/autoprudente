#!/usr/bin/env python3
"""
Upload templates via API do Render
"""

import requests
import json

API_URL = "https://carrental-api-5f8q.onrender.com"

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def upload_templates():
    templates = [
        {
            'lang': 'pt',
            'name': 'Português',
            'subject': 'Relatório de Danos {drNumber} - Auto Prudente',
            'file': 'email_template_pt_complete.html'
        },
        {
            'lang': 'en',
            'name': 'English',
            'subject': 'Damage Report {drNumber} - Auto Prudente',
            'file': 'email_template_en_complete.html'
        },
        {
            'lang': 'fr',
            'name': 'Français',
            'subject': 'Rapport de Dommages {drNumber} - Auto Prudente',
            'file': 'email_template_fr_complete.html'
        },
        {
            'lang': 'de',
            'name': 'Deutsch',
            'subject': 'Schadensbericht {drNumber} - Auto Prudente',
            'file': 'email_template_de_complete.html'
        }
    ]
    
    print("="*60)
    print("📧 UPLOAD TEMPLATES VIA API")
    print("="*60)
    
    for t in templates:
        print(f"\n📤 {t['name']} ({t['lang']})...")
        
        body = read_template(t['file'])
        print(f"   Lido: {len(body):,} caracteres")
        
        data = {
            'subject_template': t['subject'],
            'body_template': body
        }
        
        response = requests.post(
            f"{API_URL}/api/damage-reports/email-template/{t['lang']}",
            json=data
        )
        
        if response.status_code == 200:
            print(f"   ✅ Upload OK!")
        else:
            print(f"   ❌ Erro: {response.status_code}")
            print(f"   {response.text}")
    
    print("\n" + "="*60)
    print("✅ CONCLUÍDO!")
    print("="*60)

if __name__ == '__main__':
    upload_templates()
