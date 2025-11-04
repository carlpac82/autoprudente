# ⚡ QUICK FIX - SQL Direto no Render

## 🚀 SOLUÇÃO RÁPIDA (Copiar e Colar)

### 1. No Render Shell, executar:

```bash
psql $DATABASE_URL
```

### 2. Copiar e colar este SQL:

```sql
-- Adicionar colunas faltantes (uma de cada vez)
ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mobile TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture_path TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS enabled INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id TEXT;
```

### 3. Verificar se funcionou:

```sql
\d users
```

Deve mostrar todas as colunas, incluindo `enabled`.

### 4. Sair do psql:

```sql
\q
```

### 5. Reiniciar o serviço:

No Dashboard do Render:
- Manual Deploy → Deploy latest commit

---

## ✅ RESULTADO ESPERADO

Depois de executar o SQL, os logs devem mostrar:

```
✅ Default users ready (admin/admin)
```

SEM erros de:
```
❌ column "enabled" of relation "users" does not exist
```

---

## 📋 SE DER ERRO "column already exists"

**Ignorar!** Significa que a coluna já existe. Continuar com as outras.

---

## 🎯 COMANDOS COMPLETOS (Copiar Tudo)

```bash
# 1. Conectar ao PostgreSQL
psql $DATABASE_URL

# 2. Executar SQL (copiar tudo de uma vez)
ALTER TABLE users ADD COLUMN IF NOT EXISTS first_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS mobile TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture_path TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS enabled INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id TEXT;

# 3. Verificar
\d users

# 4. Sair
\q
```

---

**Copia os comandos acima e cola no Render Shell!** ⚡
