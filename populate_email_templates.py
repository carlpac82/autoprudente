#!/usr/bin/env python3
"""
Script para popular a base de dados com os templates de email completos.
Lê os ficheiros HTML e guarda na tabela dr_email_templates.
"""

import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.env.render')

def read_template_file(filename):
    """Lê o conteúdo de um ficheiro de template."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def populate_templates():
    """Popular a BD com os templates de email."""
    
    # Conectar à BD do Render
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrado em .env.render")
        return
    
    print("📡 Conectando ao PostgreSQL do Render...")
    conn = psycopg2.connect(database_url)
    
    try:
        # Templates a carregar
        templates = [
            {
                'code': 'pt',
                'name': 'Português',
                'subject': 'Relatório de Danos {drNumber} - Auto Prudente',
                'file': 'email_template_pt_complete.html'
            },
            {
                'code': 'en',
                'name': 'English',
                'subject': 'Damage Report {drNumber} - Auto Prudente',
                'file': 'email_template_en_complete.html'
            },
            {
                'code': 'fr',
                'name': 'Français',
                'subject': 'Rapport de Dommages {drNumber} - Auto Prudente',
                'file': 'email_template_fr_complete.html'
            },
            {
                'code': 'de',
                'name': 'Deutsch',
                'subject': 'Schadensbericht {drNumber} - Auto Prudente',
                'file': 'email_template_de_complete.html'
            }
        ]
        
        with conn.cursor() as cur:
            for template in templates:
                print(f"\n📧 {template['name']} ({template['code']})...")
                
                # Ler ficheiro HTML
                if not os.path.exists(template['file']):
                    print(f"   ❌ Ficheiro não encontrado: {template['file']}")
                    continue
                
                body = read_template_file(template['file'])
                print(f"   ✅ Lido: {len(body)} caracteres")
                
                # Upsert na BD
                cur.execute("""
                    INSERT INTO dr_email_templates (language_code, language_name, subject_template, body_template, updated_at)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (language_code) DO UPDATE SET
                        language_name = EXCLUDED.language_name,
                        subject_template = EXCLUDED.subject_template,
                        body_template = EXCLUDED.body_template,
                        updated_at = CURRENT_TIMESTAMP
                """, (template['code'], template['name'], template['subject'], body))
                
                print(f"   ✅ Guardado na BD!")
        
        conn.commit()
        print("\n" + "="*60)
        print("✅ TODOS OS TEMPLATES GUARDADOS COM SUCESSO!")
        print("="*60)
        
        # Verificar
        with conn.cursor() as cur:
            cur.execute("SELECT language_code, language_name, LENGTH(body_template) FROM dr_email_templates ORDER BY language_code")
            print("\n📋 Templates na BD:")
            for row in cur.fetchall():
                print(f"   {row[0].upper()}: {row[1]} ({row[2]:,} caracteres)")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\n🔌 Conexão fechada")

if __name__ == '__main__':
    print("="*60)
    print("📧 POPULAR TEMPLATES DE EMAIL NA BASE DE DADOS")
    print("="*60)
    populate_templates()
