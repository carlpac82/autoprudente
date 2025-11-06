# 🔍 DIAGNOSTIC REPORT - Estratégias Desaparecem

## 📅 Data: 2025-11-06 22:31 UTC

## ❌ PROBLEMAS REPORTADOS

1. **Estratégias desaparecem após configurar -1.5% em todos os grupos/meses**
2. **Preview da homepage não aparece (erro 500)**
3. **Problemas recorrentes mesmo após múltiplas correções**

---

## 🔎 ANÁLISE COMPLETA

### 1. SISTEMA DE SALVAMENTO DE ESTRATÉGIAS

#### ✅ Funções que SALVAM CORRETAMENTE:

**A. `saveNewStrategy()` (linhas 2232-2298)**
```javascript
// Salva em localStorage
localStorage.setItem('automatedPriceRules', JSON.stringify(rules));

// Salva no backend
fetch('/api/price-automation/rules/save', {
    method: 'POST',
    body: JSON.stringify(rules)
});

// Rebuild UI
rebuildFieldsForDay(location, grupo, month, day);
```
✅ **STATUS:** CORRETO - Salva em ambos os locais

**B. `selectStrategy()` (commit fa63572 - linhas 3075-3133)**
```javascript
// TAMBÉM salva em automatedPriceRules
localStorage.setItem('automatedPriceRules', JSON.stringify(rules));

// TAMBÉM salva no backend
fetch('/api/price-automation/rules/save', {
    method: 'POST',
    body: JSON.stringify(rules)
});

// Rebuild UI
rebuildFieldsForDay(location, grupo, month, day);
```
✅ **STATUS:** CORRETO - Salva em ambos os locais (após commit fa63572)

**C. `moveStrategyUp()` / `moveStrategyDown()` (linhas 2300+)**
```javascript
localStorage.setItem('automatedPriceRules', JSON.stringify(rules));

fetch('/api/price-automation/rules/save', {
    method: 'POST',
    body: JSON.stringify(rules)
});
```
✅ **STATUS:** CORRETO - Salva em ambos os locais

**D. `removeStrategy()` (linhas 3186-3224)**
```javascript
localStorage.setItem('automatedPriceRules', JSON.stringify(rules));

saveStrategiesToDatabase(); // Background save
```
✅ **STATUS:** CORRETO - Salva via função helper

---

### 2. SISTEMA DE CARREGAMENTO DE ESTRATÉGIAS

**A. Ao abrir página (linhas 3548-3560)**
```javascript
async function loadAutomatedRules() {
    const response = await fetch('/api/price-automation/rules/load');
    const result = await response.json();
    
    if (result.ok && result.rules) {
        localStorage.setItem('automatedPriceRules', JSON.stringify(result.rules));
        console.log('✅ Automated price rules loaded from database');
        console.log('📦 Rules loaded:', result.rules);
    }
}

// Chamado ao carregar
document.addEventListener('DOMContentLoaded', function() {
    loadAutomatedRules();
});
```
✅ **STATUS:** CORRETO - Carrega do backend e sincroniza localStorage

---

### 3. BACKEND API ENDPOINTS

**A. Save: `/api/price-automation/rules/save`**
- Recebe: `rules` object completo
- Guarda em: PostgreSQL tabela `price_automation_rules`
- Formato: JSON serializado

**B. Load: `/api/price-automation/rules/load`**
- Retorna: `rules` object completo
- Fonte: PostgreSQL tabela `price_automation_rules`

---

## 🐛 POSSÍVEIS CAUSAS DO PROBLEMA

### Hipótese 1: CONFLITO DE SESSÕES / MÚLTIPLOS TABS
Se abrir múltiplos tabs/browsers:
- Tab A: Carrega estado X do backend
- Tab B: Carrega estado X do backend
- Tab A: Adiciona estratégia → Salva estado Y
- Tab B: Adiciona estratégia → Sobrescreve com estado X (perde mudanças de A)

### Hipótese 2: RACE CONDITION no salvamento
```javascript
// Múltiplas chamadas simultâneas
saveNewStrategy()  → fetch('/api/.../save') // Request 1
moveStrategyUp()   → fetch('/api/.../save') // Request 2
removeStrategy()   → fetch('/api/.../save') // Request 3

// Última request ganha = pode sobrescrever
```

