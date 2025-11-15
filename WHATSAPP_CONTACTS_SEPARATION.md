# Separação de Contactos e Conversas no WhatsApp Dashboard

## ✅ Implementado (Nov 15, 2025)

### 🎯 Problema Resolvido

**ANTES:** Quando se eliminava uma conversa, eliminava também o contacto da lista de Contactos.

**CAUSA:** Contactos e Conversas eram a mesma coisa (tabela `whatsapp_conversations`).

**AGORA:** Contactos e Conversas estão SEPARADOS em tabelas diferentes.

---

## 🏗️ Arquitetura Nova

### Tabelas

#### 1. `whatsapp_contacts` (NOVA)
```sql
CREATE TABLE whatsapp_contacts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    has_whatsapp BOOLEAN,
    profile_picture_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Propósito:** Armazena APENAS dados do contacto (pessoa).

#### 2. `whatsapp_conversations` (MODIFICADA)
```sql
CREATE TABLE whatsapp_conversations (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES whatsapp_contacts(id),  -- ✅ NOVO!
    phone_number TEXT NOT NULL UNIQUE,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_preview TEXT,
    unread_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'open',
    assigned_to TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Mudanças:**
- ✅ Adicionada coluna `contact_id` (FOREIGN KEY)
- ❌ Removidas colunas `name`, `has_whatsapp`, `profile_picture_url` (agora em `whatsapp_contacts`)

---

## 📡 Endpoints Novos/Modificados

### 1. **GET `/api/whatsapp/contacts`** (NOVO)
Retorna lista de contactos com contagem de conversas.

**Response:**
```json
{
  "ok": true,
  "success": true,
  "contacts": [
    {
      "id": 1,
      "name": "João Silva",
      "phone_number": "+351912345678",
      "has_whatsapp": true,
      "profile_picture_url": "/static/whatsapp_profiles/contact_1.jpg",
      "created_at": "2025-11-15T14:30:00",
      "conversation_count": 2  // ✅ Quantas conversas tem este contacto
    }
  ]
}
```

### 2. **POST `/api/whatsapp/contacts/add`** (MODIFICADO)
Agora cria PRIMEIRO o contacto, DEPOIS a conversa.

**Fluxo:**
1. Verifica se contacto já existe (por phone_number)
2. Se não existe, cria em `whatsapp_contacts`
3. Cria conversa em `whatsapp_conversations` com `contact_id`
4. Retorna ambos os IDs

**Response:**
```json
{
  "ok": true,
  "success": true,
  "message": "Contacto adicionado",
  "contact": {
    "name": "João Silva",
    "phone": "+351912345678",
    "id": 5,  // ID do contacto
    "conversation_id": 12,  // ID da conversa
    "has_whatsapp": true
  }
}
```

### 3. **DELETE `/api/whatsapp/contacts/{contact_id}`** (MODIFICADO)
Elimina contacto E TODAS as suas conversas + mensagens.

**Fluxo:**
1. Busca `contact_id` em `whatsapp_contacts`
2. Busca todas as conversas desse contacto
3. Elimina TODAS as mensagens dessas conversas
4. Elimina TODAS as conversas do contacto
5. Elimina o contacto

**Confirmação no Frontend:**
```
Eliminar CONTACTO e TODAS conversas?

Apaga:
- Contacto
- Todas as conversas deste contacto
- Todas as mensagens

Ação PERMANENTE

Tem certeza?
```

### 4. **DELETE `/api/whatsapp/conversations/{conversation_id}`** (SEM ALTERAÇÃO)
Elimina apenas conversa + mensagens, **MANTÉM o contacto**.

**Confirmação no Frontend:**
```
Eliminar CONVERSA?

Apaga: conversa + mensagens
Mantém: contacto (para apagar contacto, use o tab Contactos)

Ação PERMANENTE

Tem certeza?
```

---

## 🎨 Frontend - Mudanças

### Tab Contactos

**ANTES:**
```javascript
// Usava /api/whatsapp/conversations
async function loadContacts() {
    const response = await fetch('/api/whatsapp/conversations');
    conversations = data.conversations;
}
```

**DEPOIS:**
```javascript
// Usa /api/whatsapp/contacts
async function loadContacts() {
    const response = await fetch('/api/whatsapp/contacts');
    const contactsList = data.contacts;
}
```

**Renderização:**
- Mostra `conversation_count` (quantas conversas o contacto tem)
- Não mostra `unread_count` (esse é por conversa, não por contacto)
- Botão delete: "Eliminar contacto e TODAS conversas"

### Tab Conversas

**SEM ALTERAÇÃO:**
- Continua a usar `/api/whatsapp/conversations`
- Botão delete: "Eliminar conversa (mantém contacto)"

---

## 🔄 Migração de Dados

### Script: `create_whatsapp_contacts_table.py`

**O que faz:**
1. Conecta ao PostgreSQL do Render
2. Cria tabela `whatsapp_contacts`
3. Adiciona coluna `contact_id` em `whatsapp_conversations`
4. Migra dados existentes de `whatsapp_conversations` → `whatsapp_contacts`
5. Atualiza `contact_id` nas conversas

**Como executar no Render:**
```bash
# 1. Subir ficheiro para Render
# 2. No Render Shell:
python create_whatsapp_contacts_table.py
```

---

## 📋 Fluxo Completo

### Cenário 1: Adicionar Contacto

```
User clica "Adicionar Contacto"
  ↓
Preenche: Nome, Telefone
  ↓
POST /api/whatsapp/contacts/add
  ↓
Backend:
  1. Cria CONTACTO em whatsapp_contacts (ID=5)
  2. Cria CONVERSA em whatsapp_conversations (ID=12, contact_id=5)
  ↓
Frontend:
  - Recarrega Tab Contactos (mostra novo contacto)
  - Recarrega Tab Conversas (mostra nova conversa)
```

### Cenário 2: Eliminar Conversa

```
User clica ícone delete numa CONVERSA
  ↓
Confirmação: "Apaga conversa, mantém contacto"
  ↓
DELETE /api/whatsapp/conversations/12
  ↓
Backend:
  - Elimina mensagens da conversa #12
  - Elimina conversa #12
  - MANTÉM contacto #5
  ↓
Frontend:
  - Conversa desaparece da lista
  - Contacto PERMANECE na tab Contactos (com conversation_count - 1)
```

### Cenário 3: Eliminar Contacto

```
User clica ícone delete num CONTACTO
  ↓
Confirmação: "Apaga contacto E TODAS conversas"
  ↓
DELETE /api/whatsapp/contacts/5
  ↓
Backend:
  - Busca todas as conversas do contacto #5 (ex: #12, #13)
  - Elimina mensagens de #12 e #13
  - Elimina conversas #12 e #13
  - Elimina contacto #5
  ↓
Frontend:
  - Contacto desaparece da tab Contactos
  - Conversas #12 e #13 desaparecem da tab Conversas
```

---

## ✅ Validação Após Deploy

### 1. Tab Contactos
- [ ] Mostra lista de contactos (não conversas)
- [ ] Mostra `conversation_count` (ex: "2 conversas")
- [ ] Botão delete: "Eliminar contacto e TODAS conversas"
- [ ] Eliminar contacto apaga também conversas

### 2. Tab Conversas
- [ ] Mostra lista de conversas
- [ ] Mostra `unread_count` (ex: badge "3")
- [ ] Botão delete: "Eliminar conversa (mantém contacto)"
- [ ] Eliminar conversa NÃO apaga contacto

### 3. Adicionar Contacto
- [ ] Cria contacto em `whatsapp_contacts`
- [ ] Cria conversa em `whatsapp_conversations`
- [ ] Ambos aparecem nas respetivas tabs
- [ ] Refresh mantém os dados

---

## 📦 Ficheiros Modificados

### Backend
- `main.py`:
  - Criação de tabelas (linhas 5391-5420, 5544-5573, 5640-5669)
  - Endpoint GET `/api/whatsapp/contacts` (novo)
  - Endpoint POST `/api/whatsapp/contacts/add` (modificado)
  - Endpoint DELETE `/api/whatsapp/contacts/{id}` (modificado)

### Frontend
- `templates/whatsapp_dashboard.html`:
  - Função `loadContacts()` (linha 506-524)
  - Função `renderContacts()` (linha 541-574)
  - Confirmação `deleteConversation()` (linha 1391-1392)

### Scripts
- `create_whatsapp_contacts_table.py` (novo)
- `test_conversations.py` (teste local)
- `MIGRATION_CONTACTS_TEST_PLAN.md` (documentação)

---

## 🚨 IMPORTANTE - Ordem de Deploy

1. ✅ **Commit + Push para GitHub**
2. ✅ **Render auto-deploy** (cria endpoint mas tabela ainda não existe)
3. ✅ **Executar script de migração** (criar tabelas)
4. ✅ **Testar no dashboard**

---

## 🐛 Troubleshooting

### Erro: "column contact_id does not exist"
**Causa:** Tabelas ainda não migradas.
**Solução:** Executar `create_whatsapp_contacts_table.py` no Render Shell.

### Contactos não aparecem
**Causa:** Endpoint retorna vazio porque tabela `whatsapp_contacts` está vazia.
**Solução:** Script de migração copia dados de `whatsapp_conversations` → `whatsapp_contacts`.

### Eliminar conversa continua a apagar contacto
**Causa:** Código antigo em cache.
**Solução:** Hard refresh (Ctrl+Shift+R) + verificar deploy no Render.

---

## ✨ Benefícios

1. **Separação de Responsabilidades**
   - Contacto = Pessoa (nome, telefone, foto)
   - Conversa = Thread de mensagens

2. **Flexibilidade**
   - Um contacto pode ter múltiplas conversas
   - Eliminar conversa ≠ Eliminar contacto

3. **Organização**
   - Tab Contactos: lista de pessoas
   - Tab Conversas: histórico de chats

4. **Persistência**
   - Contacto guardado mesmo sem conversas ativas
   - Histórico de conversas por contacto

---

## 📊 Estrutura Final

```
whatsapp_contacts (PESSOAS)
├── id: 1
├── name: "João Silva"
├── phone: "+351912345678"
└── conversation_count: 2
    │
    ├── whatsapp_conversations (CHATS)
    │   ├── id: 12, contact_id: 1, status: "open"
    │   └── id: 13, contact_id: 1, status: "archived"
    │
    └── whatsapp_messages (MENSAGENS)
        ├── conversation_id: 12, text: "Olá!"
        └── conversation_id: 13, text: "Obrigado!"
```
