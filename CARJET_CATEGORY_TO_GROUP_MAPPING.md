# Mapeamento de Categorias CarJet para Grupos do Sistema

## 📋 Visão Geral

Este documento descreve como as **categorias de filtro do CarJet** (`frmAgrp`) são mapeadas para os **grupos de carros** do sistema.

## 🔍 Categorias do CarJet (frmAgrp)

As categorias são usadas para filtrar carros na página de resultados do CarJet:

| Código | Nome | Descrição |
|--------|------|-----------|
| `MINI` | Small | Carros pequenos (Mini, Economy) |
| `COMP` | Medium | Carros médios |
| `FAMI` | Large | Carros grandes |
| `SUVS` | SUV | SUVs e Crossovers |
| `VANS` | People Carrier | Carrinhas de passageiros (7 e 9 lugares) |
| `LUXU` | Premium | Carros de luxo e cabrio |
| `ESTA` | Estate Cars | Station Wagons (carrinhas) |
| `AUTO` | Automatic | Categoria cruzada de automáticos |
| `CARG` | Vans | Vans comerciais |
| `MOTO` | Moto | Motos (não usado) |

## 🎯 Mapeamento para Grupos do Sistema

### MINI (Small)
**Grupos possíveis:** B1, B2, D, E1, E2

- **B1** - Mini 4 Lugares (Manual)
  - Exemplo: Fiat 500, Peugeot 108
  
- **B2** - Mini 5 Lugares (Manual)
  - Exemplo: Hyundai i10, Fiat Panda
  
- **D** - Economy (Manual)
  - Exemplo: VW Polo, Renault Clio
  
- **E1** - Mini Automatic
  - Exemplo: Fiat 500 Auto, Hyundai i10 Auto
  
- **E2** - Economy Automatic
  - Exemplo: VW Polo Auto, Renault Clio Auto

### COMP (Medium)
**Grupos intermediários** (mapeamento depende do modelo específico)

### FAMI (Large)
**Grupos grandes** (mapeamento depende do modelo específico)

### SUVS (SUV)
**Grupos possíveis:** F, J1, L1

- **F** - SUV (Manual)
  - Exemplo: Nissan Qashqai, Peugeot 3008
  
- **J1** - Crossover
  - Exemplo: SUVs compactos
  
- **L1** - SUV Automatic
  - Exemplo: Nissan Qashqai Auto, Peugeot 3008 Auto

### VANS (People Carrier)
**Grupos possíveis:** M1, M2, N

- **M1** - 7 Seater (Manual)
  - Exemplo: VW Sharan, Ford Galaxy
  
- **M2** - 7 Seater Automatic
  - Exemplo: VW Sharan Auto, Ford S-Max Auto
  
- **N** - 9 Seater
  - Exemplo: Ford Transit, Mercedes Vito

### LUXU (Premium)
**Grupos possíveis:** G

- **G** - Cabrio / Premium
  - Exemplo: Mini Cooper Cabrio, Mercedes E Class Cabrio

### ESTA (Estate Cars)
**Grupos possíveis:** J2, L2

- **J2** - Station Wagon (Manual)
  - Exemplo: Ford Focus SW, Peugeot 308 SW
  
- **L2** - Station Wagon Automatic
  - Exemplo: Ford Focus SW Auto, Mercedes C Class SW Auto

## 🔄 Lógica de Mapeamento

O sistema usa uma **hierarquia de prioridades** para determinar o grupo correto:

### Prioridade 1: Padrões Específicos
```python
# MÁXIMA PRIORIDADE - Verificado ANTES de tudo
1. Cabrio no nome → G
2. 9 lugares (Transit, Vito, etc) → N
3. 7 lugares (Sharan, Galaxy, etc) → M1/M2
```

### Prioridade 2: VEHICLES Dictionary
```python
# Dicionário parametrizado em carjet_direct.py
# Se o carro está aqui, usar categoria definida manualmente
if car_name in VEHICLES:
    category = VEHICLES[car_name]
    group = map_category_to_group_code(category)
```

