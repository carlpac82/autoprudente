# 🎯 LISTA COMPLETA - 11 GRUPOS DA CARJET

**Data:** 4 de Novembro de 2025, 21:01  
**Status:** ⏳ Download em execução  
**Script:** `download_by_groups.py`  
**Log:** `download_all_11_groups.log`

---

## ✅ TODOS OS GRUPOS CONFIGURADOS (11 GRUPOS)

### 1️⃣ Grupo B1 e B2 - Mini/Económicos
- **Código:** `B1_B2`
- **URL:** `s=9885cac3...`
- **Pasta:** `group_B1_B2/`
- **Exemplos:** Fiat Panda, Fiat 500, VW Up, Toyota Aygo

### 2️⃣ Grupo N - Pequenos
- **Código:** `N`
- **URL:** `s=36b4f78e...`
- **Pasta:** `group_N/`
- **Exemplos:** Renault Clio, Peugeot 208, Opel Corsa

### 3️⃣ Grupo C e D - Compactos e Intermédios
- **Código:** `C_D`
- **URL:** `s=f66105ae...`
- **Pasta:** `group_C_D/`
- **Exemplos:** VW Golf, Ford Focus, Seat Leon

### 4️⃣ Grupo M1 - Médios 1
- **Código:** `M1`
- **URL:** `s=f45d195b...`
- **Pasta:** `group_M1/`
- **Exemplos:** Renault Megane, Peugeot 308

### 5️⃣ Grupo M2 - Médios 2
- **Código:** `M2`
- **URL:** `s=d197f989...`
- **Pasta:** `group_M2/`
- **Exemplos:** Opel Astra, Mazda 3

### 6️⃣ Grupo E1 e E2 - Estate/SW
- **Código:** `E1_E2`
- **URL:** `s=0c939e90...`
- **Pasta:** `group_E1_E2/`
- **Exemplos:** VW Golf SW, Ford Focus SW, Skoda Octavia SW

### 7️⃣ Grupo L1 - Grandes 1
- **Código:** `L1`
- **URL:** `s=e36f74ac...`
- **Pasta:** `group_L1/`
- **Exemplos:** VW Passat, Skoda Superb

### 8️⃣ Grupo L2 - Grandes 2
- **Código:** `L2`
- **URL:** `s=a02a4f13...`
- **Pasta:** `group_L2/`
- **Exemplos:** BMW 5 Series, Mercedes E Class

### 9️⃣ Grupo F e J1 - Familiares e SUVs 1
- **Código:** `F_J1`
- **URL:** `s=1c29e1ba...`
- **Pasta:** `group_F_J1/`
- **Exemplos:** Nissan Qashqai, Peugeot 3008, Renault Captur

### 🔟 Grupo J2 - SUVs 2
- **Código:** `J2`
- **URL:** `s=43f2520b...`
- **Pasta:** `group_J2/`
- **Exemplos:** VW Tiguan, Nissan X-Trail, Kia Sportage

### 1️⃣1️⃣ Grupo G e X - Premium/Luxo
- **Código:** `G_X`
- **URL:** `s=3aeff12c...`
- **Pasta:** `group_G_X/`
- **Exemplos:** BMW X5, Mercedes GLE, Audi Q7, Tesla Model 3

---

## 📊 ESTIMATIVAS TOTAIS

### Por Grupo (média):
- **Carros:** 30-60 por grupo
- **Fotos reais:** 60-80% (20-48 fotos)
- **Tempo:** 5-8 minutos por grupo

### TOTAL (11 Grupos):
- **Carros:** 330-660 carros
- **Fotos reais:** 198-528 fotos (60-80%)
- **Tempo total:** 55-88 minutos (~1h-1h30)

---

## 📁 ESTRUTURA COMPLETA DE SAÍDA

