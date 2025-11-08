# 🎯 GUIA DE MAPEAMENTO CORRETO - RENTAL AGREEMENT

## ⚠️ MUITO IMPORTANTE - LEIA ANTES DE MAPEAR!

**CADA CAIXA** que você desenha deve cobrir **EXATAMENTE** o texto que quer extrair!

**ANTES de desenhar**, verifique o **DROPDOWN** - qual campo está selecionado?

---

## 📋 ORDEM DE MAPEAMENTO (RECOMENDADA)

Siga esta ordem para não se perder:

### 1️⃣ **DADOS DO CONTRATO**

| Campo no Dropdown | Texto no PDF | Onde está no PDF |
|------------------|--------------|------------------|
| `contractNumber` | **06424-09** | Canto superior direito, em cima de "RA" |
| ~~`contractDate`~~ | 08/11/2025 | Data do contrato (se tiver) |

---

### 2️⃣ **DADOS DO CLIENTE**

| Campo no Dropdown | Texto no PDF | Onde está no PDF |
|------------------|--------------|------------------|
| `clientName` | **EIKE BERENS** | Nome do cliente (primeira linha da secção cliente) |
| `clientEmail` | **eike.berens11@googlemail.com** | Email do cliente |
| `clientPhone` | **+49 15123413660** | Telefone com código do país |
| `address` | **HAFERBOGEN 14** | Morada/rua |
| `postalCodeCity` | **GROSSENWIEHE 24969** | Código postal + Cidade (juntos ou separados) |
| ~~`country`~~ | DE | País (2 letras) - opcional |

---

### 3️⃣ **DADOS DO VEÍCULO**

| Campo no Dropdown | Texto no PDF | Onde está no PDF |
|------------------|--------------|------------------|
| `vehiclePlate` | **3 0 - X Q - 9 7** | Matrícula do carro |
| `vehicleBrandModel` | **PEUGEOT / 108** | Marca e modelo juntos (ou separados) |

**OU** se estiverem separados:
- `vehicleBrand` → **PEUGEOT**
- `vehicleModel` → **108**

---

### 4️⃣ **LEVANTAMENTO (PICKUP)**

| Campo no Dropdown | Texto no PDF | Onde está no PDF |
|------------------|--------------|------------------|
| `pickupLocation` | **AEROPORTO DE FARO** | Local de levantamento |
| `pickupDate` | **06 - 11 - 2025** | Data de levantamento |
| `pickupTime` | **10 : 30** | Hora de levantamento |
| ~~`pickupFuel`~~ | 3/8, 1/2, etc | Nível combustível (se tiver) |

---

### 5️⃣ **DEVOLUÇÃO (RETURN/DROPOFF)**

| Campo no Dropdown | Texto no PDF | Onde está no PDF |
|------------------|--------------|------------------|
| `returnLocation` | **AEROPORTO DE FARO** | Local de devolução |
| `returnDate` | **06 - 12 - 2025** | Data de devolução |
| `returnTime` | **12 : 00** | Hora de devolução |
| ~~`returnFuel`~~ | 3/8, 1/2, etc | Nível combustível (se tiver) |

---

## ✅ CHECKLIST ANTES DE CADA CAIXA

1. [ ] Verificar dropdown - campo correto selecionado?
2. [ ] Encontrar o texto correto no PDF
3. [ ] Desenhar caixa sobre o texto (não muito grande, não muito pequena)
4. [ ] Verificar se a caixa está bem posicionada
5. [ ] Clicar em "Salvar Coordenadas" (de vez em quando)

---

## 🚫 ERROS COMUNS

❌ **ERRO:** Desenhar caixa sobre "DE" quando tem "contractNumber" selecionado
✅ **CORRETO:** Desenhar sobre "06424-09"

❌ **ERRO:** Desenhar caixa sobre "PEUGEOT 108" quando tem "clientName" selecionado
✅ **CORRETO:** Desenhar sobre "EIKE BERENS"

❌ **ERRO:** Desenhar caixa sobre "HAFERBOGEN 14" quando tem "vehiclePlate" selecionado
✅ **CORRETO:** Desenhar sobre "3 0 - X Q - 9 7"

---

## 💡 DICAS

1. **Use ZOOM** no PDF para ver melhor os textos pequenos
2. **Salve frequentemente** (botão "Salvar Coordenadas")
3. **Teste depois de mapear 3-4 campos** (fazer upload e extrair)
4. Se um campo vier errado, **remapear só esse campo**
5. **Não precisa mapear TUDO** - só os campos que existem no PDF

---

## 🎯 TESTE RÁPIDO

Depois de mapear os primeiros 3 campos, teste:

1. Fazer upload do PDF no Damage Report
2. Ver se os 3 campos vieram corretos
3. Se sim, continuar mapeando
4. Se não, verificar o que está errado e corrigir

---

## 📝 ORDEM MÍNIMA NECESSÁRIA

Se quiser mapear apenas o essencial:

1. ✅ contractNumber
2. ✅ clientName
3. ✅ clientEmail
4. ✅ clientPhone
5. ✅ vehiclePlate
6. ✅ vehicleBrandModel (ou brand + model)
7. ✅ pickupLocation
8. ✅ pickupDate
9. ✅ returnLocation
10. ✅ returnDate

**Estes 10 campos são os mais importantes!**

---

## 🚀 QUANDO TERMINAR

1. Salvar coordenadas
2. Fazer upload do PDF no Damage Report
3. Verificar se TODOS os campos vieram corretos
4. Se sim → Deploy para produção! 🎉
5. Se não → Identificar campos errados e remapear

---

**BOA SORTE! MAPEAR COM CALMA E ATENÇÃO! 🎯**
