# 🔧 Diagnóstico e Correção: Auto-Save ID=0

## 🐛 Problema Identificado

**Sintomas**:
```
[Log] Automated price history saved to PostgreSQL: ID=0, Month=2025-12, Prices=56
```

**Causa Provável**:
A tabela `automated_search_history` foi criada com `INTEGER PRIMARY KEY AUTOINCREMENT` (sintaxe SQLite), mas o PostgreSQL não reconhece `AUTOINCREMENT` e não gera IDs automaticamente. Resultado: `RETURNING id` retorna `0` ou `NULL`.

---

## 📋 Passo 1: Verificar Estrutura da Tabela

### Endpoint de Debug

Aceder (após login): 
```
https://carrental-api-5f8q.onrender.com/api/automated-search/debug-table-structure
```

**Esperado (INCORRETO)**:
```json
{
  "ok": true,
  "database_type": "PostgreSQL",
  "table_exists": true,
  "columns": [
    {
      "name": "id",
      "type": "integer",
      "default": null,  // ❌ NULL = SEM AUTO-INCREMENT!
      "nullable": "NO"
    },
    ...
  ]
}
```

**Esperado (CORRETO)**:
```json
{
  "ok": true,
  "database_type": "PostgreSQL",
  "table_exists": true,
  "columns": [
    {
      "name": "id",
      "type": "integer",
      "default": "nextval('automated_search_history_id_seq'::regclass)",  // ✅ SERIAL!
      "nullable": "NO"
    },
    ...
  ]
}
```

---

## 📋 Passo 2: Verificar Logs do Render

Após deploy (commit `c11bac4`), editar um preço e ver logs:

**Logs esperados**:
```
[INFO] [INSERT-DEBUG] PostgreSQL INSERT returned ID: 123  // ✅ ID > 0
```

**OU (se colunas faltam)**:
```
[WARNING] [FALLBACK-1] pickup_date or supplier_data column not found...
[INFO] [INSERT-DEBUG] Fallback 1 returned ID: 123  // ✅ Ainda deve funcionar
```

**OU (problema crítico)**:
```
[WARNING] [FALLBACK-2] supplier_data column also not found...
[INFO] [INSERT-DEBUG] Fallback 2 returned ID: 0  // ❌ PROBLEMA!
```

---

## 🔧 Passo 3: Corrigir Estrutura da Tabela

### Opção A: Migration Script (Recomendado)

Script criado: `fix_automated_search_history_table.py`

**Como usar**:

1. **Aceder ao servidor via SSH/console** (se possível no Render)
2. **Definir DATABASE_URL**:
   ```bash
   export DATABASE_URL="postgresql://..."
   ```
3. **Executar migration**:
   ```bash
   python fix_automated_search_history_table.py
   ```

**O que faz**:
- ✅ Verifica se tabela existe
- ✅ Adiciona coluna `supplier_data` (JSONB) se não existir
- ✅ Adiciona coluna `pickup_date` (DATE) se não existir
- ✅ Verifica se `id` é SERIAL (auto-increment)

**Limitação**: Não consegue converter `INTEGER` → `SERIAL` automaticamente (requer DROP/RECREATE)

---

### Opção B: SQL Manual (via Render Console)

**Se a coluna `id` NÃO for SERIAL**, executar:

```sql
-- Verificar estrutura atual
\d automated_search_history

-- Se id não tem default (nextval), fazer conversão:
-- ATENÇÃO: Requer backup da tabela!

-- 1. Criar sequence
CREATE SEQUENCE IF NOT EXISTS automated_search_history_id_seq;

-- 2. Definir sequence ownership
ALTER SEQUENCE automated_search_history_id_seq OWNED BY automated_search_history.id;

-- 3. Sincronizar sequence com max ID
SELECT setval('automated_search_history_id_seq', COALESCE(MAX(id), 1)) FROM automated_search_history;

-- 4. Definir default para a coluna id
ALTER TABLE automated_search_history 
ALTER COLUMN id SET DEFAULT nextval('automated_search_history_id_seq'::regclass);

-- 5. Verificar
\d automated_search_history
-- Deve mostrar: id | integer | not null default nextval('automated_search_history_id_seq'::regclass)
```

---

### Opção C: Adicionar Colunas Faltantes (se migration falhar)

