# 🔄 GUIA DE SINCRONIZAÇÃO WINDSURF ↔ RENDER

## 📋 VISÃO GERAL

Este documento explica como funciona a sincronização de dados entre o ambiente de desenvolvimento (Windsurf) e produção (Render).

---

## 🐘 POSTGRESQL - FONTE ÚNICA DE VERDADE

### Como Funciona:
1. **Render (Produção)** usa PostgreSQL externo (Render PostgreSQL)
2. **Windsurf (Local)** usa SQLite para desenvolvimento
3. **Sincronização** acontece via PostgreSQL quando `DATABASE_URL` está definido

### Configuração:

#### No Render:
```bash
# Variável de ambiente automática
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

#### No Windsurf (para testar com PostgreSQL):
```bash
# .env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## 🔄 FLUXO DE SINCRONIZAÇÃO

### 1. **Desenvolvimento Local (Windsurf)**
```
SQLite (data.db) → Testes locais
```

### 2. **Commit & Push para GitHub**
```bash
git add .
git commit -m "Suas alterações"
git push origin main
```

### 3. **Deploy Automático no Render**
```
GitHub → Render (auto-deploy)
Render usa PostgreSQL externo
Dados persistem mesmo em sleep mode
```

---

## ⚠️ PROBLEMAS ATUAIS

### ❌ Sincronização Bilateral NÃO Existe:
- Commits no Windsurf **NÃO** atualizam dados no Render
- Sleep mode do Render **NÃO** causa perda de dados (PostgreSQL)
- Dados criados no Render **NÃO** aparecem no Windsurf

### ✅ O Que Está Sincronizado:
- **Código** (via Git)
- **Estrutura da BD** (via migrations)
- **Configurações** (via environment variables)

### ❌ O Que NÃO Está Sincronizado:
- **Dados da BD** (cada ambiente tem sua própria BD)
- **Uploads** (filesystem efêmero no Render)
- **Cache** (local)

---

## ✅ SOLUÇÕES IMPLEMENTADAS

### 1. **PostgreSQL Externo (Render)**
✅ **IMPLEMENTADO** - `database.py`
- Dados persistem mesmo com sleep mode
- Não há perda de dados em restarts
- Backup automático do Render

### 2. **Armazenamento na BD (BLOB)**
✅ **IMPLEMENTADO** - Tabela `file_storage`
- Uploads salvos na BD (não no filesystem)
- Excel exports salvos na BD
- Fotos de carros na BD

### 3. **Backups Completos**
✅ **IMPLEMENTADO** - `/api/backup/create`
- Backup de todas as BDs
- Backup de uploads
- Backup de configurações
- Download em ZIP

---

## 🚀 WORKFLOW RECOMENDADO

### Desenvolvimento:
```bash
# 1. Desenvolver localmente (SQLite)
python main.py

# 2. Testar funcionalidades
# ...

# 3. Commit & Push
git add .
git commit -m "Feature X"
git push origin main

# 4. Render faz deploy automático
# Aguardar ~2-5 minutos
```

### Produção:
```bash
# 1. Render recebe push do GitHub
# 2. Build automático
# 3. Deploy automático
# 4. PostgreSQL mantém todos os dados
```

---

## 📦 BACKUP & RESTORE

### Criar Backup (Render):
1. Aceder: `https://seu-app.onrender.com/admin/backup`
2. Selecionar opções:
   - ✅ Database
   - ✅ Settings
   - ✅ Uploads
   - ✅ Static files
   - ✅ Templates
   - ✅ Code
3. Clicar "Create Backup"
4. Download do ZIP

### Restaurar Backup:
1. Aceder: `https://seu-app.onrender.com/admin/backup`
2. Upload do ZIP de backup
3. Sistema restaura automaticamente
4. Backup da BD atual é criado antes de sobrescrever

---

## 🔐 DADOS SENSÍVEIS

### Nunca Commitar:
- ❌ `.env` (credenciais)
- ❌ `data.db` (base de dados local)
- ❌ `*.db` (qualquer base de dados)
- ❌ Passwords
- ❌ API Keys

### Usar Environment Variables:
```bash
# Render Dashboard → Environment
DATABASE_URL=...
SMTP_HOST=...
SMTP_USERNAME=...
SMTP_PASSWORD=...
```

---

## 🐛 TROUBLESHOOTING

### Problema: Dados não aparecem após deploy
**Causa:** Render usa PostgreSQL, local usa SQLite  
**Solução:** Dados são separados por ambiente (esperado)

### Problema: Sleep mode apaga dados
**Causa:** Filesystem efêmero do Render  
**Solução:** ✅ Já resolvido - dados na BD (PostgreSQL)

### Problema: Uploads desaparecem
**Causa:** Filesystem efêmero  
**Solução:** ✅ Já resolvido - uploads na tabela `file_storage`

### Problema: Excel exports perdidos
**Causa:** Filesystem efêmero  
**Solução:** ✅ Já resolvido - exports salvos na BD

---

## 📊 TABELAS CRÍTICAS

### Dados Persistentes (PostgreSQL):
- ✅ `users` - Utilizadores
- ✅ `price_snapshots` - Preços
- ✅ `search_history` - **NOVO** - Histórico de pesquisas
- ✅ `notification_rules` - **NOVO** - Regras de notificação
- ✅ `notification_history` - **NOVO** - Histórico de notificações
- ✅ `file_storage` - Ficheiros (BLOB)
- ✅ `export_history` - Histórico de exports
- ✅ `car_images` - Fotos de carros
- ✅ `ai_learning_data` - Dados de AI
- ✅ `user_settings` - Configurações

---

## 🎯 CHECKLIST PRÉ-DEPLOY

Antes de fazer push para produção:

- [ ] Código testado localmente
- [ ] Sem credenciais hardcoded
- [ ] `.env` no `.gitignore`
- [ ] Migrations de BD incluídas
- [ ] Testes passam
- [ ] Logs implementados
- [ ] Error handling adequado
- [ ] Backup recente criado

---

## 📞 SUPORTE

### Logs do Render:
```
Render Dashboard → Logs → View Logs
```

### Logs da Aplicação:
```sql
SELECT * FROM system_logs 
ORDER BY created_at DESC 
LIMIT 100;
```

### Verificar BD:
```sql
-- Contar registos
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM price_snapshots;
SELECT COUNT(*) FROM search_history;

-- Último backup
SELECT * FROM file_storage 
WHERE filepath LIKE '/exports/%' 
ORDER BY created_at DESC 
LIMIT 10;
```

---

## ✅ RESUMO

| Item | Status | Sincronizado |
|------|--------|--------------|
| Código | ✅ | Via Git |
| Estrutura BD | ✅ | Via migrations |
| Dados BD | ❌ | Separado por ambiente |
| Uploads | ✅ | Via BD (BLOB) |
| Excel | ✅ | Via BD (BLOB) |
| Configurações | ✅ | Via env vars |
| Backups | ✅ | Manual (ZIP) |

**Conclusão:** Sistema está preparado para produção com persistência completa via PostgreSQL! 🚀
