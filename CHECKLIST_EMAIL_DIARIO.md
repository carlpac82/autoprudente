# ✅ CHECKLIST: EMAIL DIÁRIO AUTOMATIZADO - 09H00

## 📅 Data: 08/11/2025 às 09:00 (Lisboa Time)

---

## ✅ 1. SCHEDULER CONFIGURADO

**Status:** ✅ CONFIGURADO

```python
# Linha 22534-22541 (main.py)
scheduler.add_job(
    send_automatic_daily_report,
    CronTrigger(hour=9, minute=0),  # ✅ 09:00 Lisboa Time
    id='daily_report',
    name='Daily Automatic Report',
    replace_existing=True
)
```

**Horários:**
- ✅ **07:00** - Daily search (2h antes)
- ✅ **09:00** - Daily email report

**Timezone:** ✅ `Europe/Lisbon` (UTC+0 no inverno, UTC+1 no verão)

---

## ✅ 2. VERIFICAÇÕES NECESSÁRIAS

### 🔐 **A. Gmail OAuth Configurado?**

**Verificar em:**
```
https://carrental-api-5f8q.onrender.com/admin/customization/email
```

**Checklist:**
- [ ] Gmail conectado (botão verde "Conectado como...")
- [ ] Token OAuth salvo no PostgreSQL
- [ ] Não mostra erro de autenticação

**Tabela BD:** `oauth_tokens`
```sql
SELECT provider, user_email, expires_at 
FROM oauth_tokens 
WHERE provider = 'gmail'
ORDER BY created_at DESC LIMIT 1;
```

---

### 📧 **B. Destinatários Configurados?**

**Verificar em:**
```
https://carrental-api-5f8q.onrender.com/admin/customization/email
```

**Checklist:**
- [ ] Lista de destinatários preenchida (1 email por linha)
- [ ] Emails válidos
- [ ] Settings salvos no PostgreSQL

**Tabela BD:** `user_settings`
```sql
SELECT setting_value 
FROM user_settings 
WHERE setting_key = 'email_settings';
```

**Estrutura esperada:**
```json
{
  "recipients": "email1@example.com\nemail2@example.com",
  "senderName": "Auto Prudente",
  "replyTo": "info@autoprudente.pt"
}
```

---

### ⚙️ **C. Relatórios Diários Ativados?**

**Verificar em:**
```
https://carrental-api-5f8q.onrender.com/admin/customization/automated-reports
```

**Checklist:**
- [ ] Toggle "Relatórios Diários" ATIVADO
- [ ] Localização selecionada (Faro ou Albufeira)
- [ ] Settings salvos no PostgreSQL

**Tabela BD:** `price_automation_settings`
```sql
SELECT setting_value 
FROM price_automation_settings 
WHERE setting_key = 'automatedReportsSettings';
```

**Estrutura esperada:**
```json
{
  "dailyEnabled": true,
  "weeklyEnabled": true,
  "searchLocation": "Aeroporto de Faro",
  "notificationEmail": "email@example.com"
}
```

---

## ✅ 3. FLUXO AUTOMÁTICO

```
07:00 Lisboa Time
  ↓
📍 run_daily_report_search()
  ↓
✅ Verifica se dailyEnabled = true
  ↓
🔍 Faz pesquisa no CarJet (2-4 dias à frente, aleatório)
  ↓
💾 Salva resultados na tabela recent_searches
  ↓
  
09:00 Lisboa Time
  ↓
📧 send_automatic_daily_report()
  ↓
✅ Verifica se dailyEnabled = true
  ↓
✅ Verifica se há Gmail OAuth token
  ↓
✅ Verifica se há destinatários
  ↓
📊 Carrega última pesquisa de recent_searches
  ↓
🎨 Gera HTML bonito com:
   - Logo Auto Prudente
   - Estatísticas (Melhores Preços, Competitivos, Taxa Liderança)
   - Cards por grupo de carro (B1, C, D, F, etc)
   - Comparação com concorrentes
  ↓
📤 Envia email para CADA destinatário via Gmail API
  ↓
✅ Log: "🎉 Daily report completed: X/Y sent successfully"
  ↓
💾 Salva no histórico (automated_search_history)
  ↓
💾 Salva preços (automated_prices_history)
```

---

## ✅ 4. VERIFICAÇÕES NO RENDER

### **A. Verificar Logs Startup**

```
https://dashboard.render.com/web/rental-price-tracker/logs
```

**Procurar por:**
```
🚀 INITIALIZING APSCHEDULER
📍 Timezone: Europe/Lisbon (UTC+0/+1)
⏰ Current Lisbon time: 2025-11-07 20:30:00
✅ Daily report search scheduler configured (daily at 7 AM)
✅ Daily report scheduler configured (daily at 9 AM)
```

### **B. Verificar Jobs Ativos**

**GET:** `https://carrental-api-5f8q.onrender.com/api/cron/status`

**Resposta esperada:**
```json
{
  "jobs": [
    {
      "id": "daily_report_search",
      "name": "Daily Report Search",
      "next_run": "2025-11-08 07:00:00"
    },
    {
      "id": "daily_report",
      "name": "Daily Automatic Report",
      "next_run": "2025-11-08 09:00:00"
    }
  ]
}
```

---

## ✅ 5. TESTE MANUAL (OPCIONAL)

### **Teste do Search (simula 07:00):**
```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/cron/daily-search \
  -H "X-Cron-Secret: YOUR_CRON_SECRET"
```

