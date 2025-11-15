# 🔑 Como Obter Token Permanente do WhatsApp Business API

## ⚠️ IMPORTANTE: Tokens "Permanentes" = 60 Dias

A Meta/Facebook **NÃO fornece tokens verdadeiramente permanentes**. O máximo são tokens de **60 dias** que precisam ser renovados.

**Mas não te preocupes!** O sistema já tem **renovação automática** implementada. 🎉

---

## 🚀 Método 1: Token de Longa Duração (60 dias) - RECOMENDADO

### Passo 1: Obter Token Temporário

1. **Ir para:** https://developers.facebook.com/apps/
2. **Selecionar** a tua app (AutoPrudente WhatsApp)
3. **Menu lateral:** WhatsApp → API Setup
4. **Copiar** o "Temporary access token" (válido 24h)

### Passo 2: Converter para Token de Longa Duração

**Opção A: Via Graph API Explorer (Mais Fácil)**

1. **Ir para:** https://developers.facebook.com/tools/explorer/
2. **Selecionar** a tua app no dropdown
3. **Colar** o token temporário no campo "Access Token"
4. **Clicar** no ícone de informação (ℹ️) ao lado do token
5. **Clicar** em "Open in Access Token Tool"
6. **Clicar** em "Extend Access Token"
7. **Copiar** o novo token (válido 60 dias)

**Opção B: Via cURL (Linha de Comandos)**

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token" \
  -d "grant_type=fb_exchange_token" \
  -d "client_id=YOUR_APP_ID" \
  -d "client_secret=YOUR_APP_SECRET" \
  -d "fb_exchange_token=YOUR_TEMP_TOKEN"
```

**Resposta:**
```json
{
  "access_token": "EAAxxxxxxxxxxxx",
  "token_type": "bearer",
  "expires_in": 5183944  // ~60 dias em segundos
}
```

### Passo 3: Configurar no Sistema

**A. Via Interface Admin (Mais Fácil):**

1. **Ir para:** Admin Settings → WhatsApp
2. **Colar** o token de 60 dias no campo "Access Token"
3. **Preencher** Phone Number ID e Business Account ID
4. **Clicar** "Save Configuration"

**B. Via Variáveis de Ambiente (.env):**

```bash
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxx  # Token de 60 dias
WHATSAPP_PHONE_NUMBER_ID=123456789
WHATSAPP_BUSINESS_ACCOUNT_ID=987654321
WHATSAPP_APP_ID=your_app_id
WHATSAPP_APP_SECRET=your_app_secret
WHATSAPP_VERIFY_TOKEN=meu_token_secreto_123
```

---

## ✅ Renovação Automática (JÁ IMPLEMENTADA!)

O sistema **já renova o token automaticamente** a cada hora. Não precisas fazer nada! 🎉

### Como Funciona:

1. **Worker em Background:** Corre a cada 1 hora
2. **Verifica Expiração:** Se faltam menos de 3 dias para expirar
3. **Renova Automaticamente:** Obtém novo token de 60 dias
4. **Guarda na Base de Dados:** Token atualizado

**Código (main.py linhas 5037-5182):**
```python
WHATSAPP_TOKEN_REFRESH_BUFFER = timedelta(days=3)
WHATSAPP_TOKEN_REFRESH_INTERVAL_SECONDS = 60 * 60  # 1 hora

async def _whatsapp_token_refresh_worker():
    while True:
        await refresh_whatsapp_access_token()
        await asyncio.sleep(WHATSAPP_TOKEN_REFRESH_INTERVAL_SECONDS)
```

### Logs de Renovação:

Podes ver nos logs do Render:
```
[WHATSAPP] Starting token refresh worker
[WHATSAPP] refreshed token, expires at 2025-01-15T10:30:00Z
```

---

## 🔧 Método 2: System User Token (MAIS PERMANENTE)

Para um token mais estável, cria um **System User** na Meta Business Suite.

### Passo 1: Criar System User

1. **Ir para:** https://business.facebook.com/settings/system-users
2. **Clicar:** "Add" → "Add System User"
3. **Nome:** "AutoPrudente API System User"
4. **Role:** Admin
5. **Clicar:** "Create System User"

### Passo 2: Gerar Token do System User

1. **Selecionar** o System User criado
2. **Clicar:** "Generate New Token"
3. **Selecionar** a tua App
4. **Permissões:**
   - ✅ `whatsapp_business_messaging`
   - ✅ `whatsapp_business_management`
   - ✅ `business_management`
5. **Expiration:** "60 days" (ou "Never expire" se disponível)
6. **Gerar** e **copiar** o token

### Passo 3: Atribuir Assets

1. **Voltar** à página do System User
2. **Clicar:** "Add Assets"
3. **Selecionar:** WhatsApp Accounts
4. **Escolher** o teu WhatsApp Business Account
5. **Permissão:** Manage WhatsApp Account
6. **Salvar**

### Vantagens do System User:

- ✅ Não associado a uma pessoa específica
- ✅ Mais estável (não expira se a pessoa sair)
- ✅ Melhor para produção
- ✅ Token pode durar 60 dias ou mais

---

## 🛡️ Configuração de Renovação Manual

Se quiseres controlar a renovação manualmente:

### Via Interface Admin:

1. **Ir para:** WhatsApp Dashboard
2. **Clicar** no botão **"Renovar Token"** (ícone de sincronização) no header
3. Sistema renova automaticamente

### Via API:

```bash
curl -X POST "https://carrental-api-5f8q.onrender.com/api/admin/whatsapp/refresh-token" \
  -H "Cookie: session=your_session_cookie"
