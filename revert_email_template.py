#!/usr/bin/env python3
"""
🔄 REVERT: Voltar ao layout original do email (simples, sem header HTML)
Mas mantém {raNumber} no texto
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
    print("🔄 Revertendo template de email para layout original...")
    print("=" * 60)
    
    # Carregar configuração
    load_env()
    
    # Template ORIGINAL SIMPLES mas com {raNumber} incluído
    simple_template = '''Olá {firstName},

Segue em anexo o Relatório de Danos nº {drNumber} referente ao contrato {raNumber}.

**Detalhes:**
- Matrícula: {vehiclePlate}
- Data: {date}

Cumprimentos,
Auto Prudente'''
    
    # Conectar à BD
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não definida!")
        return 1
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Atualizar template PT
        print("\n📝 Revertendo template PT para formato simples...")
        cursor.execute("""
            UPDATE dr_email_templates
            SET body_template = %s,
                updated_at = NOW()
            WHERE language_code = 'pt'
        """, (simple_template,))
        
        rows_updated = cursor.rowcount
        print(f"   ✅ {rows_updated} template(s) revertidos")
        
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
        print("✅ TEMPLATE REVERTIDO PARA LAYOUT ORIGINAL!")
        print("=" * 60)
        print("\nO email agora é:")
        print("  • Formato SIMPLES (texto apenas)")
        print("  • SEM header HTML visual")
        print("  • MAS mantém {raNumber} no texto ✅")
        print("\nTeste enviando um email para confirmar!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
