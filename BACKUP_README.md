# 💾 Sistema de Backup Completo

Sistema de backup e restauração da base de dados com todas as parametrizações e coordenadas.

## 📋 O Que É Incluído

### ✅ Tabelas Exportadas:
- **damage_reports** (44 registos) - Todos os Damage Reports
- **damage_report_coordinates** (90 registos) - Parametrizações do template DR
- **rental_agreement_coordinates** (15 registos) - Parametrizações do template RA
- **rental_agreement_templates** (8 registos) - Templates de RA
- **users** (3 registos) - Utilizadores do sistema
- **system_logs** (2,360+ registos) - Logs do sistema

### 📊 Estatísticas:
- **Tamanho médio:** 2-3 MB por backup
- **Formato:** JSON (legível e portável)
- **Backups mantidos:** Últimos 10 automaticamente

---

## 🚀 Como Usar

### 1️⃣ **Fazer Backup**

```bash
python3 backup_full.py
```

**O que faz:**
- ✅ Exporta todas as tabelas para JSON
- ✅ Guarda em `backups_local/backup_YYYYMMDD_HHMMSS.json`
- ✅ Apaga backups antigos (mantém 10)
- ✅ Faz commit e push para GitHub (código, não backups)

**Exemplo de output:**
```
🚀 Iniciando backup completo...
📦 1. Exportando base de dados...
   ✅ Conectado à BD
   📊 Exportando damage_reports... ✅ 44 rows
   📊 Exportando damage_report_coordinates... ✅ 90 rows
   ...
💾 2. Salvando backup...
   ✅ Backup criado: backup_20251109_181342.json (2.22 MB)
✅ BACKUP COMPLETO CONCLUÍDO!
```

---

### 2️⃣ **Listar Backups Disponíveis**

```bash
ls -lh backups_local/
```

Ou simplesmente:
```bash
python3 restore_backup.py
```

---

### 3️⃣ **Testar Restauração (Dry-Run)**

Antes de restaurar, pode testar sem fazer alterações:

```bash
python3 restore_backup.py backups_local/backup_20251109_181342.json --dry-run
```

**O que faz:**
- 🔍 Mostra o que seria restaurado
- 🔍 Conta registos existentes vs backup
- ❌ NÃO faz alterações na BD

---

### 4️⃣ **Restaurar Backup**

```bash
python3 restore_backup.py backups_local/backup_20251109_181342.json
```

**Processo interativo:**
1. Carrega o backup
2. Conecta à BD
3. **Pergunta se quer continuar** ⚠️
4. Para cada tabela com dados:
   - Mostra quantos registos existem
   - **Pergunta se quer apagar** (para evitar duplicados)
5. Insere os dados do backup
6. Commit das alterações

**Exemplo:**
```
🔧 Iniciando restauração de backup...
📦 Backup: backup_20251109_181342.json
   ✅ Backup de: 2025-11-09T18:13:42
   📊 Tabelas: 6

⚠️  AVISO: Esta operação irá modificar a base de dados!
Continuar? [s/N]: s

📥 3. Restaurando tabelas...
   ⚠️  damage_reports tem 44 registos. Apagar? [s/N]: s
   🗑️  44 registos apagados
   ✅ damage_reports: 44 rows inseridas
   ...

✅ RESTAURAÇÃO CONCLUÍDA!
```

---

## 📁 Estrutura de Ficheiros

```
RentalPriceTrackerPerDay/
├── backups_local/                  ← Backups locais (não vão para Git)
│   ├── backup_20251109_181342.json (2.22 MB)
│   ├── backup_20251109_120000.json
│   └── ... (até 10 backups)
│
├── backup_full.py                  ← Script de backup ✅
├── restore_backup.py               ← Script de restauração ✅
├── backup_full.sh                  ← Alternativa (pg_dump)
├── BACKUP_README.md                ← Esta documentação
└── .gitignore                      ← Exclui backups_local/
```

---

## ⚠️ Importante

### ✅ **Backups Locais:**
- Ficam em `backups_local/`
- **NÃO** vão para o Git (ficheiros grandes)
- Mantém-se apenas no teu computador
- Máximo de 10 backups (auto-limpeza)

### ✅ **GitHub:**
- **SIM:** Scripts (`backup_full.py`, `restore_backup.py`)
- **SIM:** Código fonte (`main.py`, `templates/`, etc.)
- **NÃO:** Ficheiros de backup (`.json` grandes)

### ⚠️ **Segurança:**
- Backups contêm dados sensíveis (emails, nomes)
- Guardar em local seguro
- Não partilhar publicamente

---

## 🔧 Resolução de Problemas

### ❌ "DATABASE_URL não definida"
**Solução:** Criar ficheiro `.env`:
```bash
echo "DATABASE_URL=postgresql://user:pass@host/db" > .env
```

### ❌ "psycopg2 not found"
**Solução:** Instalar dependências:
```bash
pip3 install -r requirements.txt
```

### ❌ "Erro ao conectar à BD"
**Solução:** Verificar se `DATABASE_URL` está correta:
```bash
cat .env | grep DATABASE_URL
```

---

## 📅 Quando Fazer Backup

### **Recomendado:**

✅ **Antes de:**
- Fazer alterações importantes nas coordenadas
- Atualizar o código com mudanças na BD
- Testar novas funcionalidades
- Fazer deploy de versão nova

✅ **Regularmente:**
- 1x por semana (mínimo)
- 1x por dia (ideal para produção)
- Antes e depois de cada sessão de trabalho importante

✅ **Backup automático:**
Adicionar ao crontab (Linux/Mac):
```bash
# Backup diário às 3h da manhã
0 3 * * * cd /path/to/project && python3 backup_full.py
```

---

## 📞 Suporte

Se tiveres problemas:
1. Verifica os logs do script
2. Testa com `--dry-run` primeiro
3. Confirma que `.env` está correto
4. Verifica se tens espaço em disco

---

## 📝 Changelog

### v1.0 (2025-11-09)
- ✅ Sistema de backup completo
- ✅ Restauração interativa
- ✅ Auto-limpeza (max 10 backups)
- ✅ Git commit automático
- ✅ Modo dry-run para testes
- ✅ Exporta todas as tabelas importantes
