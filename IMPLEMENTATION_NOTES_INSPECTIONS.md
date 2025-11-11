# 📋 Notas de Implementação - Sistema de Inspeções

## ✅ O QUE JÁ ESTÁ IMPLEMENTADO

### 1. Mapeadores Separados
- ✅ **Damage Report** → `/damage-report-mapper` (62 campos)
- ✅ **Check-out** → `/checkout-mapper` (30 campos)
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

## 📝 CAMPOS DO CHECK-OUT

30 campos disponíveis:
- `plate` - Matrícula
- `ra` - RA
- `receptionist` - Rececionista
- `date` - Data
- `time` - Hora
- `photo_front` - Foto Frente
- `photo_rear` - Foto Traseira
- `photo_left` - Foto Esquerda
- `photo_right` - Foto Direita
- `photo_interior` - Foto Interior
- `photo_dashboard` - Foto Dashboard
- `photo_trunk` - Foto Bagageira
- `photo_roof` - Foto Tejadilho
- `photo_windshield` - Foto Para-brisas
- `photo_wheels` - Foto Rodas
- `photo_seats` - Foto Bancos
- `photo_steering_wheel` - Foto Volante
- `photo_gear_shift` - Foto Mudanças
- `photo_pedals` - Foto Pedais
- `photo_mirrors` - Foto Espelhos
- `photo_documents` - Foto Documentos
- `photo_keys` - Foto Chaves
- `photo_fuel` - Foto Combustível
- `photo_odometer` - Foto Conta-km
- `diagram` - Diagrama de danos
- `observations` - Observações
- `fuel_level` - Nível combustível
- `odometer_reading` - Quilometragem
- `signature_client` - Assinatura Cliente
- `signature_receptionist` - Assinatura Rececionista

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
