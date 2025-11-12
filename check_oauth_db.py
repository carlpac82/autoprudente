#!/usr/bin/env python3
"""
Verificar tokens OAuth direto na base de dados
"""
import requests
import json

RENDER_URL = "https://carrental-api-5f8q.onrender.com"
USERNAME = "admin"
PASSWORD = "admin"

print("=" * 80)
print("🔐 VERIFICAR TOKENS OAUTH NA BASE DE DADOS")
print("=" * 80)
print()

# Login
print("🔐 Login...")
session = requests.Session()
session.post(f"{RENDER_URL}/login", 
             data={'username': USERNAME, 'password': PASSWORD},
             timeout=60)
print("✅ Login OK")
print()

# Carregar token
print("📥 Carregando token OAuth...")
response = session.get(f"{RENDER_URL}/api/oauth/load-token", timeout=60)

print(f"Status: {response.status_code}")
print()

if response.status_code == 200:
    data = response.json()
    
    if data.get('ok'):
        token_info = data.get('token', {})
        
        print("✅ TOKEN ENCONTRADO!")
        print()
        print(f"📧 Email: {token_info.get('email', 'N/A')}")
        print(f"👤 Nome: {token_info.get('name', 'N/A')}")
        print(f"🔑 Google ID: {token_info.get('googleId', 'N/A')}")
        print(f"⏰ Expira em: {token_info.get('expiresAt', 'N/A')}")
        print(f"🖼️  Foto: {token_info.get('picture', 'N/A')[:50]}..." if token_info.get('picture') else "N/A")
        print()
        
        # Verificar se token expirou
        if token_info.get('expiresAt'):
            from datetime import datetime
            try:
                expires_at = datetime.fromisoformat(token_info['expiresAt'].replace('Z', '+00:00'))
                now = datetime.now(expires_at.tzinfo)
                
                if now > expires_at:
                    print("⚠️  TOKEN EXPIRADO!")
                    print(f"   Expirou em: {expires_at}")
                    print(f"   Hora atual: {now}")
                    print()
                    print("🔄 SOLUÇÃO:")
                    print("   1. Vai a: /customization-email")
                    print("   2. Clica 'Connect Gmail' novamente")
                    print()
                else:
                    print("✅ Token ainda válido")
                    print(f"   Expira em: {(expires_at - now).total_seconds() / 3600:.1f} horas")
                    print()
            except Exception as e:
                print(f"⚠️  Erro ao verificar expiração: {e}")
                print()
    else:
        print("❌ NENHUM TOKEN ENCONTRADO!")
        print()
        print("🔄 SOLUÇÃO:")
        print("   1. Vai a: /customization-email")
        print("   2. Clica 'Connect Gmail'")
        print("   3. Autoriza a aplicação")
        print()
else:
    print(f"❌ Erro HTTP {response.status_code}")
    print(response.text)
    print()

print("=" * 80)
