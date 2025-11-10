#!/usr/bin/env python3
"""
Script para atualizar os templates de email na base de dados do Render (PostgreSQL).
Lê os ficheiros HTML corrigidos e atualiza a tabela dr_email_templates.
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

def update_templates():
    """Atualizar os templates na BD do Render."""
    
    # Conectar à BD do Render
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrado em .env.render")
        print("\n💡 ALTERNATIVA: Copia este código e executa diretamente no Render:")
        print("="*80)
        print("""
# No Render Shell, executa:
cd /opt/render/project/src
python3 << 'EOF'
import psycopg2
import os

# Templates corrigidos
templates = {
    'pt': {
        'name': 'Português',
        'subject': 'Relatório de Danos {drNumber} - Auto Prudente',
        'file': 'email_template_pt_complete.html'
    },
    'en': {
        'name': 'English', 
        'subject': 'Damage Report {drNumber} - Auto Prudente',
        'file': 'email_template_en_complete.html'
    },
    'fr': {
        'name': 'Français',
        'subject': 'Rapport de Dommages {drNumber} - Auto Prudente',
        'file': 'email_template_fr_complete.html'
    },
    'de': {
        'name': 'Deutsch',
        'subject': 'Schadensbericht {drNumber} - Auto Prudente',
        'file': 'email_template_de_complete.html'
    }
}

conn = psycopg2.connect(os.environ['DATABASE_URL'])
print("✅ Conectado ao PostgreSQL")

with conn.cursor() as cur:
    for code, template in templates.items():
        with open(template['file'], 'r', encoding='utf-8') as f:
            body = f.read()
        
        cur.execute('''
            UPDATE dr_email_templates 
            SET body_template = %s, 
                subject_template = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE language_code = %s
        ''', (body, template['subject'], code))
        
        print(f"✅ {template['name']} ({code}) atualizado: {len(body)} caracteres")

conn.commit()
conn.close()
print("\\n✅ TODOS OS TEMPLATES ATUALIZADOS!")
EOF
""")
        print("="*80)
        return
    
    print("📡 Conectando ao PostgreSQL do Render...")
    conn = psycopg2.connect(database_url)
    
    try:
        # Templates a atualizar
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
                
                # Ler ficheiro HTML corrigido
                if not os.path.exists(template['file']):
                    print(f"   ❌ Ficheiro não encontrado: {template['file']}")
                    continue
                
                body = read_template_file(template['file'])
                print(f"   ✅ Lido: {len(body)} caracteres")
                
                # Update na BD (não INSERT, apenas UPDATE dos existentes)
                cur.execute("""
                    UPDATE dr_email_templates
                    SET body_template = %s,
                        subject_template = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE language_code = %s
                """, (body, template['subject'], template['code']))
                
                if cur.rowcount > 0:
                    print(f"   ✅ Atualizado na BD!")
                else:
                    print(f"   ⚠️ Template não encontrado na BD, criando...")
                    cur.execute("""
                        INSERT INTO dr_email_templates (language_code, language_name, subject_template, body_template, updated_at)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """, (template['code'], template['name'], template['subject'], body))
                    print(f"   ✅ Criado na BD!")
        
        conn.commit()
        print("\n" + "="*60)
        print("✅ TODOS OS TEMPLATES ATUALIZADOS COM SUCESSO!")
        print("="*60)
        
        # Verificar
        with conn.cursor() as cur:
            cur.execute("SELECT language_code, language_name, LENGTH(body_template), updated_at FROM dr_email_templates ORDER BY language_code")
            print("\n📋 Templates na BD:")
            for row in cur.fetchall():
                print(f"   {row[0].upper()}: {row[1]} ({row[2]:,} caracteres) - Updated: {row[3]}")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()
        print("\n🔌 Conexão fechada")

if __name__ == '__main__':
    print("="*60)
    print("📧 ATUALIZAR TEMPLATES DE EMAIL NO RENDER")
    print("="*60)
    update_templates()
