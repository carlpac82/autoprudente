#!/bin/bash
echo "================================================"
echo "📧 CONFIGURAÇÃO RÁPIDA GMAIL OAUTH2"
echo "================================================"
echo ""
echo "Para conectar ao Gmail REAL, precisas de:"
echo ""
echo "1. Ir para: https://console.cloud.google.com"
echo "2. Criar novo projeto"
echo "3. Ativar Gmail API"
echo "4. Criar OAuth 2.0 credentials"
echo "5. Redirect URI: http://127.0.0.1:8000/api/oauth/gmail/callback"
echo ""
echo "Depois de obter as credenciais, cria o ficheiro .env:"
echo ""
echo "GOOGLE_CLIENT_ID=teu-client-id"
echo "GOOGLE_CLIENT_SECRET=teu-client-secret"
echo "OAUTH_REDIRECT_URI=http://127.0.0.1:8000/api/oauth/gmail/callback"
echo ""
echo "================================================"
echo ""
read -p "Tens as credenciais? (s/n): " resposta

if [ "$resposta" = "s" ]; then
    echo ""
    read -p "Cole o GOOGLE_CLIENT_ID: " client_id
    read -p "Cole o GOOGLE_CLIENT_SECRET: " client_secret
    
    cat > .env << ENVEOF
# Gmail OAuth2 Configuration
GOOGLE_CLIENT_ID=$client_id
GOOGLE_CLIENT_SECRET=$client_secret
OAUTH_REDIRECT_URI=http://127.0.0.1:8000/api/oauth/gmail/callback
ENVEOF
    
    echo ""
    echo "✅ Ficheiro .env criado!"
    echo "✅ Reinicia o servidor agora"
    echo ""
else
    echo ""
    echo "📖 Segue o guia em GMAIL_OAUTH_SETUP.md"
    echo ""
fi
