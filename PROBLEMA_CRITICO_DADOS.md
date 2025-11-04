# 🚨 PROBLEMA CRÍTICO: Perda de Configurações após Deploy

**Problema:** Quando fazes alterações no Windsurf e deploy, todas as parametrizações (automated prices, etc.) desaparecem no Render.

**Causa:** Bases de dados SEPARADAS sem sincronização!

---

## 🔍 CAUSA RAIZ

### Arquitetura Atual:

```
┌─────────────────────────┐          ┌─────────────────────────┐
│  WINDSURF (Local)       │          │  RENDER (Produção)      │
│                         │          │                         │
│  SQLite (data.db)       │   ❌     │  PostgreSQL             │
│  - 21 automated prices  │  SYNC    │  - Configurações prod   │
│  - Tuas configurações   │          │  - Dados reais          │
└─────────────────────────┘          └─────────────────────────┘
```

**O que acontece:**
1. Fazes configurações no **Local** (SQLite)
2. Fazes commit e deploy
3. **Código** atualiza no Render ✅
4. **Dados** NÃO atualizam ❌
5. Render continua a usar PostgreSQL (sem tuas configurações)
6. Parece que as configurações "desapareceram"

**Realidade:**
- Configurações locais estão em `data.db` (SQLite)
- Configurações produção estão em PostgreSQL (Render)
- São **bases de dados diferentes**!

---

## ❌ PROBLEMAS

### 1. Dados Não Sincronizam

**Tabelas afetadas:**
- `price_automation_settings` (21 registos local, ? no Render)
- `automated_price_rules` (regras de automação)
- `vehicle_photos` (fotos)
- `vehicle_name_overrides` (nomes editados)
- `pricing_strategies` (estratégias)
- `car_groups` (grupos de carros)
- Todas as outras tabelas!

### 2. Configurações Locais ≠ Produção

**Exemplo:**
```
Local (Windsurf):
- Automated Prices: 21 configurações
- Vehicle Photos: 340 fotos
- Car Groups: 22 grupos

Render (Produção):
- Automated Prices: ??? (diferentes!)
- Vehicle Photos: ??? (diferentes!)
- Car Groups: ??? (diferentes!)
```

### 3. Trabalho Duplicado

- Configuras no local → Não aparece no Render
- Configuras no Render → Não aparece no local
- Tens que configurar DUAS VEZES!

---

## ✅ SOLUÇÕES

### Opção 1: Usar APENAS Render (Recomendado)

**Fazer TODAS as configurações diretamente no Render:**

✅ **Vantagens:**
- Configurações persistem sempre
- Não há perda de dados
- Dados de produção são a fonte da verdade

❌ **Desvantagens:**
- Não podes testar configurações localmente
- Cada mudança tem que ser no Render

**Como fazer:**
1. Acede ao Render: https://carrental-api-5f8q.onrender.com/
2. Faz TODAS as configurações lá
3. Local só para desenvolvimento de código
4. Deploy só atualiza código, não dados

---

### Opção 2: Sincronização Manual (Atual)

**Usar script `sync_databases.py` para sincronizar:**

```bash
# Sincronizar Render → Local
python3 sync_databases.py
# Escolher opção 4: Sincronizar Render → Local

# Sincronizar Local → Render
python3 sync_databases.py
# Escolher opção 5: Sincronizar Local → Render
```

✅ **Vantagens:**
- Podes trabalhar localmente
- Sincronizas quando quiseres

❌ **Desvantagens:**
- Manual (tens que lembrar)
- Pode haver conflitos
- Risco de sobrescrever dados

---

### Opção 3: PostgreSQL Local (Avançado)

**Usar PostgreSQL também no local:**

```bash
# 1. Instalar PostgreSQL
brew install postgresql@14

# 2. Criar base de dados local
createdb rental_tracker_dev

# 3. Configurar .env
DATABASE_URL=postgresql://localhost/rental_tracker_dev

# 4. Sincronizar dados do Render
pg_dump $RENDER_DATABASE_URL | psql rental_tracker_dev
```

