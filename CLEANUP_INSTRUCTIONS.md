# 🧹 Instruções de Limpeza de Duplicados

## ⚠️ Problema
Após o deploy, ainda aparecem **199 versões duplicadas** em Dezembro porque:
- ✅ O código UPSERT **previne novas duplicações** (funciona!)
- ❌ Mas as **duplicações antigas** ainda estão na base de dados

## ✅ Solução: Executar Cleanup

### **Opção 1: Via Browser (RECOMENDADO)** 🌐

1. **Aguardar deploy** (~5 minutos após push)
   - URL: https://carrental-api-5f8q.onrender.com

2. **Abrir página de cleanup**:
   ```
   https://carrental-api-5f8q.onrender.com/cleanup-ui
   ```

3. **Clicar em "Run Cleanup Now"**
   - O sistema vai mostrar:
     - **Before**: Número total de entradas antes
     - **After**: Número total após limpeza
     - **Deleted**: Quantas duplicadas foram removidas

4. **Aguardar confirmação** ✅

5. **Refresh histórico**:
   - Voltar para: https://carrental-api-5f8q.onrender.com/price-automation
   - Ir para aba "History"
   - Filtrar "Aeroporto de Faro"
   - **Deve mostrar**: Apenas 1-2 versões em vez de 199!

---

### **Opção 2: Via API (cURL)**

```bash
curl -X POST https://carrental-api-5f8q.onrender.com/api/automated-search/cleanup-duplicates \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -H "Content-Type: application/json"
```

**Resposta esperada**:
```json
{
  "ok": true,
  "message": "Cleanup completed successfully",
  "before": 500,
  "after": 200,
  "deleted": 300
}
```

---

### **Opção 3: Via Script Python**

```bash
# No Render Shell ou localmente
export DATABASE_URL="postgresql://..."
python cleanup_duplicate_searches.py
```

---

## 📊 Resultado Esperado

### Antes do Cleanup:
```
📅 History Visual:
  2025-12: Total=199 versions (1 auto, 198 current)  ❌
  2025-11: Total=1 versions (1 auto, 0 current)
```

### Depois do Cleanup:
```
📅 History Visual:
  2025-12: Total=1 version (1 auto, 0 current)       ✅
  2025-11: Total=5 versions (5 auto, 0 current)      ✅
```

---

## 🔍 Como Funciona o Cleanup

O endpoint `/api/automated-search/cleanup-duplicates`:

1. **Identifica duplicados**:
   - Mesmo `location` (Aeroporto de Faro)
   - Mesmo `search_type` (automated/current)
   - Mesmo `pickup_date` ou `month_key`
   - Mesmo `DATE(search_date)` (dia que foi salva)

2. **Mantém apenas a versão mais recente**:
   - Ordena por `search_date DESC`
   - Mantém o primeiro ID (mais recente)
   - Deleta todos os outros IDs do grupo

3. **Retorna estatísticas**:
   - `before`: Total antes
   - `after`: Total depois
   - `deleted`: Quantas foram removidas

---

## 🔒 Segurança

- ✅ **Autenticação**: Requer sessão de usuário válida
- ✅ **PostgreSQL Only**: Só funciona em produção (não SQLite)
- ✅ **Transação**: Usa commit/rollback para garantir integridade
- ✅ **Logs**: Registra todas as operações

---

## 🧪 Testar Após Cleanup

### 1. **Verificar Histórico**:
   - Ir para "History" tab
   - Filtrar "Aeroporto de Faro"
   - **Esperado**: 1-2 versões (não 199!)

### 2. **Fazer Nova Pesquisa**:
   - Aeroporto de Faro, Janeiro 2026, 31 dias
   - Fazer pesquisa
   - **Verificar logs**: `[UPSERT] Inserted new search ID: X`

### 3. **Editar Preços**:
   - Editar um preço qualquer
   - Aguardar auto-save
   - **Verificar logs**: `[UPSERT] Updated existing search ID: X` (mesmo ID!)

### 4. **Verificar Histórico Novamente**:
   - **Esperado**: Continua apenas 1 versão (não cria duplicado!)

---

## 🚨 Se Algo Correr Mal

### Erro: "Unauthorized"
- **Causa**: Não está logado
- **Solução**: Fazer login primeiro em /login

### Erro: "Cleanup only works with PostgreSQL"
- **Causa**: Tentou executar em ambiente local com SQLite
- **Solução**: Executar apenas em produção (Render)

### Erro: "column pickup_date does not exist"
- **Causa**: Tabela ainda não tem coluna pickup_date
- **Solução**: Script usa fallback automático para month_key

---

## 📝 Logs de Sucesso

Procurar nos logs do Render:

```
✅ [CLEANUP] Removed 300 duplicate entries (500 → 200)
```

---

## ✅ Checklist Final

- [ ] Deploy concluído (aguardar ~5 min)
- [ ] Abrir `cleanup_ui.html`
- [ ] Clicar "Run Cleanup Now"
- [ ] Verificar stats (before/after/deleted)
- [ ] Refresh página de histórico
- [ ] **Confirmar**: Aeroporto de Faro tem apenas 1-2 versões
- [ ] Testar auto-save (editar preços)
- [ ] **Confirmar**: Não cria duplicados

---

**Status**: ⏳ Deploy em andamento...  
**Próximo Passo**: Aguardar deploy e executar cleanup via `cleanup_ui.html`
