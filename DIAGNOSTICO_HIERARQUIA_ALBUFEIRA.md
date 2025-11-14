# 🔍 DIAGNÓSTICO - Hierarquia Não Funciona em Albufeira

## ❌ Problema Observado

**Sintomas:**
- ✅ Hierarquia configurada no Admin (Imagem 1 mostra regras B1<B2, B1<D, etc)
- ✅ Checkbox "Ativar Validação de Hierarquia de Grupos" parece marcada
- ❌ **D - Economy** aparece mais barato (24.60€) que B1 (39.45€) e B2 (40.35€)
- ❌ **Viola regra:** B1 < D (D deveria ser ≥ B1)

**Console logs mostram:**
```
[SAVE-HISTORY] Checking if should save: autoPricesGenerated=14
[SAVE-FUNCTION] Collected prices: {D: {5: 24.60}, B1: {5: 39.45}, ...}
```

**NÃO aparece:**
```
🔧 [HIERARCHY] Starting for location: Albufeira
🔧 [HIERARCHY] Applying dependency rules...
```

---

## 🔍 DIAGNÓSTICO PASSO A PASSO

### 1. Verificar localStorage

Abre **DevTools** (F12) → **Console** e executa:

```javascript
// 1. Ver todas as settings
const settings = JSON.parse(localStorage.getItem('priceAutomationSettings') || '{}');
console.log('Settings completas:', settings);

// 2. Ver se hierarquia está ativa
console.log('Hierarquia ativa?', settings.enableGroupHierarchy);

// 3. Ver regras configuradas
console.log('Regras:', settings.groupHierarchyRules);

// 4. Ver se tem regras para cada grupo
if (settings.groupHierarchyRules) {
    console.log('Grupos com regras:', Object.keys(settings.groupHierarchyRules));
    for (const [grupo, regras] of Object.entries(settings.groupHierarchyRules)) {
        console.log(`  ${grupo}:`, regras);
    }
}
```

**Resultado Esperado:**
```javascript
Hierarquia ativa? true
Regras: {
  "D": [
    {group: "B2", operator: ">=", percentage: -5},
    {group: "B1", operator: ">=", percentage: -6}
  ],
  "E2": [...],
  ...
}
Grupos com regras: ["D", "E2", "F", ...]
```

**❌ Se aparecer:**
```javascript
Hierarquia ativa? undefined  // OU false
Regras: undefined  // OU {}
```

**→ CAUSA:** Settings não foram salvas no localStorage

---

### 2. Verificar Checkbox Ativa

No painel **Admin Settings → Price Adjustment → Group Hierarchy:**

```javascript
// No console:
const checkbox = document.getElementById('enableGroupHierarchy');
console.log('Checkbox existe?', !!checkbox);
console.log('Checkbox marcada?', checkbox?.checked);
```

**Resultado Esperado:**
```
Checkbox existe? true
Checkbox marcada? true
```

**❌ Se `checkbox.checked = false`:**
- Marca a checkbox manualmente
- Clica "Save Settings" (botão azul no topo)
- Aguarda confirmação
- Re-testa

---

### 3. Forçar Reload das Settings

No **Admin Settings:**

```javascript
// No console:
async function reloadSettings() {
    console.log('[DEBUG] Reloading settings from database...');
    
    const response = await fetch('/api/price-automation/settings/load');
    const result = await response.json();
    
    console.log('[DEBUG] Server response:', result);
    
    if (result.ok && result.settings) {
        console.log('[DEBUG] enableGroupHierarchy:', result.settings.enableGroupHierarchy);
        console.log('[DEBUG] groupHierarchyRules:', result.settings.groupHierarchyRules);
        
        // Salvar no localStorage
        localStorage.setItem('priceAutomationSettings', JSON.stringify(result.settings));
        console.log('[DEBUG] Saved to localStorage');
        
        return result.settings;
    } else {
        console.error('[DEBUG] Failed to load settings:', result);
    }
}

const settings = await reloadSettings();
```

**Resultado Esperado:**
```
[DEBUG] Server response: {ok: true, settings: {...}}
[DEBUG] enableGroupHierarchy: true
[DEBUG] groupHierarchyRules: {D: [...], E2: [...], ...}
[DEBUG] Saved to localStorage
```

---

### 4. Testar Hierarquia Manualmente

No **Price Automation** (tab Preços Automatizados):

```javascript
// No console, após gerar preços:
async function testHierarchy() {
    console.log('[TEST] Testing hierarchy rules...');
    
    // Carregar settings
    const settings = JSON.parse(localStorage.getItem('priceAutomationSettings') || '{}');
    console.log('[TEST] enableGroupHierarchy:', settings.enableGroupHierarchy);
    console.log('[TEST] Rules:', settings.groupHierarchyRules);
    
    if (!settings.enableGroupHierarchy) {
        console.error('[TEST] ❌ Hierarchy is DISABLED!');
        return;
    }
    
    if (!settings.groupHierarchyRules || Object.keys(settings.groupHierarchyRules).length === 0) {
        console.error('[TEST] ❌ No rules configured!');
        return;
    }
    
    // Chamar função de hierarquia
    console.log('[TEST] Calling applyGroupHierarchyRules()...');
    const adjusted = await applyGroupHierarchyRules();
    console.log('[TEST] Adjusted prices:', adjusted);
}

await testHierarchy();
```