✅ **Vantagens:**
- Ambiente local idêntico à produção
- Podes testar com dados reais
- Sincronização via pg_dump/pg_restore

❌ **Desvantagens:**
- Mais complexo
- Requer PostgreSQL instalado
- Mais lento que SQLite

---

### Opção 4: Sincronização Automática (Futuro)

**Implementar sincronização automática:**

```python
# Ao fazer deploy, sincronizar dados automaticamente
@app.on_event("startup")
async def sync_on_startup():
    if USE_POSTGRES:
        # Estamos no Render, não fazer nada
        pass
    else:
        # Estamos no local, sincronizar do Render
        sync_from_render()
```

✅ **Vantagens:**
- Automático
- Sempre sincronizado

❌ **Desvantagens:**
- Complexo de implementar
- Pode haver conflitos
- Requer lógica de merge

---

## 🎯 RECOMENDAÇÃO IMEDIATA

### Para JÁ: Usar APENAS Render

**Passo a passo:**

1. **Fazer TODAS as configurações no Render:**
   - Acede: https://carrental-api-5f8q.onrender.com/
   - Configura Automated Prices
   - Configura Vehicle Groups
   - Upload de fotos
   - Etc.

2. **Local APENAS para desenvolvimento:**
   - Escrever código
   - Testar funcionalidades
   - Debug

3. **Deploy APENAS atualiza código:**
   - Não toca em dados
   - Configurações do Render permanecem

4. **Se precisares dos dados localmente:**
   ```bash
   python3 sync_databases.py
   # Opção 4: Sincronizar Render → Local
   ```

---

## 📋 CHECKLIST

### Configurações a Fazer no Render:

- [ ] Automated Prices (todas as regras)
- [ ] Vehicle Groups (todos os grupos)
- [ ] Vehicle Photos (todas as fotos)
- [ ] Vehicle Name Overrides (nomes editados)
- [ ] Pricing Strategies (estratégias)
- [ ] User Settings (configurações)
- [ ] Notification Rules (se usares)

### Workflow Correto:

1. **Desenvolvimento de código:**
   - ✅ Fazer no Windsurf (local)
   - ✅ Testar localmente
   - ✅ Commit e deploy

2. **Configurações e dados:**
   - ✅ Fazer no Render (produção)
   - ❌ NÃO fazer no local
   - ❌ NÃO esperar que sincronizem

---

## 🔄 SINCRONIZAÇÃO FUTURA

### Quando Implementar:

**Opção A: Backup/Restore Manual**
```bash
# Backup do Render
python3 sync_databases.py → Opção 1

# Restore no Local
python3 sync_databases.py → Opção 4
```

**Opção B: PostgreSQL Local**
```bash
# Sincronizar dados
pg_dump $RENDER_URL | psql local_db
```

**Opção C: Sincronização Automática**
- Implementar webhook no Render
- Notifica local quando há mudanças
- Sincroniza automaticamente

---

## 📊 COMPARAÇÃO

| Aspecto | Local (SQLite) | Render (PostgreSQL) |
|---------|----------------|---------------------|
| **Dados** | Teste/Dev | Produção |
| **Persistência** | Temporária | Permanente |
| **Configurações** | ❌ Não usar | ✅ Usar aqui |
| **Código** | ✅ Desenvolver | ✅ Deploy |
| **Sincronização** | Manual | - |

---

## ✅ SOLUÇÃO APLICADA

### Agora:

1. ✅ Documentação criada
2. ✅ Script de sincronização existe (`sync_databases.py`)
3. ⏳ Aguarda decisão: qual opção usar?

### Recomendação:

**Usar APENAS Render para configurações!**

- Simples
- Sem risco de perda
- Dados sempre corretos
- Workflow claro

---

**Data:** 4 de Novembro de 2025, 22:05  
**Status:** PROBLEMA IDENTIFICADO  
**Próximo:** Decidir qual solução implementar
