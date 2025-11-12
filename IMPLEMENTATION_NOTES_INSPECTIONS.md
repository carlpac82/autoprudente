# 📋 Notas de Implementação - Sistema de Inspeções

## ✅ O QUE JÁ ESTÁ IMPLEMENTADO

### 1. Mapeadores Separados
- ✅ **Damage Report** → `/damage-report-mapper` (62 campos)
- ✅ **Check-out** → `/checkout-mapper` (31 campos)
  - ⚠️ Inclui 2 assinaturas de inspetores separadas (Check-out e Check-in)
  - Inspetores podem ser diferentes em cada processo
- ✅ **Check-in** → Será criado futuramente

### 2. Páginas de Configuração
- ✅ `/admin/damage-report` - Configuração Damage Report
- ✅ `/admin/contracts` - Configuração Inspeções (Check-out)
- ✅ Upload/Download de coordenadas separados
- ✅ Upload de PDF T&C para Check-out

### 3. Histórico de Inspeções
- ✅ Filtro Check-out (verde) / Check-in (vermelho - desativado)
- ✅ Lista de inspeções por ano/mês/dia
- ✅ Ícones monocromáticos clean

---

## ✅ APIs DE MAPEAMENTO IMPLEMENTADAS

### APIs Check-out (ATIVAS)
- ✅ `POST /api/checkout/upload-template` - Upload do PDF Check-out
- ✅ `GET /api/checkout/get-active-template` - Obter PDF para mapeador
- ✅ `GET /api/checkout/get-coordinates` - Obter coordenadas mapeadas
- ✅ `POST /api/checkout/save-coordinates` - Guardar coordenadas

### Storage
- PDF: `settings.checkout_template_data` (formato hex)
- Coordenadas: `settings.checkout_coordinates` (formato JSON)
- Totalmente separado do Damage Report

---

## ⚠️ O QUE PRECISA SER IMPLEMENTADO

### 1. Preview de PDF Check-out
**Rota:** `GET /api/inspections/{inspection_number}/preview`

**Deve fazer:**
1. Buscar inspeção da base de dados pelo `inspection_number`
2. Identificar o tipo: `checkout` ou `checkin`
3. Buscar coordenadas CORRETAS:
   - **Check-out** → Coordenadas de `/admin/contracts` (checkout-mapper)
   - **Check-in** → Coordenadas próprias (futuro)
   - **❌ NÃO** usar coordenadas do Damage Report!
4. Gerar PDF com campos preenchidos nas posições mapeadas
5. Retornar PDF para preview no browser

---

### 2. Download de PDF Check-out
**Rota:** `GET /api/inspections/{inspection_number}/download`

**Deve fazer:**
1. Buscar inspeção da base de dados pelo `inspection_number`
2. Identificar o tipo: `checkout` ou `checkin`
3. Buscar coordenadas CORRETAS:
   - **Check-out** → Coordenadas de `/admin/contracts` (checkout-mapper)
   - **Check-in** → Coordenadas próprias (futuro)
   - **❌ NÃO** usar coordenadas do Damage Report!
4. Gerar PDF com campos preenchidos
5. Retornar PDF com header `Content-Disposition: attachment`

---

### 3. Envio de Email
**Rota:** `POST /api/inspections/{inspection_number}/email`

**Deve fazer:**
1. Buscar inspeção da base de dados
2. Identificar o tipo: `checkout` ou `checkin`
3. Buscar coordenadas CORRETAS (não Damage Report!)
4. Gerar PDF da inspeção com campos mapeados
5. **Se Check-out:**
   - Buscar PDF T&C: `_get_setting('checkout_tc_path')`
   - Anexar 2 PDFs: Inspeção + T&C
6. **Se Check-in (futuro):**
   - Anexar apenas PDF da inspeção
7. Enviar email com anexos

---

## 🗂️ ESTRUTURA DE COORDENADAS

### Base de Dados
As coordenadas devem estar em tabelas/settings separadas:

```sql
-- Damage Report (já existe)
damage_report_coordinates

-- Check-out (precisa ser criado/usado)
checkout_coordinates  -- ou armazenar em settings

-- Check-in (futuro)
checkin_coordinates
```

### Formato das Coordenadas
```json
{
  "plate": {"x": 100, "y": 200, "page": 1},
  "ra": {"x": 150, "y": 200, "page": 1},
  "receptionist": {"x": 200, "y": 200, "page": 1},
  "date": {"x": 250, "y": 200, "page": 1},
  "time": {"x": 300, "y": 200, "page": 1},
  "photo_front": {"x": 100, "y": 400, "page": 1},
  ...
}
```

---

## 📄 PÁGINAS DO PDF

### IMPORTANTE: O PDF tem 3 páginas

**PDF Upload:** O mesmo PDF de 3 páginas é usado para ambos, mas cada tipo usa páginas diferentes!

