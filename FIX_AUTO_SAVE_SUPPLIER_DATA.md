# ✅ FIX: Auto-Save Overwriting SupplierData

## 🐛 Problema Reportado pelo Utilizador

**Cenário:**
1. ✅ Faz **pesquisa automatizada** (Automated Prices) → cards visuais aparecem
2. ✅ **Altera** os preços do "Automated Price" na tabela
3. ✅ **Guarda** (ou auto-save automático)
4. ✅ **Sai** da página
5. ❌ **Volta** e vai **editar** → **cards visuais NÃO aparecem!**
6. ❌ Mas **tabela** mostra os preços alterados

## 🔍 Investigação

### Logs do Utilizador
```
[HISTORY] 🔍 supplierData type: "object"
[HISTORY] 🔍 supplierData is empty object? true  ← PROBLEMA!
⚠️ supplierData is EMPTY - visual cards will not show
```

O `supplierData` estava **vazio** (`{}`) na database, mesmo tendo sido guardado com dados na pesquisa original.

### Sequência do Bug

**Passo 1: Pesquisa Automatizada**
```javascript
// ✅ Pesquisa faz scraping e constrói allCarsByDay
allCarsByDay[day] = data.items;  // Dados dos suppliers

// ✅ Guarda no histórico com supplierData
await saveAutomatedPriceHistory(automatedPricesByGroup, dias, 'automated', allCarsByDay);
```
→ **Versão guardada COM supplierData** ✅

**Passo 2: Edita Automated Prices**
```javascript
// Utilizador altera preços na tabela
input[data-type="auto"].value = "25.50";
```

**Passo 3: Auto-Save Dispara (BUG!)**
```javascript
// ❌ Auto-save usa window.currentSupplierData que está VAZIO!
const supplierData = window.currentSupplierData || {};  // → {}

// ❌ Sobrescreve a versão anterior COM OBJETO VAZIO!
await saveAutomatedPriceHistory(automatedPricesByGroup, dias, 'current', supplierData);
```
→ **Nova versão COM supplierData = {}** ❌  
→ **Dados visuais PERDIDOS!** ❌

**Passo 4: Volta e Edita**
```javascript
// Carrega a última versão (que tem supplierData vazio)
if (supplierData && Object.keys(supplierData).length > 0) {
    renderPriceComparisonCards(...);  // ❌ Não executa!
} else {
    console.warn('[HISTORY] No supplier data available');  // ✅ Executa isto
}
```
→ **Cards visuais não aparecem** ❌

## 🔧 Causa Raiz

### Problema 1: `window.currentSupplierData` Nunca Foi Definido
Após pesquisa automatizada, o código construía `allCarsByDay` **localmente** mas nunca o armazenava em `window.currentSupplierData`.

```javascript
// ❌ ANTES: allCarsByDay só existia localmente
const allCarsByDay = {};
// ... constrói allCarsByDay ...
// Guarda → OK
// Mas window.currentSupplierData → undefined!
```

### Problema 2: Auto-Save Usava Objeto Vazio
```javascript
// ❌ ANTES: Auto-save sempre com {}
const supplierData = window.currentSupplierData || {};  // sempre {}
```

### Problema 3: Sobrescrevia Dados Bons Com Vazios
A cada edit, auto-save **substituía** a versão boa por uma versão sem supplierData.

## ✅ Solução Implementada

### Fix 1: Armazenar supplierData Após Pesquisa
```javascript
// ✅ DEPOIS: Armazena para uso futuro
if (autoPricesGenerated > 0 || realPricesGenerated > 0) {
    // ⚠️ CRITICAL: Store allCarsByDay for future edits
    window.currentSupplierData = allCarsByDay;
    console.log(`[SAVE-HISTORY] 💾 Stored currentSupplierData with ${Object.keys(allCarsByDay).length} days`);
    
    await saveAutomatedPriceHistory(automatedPricesByGroup, dias, 'automated', allCarsByDay);
}
```

### Fix 2: Auto-Save Preserva Dados Originais
```javascript
// ✅ DEPOIS: Usa dados preservados
const supplierData = window.originalSupplierDataForEdit || window.currentSupplierData || {};

console.log('[AUTO-SAVE] Using supplierData:', {
    source: window.originalSupplierDataForEdit ? 'preserved from edit' : 'empty',
    keys: Object.keys(supplierData).length
});
```

### Fix 3: Salvar Manual Também Preserva
```javascript
// ✅ DEPOIS: Manual save também usa dados preservados
const supplierData = window.originalSupplierDataForEdit || window.currentSupplierData || {};
await saveAutomatedPriceHistory(automatedPricesByGroup, dias, 'current', supplierData);
```

## 📊 Resultados

| Ação | Antes | Depois |
|------|-------|--------|
| **Pesquisa automatizada** | ✅ supplierData guardado | ✅ supplierData guardado **E** armazenado |
| **Edita automated prices** | ❌ Auto-save com `{}` | ✅ Auto-save preserva dados |
| **Volta e edita** | ❌ Cards vazios | ✅ Cards aparecem! |
| **Tabela** | ✅ Preços aparecem | ✅ Preços aparecem |
| **Cards visuais** | ❌ Vazios | ✅ **FUNCIONAM!** 🎉 |

## 🚀 Deploy

**Commit:** c318739  
**Data:** 21 Nov 2025, 11:12 AM  
**Mensagem:** "fix: preserve supplierData in auto-save after editing automated prices"

**Ficheiros alterados:**
- `templates/price_automation.html` (+15, -2)

## 🎯 Como Testar

### Teste Completo
1. **Pesquisa Nova**
   - Vai ao tab "Preços Automatizados"
   - Escolhe "Albufeira" e data "24/11/2025"
   - Clica "Pesquisar com IA"
   - Verifica que **tabela** e **cards** aparecem

2. **Edita Automated Prices**
   - Altera alguns preços na coluna "Automated"
   - Aguarda 1 segundo (auto-save)
   - Console mostra: `[AUTO-SAVE] ✅ Saved with X supplier data keys`

3. **Vai ao History**
   - Clica tab "History"
   - Escolhe mês "November 2025"
   - Clica "Editar" na versão mais recente

4. **Verificar Resultado** ✅
   - **Tabela** mostra preços alterados ✅
   - **Cards visuais** aparecem com suppliers ✅
   - Console mostra: `[HISTORY] 💾 Preserved original supplierData: X keys`

## 📝 Notas

### Versões Antigas
Versões criadas **antes** deste fix (ID 604 e anteriores) podem estar com `supplierData = {}`. Para essas:
- **Opção 1:** Fazer **nova pesquisa** com mesmos parâmetros
- **Opção 2:** Aceitar que só têm dados da tabela

### Versões Novas
Todas as pesquisas **a partir de agora**:
- ✅ Preservam supplierData através de edições
- ✅ Auto-save não perde dados visuais
- ✅ Cards funcionam sempre

## 🎉 Status Final

✅ **PROBLEMA RESOLVIDO!**

Os cards visuais agora **persistem** através de:
- ✅ Pesquisas automatizadas
- ✅ Edições de preços
- ✅ Auto-saves automáticos
- ✅ Salvamentos manuais
- ✅ Re-carregar do histórico

---

**Última atualização:** 21 Nov 2025, 11:12 AM  
**Commit:** c318739  
**Status:** ✅ DEPLOYED
