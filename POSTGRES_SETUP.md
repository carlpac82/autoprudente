# 🐘 PostgreSQL Setup Guide - Render

Este guia explica como configurar PostgreSQL no Render para ter dados persistentes que nunca se perdem.

## 📋 Benefícios

✅ **Dados persistem sempre** - Mesmo com sleep mode
✅ **Sincronização automática** - Windsurf e Render usam a mesma DB
✅ **Backups automáticos** - Render faz backups diários
✅ **Grátis até 1GB** - Suficiente para o projeto
✅ **Sem perda de dados** - Nunca mais perder configurações

---

## 🚀 Passo 1: Criar PostgreSQL Database no Render

1. **Aceder ao Dashboard do Render**
   - Ir para: https://dashboard.render.com

2. **Criar Nova Database**
   - Clicar em **"New +"** → **"PostgreSQL"**
   
3. **Configurar Database**
   ```
   Name: carrental_db
   Database: carrental_db
   User: carrental_user
   Region: Frankfurt (EU Central)
   PostgreSQL Version: 16
   Plan: Free
   ```
   
   **⚠️ IMPORTANTE:** 
   - Database name deve usar apenas: `a-z`, `0-9`, `_`
   - Não usar hífens (`-`)
   - Deve começar com letra ou underscore

4. **Criar Database**
   - Clicar em **"Create Database"**
   - Aguardar 2-3 minutos até ficar **"Available"**

5. **Copiar Connection String**
   - Na página da database, copiar **"External Database URL"**
   - Formato: `postgresql://user:password@host:port/database`

---

## 🔧 Passo 2: Configurar Web Service

1. **Aceder ao Web Service**
   - Ir para o teu Web Service (carrental_api)

2. **Adicionar Environment Variable**
   - Ir para **"Environment"**
   - Clicar em **"Add Environment Variable"**
   
   ```
   Key: DATABASE_URL
   Value: [COLAR A CONNECTION STRING COPIADA]
   ```

3. **Salvar**
   - Clicar em **"Save Changes"**
   - O Render vai fazer **redeploy automático**

---

## 📊 Passo 3: Inicializar Database (Automático)

Quando o Render fizer deploy, o código vai:

1. ✅ Detectar `DATABASE_URL` automaticamente
2. ✅ Criar todas as 22 tabelas no PostgreSQL
3. ✅ Começar a usar PostgreSQL em vez de SQLite

**Não precisas fazer nada!** É automático.

---

## 🔄 Passo 4: Migrar Dados Existentes (Opcional)

Se já tens dados no SQLite que queres migrar:

### **Opção A: Migração Manual (Recomendado)**

1. **No Render Shell**
   ```bash
   # Aceder ao Shell do Web Service
   python init_postgres.py  # Criar tabelas
   python migrate_to_postgres.py  # Migrar dados
   ```

### **Opção B: Via Backup/Restore**

1. Fazer backup do SQLite local
2. Restaurar no Render
3. Executar migração

---

## 🧪 Passo 5: Testar

1. **Verificar Logs do Render**
   ```
   🐘 Using PostgreSQL: [hostname]/carrental
   ✅ Table: app_settings
   ✅ Table: users
   ...
   ```

2. **Fazer uma Pesquisa de Preços**
   - Os dados devem ser salvos no PostgreSQL

3. **Verificar Persistência**
   - Esperar o sleep mode
   - Acordar o serviço
   - Dados continuam lá! ✅

---

## 🔐 Passo 6: Configurar Localmente (Desenvolvimento)

Para usar PostgreSQL também localmente:

1. **Instalar PostgreSQL**
   ```bash
   # Mac
   brew install postgresql@16
   brew services start postgresql@16
   
   # Ubuntu/Debian
   sudo apt install postgresql-16
   ```

2. **Criar Database Local**
   ```bash
   createdb carrental_local
   ```

3. **Configurar .env**
   ```bash
   # .env
   DATABASE_URL=postgresql://localhost/carrental_local
   ```

4. **Inicializar**
   ```bash
   python init_postgres.py
   ```

**OU** simplesmente não configurar nada e usar SQLite local automaticamente!

---

## 📝 Como Funciona

### **Detecção Automática**

```python
# O código detecta automaticamente:
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Produção: Usa PostgreSQL
    print("🐘 Using PostgreSQL")
else:
    # Local: Usa SQLite
    print("📁 Using SQLite")
```

### **Sem Mudanças no Código**

- ✅ Código funciona igual
- ✅ Queries funcionam em ambos
- ✅ Conversão automática de sintaxe
- ✅ Zero downtime

---

## 🎯 Resultado Final

### **Antes (SQLite)**
```
Windsurf (Local)     Render (Produção)
    data.db    ❌      data.db (perdido em sleep)
```

### **Depois (PostgreSQL)**
```
Windsurf (Local)     Render (Produção)
    data.db              PostgreSQL
                             ↓
                    [Sempre disponível]
                    [Backups automáticos]
                    [Nunca se perde]
```

---

## ⚠️ Notas Importantes

1. **Free Tier Limits**
   - 1 GB storage
   - 90 dias de inatividade = database deletada
   - Backups: 7 dias de retenção

2. **Conexões**
   - Máximo 97 conexões simultâneas (Free)
   - O código usa connection pooling

3. **Performance**
   - PostgreSQL é mais rápido que SQLite para múltiplos users
   - Queries complexas são otimizadas

---

## 🆘 Troubleshooting

### **Erro: "relation does not exist"**
```bash
# Executar no Render Shell:
python init_postgres.py
```

### **Erro: "password authentication failed"**
- Verificar se `DATABASE_URL` está correto
- Copiar novamente do Render Dashboard

### **Dados não aparecem**
```bash
# Verificar se migração foi feita:
python migrate_to_postgres.py
```

---

## 📞 Suporte

Se tiveres problemas:
1. Verificar logs do Render
2. Testar conexão: `psql $DATABASE_URL`
3. Verificar tabelas: `\dt` no psql

---

**🎉 Pronto! Agora tens uma base de dados profissional que nunca perde dados!**
