#!/usr/bin/env python3
"""
Script para criar a tabela user_settings no PostgreSQL
Execute no Render Shell se houver erro: no such table: user_settings
"""

import os
import psycopg2
from psycopg2 import sql

def fix_user_settings_table():
    """Criar tabela user_settings se não existir"""
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrado!")
        print("   Este script deve ser executado no Render Shell")
        return False
    
    try:
        print("=" * 80)
        print("🔧 CRIANDO TABELA user_settings")
        print("=" * 80)
        print()
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Create user_settings table
        print("📋 Criando tabela user_settings...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_key TEXT NOT NULL,
                setting_key TEXT NOT NULL,
                setting_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_key, setting_key)
            )
        """)
        
        # Create index
        print("📊 Criando índice...")
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_settings_user 
                ON user_settings(user_key)
            """)
        except Exception as e:
            print(f"⚠️  Índice já existe ou erro: {e}")
            conn.rollback()
        
        conn.commit()
        
        # Verify table exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'user_settings'
        """)
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("✅ Tabela user_settings criada com sucesso!")
            
            # Check if there are any rows
            cursor.execute("SELECT COUNT(*) FROM user_settings")
            row_count = cursor.fetchone()[0]
            print(f"📊 Registos existentes: {row_count}")
        else:
            print("❌ Erro: Tabela não foi criada!")
            return False
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 80)
        print("✅ TABELA user_settings PRONTA!")
        print("=" * 80)
        print()
        print("📋 Estrutura:")
        print("   - user_key (TEXT) - Chave do utilizador")
        print("   - setting_key (TEXT) - Nome da configuração")
        print("   - setting_value (TEXT) - Valor da configuração")
        print("   - updated_at (TIMESTAMP) - Data de atualização")
        print()
        print("🔑 Primary Key: (user_key, setting_key)")
        print("📊 Index: idx_user_settings_user")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executar fix"""
    print()
    print("🔧 FIX: Tabela user_settings")
    print()
    
    success = fix_user_settings_table()
    
    if success:
        print("✅ Tabela criada com sucesso!")
        print()
        print("📋 Próximos passos:")
        print("   1. Reiniciar o serviço no Render")
        print("   2. Testar funcionalidade de user settings")
        print()
    else:
        print("❌ Erro ao criar tabela!")
        print()
        print("💡 Dicas:")
        print("   1. Verificar se DATABASE_URL está configurado")
        print("   2. Verificar permissões do PostgreSQL")
        print("   3. Executar no Render Shell")
        print()

if __name__ == "__main__":
    main()
