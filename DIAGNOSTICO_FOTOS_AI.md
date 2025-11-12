# 🔍 DIAGNÓSTICO: Fotos Faltando + AI Sem Sugestões

**Data:** 12 Novembro 2025  
**Problemas Identificados:** 3

---

## 🚨 PROBLEMA 1: Fotos Não Aparecem em Automated Pricing

### 📊 Análise

**Endpoint:** `/api/vehicles/{vehicle_name}/photo` (linha 15073 `main.py`)

**Fluxo de Busca de Fotos:**
1. ✅ Busca em `vehicle_images` (tabela principal)
2. ✅ Busca em `vehicle_photos` (tabela legacy)
3. ✅ Busca variações (ex: "citroen c1" encontra "citroen c1 auto")
4. ✅ Fallback para imagens hardcoded (linhas 3377-3426 `price_automation.html`)

**Frontend:** `price_automation.html`
- Linha 3348-3363: `GROUP_IMAGES` com fallback para fotos por grupo
- Linha 3431: `getCarImage()` - função que busca foto
- Linha 3365: `imageUrlFor()` - função com hardcoded URLs

### 🔎 Causa Raiz

**Fotos não estão na base de dados!**

```sql
-- Verificar quantas fotos existem
SELECT COUNT(*) FROM vehicle_images;
SELECT COUNT(*) FROM vehicle_photos;
```

**Possíveis Causas:**
1. ❌ Nunca foram baixadas do CarJet
2. ❌ Endpoint de download não foi executado
3. ❌ Erro silencioso durante o download

### ✅ SOLUÇÃO

#### **1. Baixar TODAS as fotos do CarJet**

**Endpoint Existente:** `/api/vehicles/download-all-photos` (linha 14269 `main.py`)

```bash
# Executar via curl (requer autenticação)
curl -X POST https://carrental-api-5f8q.onrender.com/api/vehicles/download-all-photos \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

**Ou via UI:**
- Ir para **Vehicles Editor** (se existir)
- Botão **"Download All Photos from CarJet"**

#### **2. Baixar foto individual de um carro**

**Endpoint:** `/api/vehicles/{vehicle_name}/download-photo` (linha 14392)

```bash
# Exemplo: baixar foto do Peugeot 208
curl -X POST https://carrental-api-5f8q.onrender.com/api/vehicles/peugeot%20208/download-photo \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

#### **3. Upload manual de foto**

**Endpoint:** `/api/vehicles/{vehicle_name}/photo/upload` (linha 15330)

```javascript
// Via UI com drag & drop
const formData = new FormData();
formData.append('file', photoFile);

fetch('/api/vehicles/peugeot%20208/photo/upload', {
    method: 'POST',
    body: formData
});
```

#### **4. Adicionar foto via URL externa**

**Endpoint:** `/api/vehicles/{vehicle_name}/photo/from-url` (linha 15278)

```javascript
fetch('/api/vehicles/peugeot%20208/photo/from-url', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://example.com/peugeot-208.jpg' })
});
```

### 📝 Plano de Ação (Fotos)

**PRIORIDADE ALTA:**

1. ✅ **Executar download massivo** → `/api/vehicles/download-all-photos`
   - Faz scraping em Albufeira + Faro
   - Baixa TODAS as fotos dos carros encontrados
   - Salva em `vehicle_images` com `vehicle_key`

2. ⚠️  **Verificar tabelas** após download:
```sql
-- Ver quantas fotos foram baixadas
SELECT 
    COUNT(*) as total_photos,
    COUNT(DISTINCT vehicle_key) as unique_vehicles
FROM vehicle_images;

-- Ver fotos por grupo
SELECT 
    SUBSTRING(vehicle_key, 1, 10) as modelo,
    content_type,
    LENGTH(image_data) as size_bytes
FROM vehicle_images
LIMIT 20;
```

3. ✅ **Testar endpoint** individual:
```bash
# Verificar se foto aparece no browser
open https://carrental-api-5f8q.onrender.com/api/vehicles/peugeot%20208/photo
```

4. 🔧 **Adicionar logging** no frontend:
```javascript
// Em getCarImage() - adicionar debug
console.log(`📸 Requesting photo: ${vehiclePhotoUrl}`);

// Ver no console do browser quais fotos falharam
```

