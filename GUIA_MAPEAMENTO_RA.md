# 🎯 GUIA DE MAPEAMENTO DO RENTAL AGREEMENT

## 📋 PASSOS PARA MAPEAR

### 1. Abrir o Mapeador
```
http://localhost:8000/rental-agreement-mapper
```

### 2. Fazer Upload do PDF
- Clique em "Upload PDF"
- Selecione o PDF do Rental Agreement

### 3. Mapear Campos (POR ORDEM)

**IMPORTANTE:** 
- ✅ Desenhar caixa **EXATAMENTE** onde está o texto no PDF
- ✅ Cobrir **TODO** o texto do campo
- ✅ **NÃO** cobrir texto de outros campos
- ✅ Verificar que selecionou o campo correto no dropdown

---

## 📝 CAMPOS OBRIGATÓRIOS (12 campos)

### 🔢 CONTRATO
1. **contractNumber** - Nº Contrato
   - Exemplo: `06424-09`
   - Desenhar caixa no número do contrato

---

### 👤 CLIENTE
2. **clientName** - Nome Cliente
   - Exemplo: `EIKE BERENS`
   - ⚠️ **ATENÇÃO:** Não confundir com marca do carro!

3. **clientEmail** - Email Cliente
   - Exemplo: `eike.berens@googlemail.com`

4. **clientPhone** - Telefone Cliente
   - Exemplo: `+49 151234136`

5. **address** - Morada
   - Exemplo: `KASTANIENWEG 123`
   - Desenhar caixa em toda a morada

6. **postalCodeCity** - Código Postal / Cidade
   - Exemplo: `23643 LÜBECK`
   - ✅ Desenhar caixa que inclui AMBOS (código + cidade)
   - Sistema divide automaticamente

7. **country** - País
   - Exemplo: `DE`
   - Código de 2 letras

---

### 🚗 VEÍCULO
8. **vehiclePlate** - Matrícula
   - Exemplo: `30-XQ-97`

9. **vehicleBrandModel** - Marca / Modelo
   - Exemplo: `PEUGEOT / 108`
   - ✅ Se estiver junto no PDF, mapear tudo junto
   - Sistema divide automaticamente

---

### 📅 LEVANTAMENTO (PICKUP)
10. **pickupDate** - Data Levantamento
    - Exemplo: `06/11/2025`

11. **pickupTime** - Hora Levantamento
    - Exemplo: `12:30`

12. **pickupLocation** - Local Levantamento
    - Exemplo: `AUTO PRUDENTE`
    - ⚠️ **ATENÇÃO:** Não confundir com nome de pessoa!

---

### 📅 DEVOLUÇÃO (RETURN/DROPOFF)
13. **returnDate** ou **dropoffDate** - Data Devolução
    - Exemplo: `08/11/2025`

14. **returnTime** ou **dropoffTime** - Hora Devolução
    - Exemplo: `12:30`

15. **returnLocation** ou **dropoffLocation** - Local Devolução
    - Exemplo: `AUTO PRUDENTE`

---

## ⚠️ ERROS COMUNS A EVITAR

### ❌ NÃO CONFUNDIR:
- **Nome Cliente** com **Marca do Carro**
  - Nome: `EIKE BERENS` ✅
  - Carro: `PEUGEOT 108` ❌

- **Local** com **Nome de Pessoa**
  - Local: `AUTO PRUDENTE` ✅
  - Pessoa: `EIKE BERENS` ❌

- **Local** com **Códigos Estranhos**
  - Local: `AUTO PRUDENTE` ✅
  - Código: `LIMJ5V4H4 08 - 07 - 2024` ❌

### ✅ DICAS:
1. Começar pelos campos **FÁCEIS** (contractNumber, vehiclePlate)
2. Depois mapear **CLIENTE** (nome, email, telefone)
3. Por fim **DATAS E LOCAIS** (mais difíceis)
4. **TESTAR** após cada 3-4 campos mapeados

---

## 🧪 TESTAR EXTRAÇÃO

### 1. Salvar Coordenadas
- Clique em "Guardar" após mapear campos
- Aguardar confirmação

### 2. Testar Extração
```bash
cd /Users/filipepacheco/CascadeProjects/RentalPriceTrackerPerDay
python3 test_extract_direct.py
```

### 3. Ver Logs
Os logs mostram:
```
📍 Campo: clientName
   DIRETO: 'EIKE BERENS'
   INVERTIDO_Y: 'PEUGEOT 108'
   ESCALA_2: ''
   ESCALA_INV: ''
   ✅ Escolhido: DIRETO → 'EIKE BERENS'
```

### 4. Verificar Resultados
- ✅ `clientName`: "EIKE BERENS" (correto!)
- ❌ `clientName`: "PEUGEOT 108" (errado - remapear!)

---

## 📊 CHECKLIST DE VALIDAÇÃO

Após mapear TODOS os campos, verificar:

- [ ] `contractNumber` = número do contrato (ex: 06424-09)
- [ ] `clientName` = nome da pessoa (ex: EIKE BERENS)
- [ ] `clientEmail` = email completo
- [ ] `clientPhone` = telefone com +XX
- [ ] `address` = morada completa
- [ ] `postalCodeCity` = código + cidade (ex: 23643 LÜBECK)
- [ ] `country` = código país (ex: DE)
- [ ] `vehiclePlate` = matrícula (ex: 30-XQ-97)
- [ ] `vehicleBrandModel` = marca e modelo (ex: PEUGEOT / 108)
- [ ] `pickupDate` = data correta
- [ ] `pickupTime` = hora correta
- [ ] `pickupLocation` = local (ex: AUTO PRUDENTE)
- [ ] `returnDate` = data correta
- [ ] `returnTime` = hora correta
- [ ] `returnLocation` = local (ex: AUTO PRUDENTE)

---

## 🚀 FAZER DEPLOY

Se TUDO estiver correto no localhost:

1. **Exportar coordenadas** (se tiver botão de export)
2. **Fazer deploy:**
   ```bash
   git add main.py
   git commit -m "Production-tested RA coordinates"
   git push origin main
   ```
3. **No Render:** Fazer upload do mesmo PDF template
4. **Importar coordenadas** (se tiver botão de import)
5. **Testar em produção**

---

## 📞 AJUDA

Se campos continuarem errados:
1. Ver logs do `test_extract_direct.py`
2. Identificar qual método está sendo escolhido
3. Remapear campos problemáticos
4. Testar novamente

**Boa sorte! 🎯**