### **Teste do Email (simula 09:00):**
```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/cron/daily-report \
  -H "X-Cron-Secret: YOUR_CRON_SECRET"
```

**OU via interface:**
```
POST /api/reports/test-daily
```

---

## ✅ 6. LOGS A MONITORIZAR AMANHÃ

### **07:00 - Daily Search**
```
🔍 DAILY REPORT SEARCH STARTED
⏰ Time: 2025-11-08 07:00:00
🔍 Starting daily report search (2h before email)...
📊 Search completed: Aeroporto de Faro, 3 dias
💾 Results saved to recent_searches
```

### **09:00 - Daily Email**
```
📧 DAILY REPORT EMAIL STARTED
⏰ Time: 2025-11-08 09:00:00
🔄 Starting automatic daily report...
[EMAIL-DEBUG] Automation settings: dailyEnabled=True
📧 Sending daily report to 2 recipient(s): [...]
📊 Found search data: Aeroporto de Faro - 45 cars
✅ Daily report sent to email1@example.com
✅ Daily report sent to email2@example.com
🎉 Daily report completed: 2/2 sent successfully
✅ Saved 64 automated price entries
🎉 Saved 2/2 locations to automated_search_history
```

---

## ❌ POSSÍVEIS ERROS E SOLUÇÕES

### **Erro 1: "Daily reports are disabled"**
```
ℹ️ Daily reports are disabled - skipping
```
**Solução:** Ativar toggle em `/admin/customization/automated-reports`

---

### **Erro 2: "No Gmail credentials found"**
```
❌ No Gmail credentials found - cannot send daily report
```
**Solução:** Conectar Gmail em `/admin/customization/email`

---

### **Erro 3: "No recipients configured"**
```
⚠️ No recipients configured in email settings
```
**Solução:** Adicionar destinatários em `/admin/customization/email`

---

### **Erro 4: "No automated reports settings found"**
```
⚠️ No automated reports settings found in price_automation_settings
```
**Solução:** Salvar settings em `/admin/customization/automated-reports`

---

## ✅ 7. ESTRUTURA DO EMAIL

### **Header:**
- ✅ Logo Auto Prudente
- ✅ "Relatório Diário de Preços"
- ✅ Data: "08 de Novembro de 2025"
- ✅ Local + Dias: "Aeroporto de Faro • 3 dias"

### **Stats:**
- ✅ Melhores Preços (verde)
- ✅ Competitivos (amarelo)
- ✅ Taxa de Liderança % (azul)

### **Cards por Grupo:**
- ✅ Grupo B1, C, D, F, I, J, etc
- ✅ Top 3 concorrentes
- ✅ Posição Auto Prudente (1º, 2º, 3º+)
- ✅ Preço por dia
- ✅ Total de ofertas

### **Footer:**
- ✅ "Auto Prudente © 2025"
- ✅ "Dados baseados na última pesquisa"

---

## ✅ 8. VARIÁVEIS DE AMBIENTE RENDER

**Verificar em:** Dashboard Render → Settings → Environment

**Necessárias:**
- ✅ `DATABASE_URL` (PostgreSQL)
- ✅ `CRON_SECRET` (para proteger endpoints)
- ✅ `SECRET_KEY` (sessões)
- ✅ `ADMIN_USERNAME` / `ADMIN_PASSWORD`

---

## ✅ 9. CRONOGRAMA COMPLETO

| Hora | Ação | Job ID |
|------|------|--------|
| **03:00** | Backup automático | `daily_backup` |
| **07:00** | Daily search | `daily_report_search` |
| **09:00** | **Daily email** ⭐ | `daily_report` |
| **12:05** | Extra search | `search_12h05` |
| **12:40** | Extra report | `report_12h40` |

---

## ✅ 10. CHECKLIST FINAL

Antes de amanhã às 09:00, verificar:

- [ ] Render está online (não em sleep)
- [ ] PostgreSQL conectado
- [ ] Gmail OAuth válido (não expirado)
- [ ] Destinatários configurados
- [ ] `dailyEnabled: true` em automated reports
- [ ] Localização selecionada (Faro ou Albufeira)
- [ ] Scheduler ativo (ver logs startup)
- [ ] Timezone = Europe/Lisbon
- [ ] Logo do email carregando (`/static/logos/logo_AUP.png`)

---

## 📞 CONTACTOS TÉCNICOS

**Dashboard Render:**
- URL: https://dashboard.render.com/web/rental-price-tracker
- Logs: https://dashboard.render.com/web/rental-price-tracker/logs
- Events: https://dashboard.render.com/web/rental-price-tracker/events

**Admin Interface:**
- Automated Reports: https://carrental-api-5f8q.onrender.com/admin/customization/automated-reports
- Email Settings: https://carrental-api-5f8q.onrender.com/admin/customization/email
- Cron Status: https://carrental-api-5f8q.onrender.com/api/cron/status

---

## ✅ RESULTADO ESPERADO AMANHÃ

```
08/11/2025 às 09:00:05

📧 Email recebido por TODOS os destinatários
📊 Relatório bonito com logo e estatísticas
🚗 Cards de grupos de carros com posição AP
✅ Histórico salvo em automated_search_history
✅ Preços salvos em automated_prices_history
```

**SE TUDO ESTIVER OK → Email chega automaticamente! 🎉**