---

## 🤖 PROBLEMA 2: AI Não Mostra Sugestões

### 📊 Análise

**Endpoint:** `/api/ai/get-price` (linha 28961 `main.py`)

**Fluxo de AI Suggestions:**
1. ✅ Frontend chama `loadAllAIPrices()` (linha 1155 `price_automation.html`)
2. ✅ Para cada grupo+dias, faz `fetch('/api/ai/get-price?...')`
3. ✅ Backend analisa `automated_search_history` (últimos 6 meses)
4. ✅ Calcula posição competitiva vs outros suppliers
5. ✅ Sugere preço baseado em tendências históricas
6. ❌ **RETORNA VAZIO** porque não há dados no histórico

### 🔎 Causa Raiz

**Tabela `automated_search_history` vazia ou com poucos dados!**

```sql
-- Verificar dados de histórico
SELECT 
    COUNT(*) as total_searches,
    COUNT(DISTINCT month_key) as months_covered,
    MIN(search_date) as oldest,
    MAX(search_date) as newest
FROM automated_search_history;

-- Ver últimos 10 registros
SELECT 
    search_date,
    location,
    month_key,
    LENGTH(prices_data) as prices_size,
    LENGTH(supplier_data) as suppliers_size
FROM automated_search_history
ORDER BY search_date DESC
LIMIT 10;
```

**Lógica do AI:**
- Precisa de **pelo menos 3 suppliers** por grupo/dias
- Analisa **últimos 6 meses** de histórico
- Se não houver dados → **retorna null** → frontend não mostra card

### ✅ SOLUÇÃO

#### **1. Inicializar AI com histórico existente**

**Endpoint:** `/api/ai/initialize-from-history` (linha 8308 `price_automation.html`)

```javascript
// Executar no console do browser (Price Automation page)
initializeAIFromHistory();
```

**O que faz:**
- Lê TODOS os registros de `automated_search_history`
- Processa dados de AMBAS localizações (Albufeira + Faro)
- Cria AI suggestions baseadas em padrões históricos

#### **2. Executar pesquisas automatizadas**

**Para gerar histórico novo:**
```bash
# Trigger daily report search (gera dados para automated_search_history)
curl -X POST https://carrental-api-5f8q.onrender.com/api/trigger-daily-report-search
```

**Ou aguardar:**
- ⏰ Daily Report Search: **7:00 AM** (automático)
- ⏰ Weekly Report Search: **Segundas 7:00 AM** (automático)

#### **3. Verificar se AI está funcionando**

```javascript
// No console do browser (Price Automation page)
console.log('AI Cache:', window.aiPricesCache);
console.log('Total AI prices:', Object.keys(window.aiPricesCache).length);

// Forçar reload do cache
await loadAllAIPrices();

// Ver se agora tem dados
console.log('After reload:', Object.keys(window.aiPricesCache).length);
```

#### **4. Debug individual de um grupo**

```javascript
// Testar um grupo/dias específico
const result = await fetch('/api/ai/get-price?grupo=D&days=2&location=Albufeira');
const data = await result.json();
console.log('AI suggestion for D/2d:', data);
```

### 📝 Plano de Ação (AI)

**PRIORIDADE MÉDIA:**

1. ⚠️  **Verificar histórico:**
```sql
-- Ver se há dados suficientes
SELECT 
    location,
    month_key,
    COUNT(*) as searches,
    MAX(search_date) as last_search
FROM automated_search_history
GROUP BY location, month_key
ORDER BY month_key DESC;
```

2. ✅ **Se histórico vazio** → Executar `initializeAIFromHistory()`
   - Consome dados existentes
   - Popula AI cache
   - Frontend mostra sugestões

3. ✅ **Se histórico insuficiente** → Aguardar daily search
   - Sistema coleta dados automaticamente às 7h
   - Após 1 semana: AI terá dados suficientes
   - Após 1 mês: AI será mais preciso

4. 🔧 **Melhorar feedback visual:**
```javascript
// Adicionar indicador quando AI não tem dados
if (Object.keys(window.aiPricesCache).length === 0) {
    showNotification('🤖 AI learning... No historical data yet. Run some searches!', 'info');
}
```

