#!/usr/bin/env python3
"""
🔍 VERIFICAR CREDENCIAIS GMAIL NA BASE DE DADOS

Executa localmente para verificar se as credenciais Gmail persistem.
"""

import os
import sys
from pathlib import Path

def load_env():
    """Load .env variables"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value

def check_credentials():
    """Check Gmail credentials in database"""
    print("\n" + "="*80)
    print("🔍 VERIFICANDO CREDENCIAIS GMAIL")
    print("="*80)
    
    load_env()
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada no .env")
        return
    
    print(f"\n📊 Conectando à base de dados...")
    print(f"   URL: {database_url[:50]}...")
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Check oauth_tokens table
        print("\n1️⃣ Verificando tabela oauth_tokens...")
        cursor.execute("""
            SELECT user_email, access_token, refresh_token, expires_at, updated_at
            FROM oauth_tokens 
            WHERE provider = 'google' 
            ORDER BY updated_at DESC 
            LIMIT 1
        """)
        row = cursor.fetchone()
        
        if not row:
            print("❌ NENHUMA CREDENCIAL GMAIL ENCONTRADA!")
            print("   → Precisa reconectar Gmail em Settings → Email Notifications")
            cursor.close()
            conn.close()
            return
        
        user_email, access_token, refresh_token, expires_at, updated_at = row
        
        print("✅ CREDENCIAIS ENCONTRADAS!")
        print(f"\n📧 Email: {user_email}")
        print(f"🔑 Access Token: {'✅ Existe' if access_token else '❌ Não existe'} ({len(access_token or '') if access_token else 0} chars)")
        print(f"🔄 Refresh Token: {'✅ Existe' if refresh_token else '❌ Não existe'} ({len(refresh_token or '') if refresh_token else 0} chars)")
        print(f"⏰ Expira em: {expires_at}")
        print(f"🕐 Última atualização: {updated_at}")
        
        # Verificar se está completo
        has_refresh = refresh_token and refresh_token.strip() != ''
        has_access = access_token and access_token.strip() != ''
        
        print("\n" + "="*80)
        if has_access and has_refresh:
            print("✅ CREDENCIAIS COMPLETAS E FUNCIONAIS!")
            print("   → O sistema pode enviar emails via Gmail")
        else:
            print("⚠️ CREDENCIAIS INCOMPLETAS!")
            if not has_access:
                print("   ❌ Access Token está vazio")
            if not has_refresh:
                print("   ❌ Refresh Token está vazio (CRÍTICO!)")
            print("\n   → SOLUÇÃO: Reconecte o Gmail:")
            print("      1. Vai a Settings → Email Notifications")
            print("      2. Clica 'Connect Gmail'")
            print("      3. Autoriza novamente")
        print("="*80)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    check_credentials()
