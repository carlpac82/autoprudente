# 🔧 Fix Render PostgreSQL Schema

## ⚠️ PROBLEMA IDENTIFICADO

O PostgreSQL no Render tem schema desatualizado. A tabela `users` está faltando colunas:

```
❌ enabled
❌ created_at
❌ (possivelmente outras)
```

**Erro:**
```
column "enabled" of relation "users" does not exist
```

---

## ✅ SOLUÇÃO

### Opção 1: Executar Script no Render Shell (RECOMENDADO)

**1. Aceder ao Render Dashboard:**
```
https://dashboard.render.com
→ carrental_api (Web Service)
→ Shell (botão no canto superior direito)
```

**2. No Shell, executar:**
```bash
python3 fix_render_schema.py
```

**3. Resultado esperado:**
```
🔧 FIXING POSTGRESQL SCHEMA ON RENDER
============================================================
📊 Conectando ao PostgreSQL...
   Host: ...
   Database: ...

✅ Conectado!

📋 Verificando schema da tabela users...
   Colunas existentes: X

🔧 Adicionando colunas faltantes...
   Adicionando: enabled...
   ✅ enabled adicionada
   Adicionando: created_at...
   ✅ created_at adicionada
   ...

✅ Todas as colunas necessárias existem!
============================================================
✅ SCHEMA CORRIGIDO COM SUCESSO!
============================================================
```

**4. Reiniciar o serviço:**
```
Dashboard → Manual Deploy → Deploy latest commit
```

---

### Opção 2: SQL Direto (Alternativa)

**1. Aceder ao PostgreSQL:**

Via Render Shell:
```bash
psql $DATABASE_URL
```

**2. Executar SQL:**
```sql
-- Adicionar colunas faltantes
ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mobile TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture_path TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS enabled INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id TEXT UNIQUE;

-- Verificar
\d users
```

**3. Sair do psql:**
```sql
\q
```

---

## 🔍 VERIFICAR SE FUNCIONOU

**1. Ver logs do Render:**
```
Dashboard → Logs
```

**2. Procurar por:**
```
✅ Default users ready (admin/admin)
```

**3. SEM erros:**
```
❌ column "enabled" of relation "users" does not exist
```

---

## 📋 COLUNAS NECESSÁRIAS NA TABELA USERS

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT,              -- ⚠️ Pode estar faltando
    last_name TEXT,               -- ⚠️ Pode estar faltando
    email TEXT,                   -- ⚠️ Pode estar faltando
    mobile TEXT,                  -- ⚠️ Pode estar faltando
    profile_picture_path TEXT,    -- ⚠️ Pode estar faltando
    is_admin INTEGER DEFAULT 0,   -- ⚠️ Pode estar faltando
    enabled INTEGER DEFAULT 1,    -- ⚠️ Pode estar faltando
    created_at TEXT,              -- ⚠️ Pode estar faltando
    google_id TEXT UNIQUE         -- ⚠️ Pode estar faltando
);
```

---

## 🚨 SE O PROBLEMA PERSISTIR

### Opção Nuclear: Recriar Tabela Users

**⚠️ ATENÇÃO: Isto vai apagar todos os utilizadores!**

```sql
-- Backup primeiro (se tiver dados importantes)
CREATE TABLE users_backup AS SELECT * FROM users;

-- Apagar tabela antiga
DROP TABLE users;

-- Criar tabela nova com schema correto
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    mobile TEXT,
    profile_picture_path TEXT,
    is_admin INTEGER DEFAULT 0,
    enabled INTEGER DEFAULT 1,
    created_at TEXT,
    google_id TEXT UNIQUE
);

-- Restaurar dados (se necessário)
INSERT INTO users (id, username, password_hash)
SELECT id, username, password_hash FROM users_backup;
```

---

## 📞 TROUBLESHOOTING

### Erro: "psycopg2 não instalado"

**Solução:**
```bash
pip install psycopg2-binary
```

### Erro: "DATABASE_URL não encontrado"

**Solução:**
- Verificar se está no Render Shell
- Verificar se DATABASE_URL está configurado no Environment

### Erro: "column already exists"

**Solução:**
- Ignorar (coluna já existe)
- Script vai continuar com as outras

### Erro: "current transaction is aborted"

**Solução:**
- Script já trata isso
- Cada coluna é adicionada em transação separada

---

## ✅ DEPOIS DE CORRIGIR

**1. Verificar logs:**
```
✅ Default users ready (admin/admin)
```

**2. Testar login:**
```
https://carrental-api-5f8q.onrender.com
Username: admin
Password: admin
```

**3. Verificar funcionalidades:**
- ✅ Login funciona
- ✅ Scraping funciona
- ✅ Automated prices funciona

---

## 📋 CHECKLIST

- [ ] Aceder ao Render Shell
- [ ] Executar `python3 fix_render_schema.py`
- [ ] Verificar output (✅ SCHEMA CORRIGIDO)
- [ ] Reiniciar serviço (Manual Deploy)
- [ ] Verificar logs (sem erros)
- [ ] Testar login
- [ ] Confirmar funcionalidades

---

**🎯 Depois de executar o script, o erro vai desaparecer!**
