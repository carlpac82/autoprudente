# Database Schema Fix - automated_prices_history

## 🐛 Problemas Identificados

### 1. **ERRO CRÍTICO**: Coluna `auto_price` não existe
```
ERROR:root:PostgreSQL execute error: column "auto_price" of relation "automated_prices_history" does not exist
LINE 3: ...                   (location, grupo, pickup_date, auto_price...
```

**Causa**: A tabela `automated_prices_history` foi criada no PostgreSQL com um schema antigo que não incluía as colunas `auto_price` e `real_price`.

**Impacto**: 
- ❌ Falha ao salvar preços automatizados
- ❌ Relatórios diários não funcionam corretamente
- ❌ Histórico de preços não é persistido

---

### 2. **Aviso**: Coluna `token_expires_at` já existe
```
ERROR:root:PostgreSQL execute error: column "token_expires_at" of relation "whatsapp_config" already exists
```

**Causa**: Tentativa de adicionar coluna que já existe (comportamento esperado).

**Impacto**: 
- ⚠️ Apenas um aviso (não é erro crítico)
- ✅ O código já trata este caso com rollback automático

---

## ✅ Soluções Implementadas

### Solução 1: Script de Migração (Execução Única)

Criado script `fix_automated_prices_history.py` que:
- ✅ Verifica colunas existentes na tabela
- ✅ Adiciona `auto_price` (DOUBLE PRECISION) se não existir
- ✅ Adiciona `real_price` (DOUBLE PRECISION) se não existir
- ✅ Adiciona `source` (TEXT) se não existir
- ✅ Mostra schema final da tabela

**Como executar**:

#### Opção A: Localmente (com acesso ao DATABASE_URL)
```bash
export DATABASE_URL='postgresql://user:password@host:port/database'
python fix_automated_prices_history.py
```

#### Opção B: No Render Shell
```bash
# 1. Aceder ao Shell do Render
# 2. O DATABASE_URL já está configurado automaticamente
python fix_automated_prices_history.py
```

#### Opção C: Diretamente no PostgreSQL
```sql
-- Se preferir executar SQL diretamente
ALTER TABLE automated_prices_history 
ADD COLUMN IF NOT EXISTS auto_price DOUBLE PRECISION;

ALTER TABLE automated_prices_history 
ADD COLUMN IF NOT EXISTS real_price DOUBLE PRECISION;

ALTER TABLE automated_prices_history 
ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual';
```

---

### Solução 2: Verificação Automática no Startup (Permanente)

**Arquivo modificado**: `main.py` (linhas ~29257-29306)

Adicionados checks automáticos ao iniciar a aplicação:
- ✅ Verifica e adiciona coluna `auto_price` se não existir
- ✅ Verifica e adiciona coluna `real_price` se não existir  
- ✅ Verifica e adiciona coluna `source` se não existir

**Código adicionado**:
```python
# 7d. Ensure automated_prices_history has 'auto_price' column
try:
    conn.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='automated_prices_history' AND column_name='auto_price'
            ) THEN
                ALTER TABLE automated_prices_history ADD COLUMN auto_price DOUBLE PRECISION;
            END IF;
        END $$;
    """)
    logging.info("✅ automated_prices_history.auto_price column ensured")
except Exception as e:
    logging.warning(f"⚠️ automated_prices_history.auto_price: {e}")

# 7e. Ensure automated_prices_history has 'real_price' column
try:
    conn.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='automated_prices_history' AND column_name='real_price'
            ) THEN
                ALTER TABLE automated_prices_history ADD COLUMN real_price DOUBLE PRECISION;
            END IF;
        END $$;
    """)
    logging.info("✅ automated_prices_history.real_price column ensured")
except Exception as e:
    logging.warning(f"⚠️ automated_prices_history.real_price: {e}")
```

**Benefícios**:
- 🔄 Auto-correção em cada restart
- 🛡️ Previne erros futuros
- 📊 Logs claros de verificação

---

## 🚀 Passos de Implementação

### Passo 1: Executar Migração (Escolher uma opção)

**Opção Recomendada** - Deixar o app fazer automaticamente:
1. ✅ Fazer commit do `main.py` atualizado
2. ✅ Fazer deploy/restart no Render
3. ✅ O app vai adicionar as colunas automaticamente no startup

**Opção Manual** - Executar script agora:
```bash
# Render Shell
python fix_automated_prices_history.py

# Ou SQL direto
psql $DATABASE_URL -c "ALTER TABLE automated_prices_history ADD COLUMN IF NOT EXISTS auto_price DOUBLE PRECISION;"
psql $DATABASE_URL -c "ALTER TABLE automated_prices_history ADD COLUMN IF NOT EXISTS real_price DOUBLE PRECISION;"
```

