#!/usr/bin/env python3
"""
Enviar email de teste em PT para carlpac82@hotmail.com
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def read_template():
    """Ler template PT"""
    with open('email_template_pt_complete.html', 'r', encoding='utf-8') as f:
        return f.read()

def send_test_email():
    """Enviar email de teste"""
    
    print("="*60)
    print("📧 ENVIAR EMAIL DE TESTE - PORTUGUÊS")
    print("="*60)
    
    # Ler template
    template = read_template()
    
    # Substituir placeholders
    email_body = template.replace('{drNumber}', 'DR 39/2025')
    email_body = email_body.replace('{raNumber}', '06424-09')
    email_body = email_body.replace('{firstName}', 'FILIPE')
    email_body = email_body.replace('{contractNumber}', '06424-09')
    email_body = email_body.replace('{vehiclePlate}', '30-XQ-97')
    email_body = email_body.replace('{date}', '08/11/2025')
    
    # Configurar email
    sender = "info@auto-prudente.com"
    recipient = "carlpac82@hotmail.com"
    subject = "Relatório de Danos DR 39/2025 - Auto Prudente"
    
    # Criar mensagem
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Adicionar corpo HTML
    html_part = MIMEText(email_body, 'html', 'utf-8')
    msg.attach(html_part)
    
    print(f"\n📤 Email Configurado:")
    print(f"   De: {sender}")
    print(f"   Para: {recipient}")
    print(f"   Assunto: {subject}")
    print(f"   Tamanho: {len(email_body):,} caracteres")
    
    print("\n⚠️  CONFIGURAÇÃO SMTP NECESSÁRIA")
    print("="*60)
    print("Para enviar o email, preciso das credenciais SMTP.")
    print("\nOpções:")
    print("1. Configurar Gmail SMTP (recomendado)")
    print("2. Usar serviço de email do servidor")
    print("3. Enviar manualmente através da interface web")
    
    print("\n🌐 ALTERNATIVA: Enviar pela Interface Web")
    print("="*60)
    print("1. Vai para: https://carrental-api-5f8q.onrender.com/damage-report")
    print("2. Tab 'Histórico'")
    print("3. Clica ✉️ no DR 39/2025")
    print("4. Altera email para: carlpac82@hotmail.com")
    print("5. Template PT será usado automaticamente!")
    print("6. Clica 'Enviar'")
    
    # Guardar HTML para preview
    preview_file = 'email_preview_pt.html'
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(email_body)
    
    print(f"\n✅ Preview guardado em: {preview_file}")
    print("   Abre este ficheiro no browser para ver como ficará!")
    
    return email_body

if __name__ == '__main__':
    send_test_email()
