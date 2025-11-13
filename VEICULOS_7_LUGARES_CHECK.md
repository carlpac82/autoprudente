# ✅ VEÍCULOS 7 LUGARES - VERIFICAÇÃO COMPLETA

## 🔧 FIX APLICADO

### Problema Resolvido:
- **Citroen C4 Picasso Auto** estava em **L1** (SUV Automatic)
- Agora corrigido para **M2** (7 Seater Automatic) ✅

---

## 📋 LISTA COMPLETA - VEÍCULOS 7 LUGARES

### Modelos que DEVEM estar em M1 (Manual) ou M2 (Automático):

#### **CITROEN:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Citroen C4 Picasso | M1 | M2 | ✅ CORRIGIDO |
| Citroen Grand C4 Picasso | M1 | M2 | ✅ CORRIGIDO |
| Citroen Grand Spacetourer | M1 | M2 | ✅ CORRIGIDO |
| Citroen Grand Space Tourer | M1 | M2 | ✅ CORRIGIDO |
| Citroen Berlingo XL | M1 | M2 | ⚠️ VERIFICAR |

#### **PEUGEOT:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Peugeot 5008 | M1 | M2 | ✅ JÁ EXISTIA |
| Peugeot Rifter | M1 | M2 | ⚠️ VERIFICAR |
| Peugeot Traveller | M1 | M2 | ⚠️ VERIFICAR |

#### **RENAULT:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Renault Grand Scenic | M1 | M2 | ⚠️ VERIFICAR |
| Renault Scenic | M1 | M2 | ⚠️ VERIFICAR |
| Renault Kangoo | M1 | M2 | ⚠️ VERIFICAR |

#### **VOLKSWAGEN:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| VW Caddy | M1 | M2 | ⚠️ VERIFICAR |
| VW Touran | M1 | M2 | ⚠️ VERIFICAR |
| VW Sharan | M1 | M2 | ⚠️ VERIFICAR |

#### **DACIA:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Dacia Lodgy | M1 | M2 | ⚠️ VERIFICAR |
| Dacia Jogger | M1 | M2 | ⚠️ VERIFICAR |

#### **SEAT:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Seat Alhambra | M1 | M2 | ⚠️ VERIFICAR |
| Seat Tarraco | M1 | M2 | ⚠️ VERIFICAR |

#### **OPEL:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Opel Combo | M1 | M2 | ⚠️ VERIFICAR |
| Opel Zafira | M1 | M2 | ⚠️ VERIFICAR |

#### **FORD:**
| Modelo | Manual | Automático | Status Fix |
|--------|--------|------------|------------|
| Ford S-Max | M1 | M2 | ⚠️ VERIFICAR |
| Ford Galaxy | M1 | M2 | ⚠️ VERIFICAR |

---

## 🔍 COMO VERIFICAR SE HÁ MAIS PROBLEMAS

### Passo 1: Fazer Pesquisa CarJet
1. Ir para "Preços Automatizados"
2. Fazer pesquisa para qualquer data
3. Ativar "Follow Lowest"

### Passo 2: Verificar Cada Grupo
Procurar nos grupos **ERRADOS**:

#### ❌ **Grupo L1 (SUV Automatic):**
Se aparecer algum destes, está ERRADO:
- Citroen C4 Picasso Auto ✅ (já corrigido)
- Grand Scenic Auto
- VW Caddy Auto
- Peugeot Rifter Auto
- Dacia Lodgy Auto

#### ❌ **Grupo F (SUV Manual):**
Se aparecer algum destes, está ERRADO:
- Citroen C4 Picasso Manual
- Grand Scenic Manual
- VW Caddy Manual
- Peugeot Rifter Manual

#### ✅ **Grupo M2 (7 Seater Auto) - CORRETO:**
Deve aparecer:
- Citroen C4 Picasso Auto ✅
- Grand Scenic Auto
- VW Caddy Auto
- Peugeot 5008 Auto ✅
- Renault Grand Scenic Auto

#### ✅ **Grupo M1 (7 Seater Manual) - CORRETO:**
Deve aparecer:
- Citroen C4 Picasso Manual
- Grand Scenic Manual
- VW Caddy Manual
- Peugeot 5008 Manual
- Dacia Lodgy

---

## 🚨 SE ENCONTRARES MAIS ERROS

### Reporta assim:
```
Modelo: [Nome completo do carro]
Transmissão: [Manual/Automático]
Aparece em: [Grupo atual - ex: L1]
Deveria ser: [Grupo correto - ex: M2]
Fornecedor: [Autoprudente/Goldcar/etc]
```

### Exemplo:
```
Modelo: Renault Grand Scenic Auto
Transmissão: Automático
Aparece em: L1 (SUV Automatic)
Deveria ser: M2 (7 Seater Automatic)
Fornecedor: Goldcar
```

---

## 📊 CATEGORIAS CARJET QUE CAUSAM CONFUSÃO

O CarJet às vezes categoriza veículos 7 lugares como:
- ❌ `SUV` ou `SUV Automatic` → Causa problema (vai para L1/F)
- ❌ `Premium` ou `Luxury` → Causa problema (vai para Others)
- ✅ `7 Seater` ou `7 Seats` → Funciona bem (vai para M1/M2)
- ✅ `MPV` ou `People Carrier` → Funciona bem (vai para M1/M2)

### Solução Implementada:
Verificar **nome do carro** antes de aplicar regra da categoria!

---

## 🔄 PRÓXIMOS PASSOS

### Se encontrares mais modelos problemáticos:
1. Faz print da pesquisa CarJet
2. Anota o modelo exato que aparece errado
3. Reporta aqui
4. Vou adicionar exceção como fiz para C4 Picasso

### Modelos Prioritários para Verificar:
- ⚠️ **Renault Grand Scenic Auto** (comum em Portugal)
- ⚠️ **VW Caddy Auto** (muito usado Autoprudente)
- ⚠️ **Dacia Lodgy** (económico, popular)
- ⚠️ **Peugeot Rifter** (novo modelo)

---

## 💡 DICA DE TESTE RÁPIDO

### Console Browser (F12):
```javascript
// Ver todos os carros e suas categorias
document.querySelectorAll('[data-grupo]').forEach(el => {
    const grupo = el.getAttribute('data-grupo');
    const carro = el.closest('.car-item')?.querySelector('.car-name')?.textContent;
    if (carro && (carro.includes('Picasso') || carro.includes('Scenic') || 
                   carro.includes('Caddy') || carro.includes('Lodgy'))) {
        console.log(`${carro} → Grupo ${grupo}`);
    }
});
```

---

## ✅ CHECKLIST FINAL

- [x] Citroen C4 Picasso Auto → M2 ✅
- [x] Citroen Grand C4 Picasso → M1/M2 ✅
- [x] Citroen Grand Spacetourer → M1/M2 ✅
- [x] Peugeot 5008 → M1/M2 ✅ (já existia)
- [ ] Renault Grand Scenic → TESTAR
- [ ] VW Caddy → TESTAR
- [ ] Dacia Lodgy → TESTAR
- [ ] Peugeot Rifter → TESTAR
- [ ] Opel Zafira → TESTAR
- [ ] Ford S-Max → TESTAR

---

**Faz uma pesquisa agora e reporta qualquer modelo 7 lugares que apareça em L1 ou F!** 🔍
