#!/usr/bin/env python3
"""
🚀 ENVIAR 2 EMAILS AGORA (sem esperar)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def load_env():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value

def send_emails():
    """Enviar os 2 emails AGORA"""
    print("\n" + "="*80)
    print("📧 ENVIANDO 2 EMAILS AGORA")
    print("="*80)
    
    load_env()
    sys.path.insert(0, str(Path(__file__).parent))
    
    import psycopg2
    import json
    from improved_reports import generate_daily_report_html_by_location
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import base64
    
    database_url = os.environ.get('DATABASE_URL')
    
    print("\n1️⃣ Conectando à base de dados...")
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Buscar credenciais Gmail
    print("2️⃣ Carregando credenciais Gmail...")
    cursor.execute("""
        SELECT setting_value FROM user_settings 
        WHERE setting_key = 'gmail_oauth_credentials'
    """)
    row = cursor.fetchone()
    
    if not row:
        print("❌ Sem credenciais Gmail!")
        return
    
    creds_data = json.loads(row[0])
    credentials = Credentials(
        token=creds_data.get('access_token'),
        refresh_token=creds_data.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token',
        client_id=creds_data.get('client_id'),
        client_secret=creds_data.get('client_secret')
    )
    
    # Buscar recipient
    print("3️⃣ Carregando destinatários...")
    cursor.execute("""
        SELECT setting_value FROM user_settings 
        WHERE setting_key = 'email_settings'
    """)
    email_row = cursor.fetchone()
    
    if not email_row:
        print("❌ Sem configurações de email!")
        return
    
    email_settings = json.loads(email_row[0])
    recipients_text = email_settings.get('recipients', '')
    recipients = [email.strip() for email in recipients_text.split('\n') if email.strip()]
    
    print(f"   📧 Destinatários: {recipients}")
    
    # Buscar dados de hoje
    print("4️⃣ Carregando dados de pesquisa de hoje...")
    cursor.execute("""
        SELECT location, start_date, days, results_data, timestamp
        FROM recent_searches
        WHERE DATE(timestamp) = CURRENT_DATE
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    
    all_results = []
    for row in rows:
        location, start_date, days, results_data, timestamp = row
        if results_data:
            results = json.loads(results_data)
            for r in results:
                r['days'] = days
                r['location'] = location
            all_results.extend(results)
    
    search_data = {'results': all_results}
    print(f"   📊 {len(all_results)} resultados encontrados")
    
    cursor.close()
    conn.close()
    
    if not search_data['results']:
        print("❌ Sem dados de hoje!")
        return
    
    # Build Gmail service
    print("5️⃣ Conectando ao Gmail...")
    service = build('gmail', 'v1', credentials=credentials)
    
    # ENVIAR 2 EMAILS
    locations = ['Albufeira', 'Aeroporto de Faro']
    total_sent = 0
    
    for location in locations:
        print(f"\n📍 Gerando relatório para: {location}")
        
        # Generate HTML
        html_content = generate_daily_report_html_by_location(search_data, location)
        
        # Send to all recipients
        for recipient in recipients:
            try:
                message = MIMEMultipart('alternative')
                message['to'] = recipient
                message['subject'] = f'📊 TESTE MANUAL Relatório Diário {location} - Auto Prudente ({datetime.now().strftime("%d/%m/%Y")})'
                
                html_part = MIMEText(html_content, 'html')
                message.attach(html_part)
                
                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                service.users().messages().send(
                    userId='me',
                    body={'raw': raw_message}
                ).execute()
                
                total_sent += 1
                print(f"   ✅ Email {location} enviado para {recipient}")
            except Exception as e:
                print(f"   ❌ Erro ao enviar para {recipient}: {str(e)}")
                import traceback
                print(traceback.format_exc())
    
    print("\n" + "="*80)
    print(f"🎉 CONCLUÍDO! {total_sent} emails enviados")
    print("="*80)

if __name__ == "__main__":
    send_emails()
