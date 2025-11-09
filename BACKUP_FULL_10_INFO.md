# 🔒 BACKUP FULL 10 - Informação Completa

**Data:** 2025-11-09 03:55:22  
**Versão:** FULL_10  
**Ficheiro:** `backup_FULL_10_20251109_035522.json`  
**Tamanho:** 9.81 MB

---

## 📊 Resumo do Backup

| Item | Quantidade |
|------|------------|
| **Tabelas exportadas** | 11/13 |
| **Total de registros** | 265 |
| **Tamanho** | 9.81 MB |

---

## 📋 Tabelas Incluídas

### ✅ Dados Principais

1. **damage_reports** - 41 registros
   - ✅ Metadados completos (DR number, cliente, veículo, datas, etc)
   - ⚠️ PDFs excluídos (campo `pdf_data` não exportado para economizar espaço)
   - ⚠️ Imagens de veículo excluídas (campo `vehicle_damage_image`)
   - **Nota:** DR40/2025 sem PDF está incluído (metadados)

2. **damage_report_templates** - 51 registros
   - ✅ Metadados (versão, número de páginas, filename, datas)
   - ⚠️ Template data (PDF blob) excluído
   - **Template ativo:** v51

3. **damage_report_coordinates** - 89 registros
   - ✅ TODOS os mapeamentos de campos PDF
   - ✅ Coordenadas (x, y, width, height, page)
   - ✅ Field IDs e tipos

4. **damage_report_numbering** - 1 registro
   - ✅ Configuração de numeração automática
   - ✅ Prefixo, contador atual, próximo número

---

### ✅ Templates e Configurações

5. **dr_email_templates** - 4 registros
   - ✅ Templates HTML profissionais (PT, EN, FR, DE)
   - ✅ Subject e body completos
   - **NOVO:** Templates HTML com gradient e design moderno

6. **oauth_tokens** - 2 registros
   - ✅ Tokens Gmail OAuth
   - ✅ Access token, refresh token, expiry
   - ⚠️ **SENSÍVEL:** Não partilhar este backup publicamente

7. **users** - 3 registros
   - ✅ Utilizadores do sistema
   - ⚠️ **SENSÍVEL:** Passwords estão hashados mas não partilhar

---

### ✅ Automação de Preços

8. **automated_search_history** - 9 registros
   - ✅ Histórico de pesquisas automatizadas
   - ✅ Preços por grupo de carro e dias

9. **recent_searches** - 65 registros
   - ✅ Pesquisas recentes (manuais e automatizadas)
   - ✅ Resultados em JSON

10. **car_groups** - 0 registros
    - ℹ️ Tabela vazia (grupos não configurados)

11. **automated_prices_history** - 0 registros
    - ℹ️ Tabela vazia

---

### ❌ Tabelas Não Encontradas

- **price_automation_rules** - Tabela não existe
- **price_automation_strategies** - Tabela não existe

---

## 🔄 Como Restaurar

### Opção 1: Restaurar Tudo (Perigoso!)
```bash
# Atenção: Isto vai SUBSTITUIR todos os dados atuais!
python3 restore_backup.py backup_FULL_10_20251109_035522.json --full
```

### Opção 2: Restaurar Tabela Específica
```bash
# Restaurar apenas coordenadas
python3 restore_backup.py backup_FULL_10_20251109_035522.json --table damage_report_coordinates

# Restaurar apenas templates de email
python3 restore_backup.py backup_FULL_10_20251109_035522.json --table dr_email_templates
```

### Opção 3: Ver Conteúdo Sem Restaurar
```bash
# Ver estrutura do backup
python3 -c "import json; data = json.load(open('backup_FULL_10_20251109_035522.json')); print(list(data['tables'].keys()))"

# Ver dados de uma tabela
python3 -c "import json; data = json.load(open('backup_FULL_10_20251109_035522.json')); print(data['tables']['dr_email_templates'])"
```

---

## ⚠️ Avisos Importantes

### 🔐 Dados Sensíveis
Este backup contém:
- ❌ **Passwords** (hashados mas sensíveis)
- ❌ **OAuth tokens** (acesso ao Gmail)
- ❌ **Dados de clientes** (nomes, emails, moradas)

**NÃO PARTILHAR PUBLICAMENTE!**

### 💾 Dados Excluídos
Para economizar espaço, estes dados NÃO estão no backup:
- ❌ PDFs dos Damage Reports (campo `pdf_data` - ~1.8-2.4 MB cada)
- ❌ Template PDFs (campo `template_data`)
- ❌ Imagens de veículos (campo `vehicle_damage_image`)

**Se precisares dos PDFs:** Fazer backup separado ou download manual.

---

## 📝 Notas da Sessão

### Problemas Corrigidos Hoje:
1. ✅ **DR40/2025** - Criado sem PDF (será gerado automaticamente agora)
2. ✅ **Botão "Criar DR"** - Mudado para verde com geração automática de PDF
3. ✅ **Templates de Email** - Atualizados para HTML profissional (4 idiomas)

### Funcionalidades Novas:
1. ✅ Endpoint `POST /api/damage-reports/{dr_number}/generate-and-save-pdf`
2. ✅ Geração automática de PDF ao criar DR
3. ✅ Templates HTML com gradient e design moderno

### Deploys Pendentes:
- Commit e440984 (templates HTML) - Deploy em progresso

---

## 🎯 Estado Atual do Sistema

| Item | Status |
|------|--------|
| **DRs na BD** | 41 (DR1-DR41) |
| **DRs com PDF** | 39 (DR1-39 uploads, DR40-41 sem PDF) |
| **Template ativo** | v51 (2 páginas) |
| **Coordenadas** | 89 campos mapeados |
| **Email templates** | 4 idiomas (HTML) |
| **OAuth Gmail** | ✅ Conectado |

---

## 📞 Suporte

Se precisares restaurar este backup ou tiver problemas:
1. Ler este ficheiro primeiro
2. Testar restauro de UMA tabela antes de restaurar tudo
3. Fazer backup atual ANTES de restaurar backup antigo

---

**Criado:** 2025-11-09 03:55:22  
**Por:** Cascade AI Assistant  
**Versão:** FULL_10
