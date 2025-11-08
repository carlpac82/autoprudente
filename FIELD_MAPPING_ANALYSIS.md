# Análise: Por que Campos Não Aparecem no PDF

## ✅ PROBLEMA ENCONTRADO E RESOLVIDO

### Causa Raiz: Mismatch de Nomes

**Coordenadas na BD (snake_case):**
```
customer_name
customer_phone  
vehicle_plate
pickup_date
```

**Dados enviados (camelCase):**
```javascript
report_data = {
  clientName: "João Silva",
  clientPhone: "+351 912345678",
  vehiclePlate: "AA-11-BB",
  pickupDate: "2025-11-08"
}
```

**O que acontecia:**
```python
field_id = 'customer_name'  # da BD
value = report_data.get('customer_name')  # ❌ NÃO EXISTE!
# Resultado: value = '' → campo não aparece
```

---

## ✅ SOLUÇÃO IMPLEMENTADA

### Sistema de Aliases

```python
field_aliases = {
    'customer_name': 'clientName',
    'customer_phone': 'clientPhone',
    'vehicle_plate': 'vehiclePlate',
    'pickup_date': 'pickupDate',
    # ... 20+ aliases
}

# Busca com fallback
value = report_data.get(field_id, '')
if not value and field_id in field_aliases:
    value = report_data.get(field_aliases[field_id], '')
```

---

## 📊 COMPARAÇÃO: Campos que FUNCIONAVAM vs NÃO FUNCIONAVAM

### ✅ FUNCIONAVAM (nome idêntico)

| Campo na BD | report_data | ✅ Match |
|-------------|-------------|----------|
| `dr_number` | `dr_number` | Sim |
| `pickup_location` | `pickup_location` | Sim |
| `return_location` | `return_location` | Sim |

### ❌ NÃO FUNCIONAVAM (nome diferente)

| Campo na BD | report_data | ❌ Mismatch |
|-------------|-------------|-------------|
| `customer_name` | `clientName` | Não |
| `customer_phone` | `clientPhone` | Não |
| `vehicle_plate` | `vehiclePlate` | Não |
| `pickup_date` | `pickupDate` | Não |
| `contract_number` | `contractNumber` | Não |

---

## 🔍 CAMPOS MAPEADOS ATUALMENTE (15)

```
✅ dr_number
✅ contract_number (agora com alias)
✅ customer_name (agora com alias)
✅ customer_phone (agora com alias)
✅ customer_email (agora com alias)
✅ customer_address (agora com alias)
✅ customer_postal (agora com alias)
✅ customer_city (agora com alias)
✅ customer_country (agora com alias)
✅ pickup_date (agora com alias)
✅ pickup_location
✅ return_date (agora com alias)
✅ return_location
✅ vehicle_brand (agora com alias)
✅ vehicle_plate (agora com alias)
```

**Todos estes campos devem APARECER agora no preview!**

---

## ❌ CAMPOS AINDA NÃO MAPEADOS

### Críticos para Damage Report
```
❌ vehicle_diagram - Diagrama SVG com pins
❌ damage_photo_1 até damage_photo_9 - Fotos dos danos
❌ signature_inspector - Assinatura do inspetor
❌ signature_client - Assinatura do cliente
```

### Opcionais
```
❌ damage_description_line_1 até 15 - Descrições textuais
❌ repair_line_1 até 10 - Linhas de reparação
❌ fuel_level_pickup / fuel_level_return
❌ vehicle_color, vehicle_km
❌ inspection_date, inspector_name
```

**Estes campos precisam ser mapeados no PDF Mapper!**

---

## 🧪 COMO TESTAR A CORREÇÃO

### 1. Preencher Formulário
```
✅ DR Number: 001-2025
✅ Contract: 12345-01
✅ Cliente: João Silva
✅ Telefone: +351 912345678
✅ Matrícula: AA-11-BB
✅ Data Recolha: 2025-11-08
```

### 2. Gerar Preview
- Clicar "Atualizar Preview"
- Abrir console do browser (F12)

### 3. Verificar Logs
```
🔍 Campo: customer_name
   Alias usado: clientName
   Tem valor? True
   Tamanho: 11

🔍 Campo: vehicle_plate
   Alias usado: vehiclePlate
   Tem valor? True
   Tamanho: 8
```

### 4. Resultado Esperado
✅ **Todos os 15 campos básicos devem aparecer no PDF**
- Nome do cliente
- Telefone
- Email
- Matrícula
- Datas
- Locais

❌ **Diagrama e fotos NÃO aparecem** (não estão mapeados)

---

## 📋 PRÓXIMOS PASSOS

### Para Diagrama e Fotos Aparecerem:

1. **Abrir Mapper**
   ```
   Admin Settings → Damage Report → Mapper de Campos
   ```

2. **Mapear Campos de Imagem**
   - `vehicle_diagram` - Diagrama do Veículo com Pins
   - `damage_photo_1` até `damage_photo_9`
   - `signature_inspector`
   - `signature_client`

3. **Clicar "Guardar"** (botão azul no topo)

4. **Testar Novamente**
   - Marcar danos no diagrama
   - Adicionar fotos
   - Gerar preview
   - ✅ Devem aparecer!

---

## 📊 RESUMO

| Status | Descrição | Quantidade |
|--------|-----------|------------|
| ✅ Resolvido | Campos básicos com aliases | 15 |
| ⏳ Pendente | Mapear campos de imagem | 4-13 |
| 📝 Opcional | Outros campos avançados | 20+ |

**Commit:** ee85a94 - "Fix: Add field name aliases..."

---

## 🔧 LOGS ADICIONADOS

Para debugar, os logs agora mostram:
```
🔍 Campo: vehicle_diagram
   Alias usado: N/A
   Tem valor? False
   Tamanho: 0
   Chaves possíveis em report_data: ['vehicle_diagram']
```

Isto ajuda a identificar:
- Se o campo está nas coordenadas
- Se o alias foi usado
- Se o valor existe em report_data
- Que chaves alternativas existem