### Prioridade 3: Análise de Categoria + Nome + Transmission
```python
# Fallback baseado em:
# 1. Categoria do CarJet (ex: "MINI", "SUVS")
# 2. Nome do carro (keywords: "sw", "4x4", etc)
# 3. Transmission (auto vs manual)
```

## 📝 Exemplos Práticos

### Exemplo 1: VW Polo Auto
```
Categoria CarJet: MINI (Small)
Nome: VW Polo Auto
Transmission: Automatic

Fluxo:
1. Não é cabrio/7/9 lugares ❌
2. Busca em VEHICLES["vw polo auto"] ✅
3. Encontra categoria: "ECONOMY Auto"
4. Mapeia para: E2

Resultado: E2 (Economy Automatic)
```

### Exemplo 2: Ford Focus SW
```
Categoria CarJet: ESTA (Estate Cars)
Nome: Ford Focus SW
Transmission: Manual

Fluxo:
1. Não é cabrio/7/9 lugares ❌
2. Busca em VEHICLES["ford focus sw"] ✅
3. Encontra categoria: "Station Wagon"
4. Mapeia para: J2

Resultado: J2 (Station Wagon Manual)
```

### Exemplo 3: VW Sharan Auto
```
Categoria CarJet: VANS (People Carrier)
Nome: VW Sharan Auto
Transmission: Automatic

Fluxo:
1. Pattern "vw sharan" → 7 lugares detectado ✅
2. is_auto = True
3. Mapeia para: M2

Resultado: M2 (7 Seater Automatic)
```

### Exemplo 4: Mini Cooper Cabrio Auto
```
Categoria CarJet: LUXU (Premium)
Nome: Mini Cooper Cabrio Auto
Transmission: Automatic

Fluxo:
1. "cabrio" no nome → MÁXIMA PRIORIDADE ✅
2. Mapeia para: G

Resultado: G (Cabrio)
```

## ⚠️ Notas Importantes

1. **Filtro Automático Ativo:**
   - Atualmente o sistema envia `frmTrans: "au"` no POST ao CarJet
   - Isso significa que TODOS os carros retornados são automáticos
   - Categorias manuais (B1, B2, D, F, J2, M1) não aparecem nos resultados

2. **Categorias Amplas:**
   - `MINI`, `SUVS`, `VANS` retornam múltiplos grupos
   - O grupo final é determinado pelo modelo específico do carro
   - Não há um mapeamento 1:1 de categoria → grupo

3. **VEHICLES Dictionary Tem Prioridade:**
   - Se o carro está parametrizado em `carjet_direct.py`, usar sempre essa categoria
   - Ignora categoria que o CarJet envia
   - Garante consistência nos preços

4. **Station Wagons (SW):**
   - Sempre verificar ANTES de qualquer normalização
   - "Ford Focus SW" ≠ "Ford Focus"
   - SW tem grupos próprios (J2/L2)

## 📊 Resumo dos Grupos

| Grupo | Descrição | Manual/Auto |
|-------|-----------|-------------|
| B1 | Mini 4 Lugares | Manual |
| B2 | Mini 5 Lugares | Manual |
| D | Economy | Manual |
| E1 | Mini Automatic | Auto |
| E2 | Economy Automatic | Auto |
| F | SUV | Manual |
| G | Cabrio / Premium | Ambos |
| J1 | Crossover | Manual |
| J2 | Station Wagon | Manual |
| L1 | SUV Automatic | Auto |
| L2 | Station Wagon Automatic | Auto |
| M1 | 7 Seater | Manual |
| M2 | 7 Seater Automatic | Auto |
| N | 9 Seater | Ambos |
| X | Luxury (depreciado) | Ambos |
| Others | Não mapeado | Ambos |

## 🔧 Código Relevante

**Função principal:** `map_category_to_group()` (linha 1857)
**Fallback:** `_map_category_fallback()` (linha 2013)
**Mapeamento direto:** `_map_category_to_group_code()` (linha 1906)

**Arquivo:** `main.py`
