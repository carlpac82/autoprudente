# ✅ Status da Database - O que está protegido vs O que pode ser perdido

## ✅ TABELAS QUE JÁ EXISTEM (Dados Protegidos)

### 1. ✅ **vans_pricing** - Preços de Carrinhas C3, C4, C5
- **Tabela**: `vans_pricing`
- **Campos**: c3_1day, c3_2days, c3_3days, c4_1day, c4_2days, c4_3days, c5_1day, c5_2days, c5_3days
- **Status**: ✅ EXISTE
- **API**: ❓ PRECISA VERIFICAR se está a usar

### 2. ✅ **automated_price_rules** - Regras Automatizadas
- **Tabela**: `automated_price_rules`
- **Campos**: location, grupo, month, day, rules_json
- **Status**: ✅ EXISTE
- **API**: ✅ `/api/price-automation/rules/save` e `/load`

### 3. ✅ **price_automation_settings** - Configurações Gerais
- **Tabela**: `price_automation_settings`
- **Campos**: setting_key, setting_value, setting_type
- **Status**: ✅ EXISTE
- **API**: ✅ `/api/price-automation/settings/save` e `/load`

### 4. ✅ **custom_days** - Dias Personalizados
- **Tabela**: `custom_days`
- **Campos**: days_array, updated_at
- **Status**: ✅ EXISTE
- **API**: ❓ PRECISA VERIFICAR se está a usar

### 5. ✅ **ai_learning_data** - Dados de IA
- **Tabela**: `ai_learning_data`
- **Campos**: grupo, days, location, adjustment_data
- **Status**: ✅ EXISTE
- **API**: ❓ PRECISA VERIFICAR se está a usar

### 6. ✅ **user_settings** - Configurações de Usuário
- **Tabela**: `user_settings`
- **Campos**: user_key, setting_key, setting_value
- **Status**: ✅ EXISTE
- **API**: ❓ PRECISA VERIFICAR se está a usar

### 7. ✅ **car_groups** - Grupos de Veículos
- **Tabela**: `car_groups`
- **Status**: ✅ EXISTE e EM USO
- **API**: ✅ `/admin/car-groups/*`

### 8. ✅ **users** - Utilizadores
- **Tabela**: `users`
- **Status**: ✅ EXISTE e EM USO
- **API**: ✅ `/admin/users/*`

### 9. ✅ **oauth_tokens** - Tokens OAuth (Gmail)
- **Tabela**: Não encontrada explicitamente, mas deve existir
- **Status**: ❓ PRECISA VERIFICAR

## ❌ O QUE FALTA (Ainda em localStorage)

### 1. ❌ **Price Validation Rules** - CRÍTICO!
- **localStorage**: `priceValidationRules`
- **Tabela**: ❌ NÃO EXISTE
- **API**: ❌ NÃO EXISTE
- **Impacto**: ALTO - Regras de comparação entre grupos
- **Ação**: CRIAR TABELA + API

### 2. ❓ **Group Hierarchy Rules**
- **localStorage**: `groupHierarchyRules`
- **Tabela**: ❓ Não encontrada
- **API**: ❓ PRECISA VERIFICAR
- **Impacto**: ALTO - Dependências de preços

### 3. ❓ **Pricing Strategies**
- **localStorage**: `pricingStrategies`
- **Tabela**: ✅ `pricing_strategies` EXISTE
- **API**: ❓ PRECISA VERIFICAR se está a usar

## 🔍 VERIFICAÇÕES NECESSÁRIAS

### APIs que precisam ser verificadas:

1. **Vans Pricing**
   - Verificar se `/api/vans-pricing/save` existe
   - Verificar se `/api/vans-pricing/load` existe
   - Se não, criar!

2. **Custom Days**
   - Verificar se há API para salvar/carregar
   - Se não, criar!

3. **AI Learning Data**
   - Verificar se há API para salvar/carregar
   - Se não, criar!

4. **Price Validation Rules**
   - ❌ CRIAR TABELA
   - ❌ CRIAR API `/api/price-validation/rules/save`
   - ❌ CRIAR API `/api/price-validation/rules/load`

5. **Group Hierarchy**
   - Verificar se tabela existe
   - Se não, criar tabela + API

## 📦 BACKUP SYSTEM

### O que deve estar no backup:
- ✅ users
- ✅ car_groups
- ✅ vehicle_name_overrides
- ✅ vehicle_photos
- ✅ price_automation_settings
- ✅ automated_price_rules
- ✅ vans_pricing
- ✅ custom_days
- ✅ ai_learning_data
- ✅ user_settings
- ❌ price_validation_rules (CRIAR!)
- ❓ oauth_tokens (VERIFICAR!)
- ❓ group_hierarchy (VERIFICAR!)

## 🎯 PLANO DE AÇÃO IMEDIATO

### Prioridade P0 - URGENTE
1. ✅ Verificar se vans_pricing tem API funcional
2. ❌ Criar tabela + API para price_validation_rules
3. ✅ Verificar se custom_days tem API funcional
4. ✅ Atualizar backup para incluir TODAS as tabelas

### Prioridade P1 - IMPORTANTE
5. ✅ Verificar oauth_tokens
6. ✅ Verificar group_hierarchy
7. ✅ Testar restore completo

### Prioridade P2 - MELHORIA
8. ✅ Documentar todas as APIs
9. ✅ Criar testes de persistência
10. ✅ Validar que nada usa localStorage sem DB

## 🚨 RISCO ATUAL

**MÉDIO RISCO**: 
- ✅ Maioria dos dados JÁ está na database
- ❌ Price Validation Rules ainda em localStorage (PERDA GARANTIDA!)
- ❓ Algumas APIs podem não estar a salvar corretamente

**AÇÃO IMEDIATA**: 
1. Criar API para Price Validation Rules
2. Verificar se todas as outras APIs estão funcionais
3. Atualizar backup system
