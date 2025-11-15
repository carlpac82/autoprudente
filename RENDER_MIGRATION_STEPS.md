# 🚀 Passos para Migração no Render - WhatsApp Contacts

## ✅ Deploy Completado!

Agora precisas executar o script de migração para criar as tabelas novas no PostgreSQL.

---

## 📋 Passo-a-Passo (5 minutos)

### 1️⃣ Aceder ao Render Dashboard

🔗 **URL:** https://dashboard.render.com/web/srv-cvi90nrcm5oc7390hg3g

- Login na conta Render
- Vai para o serviço `carrental-api`

---

### 2️⃣ Abrir o Shell

No topo da página do serviço, vais ver botões:
- **Manual Deploy**
- **Shell** ← CLICA AQUI
- **Logs**

Clica em **Shell** - vai abrir um terminal no browser.

---

### 3️⃣ Verificar se o ficheiro existe

No Shell do Render, escreve:

```bash
ls -la create_whatsapp_contacts_table.py
```

**Resultado esperado:**
```
-rw-r--r-- 1 render render 3456 Nov 15 17:23 create_whatsapp_contacts_table.py
```

✅ Se apareceu → Continua  
❌ Se "No such file" → Avisa-me

---

### 4️⃣ Executar o Script de Migração

No Shell, escreve:

```bash
python create_whatsapp_contacts_table.py
```

**Resultado esperado:**

```
🔌 Conectando ao PostgreSQL...
✅ Conectado com sucesso!

🔍 Verificando se tabela whatsapp_contacts existe...
❌ Tabela whatsapp_contacts NÃO EXISTE. Criando...
✅ Tabela whatsapp_contacts criada com sucesso!

🔍 Verificando tabela whatsapp_conversations...
❌ Coluna contact_id NÃO EXISTE em whatsapp_conversations. Adicionando...
✅ Coluna contact_id adicionada!

🎉 TUDO PRONTO! Base de dados atualizada com sucesso!
```

---

### 5️⃣ Verificar que tudo correu bem

Ainda no Shell, vamos confirmar que as tabelas foram criadas:

```bash
python -c "
import os
import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

# Verificar whatsapp_contacts
cur.execute(\"SELECT COUNT(*) FROM whatsapp_contacts\")
contacts = cur.fetchone()[0]
print(f'✅ whatsapp_contacts: {contacts} contactos')

# Verificar contact_id em whatsapp_conversations
cur.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name='whatsapp_conversations' AND column_name='contact_id'\")
has_col = cur.fetchone()
print(f'✅ contact_id existe: {\"SIM\" if has_col else \"NAO\"}')

cur.close()
conn.close()
"
```

**Resultado esperado:**
```
✅ whatsapp_contacts: 0 contactos
✅ contact_id existe: SIM
```

(0 contactos é normal se ainda não tinhas conversas guardadas)

---

## 🧪 Testar no Dashboard

Agora vai ao WhatsApp Dashboard testar:

🔗 https://carrental-api-5f8q.onrender.com/whatsapp/dashboard

### Tab Contactos:
- [ ] Lista aparece vazia ou com contactos migrados
- [ ] Adicionar novo contacto funciona
- [ ] Mostra "X conversas" em vez de badge de não lidas

### Tab Conversas:
- [ ] Lista de conversas funciona
- [ ] Adicionar contacto cria conversa automaticamente
- [ ] **TESTE CRÍTICO:** Eliminar conversa → Contacto MANTÉM-SE na tab Contactos ✅

---

## ❌ Problemas Possíveis

### Erro: "column contact_id already exists"

**Significa:** Script já foi executado antes  
**Solução:** Tudo OK! Podes ignorar

### Erro: "permission denied"

**Causa:** DATABASE_URL não configurado  
**Solução:** Verificar variáveis de ambiente no Render

### Erro: "ModuleNotFoundError: No module named 'psycopg2'"

**Causa:** Dependências não instaladas  
**Solução:** Verificar que `requirements.txt` tem `psycopg2-binary`

---

## 📊 O que o Script Faz

```
ANTES:
whatsapp_conversations
├── id
├── name              ← Dados do contacto
├── phone_number      ← Dados do contacto
├── has_whatsapp      ← Dados do contacto
├── profile_picture   ← Dados do contacto
├── last_message_at   ← Dados da conversa
└── unread_count      ← Dados da conversa

DEPOIS:
whatsapp_contacts (NOVO!)
├── id
├── name
├── phone_number
├── has_whatsapp
└── profile_picture_url

whatsapp_conversations (MODIFICADO)
├── id
├── contact_id        ← NOVO! Link para whatsapp_contacts
├── phone_number
├── last_message_at
└── unread_count
```

---

## ✅ Checklist Final

Após migração, verifica:

- [ ] Script executou sem erros
- [ ] Tabela `whatsapp_contacts` criada
- [ ] Coluna `contact_id` existe em `whatsapp_conversations`
- [ ] Dashboard WhatsApp abre sem erros
- [ ] Tab Contactos funciona
- [ ] Tab Conversas funciona
- [ ] Eliminar conversa NÃO elimina contacto ✅

---

## 🆘 Se algo correr mal

1. **Copia o erro completo** do Shell
2. **Avisa-me** - posso ajudar a resolver
3. **NÃO re-executar** o script múltiplas vezes

---

## 📞 Próximo Passo

Após executar o script com sucesso, avisa-me e vamos testar juntos no dashboard!

✨ Boa sorte com a migração!
