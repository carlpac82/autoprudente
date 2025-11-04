# 🚗 DOWNLOAD DE FOTOS - 7 GRUPOS DA CARJET

**Data:** 4 de Novembro de 2025, 20:55  
**Status:** ⏳ Em execução  
**Script:** `download_by_groups.py`

---

## 📋 GRUPOS CONFIGURADOS (7 GRUPOS)

### ✅ Grupo N - Pequenos
- **URL:** `s=36b4f78e...`
- **Descrição:** Carros pequenos (Fiat Panda, Fiat 500, VW Up, etc.)
- **Pasta:** `carjet_photos_by_group/group_N/`
- **Status:** ⏳ Processando

### ✅ Grupo M1 - Médios 1
- **URL:** `s=f45d195b...`
- **Descrição:** Carros médios parte 1 (VW Golf, Ford Focus, etc.)
- **Pasta:** `carjet_photos_by_group/group_M1/`
- **Status:** ⏳ Aguardando

### ✅ Grupo M2 - Médios 2
- **URL:** `s=d197f989...`
- **Descrição:** Carros médios parte 2 (Renault Megane, Peugeot 308, etc.)
- **Pasta:** `carjet_photos_by_group/group_M2/`
- **Status:** ⏳ Aguardando

### ✅ Grupo L1 - Grandes 1
- **URL:** `s=e36f74ac...`
- **Descrição:** Carros grandes parte 1
- **Pasta:** `carjet_photos_by_group/group_L1/`
- **Status:** ⏳ Aguardando

### ✅ Grupo L2 - Grandes 2
- **URL:** `s=a02a4f13...`
- **Descrição:** Carros grandes parte 2
- **Pasta:** `carjet_photos_by_group/group_L2/`
- **Status:** ⏳ Aguardando

### ✅ Grupo F_J1 - Familiares e SUVs 1
- **URL:** `s=1c29e1ba...`
- **Descrição:** Familiares e SUVs parte 1
- **Pasta:** `carjet_photos_by_group/group_F_J1/`
- **Status:** ⏳ Aguardando

### ✅ Grupo J2 - SUVs 2
- **URL:** `s=43f2520b...`
- **Descrição:** SUVs parte 2
- **Pasta:** `carjet_photos_by_group/group_J2/`
- **Status:** ⏳ Aguardando

---

## 📊 ESTIMATIVAS

### Por Grupo:
- **Carros:** 30-60 por grupo
- **Fotos reais:** 60-80% (20-48 fotos)
- **Tempo:** 5-8 minutos por grupo

### Total (7 Grupos):
- **Carros:** 210-420 carros
- **Fotos reais:** 126-336 fotos (60-80%)
- **Tempo total:** 35-56 minutos

---

## 🔄 PROCESSO

Para cada grupo, o script:

1. ✅ Abre Chrome com mobile emulation
2. ✅ Carrega URL do grupo
3. ✅ Rejeita cookies
4. ✅ Faz scroll agressivo (150px, 2.5s)
5. ✅ Extrai HTML e guarda debug
6. ✅ Parse com BeautifulSoup
7. ✅ Identifica códigos únicos (C45, F12, etc.)
8. ✅ Detecta variantes (Cabrio, SW, Auto, etc.)
9. ✅ Download fotos para pasta do grupo
10. ✅ Guarda metadados em JSON

---

## 📁 ESTRUTURA DE SAÍDA

```
carjet_photos_by_group/
├── group_N/          # Pequenos
│   ├── C45_Fiat_Panda.jpg
│   ├── C25_Fiat_500.jpg
│   └── ...
├── group_M1/         # Médios 1
│   ├── F12_VW_Golf.jpg
│   └── ...
├── group_M2/         # Médios 2
│   ├── F05_Renault_Megane.jpg
│   └── ...
├── group_L1/         # Grandes 1
│   └── ...
├── group_L2/         # Grandes 2
│   └── ...
├── group_F_J1/       # Familiares e SUVs 1
│   └── ...
└── group_J2/         # SUVs 2
    └── ...
```

**Ficheiros JSON:**
- `carjet_cars_by_groups.json` - Todos os carros com metadados

**Ficheiros HTML (debug):**
- `carjet_group_N.html`
- `carjet_group_M1.html`
- `carjet_group_M2.html`
- `carjet_group_L1.html`
- `carjet_group_L2.html`
- `carjet_group_F_J1.html`
- `carjet_group_J2.html`

---

## 📊 METADADOS POR CARRO

```json
{
  "group": "N",
  "group_name": "Grupo N",
  "index": 1,
  "name": "Fiat Panda",
  "brand": "Fiat",
  "model": "Panda",
  "variant": null,
  "category": "Pequeno",
  "car_code": "C45",
  "photo_url": "https://www.carjet.com/cdn/img/cars/L/car_C45.jpg",
  "is_placeholder": false
}
```

---

## 🎯 MAPEAMENTO PARA SISTEMA

### Grupos → Categorias do Sistema

| Grupo Carjet | Categoria Sistema | Código |
|--------------|-------------------|--------|
| N | Pequenos | B1 |
| M1, M2 | Médios | C |
| L1, L2 | Grandes | D |
| F_J1, J2 | SUVs/Familiares | F, J |

---

## ✅ VANTAGENS

1. **Organização Clara**
   - Fotos separadas por grupo
   - Fácil identificar categoria
   - Mapeamento direto para pricing

2. **Links Diretos**
   - Sem formulários
   - Mais rápido
   - Mais confiável

3. **Metadados Completos**
   - Grupo identificado
   - Código único preservado
   - Variantes detectadas
   - URL original guardada

4. **Escalável**
   - Fácil adicionar mais grupos
   - Processo automatizado
   - Reutilizável

---

## 📝 PRÓXIMOS PASSOS

Após conclusão:

1. ✅ Verificar estatísticas por grupo
2. ✅ Validar taxa de fotos reais
3. ✅ Criar script de importação para BD
4. ✅ Mapear grupos para categorias
5. ✅ Atualizar tabela `vehicle_photos`

---

**Log:** `download_all_7_groups.log`  
**Tempo estimado:** 35-56 minutos  
**Status:** ⏳ Em execução...
