# 🚧 TODO: Separar Contactos de Conversas

## ✅ FEITO

### 1. Schema PostgreSQL Atualizado
```sql
-- Nova tabela
CREATE TABLE whatsapp_contacts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL UNIQUE,
    has_whatsapp BOOLEAN,
    profile_picture_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela modificada
CREATE TABLE whatsapp_conversations (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES whatsapp_contacts(id),  -- NOVO
    phone_number TEXT NOT NULL UNIQUE,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_preview TEXT,
    unread_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'open',
    assigned_to TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- REMOVIDO: name, has_whatsapp, profile_picture_url
);
```

---

## ⏳ PENDENTE

### 2. Schema SQLite Atualizado

Procurar em `main.py` por `else:` após o PostgreSQL e atualizar:

```python
# Linha ~5381 (aproximadamente)
else:  # SQLite
    con.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE,
            has_whatsapp INTEGER,
            profile_picture_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    con.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER,
            phone_number TEXT NOT NULL UNIQUE,
            last_message_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_message_preview TEXT,
            unread_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'open',
            assigned_to TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (contact_id) REFERENCES whatsapp_contacts(id)
        )
    """)
```

### 3. Endpoint `/api/whatsapp/contacts/add`

Modificar para adicionar APENAS à tabela `whatsapp_contacts`:

```python
@app.post("/api/whatsapp/contacts/add")
async def add_whatsapp_contact(request: Request):
    # ...
    
    # INSERT em whatsapp_contacts (não em whatsapp_conversations)
    if is_postgres:
        cur.execute("""
            INSERT INTO whatsapp_contacts (name, phone_number, has_whatsapp, profile_picture_url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (phone_number) DO UPDATE
            SET name = EXCLUDED.name,
                has_whatsapp = EXCLUDED.has_whatsapp,
                profile_picture_url = EXCLUDED.profile_picture_url
            RETURNING id
        """, (name, phone, has_whatsapp, profile_picture_url))
```

### 4. Endpoint `/api/whatsapp/conversations`

Modificar SELECT para fazer JOIN:

```python
@app.get("/api/whatsapp/conversations")
async def get_whatsapp_conversations(request: Request):
    # ...
    
    query = """
        SELECT c.id, ct.name, c.phone_number, c.last_message_at, c.last_message_preview,
               c.unread_count, c.status, c.assigned_to, ct.has_whatsapp, ct.profile_picture_url
        FROM whatsapp_conversations c
        LEFT JOIN whatsapp_contacts ct ON c.contact_id = ct.id
        ORDER BY COALESCE(c.last_message_at, c.created_at) DESC
    """
```

### 5. Webhook - Criar Conversa Automaticamente

Quando recebe mensagem, criar conversa se não existir:

```python
# 1. Verificar/criar contacto
INSERT INTO whatsapp_contacts (name, phone_number)
VALUES (%s, %s)
ON CONFLICT (phone_number) DO UPDATE SET name = EXCLUDED.name
RETURNING id

# 2. Verificar/criar conversa
INSERT INTO whatsapp_conversations (contact_id, phone_number)
VALUES (%s, %s)
ON CONFLICT (phone_number) DO NOTHING
RETURNING id
```

### 6. Endpoint DELETE Conversa

Modificar para NÃO eliminar contacto:

```python
@app.delete("/api/whatsapp/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    # DELETE apenas de whatsapp_conversations
    # NÃO delete de whatsapp_contacts
    DELETE FROM whatsapp_conversations WHERE id = %s
```

### 7. Endpoint DELETE Contacto (NOVO)

Criar endpoint para eliminar contacto:

```python
@app.delete("/api/whatsapp/contacts/{contact_id}")
async def delete_contact(contact_id: int):
    # Delete do contacto (conversas deletadas em cascata)
    DELETE FROM whatsapp_contacts WHERE id = %s
```

### 8. Frontend - Tab Contactos

Modificar para mostrar contactos (não conversas):

```javascript
async function loadContacts() {
    const response = await fetch('/api/whatsapp/contacts');  // Novo endpoint
    const data = await response.json();
    renderContacts(data.contacts);  // Não data.conversations
}
```

### 9. Frontend - Eliminar Conversa

NÃO deve eliminar contacto:

```javascript
async function deleteConversation(conversationId) {
    // DELETE /api/whatsapp/conversations/{id}
    // Contacto permanece na tab Contactos
}
```

### 10. Migração de Dados Existentes

Script para migrar dados antigos:

```sql
-- Copiar dados de conversations para contacts
INSERT INTO whatsapp_contacts (name, phone_number, has_whatsapp, profile_picture_url, created_at)
SELECT DISTINCT name, phone_number, has_whatsapp, profile_picture_url, created_at
FROM whatsapp_conversations
ON CONFLICT (phone_number) DO NOTHING;

-- Atualizar conversations com contact_id
UPDATE whatsapp_conversations c
SET contact_id = (
    SELECT ct.id FROM whatsapp_contacts ct WHERE ct.phone_number = c.phone_number
);
```

---

## 🎯 Resultado Esperado

### Comportamento Atual (Errado)
```
1. Adicionar contacto "João"
   → Cria whatsapp_conversations
   
2. Eliminar conversa com "João"
   → Elimina whatsapp_conversations
   → ❌ Contacto desaparece da lista
```

### Comportamento Novo (Correto)
```
1. Adicionar contacto "João"
   → Cria whatsapp_contacts ✅
   → NÃO cria conversa ainda
   
2. Receber mensagem de "João"
   → Cria whatsapp_conversations ✅
   → Associa a whatsapp_contacts
   
3. Eliminar conversa com "João"
   → Delete whatsapp_conversations ✅
   → ✅ Contacto permanece em whatsapp_contacts
   → ✅ Aparece na tab Contactos
   → ❌ NÃO aparece na tab Conversas
   
4. Eliminar contacto "João"
   → Delete whatsapp_contacts
   → Conversas eliminadas em cascata
```

---

## 📋 Checklist

- [x] Schema PostgreSQL - whatsapp_contacts
- [x] Schema PostgreSQL - whatsapp_conversations modificado
- [ ] Schema SQLite - whatsapp_contacts  
- [ ] Schema SQLite - whatsapp_conversations modificado
- [ ] Endpoint POST /api/whatsapp/contacts/add
- [ ] Endpoint GET /api/whatsapp/contacts (NOVO)
- [ ] Endpoint GET /api/whatsapp/conversations (modificar JOIN)
- [ ] Endpoint DELETE /api/whatsapp/conversations/:id (não delete contact)
- [ ] Endpoint DELETE /api/whatsapp/contacts/:id (NOVO)
- [ ] Webhook - criar conversa quando recebe mensagem
- [ ] Frontend - loadContacts() usar novo endpoint
- [ ] Frontend - renderContacts() mostrar apenas contacts
- [ ] Frontend - deleteConversation() não afetar contacts
- [ ] Script migração de dados

---

## 🚀 Prioridade

1. **URGENTE:** Schema SQLite (para desenvolvimento local funcionar)
2. **URGENTE:** Endpoint add contact (para não criar conversas vazias)
3. **URGENTE:** Query conversations com JOIN (para mostrar nome do contacto)
4. **MÉDIO:** Webhook criar conversa automaticamente
5. **MÉDIO:** Frontend separar tabs corretamente
6. **BAIXO:** Migração de dados (pode ser manual)
