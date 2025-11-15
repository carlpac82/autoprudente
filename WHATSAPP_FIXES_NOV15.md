# WhatsApp Dashboard - Correções 15 Nov 2025

## 🎯 Problemas Resolvidos

### 1. ✅ Coluna `token_expires_at` Missing (CRÍTICO)
**Erro:** `column "token_expires_at" of relation "whatsapp_config" does not exist`

**Causa:** Função `_ensure_whatsapp_config_token_column()` não fazia commit

**Solução:**
- Adicionado `con.commit()` após ALTER TABLE
- Verificação automática no startup
- Logs informativos de sucesso
- Tratamento de erros melhorado

**Commit:** `9a2d600`

---

### 2. ✅ Opções Eliminar/Arquivar Mensagens e Conversas
**Requisitos:** Eliminar mensagens individuais, arquivar e eliminar conversas

**Implementado:**

#### **Backend - Novos Endpoints:**
```python
DELETE /api/whatsapp/messages/{message_id}          # Eliminar mensagem
DELETE /api/whatsapp/conversations/{conversation_id} # Eliminar conversa
POST   /api/whatsapp/conversations/{conversation_id}/archive  # Já existia
```

#### **Frontend - UI:**
- ✅ Botão **eliminar mensagem** (hover vermelho em cada mensagem)
- ✅ Menu dropdown no header da conversa (⋮):
  - Exportar Conversa
  - Arquivar
  - Eliminar (permanente)

**Commit:** `86e612d`

---

### 3. ✅ Mensagens com "Auto Prudente Rent a Car"
**Problema:** Mensagens mostram nome da empresa

**Causa:** Campo `sender_name` com dados indesejados salvos na base de dados

**Solução:**

#### **Endpoint de Diagnóstico e Correção:**
```
POST /api/admin/whatsapp/fix-messages
```
- Verifica últimas 100 mensagens
- Remove `sender_name` se contém "Auto Prudente"
- Retorna estatísticas: quantas mensagens foram corrigidas

#### **Interface Admin:**
- **Admin Settings → WhatsApp → Tab "Contactos"**
- Botão amarelo: **"🔧 Corrigir Mensagens (remove 'Auto Prudente')"**
- Feedback com estatísticas após execução

**Commit:** `e0841e8`

---

### 4. ⚠️ Cores das Mensagens (Verificação Necessária)

**CSS Correto:**
```css
.message-inbound {
    background-color: rgba(245, 158, 11, 0.2);  /* AMARELO com transparência */
    border-radius: 0 7.5px 7.5px 7.5px;
    color: #303030;
}

.message-outbound {
    background-color: rgba(0, 156, 182, 0.2);   /* AZUL com transparência */
    border-radius: 7.5px 0 7.5px 7.5px;
    color: #303030;
}
```

**HTML Correto:**
```javascript
<div class="flex ${msg.direction === 'outbound' ? 'justify-end' : 'justify-start'} mb-2">
    <div class="message-bubble ${msg.direction === 'inbound' ? 'message-inbound' : 'message-outbound'} ...">
```

**Se mensagens continuam todas em azul:**
- Problema está nos **dados da base de dados**
- Campo `direction` pode estar incorreto (todas como "outbound")
- Verificar: mensagens recebidas devem ter `direction = 'inbound'`

**Possível solução futura:** Criar script para corrigir campo `direction` baseado em lógica de remetente

---

## 🚀 Como Usar Após Deploy

### **Passo 1: Corrigir Mensagens com "Auto Prudente"**
1. Ir para: **Admin Settings** → **WhatsApp**
2. Tab: **Contactos**
3. Clicar botão amarelo: **"🔧 Corrigir Mensagens"**
4. Confirmar
5. Ver estatísticas de quantas mensagens foram corrigidas
6. Recarregar WhatsApp Dashboard

### **Passo 2: Eliminar Mensagens Individuais**
1. Ir para: **WhatsApp Dashboard**
2. Abrir conversa
3. Passar mouse sobre mensagem → aparece botão vermelho 🗑️
4. Clicar → confirmar eliminação

### **Passo 3: Arquivar/Eliminar Conversas**
1. WhatsApp Dashboard → abrir conversa
2. Clicar botão **⋮** (menu) no header
3. Escolher:
   - **Exportar Conversa** (download JSON)
   - **Arquivar** (oculta conversa)
   - **Eliminar** (permanente - confirma 2x)

---

## 📊 Endpoints Implementados

| Método | Endpoint | Função |
|--------|----------|--------|
| `DELETE` | `/api/whatsapp/messages/{message_id}` | Eliminar mensagem |
| `DELETE` | `/api/whatsapp/conversations/{conversation_id}` | Eliminar conversa |
| `POST` | `/api/whatsapp/conversations/{conversation_id}/archive` | Arquivar conversa |
| `POST` | `/api/admin/whatsapp/fix-messages` | Corrigir sender_name |

---

## 🔍 Verificações Pós-Deploy

### ✅ **Token Expires At:**
```bash
# Logs Render devem mostrar:
[WHATSAPP] ✅ Ensured token_expires_at column exists (PostgreSQL)
[WHATSAPP] Starting token refresh worker
```

### ✅ **Mensagens Corrigidas:**
```bash
# Após clicar botão "Corrigir Mensagens":
✅ Correção concluída!
📊 Total verificado: 100
🔧 Mensagens corrigidas: X
```

### ✅ **Eliminar Mensagens:**
```bash
# Logs ao eliminar:
[WHATSAPP] ✅ Message {id} deleted
```

### ✅ **Eliminar Conversas:**
```bash
# Logs ao eliminar:
[WHATSAPP] ✅ Conversation #{id} deleted
```

---

## 🐛 Debugging - Se Cores Ainda Estão Erradas

### **Verificar Dados no PostgreSQL:**
```sql
-- Ver últimas mensagens com direção
SELECT id, message_text, direction, sender_name, timestamp 
FROM whatsapp_messages 
ORDER BY timestamp DESC 
LIMIT 20;
```

**Esperado:**
- Mensagens RECEBIDAS: `direction = 'inbound'`
- Mensagens ENVIADAS: `direction = 'outbound'`

**Se estiver tudo como `'outbound'`:**
- Problema no webhook que recebe mensagens
- Verificar endpoint: `/api/whatsapp/webhook`
- Mensagens recebidas devem ser salvas com `direction='inbound'`

---

## 📝 Próximos Passos (Se Necessário)

### **Se mensagens ainda aparecem em azul:**
1. Verificar dados: `SELECT direction FROM whatsapp_messages`
2. Se todas são `'outbound'`, criar script fix:
   ```python
   # Corrigir direction baseado em lógica
   # Ex: se não tem message_id do WhatsApp API = inbound
   ```

### **Se "Auto Prudente" ainda aparece:**
1. Executar botão "Corrigir Mensagens" novamente
2. Verificar se webhook está a salvar sender_name
3. Remover lógica que salva sender_name no webhook

---

## 🎉 Commits desta Sessão

| Commit | Descrição |
|--------|-----------|
| `9a2d600` | Fix: coluna token_expires_at + commit |
| `86e612d` | Feature: eliminar/arquivar mensagens e conversas |
| `e0841e8` | Feature: botão admin para corrigir mensagens |

---

## 📞 Suporte

**Problemas persistentes:**
1. Verificar logs do Render
2. Testar endpoints manualmente via Postman
3. Inspecionar dados no PostgreSQL
4. Verificar que token WhatsApp está válido

**Deploy:** https://dashboard.render.com → Auto-deploy em ~2-3 min