```
carjet_photos_by_group/
├── group_B1_B2/      # Mini/Económicos
│   ├── C45_Fiat_Panda.jpg
│   ├── C25_Fiat_500.jpg
│   └── ...
├── group_N/          # Pequenos
│   ├── C04_Renault_Clio.jpg
│   └── ...
├── group_C_D/        # Compactos e Intermédios
│   ├── F12_VW_Golf.jpg
│   └── ...
├── group_M1/         # Médios 1
│   └── ...
├── group_M2/         # Médios 2
│   └── ...
├── group_E1_E2/      # Estate/SW
│   └── ...
├── group_L1/         # Grandes 1
│   └── ...
├── group_L2/         # Grandes 2
│   └── ...
├── group_F_J1/       # Familiares e SUVs 1
│   └── ...
├── group_J2/         # SUVs 2
│   └── ...
└── group_G_X/        # Premium/Luxo
    └── ...
```

---

## 🗂️ MAPEAMENTO PARA SISTEMA DE PRICING

| Grupo Carjet | Categoria Sistema | Descrição |
|--------------|-------------------|-----------|
| B1_B2 | Mini/Económicos | Carros muito pequenos |
| N | Pequenos | Carros pequenos |
| C_D | Compactos | Carros médios compactos |
| M1, M2 | Médios | Carros médios |
| E1_E2 | Estate | Station Wagons |
| L1, L2 | Grandes | Carros grandes |
| F_J1, J2 | SUVs | SUVs e Crossovers |
| G_X | Premium | Carros de luxo |

---

## 📋 FICHEIROS GERADOS

### Fotos (por grupo):
- 11 pastas com fotos organizadas

### JSON:
- `carjet_cars_by_groups.json` - **TODOS os carros com metadados**

### HTML Debug (11 ficheiros):
- `carjet_group_B1_B2.html`
- `carjet_group_N.html`
- `carjet_group_C_D.html`
- `carjet_group_M1.html`
- `carjet_group_M2.html`
- `carjet_group_E1_E2.html`
- `carjet_group_L1.html`
- `carjet_group_L2.html`
- `carjet_group_F_J1.html`
- `carjet_group_J2.html`
- `carjet_group_G_X.html`

---

## 🔄 ORDEM DE PROCESSAMENTO

O script processa sequencialmente:

1. ⏳ Grupo B1_B2 (Mini/Económicos)
2. ⏳ Grupo N (Pequenos)
3. ⏳ Grupo C_D (Compactos)
4. ⏳ Grupo M1 (Médios 1)
5. ⏳ Grupo M2 (Médios 2)
6. ⏳ Grupo E1_E2 (Estate)
7. ⏳ Grupo L1 (Grandes 1)
8. ⏳ Grupo L2 (Grandes 2)
9. ⏳ Grupo F_J1 (Familiares/SUVs 1)
10. ⏳ Grupo J2 (SUVs 2)
11. ⏳ Grupo G_X (Premium/Luxo)

---

## 📊 ESTATÍSTICAS FINAIS ESPERADAS

```
GRUPO          CARROS    FOTOS REAIS    %
─────────────────────────────────────────
B1_B2          40-60     24-48         60-80%
N              40-60     24-48         60-80%
C_D            40-60     24-48         60-80%
M1             30-50     18-40         60-80%
M2             30-50     18-40         60-80%
E1_E2          30-50     18-40         60-80%
L1             30-50     18-40         60-80%
L2             30-50     18-40         60-80%
F_J1           40-60     24-48         60-80%
J2             30-50     18-40         60-80%
G_X            20-40     12-32         60-80%
─────────────────────────────────────────
TOTAL          330-660   198-528       60-80%
```

---

## ✅ CONFIRMAÇÃO

**Todos os grupos estão configurados?** ✅ SIM

Grupos recebidos:
- ✅ N (Pequenos)
- ✅ M1, M2 (Médios)
- ✅ L1, L2 (Grandes)
- ✅ F_J1, J2 (Familiares/SUVs)
- ✅ B1_B2 (Mini/Económicos)
- ✅ C_D (Compactos)
- ✅ E1_E2 (Estate)
- ✅ G_X (Premium/Luxo)

**Total:** 11 grupos ✅

---

**Status:** ⏳ Download em execução  
**Tempo estimado:** 55-88 minutos  
**Início:** 21:01  
**Conclusão estimada:** 21:56 - 22:29
