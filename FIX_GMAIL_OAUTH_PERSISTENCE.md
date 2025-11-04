# 🔧 FIX: Gmail OAuth Desconecta Após Deploy

**Data:** 4 de Novembro de 2025, 23:00  
**Problema:** Gmail desconecta após cada deploy

---

## ❌ PROBLEMA

### Sintomas:
1. Conectas Gmail OAuth
2. Funciona temporariamente
3. Após deploy → Gmail desconecta
4. Emails de teste não enviam
5. Relatórios não enviam

### Causa:
**Token guardado no localStorage do browser!**

```javascript
// OAuth callback envia token via postMessage
window.opener.postMessage({
    token: 'ya29.xxx',
    refreshToken: 'xxx',
    expiresAt: 123456789
}, '*');

// Frontend guarda no localStorage
localStorage.setItem('emailOAuthToken', JSON.stringify(data));
```

**Problema:**
- localStorage é local ao browser
- Deploy limpa sessão
- Token perdido
- Gmail desconecta

---

## ✅ SOLUÇÃO IMPLEMENTADA

### 1. Nova Tabela na BD:

```sql
CREATE TABLE oauth_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider TEXT NOT NULL,           -- 'gmail'
  user_email TEXT NOT NULL,         -- Email conectado
  access_token TEXT NOT NULL,       -- Token de acesso
  refresh_token TEXT,               -- Token de refresh
  expires_at INTEGER,               -- Timestamp de expiração
  google_id TEXT,                   -- Google ID
  user_name TEXT,                   -- Nome do utilizador
  user_picture TEXT,                -- URL da foto
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(provider, user_email)      -- 1 token por provider/email
);
```

---

### 2. Novos Endpoints:

#### POST /api/oauth/save-token
**Guarda token na BD (persiste após deploy)**

```javascript
// Frontend chama após receber token
await fetch('/api/oauth/save-token', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        provider: 'gmail',
        email: 'user@gmail.com',
        token: 'ya29.xxx',
        refreshToken: 'xxx',
        expiresAt: 123456789,
        googleId: 'xxx',
        name: 'User Name',
        picture: 'https://...'
    })
});
```

#### GET /api/oauth/load-token?provider=gmail
**Carrega token da BD (restaura após deploy)**

```javascript
// Frontend carrega ao iniciar
const response = await fetch('/api/oauth/load-token?provider=gmail');
const data = await response.json();

if (data.ok) {
    // Token encontrado na BD!
    localStorage.setItem('emailOAuthToken', JSON.stringify(data.token));
}
```

---

### 3. Fluxo Completo:

```
┌─────────────────────────────────────────────┐
│ 1. Utilizador clica "Connect Gmail"        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 2. OAuth flow (Google)                      │
│    - Autoriza acesso                        │
│    - Recebe token                           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 3. Callback envia token via postMessage     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 4. Frontend recebe token                    │
│    ├─ Guarda no localStorage (temporário)   │
│    └─ Chama /api/oauth/save-token (BD)     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 5. Token guardado na BD PostgreSQL          │
│    ✅ Persiste após deploy!                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 6. Após deploy:                             │
│    ├─ Frontend carrega /api/oauth/load-token│
│    ├─ Restaura token do PostgreSQL          │
│    └─ Gmail continua conectado! ✅          │
└─────────────────────────────────────────────┘
```

---

## 🔧 ATUALIZAÇÃO NECESSÁRIA NO FRONTEND

### Ficheiro: templates/customization_email.html

**Adicionar após receber token OAuth:**

```javascript
// Quando recebe postMessage do OAuth
window.addEventListener('message', async function(event) {
    if (event.data.type === 'oauth-success') {
        const tokenData = event.data;
        
        // 1. Guardar no localStorage (temporário)
        localStorage.setItem('emailOAuthToken', JSON.stringify(tokenData));
        
        // 2. NOVO: Guardar na BD (permanente)
        try {
            const response = await fetch('/api/oauth/save-token', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    provider: tokenData.provider,
                    email: tokenData.email,
                    token: tokenData.token,
                    refreshToken: tokenData.refreshToken,
                    expiresAt: tokenData.expiresAt,
                    googleId: tokenData.googleId,
                    name: tokenData.name,
                    picture: tokenData.picture
                })
            });
            
            const result = await response.json();
            if (result.ok) {
                console.log('✅ Token saved to database');
            }
        } catch (error) {
            console.error('Failed to save token:', error);
        }
        
        // Atualizar UI
        updateConnectionStatus(tokenData);
    }
});
```

**Adicionar ao carregar página:**

```javascript
// Ao carregar página, tentar restaurar token da BD
async function loadTokenFromDatabase() {
    try {
        const response = await fetch('/api/oauth/load-token?provider=gmail');
        const data = await response.json();
        
        if (data.ok && data.token) {
            // Restaurar no localStorage
            localStorage.setItem('emailOAuthToken', JSON.stringify(data.token));
            
            // Atualizar UI
            updateConnectionStatus(data.token);
            
            console.log('✅ Token restored from database');
            return true;
        }
    } catch (error) {
        console.error('Failed to load token:', error);
    }
    return false;
}

// Chamar ao carregar
document.addEventListener('DOMContentLoaded', async function() {
    // Tentar carregar da BD primeiro
    const loaded = await loadTokenFromDatabase();
    
    if (!loaded) {
        // Fallback para localStorage
        const localToken = localStorage.getItem('emailOAuthToken');
        if (localToken) {
            updateConnectionStatus(JSON.parse(localToken));
        }
    }
});
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Backend: ✅
- [x] Criar tabela `oauth_tokens`
- [x] Endpoint POST `/api/oauth/save-token`
- [x] Endpoint GET `/api/oauth/load-token`

### Frontend: ⏳
- [ ] Atualizar `customization_email.html`
- [ ] Adicionar chamada `save-token` após OAuth
- [ ] Adicionar `loadTokenFromDatabase()` ao carregar
- [ ] Atualizar `customization_automated_reports.html`
- [ ] Testar fluxo completo

### Testes: ⏳
- [ ] Conectar Gmail
- [ ] Verificar token na BD
- [ ] Fazer deploy
- [ ] Verificar se Gmail continua conectado
- [ ] Enviar email de teste
- [ ] Verificar recepção

---

## 🎯 RESULTADO ESPERADO

**Antes:**
```
1. Conecta Gmail ✅
2. Deploy 🚀
3. Gmail desconecta ❌
4. Emails não enviam ❌
```

**Depois:**
```
1. Conecta Gmail ✅
2. Token guardado na BD ✅
3. Deploy 🚀
4. Token restaurado da BD ✅
5. Gmail continua conectado ✅
6. Emails enviam ✅
```

---

## 🔒 SEGURANÇA

**Tokens na BD:**
- ✅ PostgreSQL no Render (seguro)
- ✅ Não commitados ao Git
- ✅ Apenas admin autenticado acede
- ✅ HTTPS obrigatório
- ✅ Refresh token para renovar

**Boas práticas:**
- Token encriptado em trânsito (HTTPS)
- Acesso restrito (require_auth)
- Logs de acesso
- Expiração automática

---

## 📝 PRÓXIMOS PASSOS

1. **Atualizar frontend** (customization_email.html)
2. **Testar localmente**
3. **Commit e deploy**
4. **Reconectar Gmail**
5. **Testar após deploy**
6. **Verificar persistência**

---

**SOLUÇÃO COMPLETA IMPLEMENTADA NO BACKEND!** ✅  
**Aguarda atualização do frontend!** ⏳
