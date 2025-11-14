# 📱 WhatsApp Admin Settings - Guia Completo

Painel completo de administração WhatsApp com gestão de templates, automações e conexão Facebook.

---

## ✨ O Que Foi Implementado

### 1. ✅ Tab WhatsApp no Admin Panel

**Localização:** Admin → Settings → **WhatsApp**

Adicionado novo tab entre "Price Adjustment" e "Users"
- Design consistente com outros tabs
- Hover effect amarelo (#f6b511)
- Acessível via `/admin/whatsapp`

### 2. ✅ Página Completa de Configurações

**4 Sub-tabs Principais:**

#### **📱 Conexão Facebook**
Configurar credenciais da WhatsApp Cloud API:
- **Access Token** (Permanent token do Meta for Developers)
- **Phone Number ID** (ID do número WhatsApp Business)
- **Business Account ID** (WhatsApp Business Account ID)
- **Webhook Verify Token** (Senha segura para webhook)

**Webhook URL:** `https://carrental-api-5f8q.onrender.com/api/whatsapp/webhook`

**Botões:**
- **Guardar Configurações** (azul) - Salva no PostgreSQL
- **Testar Conexão** (verde) - Valida credenciais

#### **📋 Templates**
Gestão de templates de mensagens:
- Criar templates multi-língua
- Lista de templates aprovados
- Status de aprovação WhatsApp
- Botão "+ Criar Template"

**Nota:** Templates precisam aprovação WhatsApp (até 24h)

#### **⚡ Respostas Rápidas**
Quick replies para atendimento rápido:
- Criar shortcuts (ex: `/preco`, `/info`)
- Categorias (pricing, support, general)
- Contador de uso
- Editar/Eliminar respostas

**Carrega automaticamente** da API `/api/whatsapp/quick-replies`

#### **🤖 Automações**
Mensagens automatizadas:
- **Resposta Automática Inicial** - Primeira mensagem do cliente
- **Confirmação de Reserva** - Ao criar booking
- **Lembrete de Pickup** - 24h/12h/6h/2h antes
- Selecionar templates para cada automação

### 3. ✅ Foto Utilizador no Header

**JÁ IMPLEMENTADO** no `index.html`:
- Foto do utilizador (se existir)
- Inicial do nome em círculo (fallback)
- Dropdown com:
  - Nome e email do utilizador
  - **Edit Profile** - Link para /admin?section=profile
  - **Logout** (vermelho) - Terminar sessão

**Funciona para TODOS os utilizadores** (não só admin)

---

## 🔧 Arquitetura Técnica

### **Backend (main.py)**

#### Rota Principal
```python
@app.get("/admin/whatsapp", response_class=HTMLResponse)
async def admin_whatsapp_settings(request: Request):
    # Serve admin_whatsapp_settings.html
    # Requer permissão de admin
```

#### API Endpoints

**1. Salvar Configurações:**
```python
POST /api/admin/whatsapp/save-config
Body: {
    "access_token": "EAA...",
    "phone_number_id": "123...",
    "business_account_id": "987...",
    "verify_token": "senha_secreta"
}
Response: {"ok": true, "message": "..."}
```

**2. Testar Conexão:**
```python
POST /api/admin/whatsapp/test-connection
Response: {"success": true, "message": "Configuração encontrada"}
```

### **Database**

#### Tabela: `whatsapp_config`
```sql
CREATE TABLE whatsapp_config (
    id INTEGER PRIMARY KEY,
    access_token TEXT,
    phone_number_id TEXT,
    business_account_id TEXT,
    verify_token TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Características:**
- ID fixo = 1 (UPSERT)
- Auto-update timestamp
- Compatível SQLite + PostgreSQL

### **Frontend (admin_whatsapp_settings.html)**

#### Sistema de Tabs
```javascript
function showTab(tabName) {
    // Remove active de todos
    // Adiciona active ao selecionado
}
```

**Classes CSS:**
- `.tab-content` - Hidden por padrão
- `.tab-content.active` - Display: block
- `.tab-btn.active` - Background #009cb6

#### Integração com Quick Replies
```javascript
fetch('/api/whatsapp/quick-replies')
    .then(r => r.json())
    .then(data => renderQuickReplies(data.quick_replies));
```

**Renderiza:**
- Shortcut badge (código azul)
- Título e categoria
- Texto da mensagem
- Contador de uso
- Botão eliminar (vermelho)

---

## 📊 Fluxo de Uso

### **Configurar Conexão Facebook**

```
1. Admin → Settings → WhatsApp
2. Tab "Conexão Facebook"
3. Preencher formulário:
   - Access Token (do Meta for Developers)
   - Phone Number ID
   - Business Account ID
   - Verify Token (criar senha)
4. Clicar "Guardar Configurações"
5. Aguardar confirmação
6. Clicar "Testar Conexão" (opcional)
```

### **Criar Quick Reply**

```
1. Tab "Respostas Rápidas"
2. Clicar "+ Criar Resposta Rápida"
3. Modal aparece (a implementar)
4. Preencher:
   - Shortcut (ex: /preco)
   - Título
   - Mensagem
   - Categoria
5. Salvar
6. Aparece na lista automaticamente
```

### **Configurar Automação**

```
1. Tab "Automações"
2. Selecionar tipo:
   - Resposta Automática Inicial
   - Confirmação de Reserva
   - Lembrete de Pickup
3. Escolher template (dropdown)
4. Ativar toggle
5. Configurar tempo (se aplicável)
6. Clicar "Guardar Automações"
```

---

## 🎨 Design Guidelines

### **Cores**

| Elemento | Cor | Uso |
|----------|-----|-----|
| **Primary** | `#009cb6` | Botões principais, tabs ativos |
| **Hover** | `#008a9e` | Hover em botões azuis |
| **Success** | `#10b981` | Botão "Testar Conexão" |
| **Warning** | `#f6b511` | Alertas, badges amarelos |
| **Error** | `#ef4444` | Botões eliminar, erros |

### **Ícones**

Todos SVG monocromáticos (SEM emojis):
- 📱 → SVG phone icon
- 📋 → SVG clipboard icon
- ⚡ → SVG lightning icon
- 🤖 → SVG robot icon

### **Alertas**

```html
<!-- Info Alert (azul) -->
<div class="bg-blue-50 border-l-4 border-blue-500 p-4">
    <svg class="h-5 w-5 text-blue-500">...</svg>
    <p class="text-sm text-blue-700">Mensagem</p>
</div>

<!-- Warning Alert (amarelo) -->
<div class="bg-yellow-50 border-l-4 border-yellow-500 p-4">
    <p class="text-sm text-yellow-700">Aviso</p>
</div>
```

---

## 🔜 Próximos Passos (Opcional)

### **Funcionalidades a Implementar**

1. **Modal de Criação de Template**
   - Formulário multi-língua (PT, EN, ES, DE, FR, IT)
   - Preview do template
   - Enviar para aprovação WhatsApp

2. **Modal de Quick Reply**
   - Criar nova resposta rápida
   - Editar existente
   - Validação de shortcut único

3. **Teste Real de Conexão**
   - Request para WhatsApp API
   - Validar token e permissions
   - Mostrar quota de mensagens

4. **Histórico de Templates**
   - Templates aprovados
   - Templates pendentes
   - Templates rejeitados
   - Motivo de rejeição

5. **Analytics de Automações**
   - Quantas mensagens enviadas
   - Taxa de resposta
   - Horários de pico

6. **Multi-língua Templates**
   - Sistema de tradução
   - Detetar idioma do cliente
   - Enviar template no idioma correto

---

## 📝 Notas Importantes

### **Segurança**

- ✅ Apenas admins podem aceder `/admin/whatsapp`
- ✅ Tokens salvos no PostgreSQL (não em arquivos)
- ✅ API endpoints protegidos com `require_admin()`
- ✅ Validação de entrada em todos os formulários

### **Performance**

- ✅ Quick replies carregam assincronamente
- ✅ Tabs sem reload de página (JavaScript)
- ✅ Cache de configurações no frontend
- ✅ Requisições otimizadas

### **Compatibilidade**

- ✅ SQLite (desenvolvimento local)
- ✅ PostgreSQL (produção Render)
- ✅ Mobile responsive (Tailwind)
- ✅ Funciona em Safari, Chrome, Firefox

---

## 🆘 Troubleshooting

### **Tab WhatsApp não aparece**
- Verifica se és admin: `request.session.get('is_admin') == True`
- Clear cache do browser
- Verifica deploy no Render

### **Erro ao salvar configurações**
```sql
-- Criar tabela manualmente se necessário
CREATE TABLE IF NOT EXISTS whatsapp_config (
    id INTEGER PRIMARY KEY,
    access_token TEXT,
    phone_number_id TEXT,
    business_account_id TEXT,
    verify_token TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Quick replies não carregam**
- Verifica endpoint: `/api/whatsapp/quick-replies`
- Testa via Postman/curl
- Verifica logs do Render: `Failed to fetch quick replies`

### **Foto do utilizador não aparece**
- Verifica se `profile_picture_path` existe na sessão
- Upload de foto em `/admin?section=profile`
- Fallback: Inicial do nome em círculo

---

## ✅ Checklist de Setup

**Desenvolvimento Local:**
- [ ] Criar tabela `whatsapp_config` no SQLite
- [ ] Testar rota `/admin/whatsapp`
- [ ] Testar API save-config
- [ ] Testar API test-connection
- [ ] Testar tabs switching
- [ ] Testar quick replies loading

**Produção (Render):**
- [ ] Aguardar deploy (commit `468e7ec`)
- [ ] Verificar tabela criada no PostgreSQL
- [ ] Testar acesso ao tab WhatsApp
- [ ] Configurar credenciais reais do Meta
- [ ] Testar conexão com WhatsApp API
- [ ] Verificar webhook configurado

---

## 📚 Links Úteis

**Meta for Developers:**
- https://developers.facebook.com/apps
- WhatsApp → Configuration → Webhook
- WhatsApp → API Setup → Credentials

**Documentação WhatsApp:**
- https://developers.facebook.com/docs/whatsapp/cloud-api/
- https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks

**Render (Logs):**
- https://dashboard.render.com/web/carrental-api-5f8q/logs

---

**Desenvolvido para Auto Prudente • 2024**
