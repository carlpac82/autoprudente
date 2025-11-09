#!/usr/bin/env python3
"""
🔧 FIX: Atualizar template de email para incluir {raNumber} no header
"""

import os
import psycopg2
from pathlib import Path

def load_env():
    """Carregar .env"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def main():
    print("🔧 Corrigindo template de email...")
    print("=" * 60)
    
    # Carregar configuração
    load_env()
    
    # Template HTML corrigido com header visual
    html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
        }
        .header {
            background-color: #009cb6;
            padding: 20px;
        }
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo img {
            height: 50px;
        }
        .header-info {
            text-align: right;
            color: #fff;
            font-size: 14px;
            font-weight: bold;
        }
        .content {
            padding: 30px 20px;
            color: #333;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="header-content">
                <div class="logo">
                    <img src="https://carrental-api-5f8q.onrender.com/static/ap-heather.png" alt="Auto Prudente" style="height:50px"/>
                </div>
                <div class="header-info">
                    <div>DR: {drNumber}</div>
                    <div>RA: {raNumber}</div>
                </div>
            </div>
        </div>
        <div class="content">
            <p>Hello {firstName},</p>
            <p>Thank you for choosing Auto Prudente Rent a Car!</p>
            <p>Due to unforeseen circumstances that occurred during the above-mentioned rental contract, the vehicle you rented has been damaged.</p>
            <p>Your rental contract reflects that you declined our premium insurance, choosing to accept full responsibility for any loss or damage that occurs, regardless of who was at fault.</p>
            <p>As such, you are responsible for the amount described in the attachment.</p>
            <p>If this matter is resolved by your insurer or credit card management entity, please send us the attached documents and contact us with your claim information.</p>
            <p>We inform that we will debit all expenses from your credit card within 48 hours after sending this notification.</p>
            <p><strong>Vehicle:</strong> {vehiclePlate}<br>
            <strong>Date:</strong> {date}</p>
            <p>Best regards,<br>Auto Prudente Team</p>
        </div>
    </div>
</body>
</html>'''
    
    # Conectar à BD
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não definida!")
        return 1
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Atualizar template PT
        print("\n📝 Atualizando template PT...")
        cursor.execute("""
            UPDATE dr_email_templates
            SET body_template = %s,
                updated_at = NOW()
            WHERE language_code = 'pt'
        """, (html_template,))
        
        rows_updated = cursor.rowcount
        print(f"   ✅ {rows_updated} template(s) atualizados")
        
        # Verificar
        cursor.execute("""
            SELECT language_code, LENGTH(body_template) as template_length
            FROM dr_email_templates
            WHERE language_code = 'pt'
        """)
        row = cursor.fetchone()
        
        if row:
            print(f"   📊 Template PT: {row[1]} caracteres")
            
            # Verificar se tem {raNumber}
            cursor.execute("""
                SELECT body_template
                FROM dr_email_templates
                WHERE language_code = 'pt'
            """)
            template = cursor.fetchone()[0]
            
            if '{raNumber}' in template:
                print("   ✅ {raNumber} presente no template")
            else:
                print("   ❌ {raNumber} NÃO encontrado no template")
        
        # Commit
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ TEMPLATE ATUALIZADO COM SUCESSO!")
        print("=" * 60)
        print("\nO email agora inclui:")
        print("  • Header visual com logo")
        print("  • DR: {drNumber}")
        print("  • RA: {raNumber} ✅ CORRIGIDO")
        print("  • Conteúdo formatado em HTML")
        print("\nTeste enviando um email para confirmar!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
