# Correção de Erros de Schema PostgreSQL

## ✅ CORRIGIDO: automated_search_history

**Erro:**
```
ERROR: relation "automated_search_history" does not exist
```

**Solução Aplicada:**
- ✅ Criado endpoint `/setup-automated-search-history` para criar tabela manualmente
- ✅ GET endpoint agora cria tabela automaticamente se não existir
- ✅ POST endpoint também cria tabela automaticamente

**Status:** RESOLVIDO no commit `9259a44`

---

## ⚠️ ERROS PENDENTES

Os seguintes erros ainda aparecem nos logs e precisam ser corrigidos:

### 1. **pricing_strategies** - Coluna "config" não existe

**Erro:**
```
ERROR: column "config" does not exist
LINE 1: SELECT location, grupo, month, day, priority, config FROM pr...
```

**Endpoint Afetado:**
- `GET /api/price-automation/strategies/load`

**Schema Atual (SQLite):**
```sql
CREATE TABLE pricing_strategies (
    location TEXT,
    grupo TEXT,
    month TEXT,
    day INTEGER,
    priority INTEGER,
    rule_type TEXT,
    rule_params TEXT,
    -- ❌ SEM coluna "config"
    PRIMARY KEY (location, grupo, month, day, priority)
)
```

**Solução Necessária:**
Opção 1 - Adicionar coluna `config`:
```sql
ALTER TABLE pricing_strategies ADD COLUMN config TEXT;
```

Opção 2 - Modificar query para não usar `config`:
```python
# Remover "config" da query
cur.execute("""
    SELECT location, grupo, month, day, priority, rule_type, rule_params 
    FROM pricing_strategies 
    ORDER BY location, grupo, month, day, priority
""")
```

---

### 2. **automated_price_rules** - Coluna "config" não existe

**Erro:**
```
ERROR: column "config" does not exist
LINE 1: SELECT location, grupo, month, day, config FROM automated_pr...
```

**Endpoint Afetado:**
- `GET /api/price-automation/rules/load`

**Schema Atual (SQLite):**
```sql
CREATE TABLE automated_price_rules (
    location TEXT,
    grupo TEXT,
    month TEXT,
    day INTEGER,
    min_price REAL,
    max_price REAL,
    margin_percent REAL,
    rounding_mode TEXT,
    -- ❌ SEM coluna "config"
    PRIMARY KEY (location, grupo, month, day)
)
```

**Solução Necessária:**
Opção 1 - Adicionar coluna:
```sql
ALTER TABLE automated_price_rules ADD COLUMN config TEXT;
```

Opção 2 - Modificar query:
```python
cur.execute("""
    SELECT location, grupo, month, day, min_price, max_price, 
           margin_percent, rounding_mode 
    FROM automated_price_rules 
    ORDER BY location, grupo, month, day
""")
```

---

### 3. **ai_learning_data** - Coluna "location" não existe

**Erro:**
```
ERROR: column "location" does not exist
LINE 1: SELECT grupo, days, location, original_price, new_price, tim...
```

**Endpoint Afetado:**
- `GET /api/ai/learning/load`

**Schema Atual (SQLite):**
```sql
CREATE TABLE ai_learning_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo TEXT NOT NULL,
    days INTEGER NOT NULL,
    original_price REAL NOT NULL,
    new_price REAL NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    competitive_data TEXT
    -- ❌ SEM coluna "location"
)
```

**Solução Necessária:**
Opção 1 - Adicionar coluna:
```sql
ALTER TABLE ai_learning_data ADD COLUMN location TEXT DEFAULT 'Albufeira';
```

Opção 2 - Modificar query:
```python
cur.execute("""
    SELECT grupo, days, original_price, new_price, timestamp, reason 
    FROM ai_learning_data 
    WHERE 1=1 
    ORDER BY timestamp DESC 
    LIMIT %s
""", (limit,))
```

---

### 4. **suppliers** - Tabela não existe

**Erro:**
```
ERROR: relation "suppliers" does not exist
LINE 1: SELECT DISTINCT logo_path FROM suppliers WHERE logo_path IS ...
```

**Endpoint Afetado:**
- `GET /` (index page)

**Solução Necessária:**
Criar tabela `suppliers`:
```sql
CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logo_path TEXT,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir fornecedores conhecidos
INSERT INTO suppliers (code, name, logo_path, active) VALUES
('AUP', 'AutoPrudente', '/static/logos/logo_AUP.png', 1),
('HER', 'Hertz', '/static/logos/logo_HER.png', 1),
('SXT', 'Sixt', '/static/logos/logo_SXT.png', 1),
('ECR', 'Europcar', '/static/logos/logo_ECR.png.avif', 1),
('CEN', 'Centauro', '/static/logos/logo_CEN.png.avif', 1),
('TAN', 'Tangerine', '/static/logos/logo_TAN.png', 1),
('BGX', 'Budget', '/static/logos/logo_BGX.png.avif', 1),
('OKR', 'OK Rent a Car', '/static/logos/logo_OKR.png', 1),
('ICT', 'InterRent', '/static/logos/logo_ICT.png', 1),
('YNO', 'YesNo', '/static/logos/logo_YNO.png.avif', 1),
('THR', 'Thrifty', '/static/logos/logo_THR.png.avif', 1),
('SUR', 'Surprice', '/static/logos/logo_SUR.png', 1)
ON CONFLICT (code) DO NOTHING;
```

---

## 📋 PLANO DE CORREÇÃO