```sql
-- Adicionar supplier_data (se não existir)
ALTER TABLE automated_search_history 
ADD COLUMN IF NOT EXISTS supplier_data JSONB;

-- Adicionar pickup_date (se não existir)
ALTER TABLE automated_search_history 
ADD COLUMN IF NOT EXISTS pickup_date DATE;

-- Verificar
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'automated_search_history';
```

---

## 🧪 Passo 4: Testar Auto-Save

1. ✅ **Aceder** à página de Automated Prices
2. ✅ **Fazer pesquisa** para Dezembro 2025 (Aeroporto de Faro)
3. ✅ **Editar preço** em um card (ex: M1 / 31 dias → 1399.21€)
4. ✅ **Aguardar auto-save** (~2 segundos)
5. ✅ **Verificar logs** no console do browser:
   ```
   [AUTO-SAVE] ✅ Saved 56 prices automatically
   Automated price history saved to PostgreSQL: ID=123  // ✅ ID > 0!
   ```
6. ✅ **Recarregar página** e **fazer mesma pesquisa**
7. ✅ **Verificar** se o preço editado está presente (1399.21€)

---

## 📊 Diagnóstico dos Logs

### Cenário 1: ID > 0 ✅
```
[INFO] [INSERT-DEBUG] PostgreSQL INSERT returned ID: 123
Automated price history saved to PostgreSQL: ID=123
```
**✅ TUDO OK! Auto-save funciona corretamente.**

---

### Cenário 2: Fallback mas ID > 0 ✅
```
[WARNING] [FALLBACK-1] pickup_date or supplier_data column not found...
[INFO] [INSERT-DEBUG] Fallback 1 returned ID: 123
```
**⚠️  Funciona, mas faltam colunas. Execute migration para adicionar.**

---

### Cenário 3: ID = 0 ❌
```
[INFO] [INSERT-DEBUG] Fallback 2 returned ID: 0
```
**❌ PROBLEMA CRÍTICO! A coluna `id` não é SERIAL. Execute Opção B (SQL Manual).**

---

### Cenário 4: Erro de INSERT ❌
```
[ERROR] ❌ Error saving automated search: ...
```
**❌ Erro no INSERT. Verificar traceback nos logs do Render.**

---

## 🔍 Como Verificar Se Preços Estão Guardados

### Via API:
```
GET https://carrental-api-5f8q.onrender.com/api/automated-search/history?months=3&location=Aeroporto de Faro
```

**Esperado**:
```json
{
  "ok": true,
  "history": {
    "2025-12": {
      "automated": [
        {
          "id": 123,  // ✅ ID válido
          "prices": {
            "M1": { "31": 1399.21 }  // ✅ Preço editado guardado!
          }
        }
      ]
    }
  }
}
```

---

## ⚠️ Outros Erros Relacionados

### Erro 1: "Missing required fields" (AI Adjustment)
```
[Error] ❌ Failed to save AI adjustment: "Missing required fields"
```

**Causa**: Endpoint `/api/ai/save-adjustment` espera campos específicos.

**Solução**: Ver logs do backend para identificar campos em falta.

---

### Erro 2: "column period_start does not exist" (Export History)
```
[Warning] Failed to save export to history: 
"column \"period_start\" of relation \"export_history\" does not exist"
```

**Causa**: Tabela `export_history` não tem coluna `period_start`.

**Solução**: Adicionar coluna:
```sql
ALTER TABLE export_history ADD COLUMN IF NOT EXISTS period_start DATE;
ALTER TABLE export_history ADD COLUMN IF NOT EXISTS period_end DATE;
```

---

## 📝 Resumo das Correções

| Problema | Solução | Prioridade |
|----------|---------|------------|
| ID=0 no auto-save | Converter `id` para SERIAL | 🔴 Alta |
| Coluna `supplier_data` faltando | Migration ou ALTER TABLE | 🟡 Média |
| Coluna `pickup_date` faltando | Migration ou ALTER TABLE | 🟡 Média |
| Coluna `period_start` faltando | ALTER TABLE export_history | 🟢 Baixa |

---

## 🚀 Próximos Passos

1. ⏰ **Aguardar deploy** do commit `c11bac4` (~5 min)
2. 🔍 **Verificar estrutura** via `/api/automated-search/debug-table-structure`
3. 📋 **Ver logs** do Render ao editar preços
4. 🔧 **Executar correção** conforme diagnóstico
5. ✅ **Testar** auto-save novamente

---

**Status Atual**: ✅ Deploy em progresso (commit `c11bac4`)  
**Última atualização**: 2025-11-20 12:30 UTC
