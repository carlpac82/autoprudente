# ✅ VERIFICAÇÃO COMPLETA - RENTAL AGREEMENT EXTRACTION

## 📊 STATUS DA BASE DE DADOS

### Tabelas Criadas:
- ✅ `rental_agreement_templates` - Armazena PDFs template
- ✅ `rental_agreement_coordinates` - Armazena coordenadas mapeadas (15 campos)
- ✅ `rental_agreement_mapping_history` - Histórico de mapeamentos

### Campos Mapeados Atualmente (15):
1. ✅ `address` - Morada do cliente
2. ✅ `clientEmail` - Email
3. ✅ `clientName` - Nome completo
4. ✅ `clientPhone` - Telefone
5. ✅ `contractNumber` - Número do contrato
6. ✅ `country` - País
7. ✅ `pickupDate` - Data de levantamento
8. ✅ `pickupLocation` - Local de levantamento
9. ✅ `pickupTime` - Hora de levantamento
10. ✅ `postalCodeCity` - Código Postal / Cidade
11. ✅ `returnDate` - Data de devolução
12. ✅ `returnLocation` - Local de devolução
13. ✅ `returnTime` - Hora de devolução
14. ✅ `vehicleBrandModel` - Marca / Modelo
15. ✅ `vehiclePlate` - Matrícula

---

## 🔗 ENDPOINTS DISPONÍVEIS

### **MAPEAMENTO:**
- ✅ `GET /rental-agreement-mapper` - Página do mapeador
- ✅ `POST /api/rental-agreements/upload-template` - Upload PDF template
- ✅ `GET /api/rental-agreements/get-active-template` - Buscar template ativo
- ✅ `GET /api/rental-agreements/get-coordinates` - Buscar coordenadas salvas
- ✅ `POST /api/rental-agreements/save-coordinates` - Salvar coordenadas

### **EXTRAÇÃO:**
- ✅ `POST /api/damage-reports/extract-from-ra` - **ENDPOINT PRINCIPAL** de extração

### **DEBUG:**
- ✅ `GET /api/rental-agreements/debug-status` - Verificar status das tabelas
- ✅ `GET /api/rental-agreements/debug-coords` - Verificar coordenadas
- ✅ `POST /api/rental-agreements/debug-lines` - Debug: listar linhas do PDF

---

## 🔄 FLUXO COMPLETO

### **1. MAPEAMENTO (Uma vez):**
```
1. Ir para: http://localhost:8000/rental-agreement-mapper
2. Upload do PDF template → Guarda em rental_agreement_templates
3. Mapear campos (desenhar caixas) → Guarda em rental_agreement_coordinates
4. Auto-save após cada campo mapeado
```

### **2. EXTRAÇÃO (Sempre que precisar):**
```
1. Ir para: http://localhost:8000/admin (Damage Report)
2. Clicar "Upload Rental Agreement" (botão laranja)
3. Fazer upload do PDF do cliente
4. Sistema:
   a. Lê coordenadas de rental_agreement_coordinates
   b. Extrai texto do PDF nas posições mapeadas
   c. Limpa e formata os dados
   d. Retorna JSON com os campos
5. Frontend popula formulário automaticamente
```

---

## 🧪 TRANSFORMAÇÕES APLICADAS

### **Backend (Python):**
1. ✅ Extrai texto das coordenadas mapeadas
2. ✅ Tenta 4 métodos de coordenadas (prioridade: DIRETO)
3. ✅ Remove espaços da matrícula: `"3 0 - X Q - 9 7"` → `"30-XQ-97"`
4. ✅ Divide campos combinados:
   - `postalCodeCity` → `postalCode` + `city`
   - `vehicleBrandModel` → `vehicleBrand` + `vehicleModel`
5. ✅ Detecta país automaticamente pelo código postal

### **Frontend (JavaScript):**
1. ✅ Remove espaços das datas: `"06 - 11 - 2025"` → `"06-11-2025"`
2. ✅ Converte formato: `"06-11-2025"` → `"2025-11-06"` (para input type="date")
3. ✅ Remove espaços das horas: `"10 : 30"` → `"10:30"`
4. ✅ Converte tudo para UPPERCASE (exceto email)

---

## 📋 CAMPOS DO DAMAGE REPORT

### **Dados do Contrato:**
- ✅ `contractNumber` ← do RA
- ✅ Data atual (não do RA)

### **Dados do Cliente:**
- ✅ `clientName` ← do RA
- ✅ `clientEmail` ← do RA
- ✅ `clientPhone` ← do RA
- ✅ `address` ← do RA
- ✅ `postalCodeCity` ← do RA (combinado ou dividido)
- ✅ `country` ← do RA

