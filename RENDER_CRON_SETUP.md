# 🚀 Render Cron Jobs - Setup Gratuito

## ✅ O QUE SÃO RENDER CRON JOBS?

**Render Cron Jobs** são tarefas agendadas **100% GRATUITAS** que executam comandos em horários específicos.

**Vantagens:**
- ✅ **GRATUITOS** no plano Free do Render
- ✅ **Persistem após restarts** do servidor web
- ✅ **Executam sempre** nos horários agendados
- ✅ **Independentes** do APScheduler interno

**Por que precisamos?**
- ❌ APScheduler **perde jobs** quando o servidor reinicia
- ❌ Render Free Tier **reinicia servidores** automaticamente
- ✅ Cron Jobs **garantem execução** mesmo após restart

---

## 📋 JOBS CONFIGURADOS

| Job | Horário Lisboa | Horário UTC | Frequência |
|-----|----------------|-------------|------------|
| **Daily Backup** | 03:00 | 02:00 | Diário |
| **Daily Search** | 07:00 | 06:00 | Diário |
| **Daily Report** | 09:00 | 08:00 | Diário |
| **Weekly Search** | 07:00 (Segunda) | 06:00 (Segunda) | Semanal |
| **Weekly Report** | 09:00 (Segunda) | 08:00 (Segunda) | Semanal |

---

## 🔧 COMO ATIVAR (Render Dashboard)

### **IMPORTANTE:** Render Cron Jobs **NÃO são criados automaticamente** pelo `render.yaml`!

Você precisa criar **manualmente** no Dashboard do Render:

### **Passo 1: Aceder ao Dashboard**
1. Vai a https://dashboard.render.com
2. Login na tua conta
3. Clica no teu serviço **rental-price-tracker**

### **Passo 2: Criar Cada Cron Job**

Para cada job abaixo, clica **"New" → "Cron Job"** e preenche:

---

#### **1. Daily Backup**
```
Name: daily-backup
Command: python3 -c "import requests; import os; requests.post('https://rental-price-tracker.onrender.com/api/cron/backup', headers={'X-Cron-Secret': os.environ['CRON_SECRET_KEY']})"
Schedule: 0 2 * * *
Docker: Same as rental-price-tracker
Environment Variables:
  - CRON_SECRET_KEY: [usar o mesmo valor do web service]
```

---

#### **2. Daily Report Search**
```
Name: daily-report-search
Command: python3 -c "import requests; import os; requests.post('https://rental-price-tracker.onrender.com/api/cron/daily-search', headers={'X-Cron-Secret': os.environ['CRON_SECRET_KEY']})"
Schedule: 0 6 * * *
Docker: Same as rental-price-tracker
Environment Variables:
  - CRON_SECRET_KEY: [usar o mesmo valor do web service]
```

---

#### **3. Daily Report Email**
```
Name: daily-report-email
Command: python3 -c "import requests; import os; requests.post('https://rental-price-tracker.onrender.com/api/cron/daily-report', headers={'X-Cron-Secret': os.environ['CRON_SECRET_KEY']})"
Schedule: 0 8 * * *
Docker: Same as rental-price-tracker
Environment Variables:
  - CRON_SECRET_KEY: [usar o mesmo valor do web service]
```

---

#### **4. Weekly Report Search**
```
Name: weekly-report-search
Command: python3 -c "import requests; import os; requests.post('https://rental-price-tracker.onrender.com/api/cron/weekly-search', headers={'X-Cron-Secret': os.environ['CRON_SECRET_KEY']})"
Schedule: 0 6 * * 1
Docker: Same as rental-price-tracker
Environment Variables:
  - CRON_SECRET_KEY: [usar o mesmo valor do web service]
```

---

#### **5. Weekly Report Email**
```
Name: weekly-report-email
Command: python3 -c "import requests; import os; requests.post('https://rental-price-tracker.onrender.com/api/cron/weekly-report', headers={'X-Cron-Secret': os.environ['CRON_SECRET_KEY']})"
Schedule: 0 8 * * 1
Docker: Same as rental-price-tracker
Environment Variables:
  - CRON_SECRET_KEY: [usar o mesmo valor do web service]
```

---

## 🔐 ONDE ENCONTRAR O CRON_SECRET_KEY?

1. Vai ao teu serviço web **rental-price-tracker**
2. Clica em **"Environment"**
3. Procura por **`CRON_SECRET_KEY`**
4. Copia o valor (foi gerado automaticamente)
5. Usa esse mesmo valor em **TODOS** os cron jobs

---

## ✅ COMO VERIFICAR SE ESTÁ A FUNCIONAR?

### **Opção 1: Render Dashboard**
- Vai a cada Cron Job
- Clica em **"Logs"**
- Vê se executou nos horários esperados

### **Opção 2: Logs do Web Service**
Procura por:
```
================================================================================
🔄 CRON JOB: Daily Report Search
⏰ Time: 2024-11-07 07:00:00
================================================================================
```

### **Opção 3: Testar Manualmente**
```bash
curl -X POST https://rental-price-tracker.onrender.com/api/cron/daily-search \
  -H "X-Cron-Secret: SEU_CRON_SECRET_KEY_AQUI"
```

---

## ⚠️ IMPORTANTE

### **APScheduler vs Render Cron Jobs**
- **APScheduler** (interno): Roda dentro do servidor web
  - ✅ Funciona bem quando o servidor está ativo
  - ❌ **Perde jobs** quando o servidor reinicia
  - ❌ No Free Tier, o Render reinicia automaticamente

- **Render Cron Jobs** (externo): Jobs separados do servidor
  - ✅ **SEMPRE executam** nos horários agendados
  - ✅ **Independentes** do estado do servidor web
  - ✅ **100% GRATUITOS**

### **Recomendação:**
- ✅ **ATIVA os Render Cron Jobs** para garantir execução
- ✅ **Mantém o APScheduler** como backup (executa se o servidor estiver ativo)
- ✅ Assim tens **dupla garantia** de execução!

---

## 🎯 TIMEZONE

**Render Cron usa UTC timezone:**
- Portugal Inverno: UTC+0 (07:00 UTC = 07:00 Lisboa)
- Portugal Verão: UTC+1 (07:00 UTC = 08:00 Lisboa)

**Os horários configurados assumem inverno (UTC+0).**

Se estiveres no verão, os jobs vão executar 1h mais cedo:
- Daily Search: 06:00 UTC = 07:00 Lisboa (inverno) / 07:00 UTC (verão)

---

## 💰 CUSTO

**100% GRATUITO!** ✅

Render Free Tier inclui:
- ✅ 750 horas de execução de Cron Jobs por mês
- ✅ Número ilimitado de jobs
- ✅ Sem custos adicionais

---

## 📝 NOTAS FINAIS

1. **Cria os 5 jobs** no Render Dashboard (não é automático!)
2. **Usa o mesmo CRON_SECRET_KEY** em todos
3. **Verifica os logs** após a primeira execução
4. **Ambos os sistemas** (APScheduler + Cron) podem coexistir!

**Após setup, os emails vão ser enviados SEMPRE, mesmo com restarts!** 🎉
