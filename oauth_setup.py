"""
Gmail OAuth2 Setup Script
Run this to configure Gmail OAuth2 credentials
"""

import os
from pathlib import Path

def setup_oauth():
    print("=" * 60)
    print("📧 GMAIL OAUTH2 SETUP")
    print("=" * 60)
    print()
    print("Para conectar ao Gmail real, precisas de:")
    print("1. Client ID do Google Cloud Console")
    print("2. Client Secret do Google Cloud Console")
    print()
    print("Se ainda não tens, segue o guia em: GMAIL_OAUTH_SETUP.md")
    print()
    
    # Check if .env exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Ficheiro .env já existe")
        print()
        with open(env_file, 'r') as f:
            content = f.read()
            if 'GOOGLE_CLIENT_ID' in content:
                print("✅ GOOGLE_CLIENT_ID já configurado")
            if 'GOOGLE_CLIENT_SECRET' in content:
                print("✅ GOOGLE_CLIENT_SECRET já configurado")
        print()
        response = input("Queres atualizar as credenciais? (s/n): ")
        if response.lower() != 's':
            print("Setup cancelado.")
            return
    
    print()
    print("Vamos configurar as credenciais OAuth2:")
    print()
    
    client_id = input("Cole o GOOGLE_CLIENT_ID: ").strip()
    client_secret = input("Cole o GOOGLE_CLIENT_SECRET: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Credenciais inválidas!")
        return
    
    # Determine redirect URI
    print()
    print("Escolhe o ambiente:")
    print("1. Local (http://127.0.0.1:8000)")
    print("2. Produção (https://teu-dominio.com)")
    choice = input("Opção (1/2): ").strip()
    
    if choice == "2":
        domain = input("Domínio de produção (ex: autoprudente.com): ").strip()
        redirect_uri = f"https://{domain}/api/oauth/gmail/callback"
    else:
        redirect_uri = "http://127.0.0.1:8000/api/oauth/gmail/callback"
    
    # Create or update .env file
    env_content = f"""# Gmail OAuth2 Configuration
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}
OAUTH_REDIRECT_URI={redirect_uri}

# Add other environment variables below
"""
    
    with open(".env", 'w') as f:
        f.write(env_content)
    
    print()
    print("=" * 60)
    print("✅ CONFIGURAÇÃO COMPLETA!")
    print("=" * 60)
    print()
    print("Ficheiro .env criado com sucesso!")
    print()
    print("⚠️  IMPORTANTE:")
    print("1. Adiciona .env ao .gitignore (se ainda não estiver)")
    print("2. Instala as dependências:")
    print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    print("3. Reinicia o servidor")
    print("4. Testa a conexão em Settings → Email Notifications")
    print()
    print("🔒 NUNCA commits o ficheiro .env no Git!")
    print()

if __name__ == "__main__":
    setup_oauth()