#### Check-out (Entrega)
- ✅ **USA:** Páginas 1 e 2
- ❌ **NÃO USA:** Página 3
- Campos mapeados em páginas 1 e 2 apenas

#### Check-in (Devolução) - FUTURO
- ✅ **USA:** Página 3
- ❌ **NÃO USA:** Páginas 1 e 2
- Campos mapeados na página 3 apenas

```
┌─────────────────────────────────────┐
│  PDF DE 3 PÁGINAS                   │
├─────────────────────────────────────┤
│  Página 1: Check-out                │ ← Check-out usa
│  Página 2: Check-out                │ ← Check-out usa
│  Página 3: Check-in                 │ ← Check-in usa (futuro)
└─────────────────────────────────────┘
```

### Ao Gerar PDFs:
- **Preview/Download Check-out:** Incluir apenas páginas 1 e 2
- **Preview/Download Check-in:** Incluir apenas página 3
- **Email Check-out:** PDF com páginas 1 e 2 + T&C
- **Email Check-in:** PDF com página 3 (sem T&C)

---

## 📝 CAMPOS DO CHECK-OUT

**31 campos disponíveis:**

### Informações do Contrato
- `contract_number` - Nº Contrato
- `ra_number` - RA (Rental Agreement)
- `contract_date` - Data Contrato
- `inspection_date` - Data Inspeção

### Informações do Cliente
- `client_name` - Nome Cliente
- `client_email` - Email Cliente
- `client_phone` - Telefone Cliente
- `client_address` - Morada Cliente

### Informações do Veículo
- `vehicle_plate` - Matrícula Veículo
- `vehicle_brand_model` - Marca / Modelo Veículo
- `vehicle_color` - Cor Veículo
- `vehicle_km_delivery` - KM na Entrega
- `fuel_level_delivery` - Nível Combustível (Entrega)

### Informações de Levantamento/Devolução
- `pickup_date` - Data Levantamento
- `pickup_time` - Hora Levantamento
- `pickup_location` - Local Levantamento
- `expected_return_date` - Data Devolução Prevista
- `expected_return_time` - Hora Devolução Prevista
- `expected_return_location` - Local Devolução Prevista

### Fotos (10 fotos)
- `photo_1_front` - Foto 1 - Frente
- `photo_2_back` - Foto 2 - Trás
- `photo_3_left` - Foto 3 - Lado Esquerdo
- `photo_4_right` - Foto 4 - Lado Direito
- `photo_5` - Foto 5
- `photo_6` - Foto 6
- `photo_7` - Foto 7
- `photo_8` - Foto 8
- `photo_9` - Foto 9
- `photo_10` - Foto 10

### Assinaturas
- `inspector_name` - Nome Inspetor
- `inspector_signature_checkout` - **Assinatura Inspector Check-out** ⚠️
- `inspector_signature_checkin` - **Assinatura Inspector Check-in** ⚠️
- `customer_signature` - Assinatura Cliente

**⚠️ IMPORTANTE - Assinaturas de Inspetores:**
- São **2 campos separados** porque podem ser inspetores diferentes
- **Check-out:** Inspector que entrega o veículo ao cliente
- **Check-in:** Inspector que recebe o veículo do cliente (futuro)
- Ambos os campos devem ser mapeados no PDF, mesmo que na prática sejam a mesma pessoa

---

## 🔍 VERIFICAÇÃO IMPORTANTE

**SEMPRE verificar:**
1. ✅ Está a usar coordenadas de Check-out?
2. ✅ Está a anexar T&C ao email de Check-out?
3. ✅ NÃO está a usar coordenadas do Damage Report?
4. ✅ Check-in terá coordenadas próprias no futuro?

---

## 📌 PRÓXIMOS PASSOS

### Fase 1 - Check-out Completo
1. [ ] Criar tabela/settings para coordenadas Check-out
2. [ ] Implementar geração de PDF Check-out
3. [ ] Implementar preview PDF Check-out
4. [ ] Implementar download PDF Check-out
5. [ ] Implementar envio email Check-out + T&C

### Fase 2 - Check-in (Futuro)
1. [ ] Criar página `/vehicle-checkin` própria
2. [ ] Criar mapeador `/checkin-mapper`
3. [ ] Criar campos próprios (diferentes do Check-out)
4. [ ] Implementar preview/download Check-in
5. [ ] Implementar envio email Check-in (sem T&C)

---

## 🚨 AVISOS CRÍTICOS

### ❌ NÃO FAZER:
- ❌ Usar coordenadas do Damage Report para Inspeções
- ❌ Misturar lógica de Check-out com Check-in
- ❌ Esquecer de anexar T&C ao email de Check-out

### ✅ SEMPRE FAZER:
- ✅ Identificar tipo de inspeção (checkout vs checkin)
- ✅ Usar coordenadas corretas para cada tipo
- ✅ Anexar T&C apenas ao Check-out
- ✅ Validar que o PDF tem os campos mapeados

---

**Última atualização:** 11 Novembro 2025, 23:27
