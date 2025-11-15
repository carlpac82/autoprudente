#!/usr/bin/env python3
"""
Script para criar a tabela whatsapp_contacts no PostgreSQL
Executa direto na base de dados atual
"""

import os
import psycopg2

# Obter DATABASE_URL do ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL não encontrado. Certifique-se que está no ambiente correto.")
    exit(1)

print(f"🔌 Conectando ao PostgreSQL...")

try:
    # Conectar ao PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("✅ Conectado com sucesso!")
    
    # Verificar se tabela já existe
    print("\n🔍 Verificando se tabela whatsapp_contacts existe...")
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'whatsapp_contacts'
        );
    """)
    exists = cur.fetchone()[0]
    
    if exists:
        print("⚠️  Tabela whatsapp_contacts JÁ EXISTE!")
        
        # Mostrar estrutura
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'whatsapp_contacts'
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        print("\n📊 Estrutura atual:")
        for col, dtype in columns:
            print(f"   - {col}: {dtype}")
    else:
        print("❌ Tabela whatsapp_contacts NÃO EXISTE. Criando...")
        
        # Criar tabela
        cur.execute("""
            CREATE TABLE whatsapp_contacts (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL UNIQUE,
                has_whatsapp BOOLEAN,
                profile_picture_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        print("✅ Tabela whatsapp_contacts criada com sucesso!")
        
        # Verificar se whatsapp_conversations precisa da coluna contact_id
        print("\n🔍 Verificando tabela whatsapp_conversations...")
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'whatsapp_conversations' 
                AND column_name = 'contact_id'
            );
        """)
        has_contact_id = cur.fetchone()[0]
        
        if not has_contact_id:
            print("❌ Coluna contact_id NÃO EXISTE em whatsapp_conversations. Adicionando...")
            
            cur.execute("""
                ALTER TABLE whatsapp_conversations 
                ADD COLUMN contact_id INTEGER REFERENCES whatsapp_contacts(id);
            """)
            
            print("✅ Coluna contact_id adicionada!")
        else:
            print("✅ Coluna contact_id JÁ EXISTE em whatsapp_conversations")
        
        # Commit
        conn.commit()
        print("\n🎉 TUDO PRONTO! Base de dados atualizada com sucesso!")
    
    # Fechar
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERRO: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