```

### Via Python:

```python
import requests

response = requests.post(
    'https://carrental-api-5f8q.onrender.com/api/admin/whatsapp/refresh-token',
    cookies={'session': 'your_session_cookie'}
)
print(response.json())
```

---

## 📊 Verificar Status do Token

### Via Interface:

1. **Ir para:** Admin Settings → WhatsApp
2. **Ver** data de expiração do token
3. **Status:** Verde (válido) ou Vermelho (expirado/perto de expirar)

### Via Logs:

Verificar logs do Render:
```bash
# Ver logs recentes
https://dashboard.render.com/web/rental-price-tracker/logs

# Procurar por:
[WHATSAPP] refreshed token, expires at ...
[WHATSAPP] Token refresh worker failure: ...
```

### Manualmente:

```bash
curl -X GET "https://graph.facebook.com/v18.0/debug_token" \
  -d "input_token=YOUR_TOKEN" \
  -d "access_token=YOUR_APP_ID|YOUR_APP_SECRET"
```

**Resposta:**
```json
{
  "data": {
    "app_id": "123456",
    "expires_at": 1736942400,  // Timestamp Unix
    "is_valid": true,
    "scopes": ["whatsapp_business_messaging"]
  }
}
```

---

## ⚠️ Problemas Comuns

### 1. Token Expirou

**Sintoma:** Mensagens não enviam, erro "Invalid OAuth access token"

**Solução:**
1. Gerar novo token de 60 dias (Método 1)
2. Atualizar no Admin Settings
3. Sistema renova automaticamente daqui para frente

### 2. Renovação Automática Falhou

**Sintoma:** Logs mostram "Token refresh failed"

**Verificar:**
- `WHATSAPP_APP_ID` e `WHATSAPP_APP_SECRET` estão corretos no Render
- App tem permissões corretas
- Token ainda está válido (não foi revogado manualmente)

**Solução:**
```bash
# No Render Dashboard:
# Environment → Add
WHATSAPP_APP_ID=your_app_id
WHATSAPP_APP_SECRET=your_app_secret
```

### 3. Token Revogado

**Sintoma:** Erro "Token has been revoked"

**Causas:**
- Mudou senha da conta Meta
- Revogou acesso manualmente
- Removeu app do Business Manager

**Solução:**
- Gerar novo token (Método 1 ou 2)
- Verificar permissões da app
- Re-adicionar WhatsApp Product se necessário

---

## 🔐 Segurança

### ✅ Boas Práticas:

1. **Nunca** partilhar token publicamente
2. **Usar** variáveis de ambiente (não hardcode)
3. **Guardar** backup do token em local seguro
4. **Renovar** antes de expirar (sistema faz automaticamente)
5. **Usar** System User para produção (Método 2)

### ❌ Não Fazer:

- ❌ Commitar token no Git
- ❌ Partilhar token por email/chat
- ❌ Usar token de teste em produção
- ❌ Ignorar avisos de expiração

---

## 📋 Checklist Final

Depois de configurar, deves ter:

- [x] Token de 60 dias configurado
- [x] `WHATSAPP_APP_ID` e `WHATSAPP_APP_SECRET` no Render
- [x] Renovação automática ativa (logs confirmam)
- [x] Backup do token em local seguro
- [x] System User criado (opcional mas recomendado)

---

## 🆘 Precisa de Ajuda?

Se o token continuar a expirar:

1. Verificar variáveis de ambiente no Render
2. Ver logs de renovação: `[WHATSAPP] Token refresh`
3. Testar renovação manual via botão na interface
4. Criar System User (Método 2) para maior estabilidade

---

## 📚 Links Úteis

- **Meta for Developers:** https://developers.facebook.com/
- **Business Manager:** https://business.facebook.com/
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Access Token Tool:** https://developers.facebook.com/tools/accesstoken/
- **System Users:** https://business.facebook.com/settings/system-users
- **Documentação WhatsApp API:** https://developers.facebook.com/docs/whatsapp/

---

## 🎉 Resumo

**O sistema JÁ tem renovação automática!** 

Só precisas:
1. Gerar um token inicial de 60 dias (Método 1 ou 2)
2. Configurar `WHATSAPP_APP_ID` e `WHATSAPP_APP_SECRET`
3. Deixar o sistema renovar automaticamente a cada hora

**O token nunca vai expirar** enquanto o servidor estiver a correr! ✅
