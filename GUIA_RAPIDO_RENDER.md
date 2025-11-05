# ⚡ GUIA RÁPIDO - MIGRAÇÃO RENDER

## 🎯 O QUE FAZER AGORA:

### ✅ **OPÇÃO 1: Usar Script do Repositório (RECOMENDADO)**

1. **Abrir Render Shell:**
   - https://dashboard.render.com
   - Selecionar serviço
   - Clicar "Shell"

2. **Executar:**
   ```bash
   python migrate_all_tables_postgres.py
   ```

3. **Pronto!** ✅

---

### ✅ **OPÇÃO 2: Copiar/Colar Script Completo**

Se o ficheiro não estiver no servidor, copia e cola isto NO RENDER SHELL:

```python
import os
import psycopg2
from urllib.parse import urlparse

database_url = os.getenv('DATABASE_URL')
result = urlparse(database_url)
conn = psycopg2.connect(
    database=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)
cursor = conn.cursor()

print("🔧 Creating tables...")

# 1. price_snapshots
cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_snapshots (
      id SERIAL PRIMARY KEY,
      ts TEXT NOT NULL,
      location TEXT NOT NULL,
      pickup_date TEXT NOT NULL,
      pickup_time TEXT NOT NULL,
      days INTEGER NOT NULL,
      supplier TEXT,
      car TEXT,
      price_text TEXT,
      price_num DOUBLE PRECISION,
      currency TEXT,
      link TEXT
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_q ON price_snapshots(location, days, ts)")

# 2. ai_learning_data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_learning_data (
      id SERIAL PRIMARY KEY,
      grupo TEXT NOT NULL,
      days INTEGER NOT NULL,
      location TEXT NOT NULL,
      original_price DOUBLE PRECISION,
      new_price DOUBLE PRECISION NOT NULL,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      user TEXT DEFAULT 'admin'
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_learning ON ai_learning_data(grupo, days, location, timestamp DESC)")

# 3. price_history
cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
      id SERIAL PRIMARY KEY,
      history_type TEXT NOT NULL,
      year INTEGER NOT NULL,
      month INTEGER NOT NULL,
      location TEXT NOT NULL,
      prices_data TEXT NOT NULL,
      saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      saved_by TEXT DEFAULT 'admin'
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_history ON price_history(history_type, year, month, location, saved_at DESC)")

# 4. search_history
cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
      id SERIAL PRIMARY KEY,
      location TEXT NOT NULL,
      start_date TEXT NOT NULL,
      end_date TEXT NOT NULL,
      days INTEGER NOT NULL,
      results_count INTEGER,
      min_price DOUBLE PRECISION,
      max_price DOUBLE PRECISION,
      avg_price DOUBLE PRECISION,
      search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      user TEXT DEFAULT 'admin',
      search_params TEXT
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_history ON search_history(location, start_date, search_timestamp DESC)")

# 5. automated_prices_history
cursor.execute("""
    CREATE TABLE IF NOT EXISTS automated_prices_history (
      id SERIAL PRIMARY KEY,
      location TEXT NOT NULL,
      grupo TEXT NOT NULL,
      dias INTEGER NOT NULL,
      pickup_date TEXT NOT NULL,
      auto_price DOUBLE PRECISION NOT NULL,
      real_price DOUBLE PRECISION NOT NULL,
      strategy_used TEXT,
      strategy_details TEXT,
      min_price_applied DOUBLE PRECISION,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      created_by TEXT
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_auto_prices_history ON automated_prices_history(location, grupo, pickup_date, created_at)")

# 6. export_history
cursor.execute("""
    CREATE TABLE IF NOT EXISTS export_history (
      id SERIAL PRIMARY KEY,
      filename TEXT NOT NULL,
      broker TEXT NOT NULL,
      location TEXT NOT NULL,
      period_start INTEGER,
      period_end INTEGER,
      month INTEGER NOT NULL,
      year INTEGER NOT NULL,
      month_name TEXT NOT NULL,
      file_content TEXT NOT NULL,
      file_size INTEGER,
      exported_by TEXT,
      export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      last_downloaded TEXT
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_export_history ON export_history(broker, location, year, month, export_date)")

# 7. system_logs
cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_logs (
      id SERIAL PRIMARY KEY,
      level TEXT NOT NULL,
      message TEXT NOT NULL,
      module TEXT,
      function TEXT,
      line_number INTEGER,
      exception TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_system_logs ON system_logs(level, created_at)")

# 8. cache_data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cache_data (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL,
      expires_at TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 9. file_storage
cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_storage (
      id SERIAL PRIMARY KEY,
      filename TEXT NOT NULL,
      filepath TEXT NOT NULL UNIQUE,
      file_data BYTEA NOT NULL,
      content_type TEXT,
      file_size INTEGER,
      uploaded_by TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_storage ON file_storage(filepath, uploaded_by)")

# 10. oauth_tokens
cursor.execute("""
    CREATE TABLE IF NOT EXISTS oauth_tokens (
      id SERIAL PRIMARY KEY,
      provider TEXT NOT NULL,
      user_email TEXT NOT NULL,
      access_token TEXT NOT NULL,
      refresh_token TEXT,
      expires_at BIGINT,
      google_id TEXT,
      user_name TEXT,
      user_picture TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(provider, user_email)
    )
""")

# 11. notification_rules
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_rules (
      id SERIAL PRIMARY KEY,
      rule_name TEXT NOT NULL,
      rule_type TEXT NOT NULL,
      condition_json TEXT NOT NULL,
      action_json TEXT NOT NULL,
      enabled INTEGER DEFAULT 1,
      priority INTEGER DEFAULT 1,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      created_by TEXT DEFAULT 'admin'
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_rules ON notification_rules(enabled, priority, rule_type)")

# 12. notification_history
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notification_history (
      id SERIAL PRIMARY KEY,
      rule_id INTEGER,
      notification_type TEXT NOT NULL,
      recipient TEXT NOT NULL,
      subject TEXT,
      message TEXT NOT NULL,
      sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      status TEXT DEFAULT 'sent',
      error_message TEXT
    )
""")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_notification_history ON notification_history(sent_at DESC, status)")

# Commit
conn.commit()
cursor.close()
conn.close()

print("✅ DONE! 12+ tables created")
```

**Depois de colar, pressiona ENTER**

---

## 🔍 **VERIFICAR SE FUNCIONOU:**

No Render Shell:

```bash
python -c "
import os, psycopg2
from urllib.parse import urlparse
result = urlparse(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(database=result.path[1:], user=result.username, password=result.password, host=result.hostname, port=result.port)
cursor = conn.cursor()
cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \\'public\\' ORDER BY table_name')
tables = cursor.fetchall()
print(f'\\n📊 {len(tables)} TABELAS:')
for t in tables: print(f'  ✅ {t[0]}')
conn.close()
"
```

---

## ✅ **RESUMO:**

1. Abrir Render Shell
2. Executar: `python migrate_all_tables_postgres.py`
3. OU copiar/colar o script acima
4. Verificar com comando de verificação
5. Pronto! ✅

---

**Simples assim!** 🎉
