# ✅ FIX: Erro ao Guardar Veículos no Editor

## 🐛 Problema Reportado

**Erro 500** ao guardar veículos no Vehicle Editor:

```
Error: function datetime(unknown) does not exist
LINE 1: ...('ford s max (sem dados recentes)', 'ford s max', datetime('...
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

## 🔍 Análise do Problema

### Sintomas
- ❌ Editor de veículos não guarda alterações
- ❌ Erro 500 no endpoint `/api/vehicles/save`
- ❌ Erro menciona `datetime('now')` que é sintaxe **SQLite**
- ❌ Mas servidor usa **PostgreSQL** que não reconhece essa função

### Causa Raiz

**Detecção de tipo de BD falhando em produção:**

```python
# ❌ ANTES: Método menos robusto
is_postgres = con.__class__.__module__ == 'psycopg2.extensions'
```

Se a detecção retornasse `False` incorretamente:
- Código usaria sintaxe SQLite: `datetime('now')`
- PostgreSQL não reconhece esta função → **Erro 500**

### Sequência do Bug

1. **Utilizador edita veículo** no Vehicle Editor
2. **Frontend envia** para `/api/vehicles/save`
3. **Backend tenta detectar** tipo de BD
4. **Detecção falha** → assume SQLite
5. **Usa `datetime('now')`** na query
6. **PostgreSQL rejeita** → Erro 500
7. **Veículo não é guardado** ❌

## 🔧 Solução Implementada

### Fix 1: Detecção Mais Robusta

```python
# ✅ DEPOIS: Método mais robusto - dois checks
is_postgres = (
    con.__class__.__module__ == 'psycopg2.extensions' or 
    'psycopg2' in str(type(con))
)
```

**Benefícios:**
- ✅ Verifica módulo **E** tipo da conexão
- ✅ Funciona em diferentes ambientes
- ✅ Mais resiliente a mudanças de versão

### Fix 2: Logging para Debug

```python
logging.info(f"[VEHICLE-SAVE] DB type: {con.__class__.__module__}, is_postgres={is_postgres}")
```

**Permite verificar:**
- Tipo de conexão em produção
- Se detecção está a funcionar
- Identificar problemas futuros rapidamente

### Fix 3: Dois Endpoints Corrigidos

**1. `/api/vehicles/save`** (linha 16585)
- Usado pelo Vehicle Editor
- Guarda veículos e categorias

**2. `/api/vehicles/name-overrides`** (linha 20156)
- Usado para sobrescrever nomes
- Atualiza vehicle_name_overrides

## 📊 Código Antes vs Depois

### Antes ❌
```python
# Detecção simples
is_postgres = con.__class__.__module__ == 'psycopg2.extensions'

# Se falhar, usa SQLite syntax em PostgreSQL
if is_postgres:
    query = "... NOW() ..."
else:
    query = "... datetime('now') ..."  # ← ERRO!
```

### Depois ✅
```python
# Detecção dupla + logging
is_postgres = (
    con.__class__.__module__ == 'psycopg2.extensions' or 
    'psycopg2' in str(type(con))
)
logging.info(f"[VEHICLE-SAVE] DB type: {con.__class__.__module__}, is_postgres={is_postgres}")

# Sempre usa sintaxe correta
if is_postgres:
    query = "... NOW() ..."  # ✅ PostgreSQL
else:
    query = "... datetime('now') ..."  # ✅ SQLite
```

## 🚀 Deploy

**Commit:** a9f6034  
**Data:** 21 Nov 2025, 11:45 AM  
**Mensagem:** "fix: improve PostgreSQL detection in vehicle save endpoints"

**Ficheiros alterados:**
- `main.py` (+5, -3)

**Endpoints corrigidos:**
- ✅ `/api/vehicles/save`
- ✅ `/api/vehicles/name-overrides`

## 🎯 Como Testar (Após Deploy)

### Aguardar Deploy
```
ETA: 11:48-11:50 AM (3-5 minutos)
```

### Teste 1: Guardar Veículo
1. Vai ao **Admin → Vehicles Editor**
2. Clica num veículo (ex: "ford s max")
3. Edita o **Clean Name** ou **Category**
4. Clica **"Save"**
5. ✅ Deve guardar sem erro 500
6. ✅ Mensagem de sucesso aparece

### Teste 2: Verificar Logs
Nos logs do Render, deve aparecer:
```
[VEHICLE-SAVE] DB type: psycopg2.extensions, is_postgres=True
```

### Teste 3: Verificar BD
```sql
SELECT original_name, edited_name, updated_at 
FROM vehicle_name_overrides 
WHERE original_name LIKE '%ford s max%'
ORDER BY updated_at DESC 
LIMIT 5;
```

Deve mostrar:
- ✅ `updated_at` com timestamp recente
- ✅ `edited_name` com o nome editado

## 📝 Notas Técnicas

### PostgreSQL vs SQLite

| Função | PostgreSQL | SQLite |
|--------|------------|--------|
| **Data atual** | `NOW()` | `datetime('now')` |
| **Placeholder** | `%s` | `?` |
| **Serial** | `SERIAL` | `AUTOINCREMENT` |
| **JSONB** | Nativo | String |

### Outros Lugares com Detecção

Há **outras funções** no código que também fazem detecção de PostgreSQL. Se este fix resolver, devemos aplicar o mesmo padrão noutros lugares:

```bash
grep -n "is_postgres = con.__class__.__module__" main.py | wc -l
# → ~50+ ocorrências
```

**Para fazer depois:**
- Aplicar detecção melhorada globalmente
- Criar função helper `_is_postgres(con)`
- Refatorar todos os checks

## ⚠️ Possíveis Problemas

### Se Erro Persistir

**Opção 1: Verificar Logs**
```
Procurar por: [VEHICLE-SAVE] DB type:
```

**Opção 2: Testar Conexão**
```python
# No Python console do Render
from main import _db_connect
con = _db_connect()
print(con.__class__.__module__)
print(type(con))
```

**Opção 3: Forçar PostgreSQL**
```python
# Último recurso - hardcode temporário
is_postgres = True  # Force PostgreSQL in production
```

## 🎉 Resultado Esperado

| Ação | Antes | Depois |
|------|-------|--------|
| **Guardar veículo** | ❌ Erro 500 | ✅ Guardado com sucesso |
| **Mensagem** | "Error: datetime..." | "Vehicle saved successfully!" |
| **Base de dados** | ❌ Não atualiza | ✅ Atualiza com NOW() |
| **Logs** | Sem info | "DB type: psycopg2..." |

---

**Status:** ✅ DEPLOYED  
**Última atualização:** 21 Nov 2025, 11:45 AM  
**Commit:** a9f6034
