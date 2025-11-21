# 🐛 Debug: SupplierData Vazio nos Cards Visuais do Histórico

## 📋 Problema Reportado

Quando abre uma versão do histórico (History tab → clica num mês → clica "Editar"):
- ✅ **Tabela de preços** mostra dados corretamente
- ❌ **Cards visuais** aparecem vazios (sem carros/suppliers)

## 🔍 Diagnóstico Inicial

Console mostra:
```
[HISTORY] 🔍 FULL supplierData structure: – "{}"
[Warning] [HISTORY] No supplier data available - visual cards will be empty
```

Isso significa que `supplierData` está **vazio** ao carregar a versão do servidor.

## 🛠️ O Que Foi Feito

### Commit ed6dfd4 (21 Nov 2025, 10:50 AM)

**Backend (`main.py`):**
- ✅ Logging detalhado do `supplier_data` ao carregar versão
- ✅ Mostra tipo, tamanho, preview do conteúdo
- ✅ Avisa se campo está NULL/vazio na database

**Frontend (`price_automation.html`):**
- ✅ Logging adicional sobre formato do supplierData
- ✅ Auto-detecção de formato: GROUP→DAY→CARS vs DAY→CARS
- ✅ Conversão automática se necessário
- ✅ Mensagens de erro mais claras

## 📊 Possíveis Causas

### 1. **SupplierData Não Foi Guardado Originalmente**
A versão que editou pode ter sido criada **antes** de implementar o salvamento de `supplierData`.

**Como verificar:**
```sql
SELECT id, location, search_type, search_date, 
       CASE 
           WHEN supplier_data IS NULL THEN 'NULL'
           WHEN supplier_data = '{}' THEN 'EMPTY OBJECT'
           WHEN supplier_data = 'null' THEN 'NULL STRING'
           ELSE 'HAS DATA'
       END as supplier_status,
       LENGTH(supplier_data::text) as data_length
FROM automated_search_history
WHERE id = 604;
```

### 2. **Formato Incorreto do SupplierData**
O `supplierData` pode estar guardado em formato diferente do esperado:
- **Esperado:** `{"7": [{car, supplier, price}, ...], "14": [...]}`
- **Ou:** `{"B1": {"7": [...], "14": [...]}, "B2": {...}}`

### 3. **Erro na Conversão JSON**
PostgreSQL JSONB pode retornar `{}` se o campo foi guardado incorretamente.

## 🎯 Próximos Passos

### 1. **Aguardar Deploy (3-5 minutos)**
```
Commit: ed6dfd4
Push: ✅ Feito às 10:50 AM
ETA: 10:53-10:55 AM
```

### 2. **Reproduzir o Problema**
1. Acede ao site: https://carrental-api-5f8q.onrender.com
2. Vai ao **History** tab
3. Escolhe location **Albufeira**
4. Clica no mês **November 2025**
5. Clica **"Editar"** na versão ID **604** (ou outra que editou)
6. Abre **Console do Browser** (F12)

### 3. **Verificar Logs no Browser**

Procura por estas mensagens:
```
[HISTORY] 📦 Loading full data for version ID: 604
[HISTORY] ✅ Full data loaded: ...
[HISTORY] 🔍 supplierData type: ...
[HISTORY] 🔍 supplierData is null? ...
[HISTORY] 🔍 supplierData is empty object? ...
```

### 4. **Verificar Logs no Servidor Render**

Acede aos logs e procura por:
```
🔍 [VERSION-LOAD] Raw supplier_data type: ...
🔍 [VERSION-LOAD] supplier_data string length: ...
🔍 [VERSION-LOAD] supplier_data keys: ...
⚠️ [VERSION-LOAD] supplier_data is EMPTY/NULL in database for ID 604
```

### 5. **Enviar Screenshots + Logs**

Precisamos de:
1. Screenshot do console do browser (F12)
2. Logs do servidor Render (última chamada ao endpoint `/api/automated-search/version/604`)
3. Informação sobre quando essa versão foi criada (data/hora)

## 🔧 Soluções Possíveis

### Se `supplierData` Está NULL na Database:

**Opção A: Re-fazer a Pesquisa**
- Fazer nova pesquisa com os mesmos parâmetros
- Os cards visuais vão aparecer
- Guardar nova versão

**Opção B: Migração de Dados**
Se muitas versões antigas não têm `supplierData`, podemos:
1. Identificar versões sem supplier data
2. Re-executar scraping para essas datas
3. Atualizar registos antigos

### Se `supplierData` Está em Formato Errado:

Adicionar migração SQL:
```sql
-- Corrigir formato se necessário
UPDATE automated_search_history
SET supplier_data = <formato correto>
WHERE supplier_data IS NOT NULL 
  AND <condição para detectar formato errado>;
```

## 📝 Notas Técnicas

### Formato Esperado de SupplierData

**Na Database (GROUP→DAY→CARS):**
```json
{
  "B1": {
    "7": [{"car": "Fiat 500", "supplier": "Hertz", "price": 25.50, "group": "B1"}],
    "14": [...]
  },
  "D": {...}
}
```

**No Frontend para Visual Cards (DAY→CARS):**
```json
{
  "7": [
    {"car": "Fiat 500", "supplier": "Hertz", "price": 25.50, "group": "B1"},
    {"car": "VW Polo", "supplier": "Avis", "price": 26.00, "group": "B1"}
  ],
  "14": [...]
}
```

O código agora **converte automaticamente** entre os dois formatos.

## 🚦 Status

- ✅ Logging implementado
- ✅ Deploy em progresso
- ⏳ Aguardando logs do utilizador
- ⏳ Identificação da causa raiz
- ⏳ Implementação da solução

---

**Última atualização:** 21 Nov 2025, 10:50 AM
**Deploy:** Commit ed6dfd4
