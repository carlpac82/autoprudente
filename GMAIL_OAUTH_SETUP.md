# 📧 Como Configurar Gmail OAuth2 Real

## Passo 1: Criar Projeto no Google Cloud Console

1. Vai para [Google Cloud Console](https://console.cloud.google.com)
2. Clica em "Select a project" → "New Project"
3. Nome do projeto: "AutoPrudente Email Notifications"
4. Clica em "Create"

## Passo 2: Ativar Gmail API

1. No menu lateral, vai para "APIs & Services" → "Library"
2. Procura por "Gmail API"
3. Clica em "Gmail API"
4. Clica em "Enable"

## Passo 3: Criar Credenciais OAuth 2.0

1. Vai para "APIs & Services" → "Credentials"
2. Clica em "Create Credentials" → "OAuth client ID"
3. Se pedido, configura o "OAuth consent screen":
   - User Type: **External**
   - App name: **AutoPrudente**
   - User support email: **teu email**
   - Developer contact: **teu email**
   - Clica "Save and Continue"
   - Scopes: Clica "Add or Remove Scopes"
     - Adiciona: `https://www.googleapis.com/auth/gmail.send`
   - Test users: Adiciona o teu email Gmail
   - Clica "Save and Continue"

4. Volta para "Credentials" → "Create Credentials" → "OAuth client ID"
5. Application type: **Web application**
6. Name: **AutoPrudente Email Integration**
7. Authorized redirect URIs:
   - **Local:** `http://127.0.0.1:8000/api/oauth/gmail/callback`
   - **Produção:** `https://teu-dominio.com/api/oauth/gmail/callback`
8. Clica "Create"

## Passo 4: Copiar Credenciais

Depois de criar, vais ver uma janela com:
- **Client ID**: algo como `123456789-abc123.apps.googleusercontent.com`
- **Client Secret**: algo como `GOCSPX-abc123def456`

**GUARDA ESTAS CREDENCIAIS!**

## Passo 5: Configurar no Projeto

### Opção A: Variáveis de Ambiente (Recomendado)

Cria um ficheiro `.env` na raiz do projeto:

```bash
GOOGLE_CLIENT_ID=teu-client-id-aqui
GOOGLE_CLIENT_SECRET=teu-client-secret-aqui
OAUTH_REDIRECT_URI=http://127.0.0.1:8000/api/oauth/gmail/callback
```

### Opção B: Direto no Código (Apenas para testes locais)

Edita `main.py` e substitui:
```python
GOOGLE_CLIENT_ID = 'teu-client-id-aqui'
GOOGLE_CLIENT_SECRET = 'teu-client-secret-aqui'
```

## Passo 6: Instalar Dependências

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Passo 7: Testar

1. Reinicia o servidor
2. Vai para Settings → Email Notifications
3. Clica "Conectar Gmail"
4. Deves ser redirecionado para o Google
5. Faz login e autoriza a aplicação
6. Serás redirecionado de volta e a conta ficará conectada!

## 🔒 Segurança

- **NUNCA** commits o `.env` ou credenciais no Git
- Adiciona `.env` ao `.gitignore`
- Em produção, usa variáveis de ambiente do Render/servidor
- Usa HTTPS em produção (obrigatório para OAuth2)

## 📝 Notas

- O Gmail tem limites de envio: 500 emails/dia para contas gratuitas
- Para produção, considera usar um serviço SMTP profissional
- Mantém o Client Secret seguro e nunca o exponhas no frontend