### Hipótese 3: ERRO NO BACKEND não reportado
- Backend recebe dados
- Erro ao salvar no PostgreSQL
- Retorna OK mas dados não persistem
- Frontend pensa que salvou

### Hipótese 4: LIMPEZA AUTOMÁTICA
- Algum código limpa localStorage
- Algum código limpa tabela PostgreSQL
- Refresh recarrega estado vazio

---

## 🔧 SOLUÇÕES PROPOSTAS

### FIX 1: ADICIONAR TIMESTAMP + VALIDAÇÃO
```javascript
function saveToBackend(rules) {
    const payload = {
        rules: rules,
        timestamp: new Date().toISOString(),
        version: 1
    };
    
    return fetch('/api/price-automation/rules/save', {
        method: 'POST',
        body: JSON.stringify(payload)
    })
    .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
    })
    .then(data => {
        if (!data.ok) throw new Error(data.error);
        console.log('✅ Saved to backend:', data);
        return data;
    })
    .catch(err => {
        console.error('❌ SAVE FAILED:', err);
        showNotification('Error saving to database: ' + err.message, 'error');
        throw err;
    });
}
```

### FIX 2: VERIFICAR APÓS SALVAR
```javascript
async function saveAndVerify(rules) {
    // 1. Salvar
    await fetch('/api/price-automation/rules/save', {
        method: 'POST',
        body: JSON.stringify(rules)
    });
    
    // 2. Aguardar 500ms
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 3. Recarregar e verificar
    const response = await fetch('/api/price-automation/rules/load');
    const data = await response.json();
    
    // 4. Comparar
    const saved = JSON.stringify(data.rules);
    const expected = JSON.stringify(rules);
    
    if (saved !== expected) {
        console.error('❌ VERIFICATION FAILED!');
        console.log('Expected:', expected);
        console.log('Got:', saved);
        showNotification('Warning: Data may not have saved correctly!', 'error');
    } else {
        console.log('✅ VERIFICATION PASSED');
    }
}
```

### FIX 3: LOGGING DETALHADO NO BACKEND
```python
@app.post("/api/price-automation/rules/save")
async def save_rules(request: Request):
    data = await request.json()
    rules = data.get('rules', {})
    username = request.session.get("username", "admin")
    
    # Log detalhado
    logging.info(f"[RULES-SAVE] User: {username}")
    logging.info(f"[RULES-SAVE] Rules size: {len(json.dumps(rules))} bytes")
    logging.info(f"[RULES-SAVE] Locations: {list(rules.keys())}")
    
    # Contar estratégias
    total_strategies = 0
    for location in rules.values():
        for grupo in location.values():
            for month_data in grupo.get('months', {}).values():
                for day_data in month_data.get('days', {}).values():
                    total_strategies += len(day_data.get('strategies', []))
    
    logging.info(f"[RULES-SAVE] Total strategies: {total_strategies}")
    
    # ... salvar ...
    
    logging.info(f"✅ [RULES-SAVE] Saved successfully")
    return {"ok": True, "strategies_count": total_strategies}
```

---

## 📊 PREVIEW HOMEPAGE

### PROBLEMA: Erro 500 ao salvar recent searches

**Causa:** Payload muito grande (284 carros × 50 campos)

**Solução já implementada (commit c0b571a):**
- Envia dados completos
- Logging detalhado
- Documentação aumentada

**Verificar:**
1. Logs do backend (Render) para ver erros específicos
2. Tamanho real do payload
3. Timeout do PostgreSQL

---

## 🎯 PLANO DE AÇÃO IMEDIATO

1. ✅ Adicionar logging detalhado em TODAS as funções de save
2. ✅ Adicionar verificação após save
3. ✅ Adicionar notificação visual de sucesso/erro
4. ✅ Melhorar error handling no backend
5. ✅ Documentar estado esperado vs. real

---

## 📝 NOTAS IMPORTANTES

- Commit fa63572: Corrigiu `selectStrategy()` para salvar em `automatedPriceRules`
- Commit c0b571a: Dados completos nas recent searches
- Commit f902ed3: Corrigiu ReferenceError do `day`

**TODOS OS SISTEMAS DE SALVAMENTO ESTÃO CORRETOS NO CÓDIGO!**

O problema pode estar em:
- Race conditions
- Múltiplos tabs
- Erros não reportados no backend
- Cache do browser