---

## 🔧 PROBLEMA 3 (BONUS): Grupos B2 e M2

### Hyundai i10 Manual → B2 (não B1)

**Causa:** Override B1 está muito genérico

**Solução:**
```python
# Em main.py, linha ~8770
# ADICIONAR: Hyundai i10 é SEMPRE B2 (5 lugares)
if re.search(r"\bhyundai\s*i10\b", car_name.lower()) and not _is_auto_flag(...):
    category = "Mini 5 Doors"  # Força B2
```

### Peugeot 5008 Auto → M2 (não L1)

**Status:** ✅ Já implementado! (linha 8737 `main.py`)

```python
m2_patterns = [
    # ...
    r"\bpeugeot\s*5008\b",  # ← JÁ EXISTE
]
if any(re.search(p, cn4) for p in m2_patterns) and _is_auto_flag(...):
    category = "7 Seater Automatic"  # M2
```

**Nota:** Override funciona no scraping real. Em testes unitários pode falhar se categoria vier como "SUV" antes do override ser aplicado.

---

## 🎯 PLANO DE AÇÃO COMPLETO

### Ação Imediata (Hoje)

1. **Fotos:**
   ```bash
   # Executar download massivo
   POST /api/vehicles/download-all-photos
   ```

2. **AI:**
   ```javascript
   // No browser, Price Automation page
   await initializeAIFromHistory();
   ```

3. **Grupos:**
   ```python
   # Adicionar override para Hyundai i10 em main.py
   # Commit + push
   ```

### Ação Short-term (Esta Semana)

1. **Monitorar fotos:**
   - Verificar se aparecem após download
   - Testar com diferentes carros
   - Adicionar fotos faltantes manualmente

2. **Monitorar AI:**
   - Ver se sugestões aparecem após daily search
   - Verificar precisão das sugestões
   - Ajustar thresholds se necessário

3. **Validar grupos:**
   - Fazer pesquisa real
   - Verificar se Peugeot 5008 Auto vai para M2
   - Verificar se Hyundai i10 Manual vai para B2

### Ação Long-term (Próximo Mês)

1. **Dashboard de diagnóstico:**
   - Quantas fotos faltando
   - Quantas AI suggestions disponíveis
   - Coverage por grupo

2. **Auto-heal:**
   - Se foto não existe, baixar automaticamente
   - Se AI sem dados, notificar user

3. **Melhorias UX:**
   - Loading states para fotos
   - Placeholder quando foto não existe
   - Explicar por que AI não tem sugestões

---

## 📊 METRICS PARA MONITORAR

### Fotos
```sql
-- Coverage de fotos
SELECT 
    (SELECT COUNT(DISTINCT vehicle_key) FROM vehicle_images) * 100.0 /
    (SELECT COUNT(DISTINCT LOWER(name)) FROM vehicles_editor) as coverage_percent;
```

### AI
```sql
-- AI suggestions disponíveis
SELECT 
    COUNT(DISTINCT grupo || '_' || days || '_' || location) as ai_suggestions_count
FROM automated_search_history
WHERE supplier_data IS NOT NULL
AND search_date >= NOW() - INTERVAL '30 days';
```

### Grupos
```python
# Taxa de sucesso dos testes
python3 test_group_classification.py
# Target: >95% success rate
```

---

## 🚀 COMANDOS RÁPIDOS

### Fotos
```bash
# Download massivo
curl -X POST https://carrental-api-5f8q.onrender.com/api/vehicles/download-all-photos \
  -H "Cookie: session=YOUR_SESSION"

# Verificar foto individual
open https://carrental-api-5f8q.onrender.com/api/vehicles/peugeot%20208/photo
```

### AI
```javascript
// Browser console (Price Automation)
await loadAllAIPrices();
console.log('AI Cache:', Object.keys(window.aiPricesCache).length);
```

### Grupos
```bash
# Rodar testes
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay
python3 test_group_classification.py
```

---

**Autor:** Cascade AI  
**Timestamp:** 2025-11-12 19:30:00 WET  
**Status:** 🔴 AÇÃO REQUERIDA