**Resultado Esperado:**
```
[TEST] enableGroupHierarchy: true
[TEST] Rules: {D: [...], ...}
[TEST] Calling applyGroupHierarchyRules()...
🔧 [HIERARCHY] Starting for location: Albufeira
🔧 [HIERARCHY] Applying dependency rules for Albufeira: {D: [...]}
🔧 [HIERARCHY] D/5d: 24.60€ → 39.45€ (must respect: B1 (39.45€))
[TEST] Adjusted prices: 1
```

---

## ✅ SOLUÇÕES

### Solução 1: Checkbox Desmarcada

**Passos:**
1. Admin Settings → Price Adjustment
2. Scroll até "Group Hierarchy Validation"
3. ✅ Marca checkbox "Ativar Validação de Hierarquia de Grupos"
4. Clica **"Save Settings"** (botão azul no topo)
5. Aguarda confirmação "Settings saved"
6. Vai para Price Automation
7. Nova pesquisa para Albufeira

---

### Solução 2: Settings Não Salvas

**Passos:**
1. Admin Settings → Group Hierarchy
2. Verifica se regras aparecem na lista (B1 < B2, B1 < D, etc)
3. Se não aparecem:
   - Clica "Configurar Dependências"
   - Seleciona grupo (ex: D)
   - Marca dependências (B2, B1)
   - Escolhe operador (< ou >=)
   - Clica "Apply Rules"
   - **IMPORTANTE:** Clica "Save Settings" no topo
4. Refresh da página (F5)
5. Verifica se regras ainda aparecem
6. Nova pesquisa

---

### Solução 3: Forçar Sincronização Manual

**Se nada funcionar, forçar no console:**

```javascript
// 1. Configurar manualmente
const manualSettings = {
    enableGroupHierarchy: true,
    groupHierarchyRules: {
        "D": [
            {group: "B2", operator: ">=", percentage: -5},
            {group: "B1", operator: ">=", percentage: -6}
        ],
        "E2": [
            {group: "D", operator: ">=", percentage: -3},
            {group: "E1", operator: ">=", percentage: -2}
        ],
        "F": [
            {group: "D", operator: ">=", percentage: -10},
            {group: "E2", operator: ">=", percentage: -5}
        ],
        "L1": [
            {group: "F", operator: ">=", percentage: -8}
        ]
    }
};

// 2. Salvar no servidor
const response = await fetch('/api/price-automation/settings/save', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(manualSettings)
});

console.log('Saved to server:', await response.json());

// 3. Salvar no localStorage
localStorage.setItem('priceAutomationSettings', JSON.stringify(manualSettings));
console.log('Saved to localStorage');

// 4. Recarregar página
location.reload();
```

---

## 🧪 TESTE FINAL

Após aplicar qualquer solução:

1. **Nova Pesquisa Albufeira:**
   - Localização: Albufeira
   - Data: 5 dias
   - Gerar preços

2. **Verificar Console:**
   ```
   🔧 [HIERARCHY-CALL] About to call applyGroupHierarchyRules()...
   🔧 [HIERARCHY] Starting for location: Albufeira
   🔧 [HIERARCHY] Applying dependency rules for Albufeira: {...}
   🔧 [HIERARCHY] D/5d: 24.60€ → 39.45€ (must respect: B1 (39.45€))
   🔧 [HIERARCHY] Adjusted 1 prices to respect dependency rules
   ```

3. **Verificar Resultados:**
   - D - Economy: ≥ 39.45€ (não mais 24.60€) ✅
   - B1 - Mini 4 Seats: 39.45€ ✅
   - B2 - Mini 5 Seats: 40.35€ ✅

---

## 📊 COMPARAÇÃO ANTES/DEPOIS

### ANTES ❌
```
B1 - Mini 4 Seats: 39.45€
B2 - Mini 5 Seats: 40.35€
D - Economy: 24.60€  ← BEST PRICE (ERRADO!)
```
❌ Viola: B1 < D (24.60 < 39.45)

### DEPOIS ✅
```
B1 - Mini 4 Seats: 39.45€  ← BEST PRICE
B2 - Mini 5 Seats: 40.35€
D - Economy: 39.45€  (ajustado para = B1)
```
✅ Respeita: B1 < D (39.45 ≤ 39.45)

---

## 🔧 DEBUG AVANÇADO

Se o problema persistir, adicionar logs extras:

```javascript
// No price_automation.html, linha 1426, ANTES de:
// if (!settings.enableGroupHierarchy || !settings.groupHierarchyRules) {

// ADICIONAR:
console.log('[HIERARCHY-DEBUG] Settings:', {
    enableGroupHierarchy: settings.enableGroupHierarchy,
    hasRules: !!settings.groupHierarchyRules,
    rulesCount: settings.groupHierarchyRules ? Object.keys(settings.groupHierarchyRules).length : 0,
    fullSettings: settings
});
```

Isso vai mostrar exatamente o que está (ou não está) carregado.

---

## ✅ CHECKLIST

- [ ] Checkbox "Ativar Validação" está marcada
- [ ] Regras aparecem na lista do Admin Settings
- [ ] Clicou "Save Settings" após configurar
- [ ] localStorage tem `enableGroupHierarchy: true`
- [ ] localStorage tem `groupHierarchyRules` com regras
- [ ] Logs de hierarquia aparecem no console
- [ ] Preços são ajustados após gerar
- [ ] D ≥ B1 e D ≥ B2 no resultado final

---

**Testa isto e diz-me o que encontraste! 🔍**
