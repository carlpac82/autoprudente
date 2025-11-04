# 🔧 Configurar Environment Variables no Render

## 📋 VARIÁVEIS OBRIGATÓRIAS

### 1. Passwords dos Utilizadores

```
Key: ADMIN_PASSWORD
Value: [escolher password segura]
```

```
Key: CARLPAC82_PASSWORD
Value: [escolher password segura]
```

```
Key: DPRUDENTE_PASSWORD
Value: [escolher password segura]
```

### 2. Secret Key

```
Key: SECRET_KEY
Value: [Clicar em "Generate Value"]
```

### 3. Database URL

```
Key: DATABASE_URL
Value: [Copiar do PostgreSQL Database]
```

**Como obter:**
1. Dashboard → PostgreSQL Database (carrental_db)
2. Info → External Database URL
3. Copiar todo o URL: `postgresql://user:password@host:port/database`

### 4. Scraping Mode

```
Key: TEST_MODE_LOCAL
Value: 0
```

### 5. Use Playwright

```
Key: USE_PLAYWRIGHT
Value: 1
```

### 6. Scraper Service

```
Key: SCRAPER_SERVICE
Value: scrapeops
```

### 7. Scraper Country

```
Key: SCRAPER_COUNTRY
Value: pt
```

### 8. Force Proxy

```
Key: FORCE_PROXY_FOR_CARJET
Value: 1
```

### 9. Price Adjustments

```
Key: CARJET_PRICE_ADJUSTMENT_PCT
Value: 3.12
```

```
Key: CARJET_PRICE_OFFSET_EUR
Value: 0
```

---

## 📋 VARIÁVEIS OPCIONAIS

### ScraperOps API Key (se usar)

```
Key: SCRAPER_API_KEY
Value: [tua API key do ScraperOps]
```

### Gmail OAuth (se usar notificações)

```
Key: GMAIL_CLIENT_ID
Value: [teu client ID]
```

```
Key: GMAIL_CLIENT_SECRET
Value: [teu client secret]
```

```
Key: OAUTH_REDIRECT_URI
Value: https://carrental-api-5f8q.onrender.com/api/oauth/gmail/callback
```

---

## ⚠️ VARIÁVEIS QUE NÃO DEVEM EXISTIR NO RENDER

**NUNCA adicionar estas:**
- ❌ `DEV_NO_AUTH` (só para desenvolvimento local)
- ❌ `APP_USERNAME` (não é usado)
- ❌ `APP_PASSWORD` (não é usado)

---

## 🎯 PASSO A PASSO

### 1. Aceder ao Dashboard

```
https://dashboard.render.com
→ carrental_api (Web Service)
→ Environment (menu lateral)
```

### 2. Limpar Variáveis Antigas

**Apagar estas se existirem:**
- `APP_USERNAME`
- `APP_PASSWORD`
- `DEV_NO_AUTH`
- Qualquer duplicada

### 3. Adicionar Novas Variáveis

Para cada variável acima:

1. **Clicar em "Add Environment Variable"**
2. **Key:** Nome da variável (ex: `ADMIN_PASSWORD`)
3. **Value:** Valor da variável
4. **Clicar em "Add"**

### 4. Variáveis Especiais

**SECRET_KEY:**
- Clicar em "Generate Value" em vez de escrever manualmente

**DATABASE_URL:**
- Copiar do PostgreSQL Database
- Não inventar, usar o URL exato

### 5. Guardar

**Clicar em "Save Changes"** no fundo da página

### 6. Aguardar Deploy

O Render vai reiniciar automaticamente (~2-3 min)

---

## ✅ VERIFICAR SE ESTÁ CORRETO

### 1. Ver Logs

```
Dashboard → Logs
```

**Procurar por:**
```
✅ Default users ready (admin/admin)
🐘 Using PostgreSQL
```

**NÃO deve ter:**
```
❌ column "enabled" does not exist
❌ unauthorized
❌ Not using PostgreSQL
```

### 2. Testar Login

```
https://carrental-api-5f8q.onrender.com/login
Username: admin
Password: [a que definiste em ADMIN_PASSWORD]
```

### 3. Testar Scraping

Fazer uma pesquisa e verificar se encontra carros.

---

## 🐛 TROUBLESHOOTING

### Erro: "Duplicate keys"

**Causa:** Variável existe 2x (no render.yaml e manualmente)

**Solução:**
1. Environment → Ver todas
2. Procurar duplicadas
3. Apagar uma
4. Save Changes

### Erro: "Not using PostgreSQL"

**Causa:** `DATABASE_URL` não está definido ou está errado

**Solução:**
1. Verificar se `DATABASE_URL` existe
2. Copiar novamente do PostgreSQL Database
3. Garantir que é o URL completo

### Erro: "column enabled does not exist"

**Causa:** Schema do PostgreSQL desatualizado

**Solução:**
1. Já foi corrigido no Render Shell
2. Se persistir, fazer Manual Deploy

### Scraping retorna HTML

**Causa:** Problema de autenticação ou Chrome não instalado

**Solução:**
1. Verificar se `DEV_NO_AUTH` NÃO existe no Render
2. Dockerfile já tem Chrome instalado
3. Fazer Manual Deploy

---

## 📊 LISTA COMPLETA DE VARIÁVEIS

### Obrigatórias (10)

1. ✅ `ADMIN_PASSWORD`
2. ✅ `CARLPAC82_PASSWORD`
3. ✅ `DPRUDENTE_PASSWORD`
4. ✅ `SECRET_KEY` (Generate Value)
5. ✅ `DATABASE_URL` (copiar do PostgreSQL)
6. ✅ `TEST_MODE_LOCAL=0`
7. ✅ `USE_PLAYWRIGHT=1`
8. ✅ `SCRAPER_SERVICE=scrapeops`
9. ✅ `SCRAPER_COUNTRY=pt`
10. ✅ `FORCE_PROXY_FOR_CARJET=1`
11. ✅ `CARJET_PRICE_ADJUSTMENT_PCT=3.12`
12. ✅ `CARJET_PRICE_OFFSET_EUR=0`

### Opcionais (3)

1. ⚪ `SCRAPER_API_KEY` (se usar ScraperOps)
2. ⚪ `GMAIL_CLIENT_ID` (se usar Gmail)
3. ⚪ `GMAIL_CLIENT_SECRET` (se usar Gmail)
4. ⚪ `OAUTH_REDIRECT_URI` (se usar Gmail)

### NUNCA Adicionar (3)

1. ❌ `DEV_NO_AUTH`
2. ❌ `APP_USERNAME`
3. ❌ `APP_PASSWORD`

---

## 🎉 DEPOIS DE CONFIGURAR

O sistema deve:
- ✅ Iniciar sem erros
- ✅ Criar utilizadores automaticamente
- ✅ Conectar ao PostgreSQL
- ✅ Fazer scraping com sucesso
- ✅ Encontrar 278-281 carros

**Tudo pronto para usar!** 🚀
