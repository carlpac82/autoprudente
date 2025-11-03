# 🔍 LocalStorage Audit - Dados que precisam migrar para Database

## ⚠️ PROBLEMA CRÍTICO
Quando o Render entra em sleep ou há um redeploy, todos os dados em localStorage são PERDIDOS!

## 📊 Dados atualmente em localStorage (PERDIDOS em sleep):

### 1. **Price Automation Settings** ⚠️ CRÍTICO
- `priceAutomationSettings` - Configurações gerais (comissão, margem, etc)
- **Status**: Parcialmente na DB, mas usa localStorage como backup
- **Impacto**: ALTO - Configurações de cálculo de preços

### 2. **Automated Price Rules** ⚠️ CRÍTICO
- `automatedPriceRules` - Regras por localização/grupo/mês/dia
- **Status**: Salvando na DB mas usando localStorage como cache
- **Impacto**: MUITO ALTO - Todas as regras de automação

### 3. **Price Validation Rules** ⚠️ CRÍTICO
- `priceValidationRules` - Regras de validação de preços
- **Status**: APENAS localStorage (SEM DATABASE!)
- **Impacto**: ALTO - Regras de comparação entre grupos

### 4. **AI Price Data** ⚠️ MÉDIO
- `priceAIData` - Ajustes e sugestões de IA
- **Status**: APENAS localStorage
- **Impacto**: MÉDIO - Histórico de aprendizagem

### 5. **Vans Pricing** ⚠️ ALTO
- `vansPricing` - Preços fixos para C3, C4, C5
- **Status**: APENAS localStorage
- **Impacto**: ALTO - Preços de carrinhas comerciais

### 6. **Custom Days** ⚠️ MÉDIO
- `customDias` - Dias personalizados para pesquisa
- **Status**: APENAS localStorage
- **Impacto**: MÉDIO - Configuração de pesquisa

### 7. **Pricing Strategies** ⚠️ ALTO
- `pricingStrategies` - Estratégias de pricing
- **Status**: APENAS localStorage
- **Impacto**: ALTO - Lógica de precificação

### 8. **Downloads History** ⚠️ BAIXO
- `downloadsHistory` - Histórico de downloads Excel
- **Status**: APENAS localStorage
- **Impacto**: BAIXO - Apenas histórico visual

### 9. **Calendar Scans History** ⚠️ BAIXO
- `calendarScansHistory` - Histórico de scans de calendário
- **Status**: APENAS localStorage
- **Impacto**: BAIXO - Apenas histórico visual

### 10. **Language Preference** ✅ OK
- `siteLanguage` - Preferência de idioma (pt/en)
- **Status**: localStorage (OK para este caso)
- **Impacto**: BAIXO - Preferência do usuário

### 11. **Group Hierarchy Rules** ⚠️ ALTO
- `groupHierarchyRules` - Regras de hierarquia entre grupos
- **Status**: APENAS localStorage
- **Impacto**: ALTO - Dependências de preços

## 📋 PLANO DE AÇÃO

### Fase 1: Criar tabelas na database ✅
```sql
-- Já existe: price_automation_settings
-- Já existe: price_automation_rules

-- CRIAR:
CREATE TABLE price_validation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vans_pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pricing_data TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ai_price_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ai_data TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE custom_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    days_data TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_hierarchy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hierarchy_data TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fase 2: Migrar APIs para usar Database
- [ ] Price Validation Rules - Criar API save/load
- [ ] Vans Pricing - Criar API save/load
- [ ] AI Price Data - Criar API save/load
- [ ] Custom Days - Criar API save/load
- [ ] Group Hierarchy - Criar API save/load

### Fase 3: Atualizar Frontend
- [ ] Remover localStorage.setItem
- [ ] Adicionar fetch() para database
- [ ] Manter localStorage apenas como cache temporário

### Fase 4: Backup System
- [ ] Incluir TODAS as tabelas no backup
- [ ] Testar restore completo
- [ ] Validar que nada se perde em redeploy

## 🎯 PRIORIDADES

### P0 - URGENTE (Perda de dados crítica)
1. ✅ Price Automation Rules (já tem DB mas precisa validar)
2. ⚠️ Price Validation Rules (SEM DB!)
3. ⚠️ Vans Pricing (SEM DB!)
4. ⚠️ Group Hierarchy (SEM DB!)

### P1 - IMPORTANTE (Perda de configuração)
5. ⚠️ Price Automation Settings (precisa validar)
6. ⚠️ AI Price Data
7. ⚠️ Custom Days

### P2 - BAIXA (Apenas histórico)
8. Downloads History (pode ficar em localStorage)
9. Calendar Scans History (pode ficar em localStorage)

## ✅ O QUE JÁ ESTÁ NA DATABASE

1. **Users** - ✅ Tabela `users`
2. **OAuth Tokens** - ✅ Tabela `oauth_tokens`
3. **Car Groups** - ✅ Tabela `car_groups`
4. **Vehicle Mappings** - ✅ Tabela `vehicle_name_mappings`
5. **Price Automation Settings** - ✅ Tabela `price_automation_settings`
6. **Price Automation Rules** - ✅ Tabela `price_automation_rules`

## 🚨 RISCO ATUAL

**ALTO RISCO**: Se o Render fizer redeploy ou entrar em sleep:
- ❌ Todas as regras de validação são PERDIDAS
- ❌ Todos os preços de carrinhas são PERDIDOS
- ❌ Todas as hierarquias de grupos são PERDIDA
- ❌ Todos os dados de IA são PERDIDOS
- ❌ Dias customizados são PERDIDOS

**IMPACTO**: Usuário tem que reconfigurar TUDO manualmente!

## 💡 SOLUÇÃO

Migrar TUDO para database e usar localStorage apenas como cache de leitura rápida.
