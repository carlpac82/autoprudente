# ✅ Render PostgreSQL Setup Checklist

Use este checklist para verificar se tudo está configurado corretamente.

## 📋 Pré-Deploy

### 1. PostgreSQL Database Criada
- [ ] Database criada no Render
- [ ] Nome: `carrental_db`
- [ ] Status: **Available** (verde)
- [ ] Region: Frankfurt (EU Central)
- [ ] Plan: Free

### 2. Connection String Copiada
- [ ] Copiei a **External Database URL**
- [ ] Formato: `postgresql://user:password@host:port/database`
- [ ] Guardei num local seguro

### 3. Environment Variable Configurada
- [ ] Acedi ao Web Service (carrental_api)
- [ ] Fui a **Environment**
- [ ] Adicionei variável:
  ```
  Key: DATABASE_URL
  Value: [URL copiada]
  ```
- [ ] Cliquei em **Save Changes**

---

## 🚀 Durante Deploy

### 4. Deploy Iniciado
- [ ] Render iniciou redeploy automático
- [ ] Status: **Building** ou **Deploying**

### 5. Verificar Logs
Procurar nos logs do Render:

```
✅ Deve aparecer:
🐘 PostgreSQL mode enabled
✅ Connected to PostgreSQL
```

```
❌ NÃO deve aparecer:
📁 SQLite mode (local development)
```

### 6. Instalação de Dependências
Verificar se instalou:
```
✅ psycopg2-binary==2.9.9
✅ sqlalchemy==2.0.23
```

---

## 🧪 Pós-Deploy

### 7. Testar Conexão
No **Shell** do Render:
```bash
python test_postgres_connection.py
```

Deve mostrar:
```
✅ PostgreSQL mode enabled
✅ Connected successfully!
✅ All tests passed!
```

### 8. Inicializar Tabelas
No **Shell** do Render:
```bash
python init_postgres.py
```

Deve criar 22 tabelas:
```
✅ Table: app_settings
✅ Table: users
✅ Table: activity_log
... (19 mais)
🎉 PostgreSQL database initialized successfully!
```

### 9. Testar Aplicação
- [ ] Aceder ao site
- [ ] Fazer login
- [ ] Fazer uma pesquisa de preços
- [ ] Verificar se dados são salvos

### 10. Verificar Persistência
- [ ] Esperar 15 minutos (sleep mode)
- [ ] Acordar o serviço
- [ ] Verificar se dados continuam lá
- [ ] ✅ Dados devem persistir!

---

## 🔍 Troubleshooting

### Erro: "relation does not exist"
**Solução:**
```bash
# No Render Shell:
python init_postgres.py
```

### Erro: "password authentication failed"
**Solução:**
1. Verificar se `DATABASE_URL` está correta
2. Copiar novamente do Render Dashboard
3. Atualizar Environment Variable

### Erro: "could not connect to server"
**Solução:**
1. Verificar se database está **Available**
2. Verificar se region é a mesma do Web Service
3. Aguardar alguns minutos

### Logs mostram "SQLite mode"
**Solução:**
1. Verificar se `DATABASE_URL` foi adicionada
2. Verificar se clicou em **Save Changes**
3. Fazer redeploy manual se necessário

---

## 📊 Verificação Final

### Tudo OK se:
- ✅ Logs mostram "🐘 PostgreSQL mode enabled"
- ✅ Site funciona normalmente
- ✅ Dados são salvos
- ✅ Dados persistem após sleep mode
- ✅ Sem erros nos logs

### Status da Database:
```
Render Dashboard → PostgreSQL → carrental_db
Status: Available ✅
Connections: Active
Storage: X MB / 1 GB
```

---

## 🎯 Próximos Passos (Opcional)

### Migrar Dados Existentes
Se tens dados no SQLite que queres migrar:

```bash
# No Render Shell:
python migrate_to_postgres.py
```

### Configurar Backups
Render faz backups automáticos (Free plan: 7 dias)

Para backups adicionais:
1. Usar `/api/backup/create` no site
2. Download manual
3. Guardar localmente ou em cloud storage

---

## 📞 Suporte

**Problemas?**
1. Verificar logs do Render
2. Executar `python test_postgres_connection.py`
3. Verificar este checklist novamente

**Tudo funciona?**
🎉 Parabéns! Tens agora uma base de dados profissional que nunca perde dados!
