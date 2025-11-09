#!/usr/bin/env python3
"""
🎨 UPDATE: Apenas remove RA e aumenta DR no template ATUAL
"""

import os
import psycopg2
from pathlib import Path

def load_env():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def main():
    print("🎨 Atualizando template atual...")
    print("=" * 60)
    
    load_env()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não definida!")
        return 1
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Ler template atual
        print("\n📖 Lendo template atual...")
        cursor.execute("""
            SELECT body_template
            FROM dr_email_templates
            WHERE language_code = 'pt'
        """)
        current_template = cursor.fetchone()[0]
        
        print(f"   Template atual: {len(current_template)} caracteres")
        print("\n📝 Template atual:")
        print("-" * 60)
        print(current_template[:500])
        print("-" * 60)
        
        # Perguntar se quer continuar
        response = input("\nQuer modificar este template? (apenas remove RA e aumenta DR) [s/N]: ")
        
        if response.lower() != 's':
            print("❌ Cancelado")
            return 0
        
        # Modificar template
        # Se for texto simples, não faz sentido remover RA (não tem header)
        # Então provavelmente precisa do template HTML
        
        if '<html>' in current_template.lower():
            # É HTML - modificar header
            # Remover linha RA e aumentar DR de 14px para 18px
            modified = current_template
            
            # Remover linha RA
            modified = modified.replace('<div>RA: {raNumber}</div>', '')
            
            # Aumentar tamanho do DR de 14px para 18px
            modified = modified.replace('font-size: 14px', 'font-size: 18px')
            modified = modified.replace('font-size:14px', 'font-size:18px')
            
            print("\n✅ Modificações:")
            print("   • RA removido do header")
            print("   • DR aumentado de 14px → 18px")
        else:
            print("\n⚠️ Template atual é texto simples (não tem header visual)")
            print("Não há RA para remover.")
            return 0
        
        # Atualizar
        cursor.execute("""
            UPDATE dr_email_templates
            SET body_template = %s,
                updated_at = NOW()
            WHERE language_code = 'pt'
        """, (modified,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ TEMPLATE ATUALIZADO!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