### Prioridade ALTA (Quebram funcionalidades principais)

1. **suppliers** → Impede carregar página inicial
   - Criar endpoint `/setup-suppliers-table`
   - Adicionar lista de fornecedores

2. **pricing_strategies** → Impede carregar estratégias de pricing
   - Modificar query para não usar coluna `config`
   - OU adicionar coluna `config`

3. **automated_price_rules** → Impede carregar regras de automação
   - Modificar query para não usar coluna `config`
   - OU adicionar coluna `config`

### Prioridade MÉDIA

4. **ai_learning_data** → Impede AI insights
   - Adicionar coluna `location`
   - OU modificar query para não usar `location`

---

## 🔧 IMPLEMENTAÇÃO RECOMENDADA

### Criar Endpoint Setup Único

```python
@app.get("/setup-missing-tables")
async def setup_missing_tables():
    """Create all missing tables and add missing columns"""
    try:
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = hasattr(conn, 'cursor')
                
                if is_postgres:
                    with conn.cursor() as cur:
                        # 1. Create suppliers table
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS suppliers (
                                id SERIAL PRIMARY KEY,
                                code TEXT UNIQUE NOT NULL,
                                name TEXT NOT NULL,
                                logo_path TEXT,
                                active INTEGER DEFAULT 1,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
                        
                        # Insert default suppliers
                        suppliers_data = [
                            ('AUP', 'AutoPrudente', '/static/logos/logo_AUP.png'),
                            ('HER', 'Hertz', '/static/logos/logo_HER.png'),
                            ('SXT', 'Sixt', '/static/logos/logo_SXT.png'),
                            # ... outros
                        ]
                        
                        for code, name, logo in suppliers_data:
                            cur.execute("""
                                INSERT INTO suppliers (code, name, logo_path, active)
                                VALUES (%s, %s, %s, 1)
                                ON CONFLICT (code) DO NOTHING
                            """, (code, name, logo))
                        
                        # 2. Add missing columns (se não existirem)
                        try:
                            cur.execute("ALTER TABLE pricing_strategies ADD COLUMN config TEXT")
                        except:
                            pass  # Coluna já existe
                        
                        try:
                            cur.execute("ALTER TABLE automated_price_rules ADD COLUMN config TEXT")
                        except:
                            pass
                        
                        try:
                            cur.execute("ALTER TABLE ai_learning_data ADD COLUMN location TEXT DEFAULT 'Albufeira'")
                        except:
                            pass
                    
                    conn.commit()
                    return {"ok": True, "message": "All missing tables/columns created"}
                    
            finally:
                conn.close()
                
    except Exception as e:
        logging.error(f"Error in setup: {str(e)}")
        return {"ok": False, "error": str(e)}
```

---

## 🚀 EXECUÇÃO

Após deploy do código acima:

1. Abrir browser: `https://your-app.onrender.com/setup-missing-tables`
2. Verificar resposta: `{"ok": true, "message": "All missing tables/columns created"}`
3. Recarregar páginas afetadas
4. Verificar logs - erros devem desaparecer

---

## 📊 STATUS ATUAL

| Tabela/Coluna | Erro | Status | Prioridade |
|---------------|------|--------|-----------|
| `automated_search_history` | Tabela não existe | ✅ CORRIGIDO | Alta |
| `suppliers` | Tabela não existe | ⚠️ PENDENTE | Alta |
| `pricing_strategies.config` | Coluna não existe | ⚠️ PENDENTE | Alta |
| `automated_price_rules.config` | Coluna não existe | ⚠️ PENDENTE | Alta |
| `ai_learning_data.location` | Coluna não existe | ⚠️ PENDENTE | Média |

---

## ⚡ SOLUÇÃO RÁPIDA (Alternativa)

Se não quiser adicionar colunas, modificar queries:

```python
# pricing_strategies - REMOVER "config"
@app.get("/api/price-automation/strategies/load")
async def load_strategies():
    # ANTES:
    # cur.execute("SELECT location, grupo, month, day, priority, config FROM ...")
    
    # DEPOIS:
    cur.execute("""
        SELECT location, grupo, month, day, priority, rule_type, rule_params 
        FROM pricing_strategies 
        ORDER BY location, grupo, month, day, priority
    """)

# automated_price_rules - REMOVER "config"
@app.get("/api/price-automation/rules/load")
async def load_rules():
    # ANTES:
    # cur.execute("SELECT location, grupo, month, day, config FROM ...")
    
    # DEPOIS:
    cur.execute("""
        SELECT location, grupo, month, day, min_price, max_price, 
               margin_percent, rounding_mode 
        FROM automated_price_rules 
        ORDER BY location, grupo, month, day
    """)

# ai_learning_data - REMOVER "location"
@app.get("/api/ai/learning/load")
async def load_learning():
    # ANTES:
    # cur.execute("SELECT grupo, days, location, original_price ... FROM ...")
    
    # DEPOIS:
    cur.execute("""
        SELECT grupo, days, original_price, new_price, timestamp, reason 
        FROM ai_learning_data 
        ORDER BY timestamp DESC 
        LIMIT %s
    """, (limit,))
```

Esta solução é **mais rápida** mas perde funcionalidade (não terá config/location nos dados).

---

## 📝 NOTAS

- Todos os erros são **não-críticos** - o sistema continua funcionando
- Apenas algumas features específicas estão quebradas
- A solução completa requer **adicionar colunas** ou **modificar queries**
- Recomendo criar endpoint `/setup-missing-tables` para fazer tudo de uma vez