---

### Passo 2: Verificar Logs

Após restart, verificar no Render Dashboard > Logs:
```
✅ automated_prices_history.auto_price column ensured
✅ automated_prices_history.real_price column ensured
✅ automated_prices_history.source column ensured
✅ automated_prices_history index created/verified
```

---

### Passo 3: Testar Funcionalidade

1. **Teste 1**: Salvar preços automatizados manualmente
   - Aceder à página de automação de preços
   - Fazer uma pesquisa
   - Verificar se salva sem erros

2. **Teste 2**: Relatório diário automático
   - Aguardar próximo relatório agendado
   - Verificar logs: `✅ Saved X automated price entries`
   - Sem erros `column "auto_price" does not exist`

3. **Teste 3**: Verificar dados no DB
   ```sql
   SELECT * FROM automated_prices_history 
   ORDER BY created_at DESC 
   LIMIT 10;
   ```

---

## 📊 Schema Final Esperado

```sql
CREATE TABLE automated_prices_history (
    id SERIAL PRIMARY KEY,
    location TEXT NOT NULL,
    grupo TEXT NOT NULL,
    dias INTEGER NOT NULL,
    pickup_date TEXT NOT NULL,
    auto_price DOUBLE PRECISION,      -- ✅ ADICIONADO
    real_price DOUBLE PRECISION,      -- ✅ ADICIONADO
    strategy_used TEXT,
    strategy_details TEXT,
    min_price_applied DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    source TEXT DEFAULT 'manual'      -- ✅ ADICIONADO
);

CREATE INDEX idx_auto_prices_history 
ON automated_prices_history(location, grupo, pickup_date, created_at);
```

---

## 🔍 Como Verificar se Está Corrigido

### Método 1: Via Logs
Procurar por estas mensagens (sem erros):
```
✅ automated_prices_history.auto_price column ensured
✅ automated_prices_history.real_price column ensured
```

### Método 2: Via SQL
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name='automated_prices_history'
ORDER BY ordinal_position;
```

Deve retornar:
```
column_name        | data_type
-------------------|-----------
id                 | integer
location           | text
grupo              | text
dias               | integer
pickup_date        | text
auto_price         | double precision  ✅
real_price         | double precision  ✅
strategy_used      | text
strategy_details   | text
min_price_applied  | double precision
created_at         | timestamp
created_by         | text
source             | text              ✅
```

### Método 3: Testar INSERT
```sql
INSERT INTO automated_prices_history 
(location, grupo, pickup_date, auto_price, real_price, source)
VALUES ('Albufeira', 'M1', '2025-11-22', 259.64, 259.64, 'automated');

-- Se não der erro, está funcionando! ✅
```

---

## 📝 Notas Importantes

1. **Não perder dados**: 
   - ✅ `ALTER TABLE ADD COLUMN` não apaga dados existentes
   - ✅ Novos registos terão os valores corretos
   - ⚠️ Registos antigos terão `NULL` nas novas colunas (se existirem)

2. **Compatibilidade retroativa**:
   - ✅ O código continua a funcionar com SQLite local
   - ✅ O código continua a funcionar com PostgreSQL antigo ou novo

3. **Sobre o aviso do `token_expires_at`**:
   - ⚠️ É apenas um aviso esperado quando a coluna já existe
   - ✅ O código já trata este caso corretamente
   - ❌ Não precisa de ação

---

## ✅ Checklist Final

- [ ] Executar migração (automática ou manual)
- [ ] Verificar logs de startup sem erros
- [ ] Testar salvar preços automatizados
- [ ] Verificar relatório diário funciona
- [ ] Confirmar dados persistidos no DB
- [ ] Remover script de migração (opcional, após confirmar)

---

## 🎉 Resultado Esperado

Após aplicar as correções:
```
✅ Preços automatizados salvam corretamente
✅ Relatórios diários funcionam sem erros  
✅ Histórico de preços persiste no PostgreSQL
✅ Sem erros "column does not exist"
✅ Sistema totalmente funcional
```

---

## 📞 Troubleshooting

### Se continuar com erro após migração:

1. **Verificar se migração foi executada**:
   ```sql
   \d automated_prices_history
   ```

2. **Verificar permissões**:
   ```sql
   SELECT has_table_privilege('automated_prices_history', 'INSERT');
   ```

3. **Forçar restart completo**:
   - Render Dashboard → Manual Deploy → Clear build cache + Deploy

4. **Verificar versão do PostgreSQL**:
   ```sql
   SELECT version();
   ```
   (Deve ser PostgreSQL 12+)

---

**Última atualização**: 2025-11-19  
**Autor**: Cascade AI Assistant  
**Status**: ✅ Correção completa implementada
