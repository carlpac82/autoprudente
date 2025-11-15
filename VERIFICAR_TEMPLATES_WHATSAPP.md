# ✅ Como Verificar se Templates WhatsApp Foram Aprovados

## 📋 Visão Geral

Os templates do WhatsApp Business precisam ser aprovados pelo WhatsApp antes de poderem ser usados. O processo pode levar até **24 horas**.

Este guia explica como verificar o status de aprovação dos seus templates.

---

## 🚀 Método 1: Via API (Recomendado)

### Endpoint
```
POST /api/whatsapp/templates/sync-status
```

### Como Usar (Browser Console)

1. **Abrir WhatsApp Dashboard** no browser
2. **Abrir Developer Tools** (F12 ou Cmd+Option+I)
3. **Colar este código no Console:**

```javascript
// Sincronizar status dos templates
const response = await fetch('/api/whatsapp/templates/sync-status', {
    method: 'POST',
    credentials: 'same-origin'
});

const data = await response.json();

if (data.ok) {
    console.log('✅ Sincronização completa!');
    console.log(`📊 Templates sincronizados: ${data.updates}`);
    console.log(`📝 Total de templates: ${data.total_templates}`);
} else {
    console.error('❌ Erro:', data.error);
}

// Buscar templates atualizados
const templates = await fetch('/api/whatsapp/templates').then(r => r.json());

console.table(templates.templates.map(t => ({
    Nome: t.name,
    Status: t.status,
    Categoria: t.category,
    Idioma: t.language_code,
    Aprovado: t.approved_at ? new Date(t.approved_at).toLocaleString('pt-PT') : 'N/A'
})));
```

### Resposta Esperada

```json
{
  "ok": true,
  "success": true,
  "message": "Sincronizado 3 templates",
  "total_templates": 5,
  "updates": 3
}
```

---

## 📊 Status dos Templates

| Status | Emoji | Significado | Ação |
|--------|-------|-------------|------|
| **APPROVED** | ✅ | Template aprovado | Pode usar! |
| **PENDING** | ⏳ | Aguardando aprovação | Aguarde até 24h |
| **REJECTED** | ❌ | Template rejeitado | Revisar e reenviar |

---

## 🔍 Método 2: Verificar no Facebook Business Manager

### Passo a Passo

1. **Aceder ao Facebook Business Manager**
   - URL: https://business.facebook.com/

2. **Ir para WhatsApp Manager**
   - Menu lateral → WhatsApp Manager

3. **Message Templates**
   - Tools → Message Templates

4. **Ver Status**
   - Lista mostra todos os templates
   - Status colorido:
     - **Verde**: Aprovado ✅
     - **Amarelo**: Pendente ⏳
     - **Vermelho**: Rejeitado ❌

---

## 🛠️ Método 3: Via cURL (Terminal)

### Requisitos
- Estar logado (ter cookie de sessão)

### Comando

```bash
# Exportar cookie de sessão (obter do browser)
export SESSION_COOKIE="session=SEU_COOKIE_AQUI"

# Sincronizar templates
curl -X POST https://carrental-api-5f8q.onrender.com/api/whatsapp/templates/sync-status \
  -H "Cookie: $SESSION_COOKIE" \
  -H "Content-Type: application/json"

# Listar templates
curl https://carrental-api-5f8q.onrender.com/api/whatsapp/templates \
  -H "Cookie: $SESSION_COOKIE" | jq '.templates[] | {name, status, approved_at}'
```

---

## ⚙️ Configuração Necessária

### Antes de Verificar Templates

Certifique-se que tem configurado:

1. ✅ **Access Token** (WhatsApp Business API)
2. ✅ **Business Account ID** (WABA ID)

### Como Obter Business Account ID

1. **Facebook Business Manager**
2. **WhatsApp Manager** → Settings
3. **Business Account ID** (número longo)
4. **Copiar** e guardar no Admin → WhatsApp Settings

---

## 📝 Exemplo Completo

### 1. Configurar WhatsApp

```
Admin → WhatsApp Settings
- Access Token: EAAxxxxxxx
- Phone Number ID: 123456789
- Business Account ID: 987654321  ← IMPORTANTE!
- Verify Token: meu_token_secreto
```

### 2. Criar Template

```
Nome: boas_vindas
Categoria: UTILITY
Conteúdo PT: Olá {{1}}! Bem-vindo à Auto Prudente.
```

### 3. Aguardar Aprovação

⏳ **0-24 horas** para WhatsApp aprovar

### 4. Verificar Status

```javascript
// Console do browser
const sync = await fetch('/api/whatsapp/templates/sync-status', {
    method: 'POST',
    credentials: 'same-origin'
}).then(r => r.json());

console.log(sync);
// { ok: true, message: "Sincronizado 1 templates" }

const templates = await fetch('/api/whatsapp/templates')
    .then(r => r.json());

const meuTemplate = templates.templates.find(t => t.name === 'boas_vindas');

console.log(meuTemplate.status);
// "APPROVED" ✅
```

---

## ❌ Erros Comuns

### 1. "WhatsApp não configurado"

**Solução:**
- Ir para Admin → WhatsApp Settings
- Configurar Access Token E Business Account ID

### 2. "WhatsApp API error: 401"

**Solução:**
- Access Token inválido ou expirado
- Gerar novo token no Facebook Business

### 3. "WhatsApp API error: 404"

**Solução:**
- Business Account ID incorreto
- Verificar ID no WhatsApp Manager

### 4. Template não aparece na lista

**Solução:**
- Template foi criado diretamente no Facebook?
- Fazer sync para importar:
  ```javascript
  await fetch('/api/whatsapp/templates/sync-status', {
      method: 'POST',
      credentials: 'same-origin'
  });
  ```

---

## 🔄 Sincronização Automática

### Opção 1: Manualmente (Recomendado)
- Executar quando precisar verificar
- Evita rate limits da API

### Opção 2: Scheduled (Futuro)
- Pode adicionar cron job
- Sincroniza 1x por hora
- Atualiza status automaticamente

---

## 📞 Suporte

**Dúvidas?**
- Documentação WhatsApp API: https://developers.facebook.com/docs/whatsapp
- WhatsApp Business Manager: https://business.facebook.com/

---

## ✅ Checklist de Verificação

- [ ] WhatsApp configurado (access_token + business_account_id)
- [ ] Template criado
- [ ] Aguardado até 24h
- [ ] Executado sync-status
- [ ] Verificado status (APPROVED/PENDING/REJECTED)
- [ ] Se APPROVED: Template pronto para usar!
- [ ] Se REJECTED: Revisar motivo e reenviar

---

**Criado:** 2025-11-15  
**Última Atualização:** 2025-11-15
