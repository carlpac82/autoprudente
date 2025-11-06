# 🔧 FIX HOMEPAGE PREVIEW - Criar Tabela no PostgreSQL

## 🚨 Problema Identificado

O preview de pesquisas na homepage **NÃO funciona** porque:
- ❌ Endpoint `/api/recent-searches/load` retorna **erro 500**
- ❌ Tabela `recent_searches` **NÃO EXISTE** no PostgreSQL do Render

## ✅ Solução

Criar a tabela `recent_searches` no PostgreSQL executando o script Python no Render Shell.

---

## 📋 Passo a Passo (Render Shell)

### **1. Abrir Render Shell**
1. Ir para https://dashboard.render.com
2. Selecionar o serviço `carrental-api`
3. Clicar em **"Shell"** no menu à esquerda
4. Aguardar terminal abrir

### **2. Executar Script**
No terminal do Render Shell, executar:

```bash
python create_recent_searches_table.py
```

### **3. Verificar Sucesso**
Deve aparecer:

```
============================================================
🔧 CREATING RECENT_SEARCHES TABLE
============================================================

🔍 Connecting to PostgreSQL...
📋 Creating recent_searches table...
✅ Table recent_searches created successfully!
📊 Current records: 0

============================================================
✅ SUCCESS!

💡 Now the homepage preview should work!
============================================================
```

---

## 🧪 Testar Homepage

Após criar a tabela:

1. **Abrir homepage**: https://carrental-api-5f8q.onrender.com/
2. **Fazer uma pesquisa** (qualquer local, qualquer duração)
3. **Aguardar 2-3 segundos** após resultados carregarem
4. **Verificar**: Secção "Recent Searches Preview" deve aparecer automaticamente!

---

## 📊 Estrutura da Tabela

```sql
CREATE TABLE recent_searches (
    id SERIAL PRIMARY KEY,
    location TEXT NOT NULL,
    start_date TEXT NOT NULL,
    days INTEGER NOT NULL,
    results_data TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    "user" TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recent_searches_user 
ON recent_searches("user", created_at DESC);
```

---

## 🔍 Troubleshooting

### **Erro: "DATABASE_URL not found!"**
**Solução:** Executar no Render Shell, NÃO localmente!

### **Preview ainda não aparece**
1. Abrir Console do browser (F12)
2. Procurar logs:
   ```
   [RECENT] ✅ Loaded from server: 1
   [RECENT] ✅ Showing container with 1 searches
   ```
3. Se aparecer erro 500, a tabela não foi criada corretamente

### **Como verificar se tabela existe**
No Render Shell:
```python
python3 -c "
import os, psycopg2
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute(\"SELECT COUNT(*) FROM recent_searches\")
print(f'Records: {cur.fetchone()[0]}')
"
```

---

## ✅ Checklist

- [ ] Script executado no Render Shell
- [ ] Tabela criada com sucesso (✅ SUCCESS!)
- [ ] Pesquisa feita na homepage
- [ ] Preview aparece automaticamente
- [ ] Comparação funciona com 2+ pesquisas

---

## 📝 Notas Técnicas

- **Backend**: `main.py` linhas 16662-16753
- **Frontend**: `templates/index.html` linhas 2765-2858
- **Endpoints**:
  - POST `/api/recent-searches/save` - Guarda pesquisas
  - GET `/api/recent-searches/load` - Carrega pesquisas
- **Limite**: Máximo 3 pesquisas por utilizador
- **Auto-delete**: Pesquisas antigas são removidas ao guardar novas