### **Dados do Veículo:**
- ✅ `vehiclePlate` ← do RA (sem espaços!)
- ✅ `vehicleBrandModel` ← do RA

### **Levantamento:**
- ✅ `pickupDate` ← do RA
- ✅ `pickupTime` ← do RA
- ✅ `pickupLocation` ← do RA

### **Devolução:**
- ✅ `returnDate` ← do RA
- ✅ `returnTime` ← do RA
- ✅ `returnLocation` ← do RA

---

## ⚠️ CAMPOS NÃO EXTRAÍDOS DO RA

Estes campos precisam ser preenchidos manualmente no DR:

- ❌ `dr_number` - Gerado automaticamente
- ❌ `vehicleColor` - Não está no RA
- ❌ `vehicleKm` - Não está no RA
- ❌ `pickupFuel` - Precisa ser marcado no DR
- ❌ `returnFuel` - Precisa ser marcado no DR
- ❌ `damageDescription` - Preenchido durante inspeção
- ❌ `photos` - Tiradas durante inspeção
- ❌ `vehicleDiagram` - Marcado durante inspeção
- ❌ `signatures` - Assinado durante entrega

---

## 🔍 LOGS IMPORTANTES

### **Extração bem-sucedida:**
```
🔍 DIAGNÓSTICO DE COORDENADAS
📍 Campo: contractNumber
   DIRETO: '06424-09'
   ✅ Escolhido: DIRETO → '06424-09'
📍 Campo: clientName
   DIRETO: 'EIKE BERENS'
   ✅ Escolhido: DIRETO → 'EIKE BERENS'
...
✅ EXTRAÇÃO CONCLUÍDA: 15 campos extraídos
✅ SUCESSO: 15 campos mapeados para Damage Report
```

### **Erros comuns:**
```
❌ "No coordinates found" → Campos não mapeados
❌ "Template not found" → PDF template não foi feito upload
❌ "__enter__" → Problema de conexão BD (já corrigido!)
```

---

## 🚀 TESTE COMPLETO

### **Checklist antes de testar:**
- ✅ Servidor rodando: `python3 main.py`
- ✅ Base de dados tem coordenadas (15 campos)
- ✅ Template PDF está na BD
- ✅ Navegador aberto: `http://localhost:8000`

### **Passos do teste:**
1. ✅ Login no sistema
2. ✅ Ir para Admin → Damage Report
3. ✅ Clicar "Upload Rental Agreement"
4. ✅ Fazer upload do PDF do cliente
5. ✅ Verificar se TODOS os 15 campos foram preenchidos
6. ✅ Verificar se valores estão corretos
7. ✅ Salvar o DR e verificar na lista

### **Validações:**
- ✅ Matrícula sem espaços: `30-XQ-97`
- ✅ Datas no formato correto: `06/11/2025`
- ✅ Horas no formato correto: `10:30`
- ✅ Locais em UPPERCASE: `AEROPORTO DE FARO`
- ✅ País em UPPERCASE: `DE`

---

## 📦 BACKUP E DEPLOY

### **Antes do deploy:**
```bash
# Backup da BD local (coordenadas)
sqlite3 data.db ".dump rental_agreement_coordinates" > ra_coords_backup.sql

# Ver coordenadas atuais
sqlite3 data.db "SELECT field_id, x, y FROM rental_agreement_coordinates;"
```

### **No Render (Produção):**
1. ✅ Push código para GitHub
2. ✅ Render faz deploy automático
3. ✅ Tabelas criadas automaticamente no PostgreSQL
4. ✅ **PRECISA MAPEAR NOVAMENTE** (coordenadas não vão do SQLite para PostgreSQL)
5. ✅ Fazer upload do template PDF em produção
6. ✅ Mapear os 15 campos no mapeador de produção

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ **TESTE LOCAL COM OUTRO PDF** - Validar que funciona com dados diferentes
2. ✅ **VERIFICAR EDGE CASES:**
   - PDF com campos em locais diferentes
   - Matrícula com formato diferente
   - Datas em formato diferente
3. ✅ **DEPLOY PARA PRODUÇÃO**
4. ✅ **MAPEAR EM PRODUÇÃO** (refazer mapeamento no Render)
5. ✅ **TESTE EM PRODUÇÃO** com PDF real

---

## ✅ TUDO ESTÁ PRONTO PARA TESTE!

**Pode testar com outro Rental Agreement agora!** 🚀
