home/**
 * Internationalization (i18n) System
 * Supports Portuguese (pt) and English (en)
 */

const translations = {
    pt: {
        // Navigation
        'nav.prices': 'Preços',
        'nav.automation': 'Automação',
        'nav.settings': 'Definições',
        'nav.logout': 'Sair',
        
        // Search
        'search.title': 'Pesquisar por Parâmetros',
        'search.location': 'Localização',
        'search.pickupDate': 'Data de Levantamento',
        'search.pickupLocation': 'Local de Levantamento',
        'search.startDate': 'Data de Início',
        'search.days': 'Dias',
        'search.button': 'Pesquisar',
        'search.searchAllDays': 'Pesquisar Todos os Dias',
        'search.searching': 'A pesquisar',
        'search.noResults': 'Nenhum resultado encontrado',
        
        // Filter
        'filter.byCompany': 'Filtrar por Empresa',
        
        // Results
        'results.supplier': 'Fornecedor',
        'results.car': 'Carro',
        'results.price': 'Preço',
        'results.pricePerDay': 'Preço/Dia',
        'results.group': 'Grupo',
        'results.loading': 'A carregar resultados...',
        
        // Vehicles Editor
        'vehicles.title': 'Editor de Nomes de Veículos',
        'vehicles.editorTitle': 'Editor de Nomes de Veículos',
        'vehicles.allVehicles': 'Todos os Veículos',
        'vehicles.uncategorized': 'Sem Categoria',
        'vehicles.categoryManagement': 'Gestão de Categorias & Grupos',
        'vehicles.categoryDescription': 'Criar e gerir categorias e grupos de veículos',
        'vehicles.newCategory': 'Nova Categoria',
        'vehicles.newGroup': 'Novo Grupo',
        'vehicles.allBrands': 'Todas as marcas',
        'vehicles.allCategories': 'Todas as categorias',
        'vehicles.photo': 'FOTO',
        'vehicles.originalName': 'NOME ORIGINAL',
        'vehicles.cleanName': 'NOME LIMPO',
        'vehicles.group': 'GRUPO',
        'vehicles.category': 'CATEGORIA',
        'vehicles.actions': 'AÇÕES',
        'vehicles.count': 'veículos',
        
        // Settings
        'settings.title': 'Definições & Personalização',
        'settings.vehicles': 'Veículos',
        'settings.priceAdjustment': 'Ajuste de Preços',
        'settings.priceValidation': 'Validação de Preços',
        'settings.automatedPriceSettings': 'Definições de Preços Automáticos',
        'settings.customization': 'PERSONALIZAÇÃO',
        'settings.backup': 'Backup & Restaurar',
        
        // Backup
        'backup.title': 'Backup & Restaurar',
        'backup.description': 'Faça backup completo de todos os dados do sistema e restaure quando necessário',
        'backup.createTitle': 'Criar Backup',
        'backup.database': 'Base de Dados',
        'backup.databaseDesc': 'Users, histórico de pesquisas, resultados, logs',
        'backup.settings': 'Definições',
        'backup.settingsDesc': 'Branding, cores, company info, formulas',
        'backup.vehicles': 'Mapeamentos de Carros',
        'backup.vehiclesDesc': 'Grupos, categorias, fotos de perfil',
        'backup.automation': 'Automação de Preços',
        'backup.automationDesc': 'Regras, alertas, validações',
        'backup.uploads': 'Ficheiros Carregados',
        'backup.uploadsDesc': 'Logos, fotos de perfil, imagens',
        'backup.oauth': 'Configurações OAuth',
        'backup.oauthDesc': 'Tokens, email settings (sensível)',
        'backup.createButton': 'Criar Backup Completo',
        'backup.selectAll': 'Selecionar Tudo',
        'backup.deselectAll': 'Desselecionar Tudo',
        'backup.restoreTitle': 'Restaurar Backup',
        'backup.restoreWarning': 'Atenção',
        'backup.restoreWarningText': 'Restaurar um backup irá substituir TODOS os dados atuais. Esta ação não pode ser desfeita.',
        'backup.uploadFile': 'Carregar Ficheiro de Backup',
        'backup.uploadDesc': 'Clique para selecionar ou arraste o ficheiro .zip aqui',
        'backup.fileSelected': 'Ficheiro Selecionado',
        'backup.restoreNow': 'Restaurar Agora',
        'backup.recentTitle': 'Backups Recentes',
        'backup.noBackups': 'Nenhum backup criado ainda',
        
        // Company Info
        'company.title': 'Informação da Empresa',
        'company.legalName': 'Nome Legal da Empresa',
        'company.taxId': 'NIF / Número de IVA',
        'company.email': 'Email',
        'company.phone': 'Telefone',
        'company.address': 'Morada',
        'company.website': 'Website',
        'company.supportEmail': 'Email de Suporte',
        'company.setupNote': 'Configuração Completa: Preencha todas as informações da empresa para uma plataforma profissional e pronta a usar. Esta informação pode ser usada em relatórios, faturas e comunicações com clientes.',
        
        // Price Adjustment
        'priceAdjustment.title': 'Ajuste de Preços',
        'priceAdjustment.carjetPercentage': 'Percentagem de Ajuste CarJet (%)',
        'priceAdjustment.carjetPercentageDefault': 'Padrão: 0.00% (sem ajuste)',
        'priceAdjustment.carjetOffset': 'Offset CarJet (€)',
        'priceAdjustment.carjetOffsetDefault': 'Padrão: 0.00€ (sem offset)',
        'priceAdjustment.abbycarExport': 'Ajuste de Exportação Excel Abbycar',
        'priceAdjustment.abbycarPercentage': 'Ajuste de Preços Abbycar (%)',
        'priceAdjustment.abbycarDescription': 'Aplica ajuste percentual a TODOS os preços no Excel Abbycar. Exemplo: 5% aumenta todos os preços em 5%, -3% diminui 3%.',
        'priceAdjustment.abbycarDefault': 'Padrão: 3.00%',
        'priceAdjustment.lowDepositGroups': 'Ajuste de Grupos Low Deposit',
        'priceAdjustment.enable': 'Ativar',
        'priceAdjustment.lowDepositDescription': 'Ajuste ADICIONAL apenas para grupos Low Deposit (12 grupos). Grupos afetados: MCMV, NDMR, HDMV, MDAV, EDAR, DFMR, DFMV, IWMV, CFAV, SVMV, SVAR, LVMR. Este valor é somado ao ajuste geral acima.',
        'priceAdjustment.lowDepositExample': 'Exemplo: Geral 3% + Low Deposit 2% = 5% total para esses grupos.',
        'priceAdjustment.lowDepositDefault': 'Padrão: 0.00% (sem ajuste adicional)',
        'priceAdjustment.interfaceAppearance': 'Interface & Aparência',
        'priceAdjustment.themeColor': 'Cor do Tema',
        'priceAdjustment.themeColorDescription': 'Cor principal do tema (botões, links, etc).',
        'priceAdjustment.themeColorDefault': 'Padrão: #3b82f6 (azul)',
        'priceAdjustment.grayscaleIcons': 'Ícones Monocromáticos (Grayscale)',
        'priceAdjustment.grayscaleEnabled': 'Quando ativado, todos os ícones de carros ficam em tons de cinza.',
        'priceAdjustment.grayscaleDisabled': 'Quando desativado, ícones mantêm as cores originais.',
        'priceAdjustment.save': 'Guardar',
        'priceAdjustment.viewJson': 'Ver valores atuais (JSON)',
        'priceAdjustment.abbycarDescription2': 'Aplica ajuste percentual a TODOS os preços no Excel Abbycar.',
        'priceAdjustment.abbycarExample': 'Exemplo: 5% aumenta todos os preços em 5%, -3% diminui 3%.',
        'priceAdjustment.lowDepositGroupsTitle': 'Ajuste de Grupos Low Deposit',
        'priceAdjustment.lowDepositAffected': 'Grupos afetados: MCMV, NDMR, HDMV, MDAV, EDAR, DFMR, DFMV, IWMV, CFAV, SVMV, SVAR, LVMR',
        'priceAdjustment.lowDepositNote': 'Este valor é somado ao ajuste geral acima.',
        'priceAdjustment.interfaceTitle': 'Interface & Aparência',
        'priceAdjustment.themeColorNote': 'Cor principal do tema (botões, links, etc).',
        'priceAdjustment.grayscaleNote1': 'Quando ativado, todos os ícones de carros ficam em tons de cinza.',
        'priceAdjustment.grayscaleNote2': 'Quando desativado, ícones mantêm as cores originais.',
        'priceAdjustment.brokerCommission': 'Comissão do Broker',
        'priceAdjustment.defaultMargin': 'Margem Padrão',
        'priceAdjustment.priceRounding': 'Arredondamento de Preços',
        'priceAdjustment.minPricePerDay': 'Preço Mínimo por Dia',
        'priceAdjustment.minPricePerMonth': 'Preço Mínimo por Mês',
        'priceAdjustment.taxRate': 'Taxa de Imposto',
        'priceAdjustment.defaultCurrency': 'Moeda Padrão',
        
        // Price Validation
        'priceValidation.title': 'Validação de Preços',
        'priceValidation.enableAlerts': 'Ativar Alertas',
        'priceValidation.thresholds': 'Limites de Alerta',
        
        // Automated Reports
        'automatedReports.title': 'Relatórios Automáticos',
        'automatedReports.dailyReport': 'Relatório Diário de Preços',
        'automatedReports.weeklyReport': 'Relatório Semanal',
        'automatedReports.alertEmails': 'Alertas Automáticos',
        
        // Price Automation Tabs
        'automation.automatedPrices': 'Preços Automatizados',
        'automation.currentPrices': 'Preços Atuais',
        'automation.commercialVans': 'Carrinhas Comerciais',
        'automation.history': 'Histórico',
        'automation.downloads': 'Downloads',
        'automation.calendarScans': 'Scans de Calendário',
        'automation.priceHistory': 'Histórico de Preços (2 anos)',
        'automation.commercialVansPricing': 'Preços de Carrinhas Comerciais',
        'automation.configureFixedPrices': 'Configurar preços fixos para grupos C3, C4, C5',
        'automation.savePrices': 'Guardar Preços',
        
        // Email Notifications
        'emailNotifications.title': 'Notificações por Email',
        'emailNotifications.description': 'Configure uma conta de email para receber notificações automáticas sobre alterações de preços, alertas e relatórios.',
        'emailNotifications.provider': 'Fornecedor de Email',
        'emailNotifications.connectGmail': 'Conectar Gmail',
        'emailNotifications.connectOutlook': 'Conectar Outlook',
        'emailNotifications.customSMTP': 'Custom SMTP',
        'emailNotifications.recipients': 'Destinatários das Notificações',
        'emailNotifications.recipientsPlaceholder': 'email1@example.com\nemail2@example.com\nemail3@example.com',
        'emailNotifications.recipientsHelp': 'Um email por linha. Estes emails receberão as notificações.',
        'emailNotifications.notificationTypes': 'Tipos de Notificações',
        'emailNotifications.priceChanges': 'Alterações de Preços',
        'emailNotifications.alerts': 'Alertas de Validação',
        'emailNotifications.reports': 'Relatórios Diários',
        'emailNotifications.testEmail': 'Enviar Email de Teste',
        'emailNotifications.saveSettings': 'Guardar Configurações',
        'emailNotifications.oauthNote': 'Conecte a sua conta de forma segura usando OAuth2. Não é necessário inserir a password.',
        'emailNotifications.connected': 'Conectado',
        'emailNotifications.disconnect': 'Desconectar',
        'emailNotifications.dailyReport': 'Relatório Diário de Preços',
        'emailNotifications.weeklyReport': 'Relatórios Semanais',
        'emailNotifications.errors': 'Erros e Alertas do Sistema',
        'emailNotifications.oauthConnection': 'Conectar Conta',
        'emailNotifications.connectedAccount': 'Conta conectada',
        'emailNotifications.connectedEmail': 'Email conectado',
        
        // Appearance / Theme
        'appearance.title': 'Tema & Cores',
        'appearance.primaryColor': 'Cor Primária',
        'appearance.primaryDesc': 'Cor principal da marca (botões, links, destaques)',
        'appearance.secondaryColor': 'Cor Secundária',
        'appearance.secondaryDesc': 'Cor de destaque secundária (realces, estados hover)',
        'appearance.colorPreview': 'Pré-visualização de Cores',
        'appearance.primary': 'Primária',
        'appearance.secondary': 'Secundária',
        'appearance.button': 'Botão',
        'appearance.primaryButton': 'Botão Primário',
        'appearance.hover': 'Hover',
        'appearance.hoverState': 'Estado Hover',
        'appearance.note': 'Nota: As alterações de cor serão aplicadas em toda a plataforma. Certifique-se de testar completamente após alterar as cores.',
        'settings.automation': 'Automação',
        'settings.branding': 'Marca',
        'settings.appearance': 'Aparência',
        'settings.companyInfo': 'Informação da Empresa',
        'settings.language': 'Idioma',
        'settings.save': 'Guardar Definições',
        'settings.reset': 'Restaurar Padrões',
        'settings.export': 'Exportar',
        'settings.import': 'Importar',
        'settings.users': 'Utilizadores',
        'settings.vehicles': 'Veículos',
        'settings.priceAdjustment': 'Ajuste de Preços',
        'settings.priceValidation': 'Validação de Preços',
        'settings.automatedPriceSettings': 'Definições de Preços Automatizados',
        'settings.companyInfo': 'Informação da Empresa',
        'settings.language': 'Idioma',
        'settings.emailNotifications': 'Notificações por Email',
        'settings.automatedReports': 'Relatórios Automáticos',
        'settings.customization': 'PERSONALIZAÇÃO',
        
        // Page Titles
        'pageTitle.priceAutomationSettings': 'Definições de Automação de Preços',
        'pageTitle.priceValidation': 'Validação de Preços',
        'pageTitle.vehicleNamesEditor': 'Editor de Nomes de Veículos',
        'pageTitle.brandIdentity': 'Identidade da Marca',
        
        // Price Automation Settings
        'priceAutomation.description': 'Configure todos os parâmetros para automação de preços. As alterações são aplicadas em tempo real.',
        'priceAutomation.exportSettings': 'Exportar Todas as Definições',
        'priceAutomation.importSettings': 'Importar Todas as Definições',
        'priceAutomation.globalSettings': 'Definições Globais',
        'priceAutomation.brokerCommission': 'Comissão do Broker (%)',
        'priceAutomation.brokerCommissionHelp': 'Preço NET = Preço Final / (1 + comissão)',
        'priceAutomation.defaultMargin': 'Margem Padrão (%)',
        'priceAutomation.defaultMarginHelp': 'Padrão: 0% (sem margem quando não existe regra)',
        'priceAutomation.rounding': 'Arredondamento',
        'priceAutomation.roundingCents': 'Cêntimos (0.01€)',
        'priceAutomation.roundingHalfEuro': 'Meio Euro (0.50€)',
        'priceAutomation.roundingEuro': 'Euro (1.00€)',
        'priceAutomation.rounding5Euros': '5 Euros (5.00€)',
        'priceAutomation.groupHierarchy': 'Hierarquia de Grupos & Validação de Preços',
        'priceAutomation.groupHierarchyDesc': 'Defina dependências de preços de grupos para garantir consistência de preços entre categorias de veículos.',
        'priceAutomation.addRule': 'Adicionar Regra',
        'priceAutomation.noRules': 'Nenhuma regra configurada',
        'priceAutomation.baseGroup': 'Grupo Base',
        'priceAutomation.targetGroup': 'Grupo Alvo',
        'priceAutomation.margin': 'Margem',
        'priceAutomation.actions': 'Ações',
        'priceAutomation.delete': 'Eliminar',
        'priceAutomation.saveAll': 'Guardar Tudo',
        'priceAutomation.alternativeSearch': 'Pesquisa Alternativa (dias à frente)',
        'priceAutomation.alternativeSearchHelp': 'Se não houver preços, pesquisar X dias à frente',
        'priceAutomation.autoSaveHistory': 'Guardar Automaticamente no Histórico',
        'priceAutomation.enabled': 'Ativado',
        'priceAutomation.disabled': 'Desativado',
        'priceAutomation.autoSaveHistoryHelp': 'Guardar automaticamente preços no histórico ao descarregar',
        'priceAutomation.enableGroupHierarchy': 'Ativar Validação de Hierarquia de Grupos',
        'priceAutomation.availableGroups': 'Grupos Disponíveis',
        'priceAutomation.configureDependencies': 'Configurar Dependências',
        'priceAutomation.ruleInfo': 'Regra: Defina regras de comparação de preços entre grupos.',
        'priceAutomation.operatorsInfo': 'Operadores: ≥ (maior ou igual), ≤ (menor ou igual), > (maior que)',
        'priceAutomation.exampleInfo': 'Exemplo: D ≥ B1 AND D ≥ B2 significa que o preço do grupo D deve ser ≥ tanto B1 como B2',
        'priceAutomation.excludeSuppliers': 'Excluir Fornecedores dos Cálculos',
        'priceAutomation.excludeSuppliersHelp': 'Os fornecedores selecionados serão excluídos dos cálculos de preços',
        'priceAutomation.defaultLocation': 'Localização Padrão',
        'priceAutomation.configuredRules': 'Regras de Dependência Configuradas',
        'priceAutomation.tip': '💡 Dica: Pode definir múltiplas dependências por grupo. Por exemplo, D pode ser definido para ser ≥ tanto B1 como B2.',
        'priceAutomation.referenceSupplier': 'Fornecedor de Referência para Cálculos de Preços (usado ao ler Preços Atuais)',
        'priceAutomation.referenceSupplierHelp': 'Os preços deste fornecedor serão usados como base para cálculos de preços automatizados. Altere se quiser seguir a estratégia de preços de outro fornecedor.',
        'priceAutomation.automatedPriceRules': 'Regras de Preços Automatizados',
        'priceAutomation.manualSettings': 'Definições Manuais',
        'priceAutomation.aiSettings': 'Definições IA',
        'priceAutomation.configureRules': 'Configure como os preços automatizados são calculados para cada localização e grupo',
        'priceAutomation.configureRulesGroup': 'Configure regras para cada grupo:',
        'priceAutomation.selectMonth': 'Selecione o mês:',
        'priceAutomation.selectDay': 'Selecione o dia para configurar:',
        'priceAutomation.changesSavedAuto': '💡 As alterações são guardadas automaticamente',
        'priceAutomation.resetDefaults': 'Restaurar Padrões',
        'priceAutomation.aiLearningSystem': 'Sistema de Aprendizagem IA',
        'priceAutomation.aiDescription': 'A IA observa os seus ajustes manuais de preços na interface visual e aprende padrões para sugerir regras automatizadas.',
        'priceAutomation.manualAdjustments': 'Ajustes Manuais',
        'priceAutomation.patternsDetected': 'Padrões Detetados',
        'priceAutomation.suggestionsReady': 'Sugestões Prontas',
        'priceAutomation.noSuggestions': 'Ainda sem sugestões. A IA precisa de mais dados para detetar padrões.',
        'priceAutomation.makeAdjustments': 'Faça pelo menos 5-10 ajustes manuais para começar a ver sugestões.',
        'priceAutomation.recentAdjustments': 'Ajustes Manuais Recentes',
        'priceAutomation.clearAIData': 'Limpar Dados IA',
        'priceAutomation.refreshSuggestions': 'Atualizar Sugestões',
        'priceAutomation.days': 'dias',
        'priceAutomation.day': 'dia',
        
        // Vehicle Groups
        'groups.mini4doors': 'Mini 4 Portas',
        'groups.mini': 'Mini',
        'groups.economy': 'Económico',
        'groups.miniAuto': 'Mini Automático',
        'groups.economyAuto': 'Económico Automático',
        'groups.suv': 'SUV',
        'groups.premium': 'Premium',
        'groups.crossover': 'Crossover',
        'groups.stationWagon': 'Carrinha',
        'groups.suvAuto': 'SUV Automático',
        'groups.swAuto': 'Carrinha Automática',
        'groups.sevenSeater': '7 Lugares',
        'groups.sevenSeaterAuto': '7 Lugares Automático',
        'groups.nineSeater': '9 Lugares',
        
        // Price Validation
        'validation.groupRules': 'Regras de Grupos',
        'validation.activeAlerts': 'Alertas Ativos',
        'validation.history': 'Histórico',
        'validation.addNewRule': 'Adicionar Nova Regra',
        'validation.baseGroup': 'Grupo Base',
        'validation.select': 'Selecione...',
        'validation.condition': 'Condição',
        'validation.mustBeGreater': 'Deve ser MAIOR que',
        'validation.mustBeGreaterEqual': 'Deve ser MAIOR OU IGUAL a',
        'validation.mustBeLess': 'Deve ser MENOR que',
        'validation.mustBeLessEqual': 'Deve ser MENOR OU IGUAL a',
        'validation.cannotExceed': 'Não pode exceder % de',
        'validation.compareGroups': 'Comparar Grupos (segure Ctrl/Cmd para múltiplos)',
        'validation.selectMultiple': 'Selecione múltiplos grupos para comparar com todos eles',
        'validation.addRule': 'Adicionar Regra',
        'validation.configuredRules': 'Regras Configuradas',
        'validation.pause': 'Pausar',
        'validation.remove': 'Remover',
        'validation.base': 'Base',
        'validation.compare': 'Comparar',
        
        // Vehicles Page
        'vehicles.vehicleNamesEditor': 'Editor de Nomes de Veículos',
        'vehicles.allVehicles': 'Todos os Veículos',
        'vehicles.uncategorized': 'Sem Categoria',
        'vehicles.categoryManagement': 'Gestão de Categorias & Grupos',
        'vehicles.categoryManagementDesc': 'Criar e gerir categorias e grupos de veículos',
        'vehicles.newCategory': 'Nova Categoria',
        'vehicles.newGroup': 'Novo Grupo',
        'vehicles.allBrands': 'Todas as marcas',
        'vehicles.allCategories': 'Todas as categorias',
        
        // Price Automation Page
        'automation.priceAutomation': 'Automação de Preços',
        'automation.description': 'Preencha os preços do CarJet para comparação e análise de competitividade',
        'automation.automatedPrices': 'Preços Automatizados',
        'automation.currentPrices': 'Preços Atuais',
        'automation.commercialVans': 'Carrinhas Comerciais',
        'automation.history': 'Histórico',
        'automation.location': 'Localização',
        'automation.dateSelection': 'Seleção de Data',
        'automation.specificDate': 'Data Específica',
        'automation.byMonth': 'Por Mês',
        'automation.byYear': 'Por Ano',
        'automation.byPricePeriod': 'Por Período de Preços',
        'automation.startDate': 'Data de Início',
        'automation.view': 'Ver:',
        'automation.manageColumns': 'Gerir colunas:',
        'automation.add': 'Adicionar',
        'automation.remove': 'Remover',
        'automation.tariffPeriod': 'Período Tarifário:',
        'automation.to': 'até',
        'automation.downloadExcel': 'Download Excel:',
        'automation.fillMethod': 'Método de Preenchimento:',
        'automation.auto': 'Auto',
        'automation.ai': 'IA',
        'automation.usingRules': 'Usando automação baseada em regras',
        'automation.group': 'Grupo',
        
        // Home Page
        'home.searchByParameters': 'Pesquisar por Parâmetros',
        'home.pickupLocation': 'Local de Recolha',
        'home.startDate': 'Data de Início',
        'home.days': 'Dias',
        'home.search': 'Pesquisar',
        'home.searchAllDays': 'Pesquisar Todos os Dias',
        
        // Branding
        'branding.title': 'Identidade da Marca',
        'branding.brandIdentity': 'Identidade da Marca',
        'branding.companyName': 'Nome da Empresa',
        'branding.defaultSupplier': 'Fornecedor Padrão',
        'branding.logoUrl': 'URL do Logotipo',
        'branding.faviconUrl': 'URL do Favicon',
        'branding.logoPreview': 'Pré-visualização do Logotipo',
        'branding.noLogo': 'Sem logotipo - a usar padrão',
        
        // Appearance
        'appearance.title': 'Tema & Cores',
        'appearance.primaryColor': 'Cor Primária',
        'appearance.secondaryColor': 'Cor Secundária',
        'appearance.preview': 'Pré-visualização',
        
        // Company Info
        'company.title': 'Informação da Empresa',
        'company.legalName': 'Nome Legal',
        'company.taxId': 'NIF / VAT',
        'company.email': 'Email',
        'company.phone': 'Telefone',
        'company.address': 'Morada',
        'company.website': 'Website',
        'company.supportEmail': 'Email de Suporte',
        
        // Formulas
        'formulas.title': 'Fórmulas & Cálculos',
        'formulas.brokerCommission': 'Comissão do Broker (%)',
        'formulas.defaultMargin': 'Margem Padrão (%)',
        'formulas.rounding': 'Arredondamento de Preços',
        'formulas.minPricePerDay': 'Preço Mínimo por Dia (€)',
        'formulas.minPricePerMonth': 'Preço Mínimo por Mês (€)',
        'formulas.taxRate': 'Taxa de IVA (%)',
        'formulas.currency': 'Moeda Padrão',
        
        // Notifications
        'notif.saved': 'Guardado com sucesso!',
        'notif.error': 'Erro ao guardar',
        'notif.loading': 'A carregar...',
        'notif.settingsSaved': 'Definições guardadas!',
        'notif.brandingSaved': 'Marca guardada!',
        'notif.colorsSaved': 'Cores guardadas e aplicadas!',
        'notif.companySaved': 'Informação da empresa guardada!',
        'notif.formulasSaved': 'Fórmulas guardadas!',
        
        // Common
        'common.yes': 'Sim',
        'common.no': 'Não',
        'common.cancel': 'Cancelar',
        'common.confirm': 'Confirmar',
        'common.close': 'Fechar',
        'common.save': 'Guardar',
        'common.delete': 'Eliminar',
        'common.edit': 'Editar',
        'common.add': 'Adicionar',
        'common.remove': 'Remover',
        'common.search': 'Pesquisar',
        'common.filter': 'Filtrar',
        'common.sort': 'Ordenar',
        'common.loading': 'A carregar...',
        'common.error': 'Erro',
        'common.success': 'Sucesso',
        'common.warning': 'Aviso',
        'common.info': 'Informação',
    },
    
    en: {
        // Navigation
        'nav.prices': 'Prices',
        'nav.automation': 'Automation',
        'nav.settings': 'Settings',
        'nav.logout': 'Logout',
        
        // Search
        'search.title': 'Search by Parameters',
        'search.location': 'Location',
        'search.pickupDate': 'Pickup Date',
        'search.pickupLocation': 'Pickup Location',
        'search.startDate': 'Start Date',
        'search.days': 'Days',
        'search.button': 'Search',
        'search.searchAllDays': 'Search All Days',
        'search.searching': 'Searching',
        'search.noResults': 'No results found',
        
        // Filter
        'filter.byCompany': 'Filter by Company',
        
        // Results
        'results.supplier': 'Supplier',
        'results.car': 'Car',
        'results.price': 'Price',
        'results.pricePerDay': 'Price/Day',
        'results.group': 'Group',
        'results.loading': 'Loading results...',
        
        // Vehicles Editor
        'vehicles.title': 'Vehicle Names Editor',
        'vehicles.editorTitle': 'Vehicle Names Editor',
        'vehicles.allVehicles': 'All Vehicles',
        'vehicles.uncategorized': 'Uncategorized',
        'vehicles.categoryManagement': 'Category & Group Management',
        'vehicles.categoryDescription': 'Create and manage vehicle categories and groups',
        'vehicles.newCategory': 'New Category',
        'vehicles.newGroup': 'New Group',
        'vehicles.allBrands': 'All brands',
        'vehicles.allCategories': 'All categories',
        'vehicles.photo': 'PHOTO',
        'vehicles.originalName': 'ORIGINAL NAME',
        'vehicles.cleanName': 'CLEAN NAME',
        'vehicles.group': 'GROUP',
        'vehicles.category': 'CATEGORY',
        'vehicles.actions': 'ACTIONS',
        'vehicles.count': 'Vehicles',
        
        // Settings
        'settings.title': 'Settings & Customization',
        'settings.vehicles': 'Vehicles',
        'settings.priceAdjustment': 'Price Adjustment',
        'settings.priceValidation': 'Price Validation',
        'settings.automatedPriceSettings': 'Automated Price Settings',
        'settings.customization': 'CUSTOMIZATION',
        'settings.backup': 'Backup & Restore',
        
        // Company Info
        'company.title': 'Company Information',
        'company.legalName': 'Legal Company Name',
        'company.taxId': 'Tax ID / VAT Number',
        'company.email': 'Email',
        'company.phone': 'Phone',
        'company.address': 'Address',
        'company.website': 'Website',
        'company.supportEmail': 'Support Email',
        'company.setupNote': 'Complete Setup: Fill in all company information for a professional, ready-to-use platform. This information can be used in reports, invoices, and customer communications.',
        
        // Price Adjustment
        'priceAdjustment.title': 'Price Adjustment',
        'priceAdjustment.carjetPercentage': 'CarJet Adjustment Percentage (%)',
        'priceAdjustment.carjetPercentageDefault': 'Default: 0.00% (no adjustment)',
        'priceAdjustment.carjetOffset': 'CarJet Offset (€)',
        'priceAdjustment.carjetOffsetDefault': 'Default: 0.00€ (no offset)',
        'priceAdjustment.abbycarExport': 'Abbycar Excel Export Adjustment',
        'priceAdjustment.abbycarPercentage': 'Price Adjustment Abbycar (%)',
        'priceAdjustment.abbycarDescription': 'Applies percentage adjustment to ALL prices in Abbycar Excel. Example: 5% increases all prices by 5%, -3% decreases by 3%.',
        'priceAdjustment.abbycarDefault': 'Default: 3.00%',
        'priceAdjustment.lowDepositGroups': 'Low Deposit Groups Adjustment',
        'priceAdjustment.enable': 'Enable',
        'priceAdjustment.lowDepositDescription': 'ADDITIONAL adjustment only for Low Deposit groups (12 groups). Affected groups: MCMV, NDMR, HDMV, MDAV, EDAR, DFMR, DFMV, IWMV, CFAV, SVMV, SVAR, LVMR. This value is added to the general adjustment above.',
        'priceAdjustment.lowDepositExample': 'Example: General 3% + Low Deposit 2% = 5% total for these groups.',
        'priceAdjustment.lowDepositDefault': 'Default: 0.00% (no additional adjustment)',
        'priceAdjustment.interfaceAppearance': 'Interface & Appearance',
        'priceAdjustment.themeColor': 'Theme Color',
        'priceAdjustment.themeColorDescription': 'Main theme color (buttons, links, etc).',
        'priceAdjustment.themeColorDefault': 'Default: #3b82f6 (blue)',
        'priceAdjustment.grayscaleIcons': 'Monochromatic Icons (Grayscale)',
        'priceAdjustment.grayscaleEnabled': 'When enabled, all car icons become grayscale.',
        'priceAdjustment.grayscaleDisabled': 'When disabled, icons keep original colors.',
        'priceAdjustment.save': 'Save',
        'priceAdjustment.viewJson': 'View current values (JSON)',
        'priceAdjustment.abbycarDescription2': 'Applies percentage adjustment to ALL prices in Abbycar Excel.',
        'priceAdjustment.abbycarExample': 'Example: 5% increases all prices by 5%, -3% decreases by 3%.',
        'priceAdjustment.lowDepositGroupsTitle': 'Low Deposit Groups Adjustment',
        'priceAdjustment.lowDepositAffected': 'Affected groups: MCMV, NDMR, HDMV, MDAV, EDAR, DFMR, DFMV, IWMV, CFAV, SVMV, SVAR, LVMR',
        'priceAdjustment.lowDepositNote': 'This value is added to the general adjustment above.',
        'priceAdjustment.interfaceTitle': 'Interface & Appearance',
        'priceAdjustment.themeColorNote': 'Main theme color (buttons, links, etc).',
        'priceAdjustment.grayscaleNote1': 'When enabled, all car icons become grayscale.',
        'priceAdjustment.grayscaleNote2': 'When disabled, icons keep original colors.',
        'priceAdjustment.brokerCommission': 'Broker Commission',
        'priceAdjustment.defaultMargin': 'Default Margin',
        'priceAdjustment.priceRounding': 'Price Rounding',
        'priceAdjustment.minPricePerDay': 'Minimum Price per Day',
        'priceAdjustment.minPricePerMonth': 'Minimum Price per Month',
        'priceAdjustment.taxRate': 'Tax Rate',
        'priceAdjustment.defaultCurrency': 'Default Currency',
        
        // Price Validation
        'priceValidation.title': 'Price Validation',
        'priceValidation.enableAlerts': 'Enable Alerts',
        'priceValidation.thresholds': 'Alert Thresholds',
        
        // Automated Reports
        'automatedReports.title': 'Automated Reports',
        'automatedReports.dailyReport': 'Daily Price Report',
        'automatedReports.weeklyReport': 'Weekly Report',
        'automatedReports.alertEmails': 'Automatic Alerts',
        
        // Price Automation Tabs
        'automation.automatedPrices': 'Automated Prices',
        'automation.currentPrices': 'Current Prices',
        'automation.commercialVans': 'Commercial Vans',
        'automation.history': 'History',
        'automation.downloads': 'Downloads',
        'automation.calendarScans': 'Calendar Scans',
        'automation.priceHistory': 'Price History (2 years)',
        'automation.commercialVansPricing': 'Commercial Vans Pricing',
        'automation.configureFixedPrices': 'Configure fixed prices for C3, C4, C5 groups',
        'automation.savePrices': 'Save Prices',
        
        // Email Notifications
        'emailNotifications.title': 'Email Notifications',
        'emailNotifications.description': 'Configure an email account to receive automatic notifications about price changes, alerts and reports.',
        'emailNotifications.provider': 'Email Provider',
        'emailNotifications.connectGmail': 'Connect Gmail',
        'emailNotifications.connectOutlook': 'Connect Outlook',
        'emailNotifications.customSMTP': 'Custom SMTP',
        'emailNotifications.recipients': 'Notification Recipients',
        'emailNotifications.recipientsPlaceholder': 'email1@example.com\nemail2@example.com\nemail3@example.com',
        'emailNotifications.recipientsHelp': 'One email per line. These emails will receive notifications.',
        'emailNotifications.notificationTypes': 'Notification Types',
        'emailNotifications.priceChanges': 'Price Changes',
        'emailNotifications.alerts': 'Validation Alerts',
        'emailNotifications.reports': 'Daily Reports',
        'emailNotifications.testEmail': 'Send Test Email',
        'emailNotifications.saveSettings': 'Save Settings',
        'emailNotifications.oauthNote': 'Connect your account securely using OAuth2. No password required.',
        'emailNotifications.connected': 'Connected',
        'emailNotifications.disconnect': 'Disconnect',
        'emailNotifications.dailyReport': 'Daily Price Report',
        'emailNotifications.weeklyReport': 'Weekly Reports',
        'emailNotifications.errors': 'System Errors and Alerts',
        'emailNotifications.oauthConnection': 'Connect Account',
        'emailNotifications.connectedAccount': 'Account connected',
        'emailNotifications.connectedEmail': 'Connected email',
        
        // Appearance / Theme
        'appearance.title': 'Theme & Colors',
        'appearance.primaryColor': 'Primary Color',
        'appearance.primaryDesc': 'Main brand color (buttons, links, accents)',
        'appearance.secondaryColor': 'Secondary Color',
        'appearance.secondaryDesc': 'Secondary accent color (highlights, hover states)',
        'appearance.colorPreview': 'Color Preview',
        'appearance.primary': 'Primary',
        'appearance.secondary': 'Secondary',
        'appearance.button': 'Button',
        'appearance.primaryButton': 'Primary Button',
        'appearance.hover': 'Hover',
        'appearance.hoverState': 'Hover State',
        'appearance.note': 'Note: Color changes will be applied across the entire platform. Make sure to test thoroughly after changing colors.',
        'settings.automation': 'Automation',
        'settings.branding': 'Branding',
        'settings.appearance': 'Appearance',
        'settings.companyInfo': 'Company Info',
        'settings.language': 'Language',
        'settings.save': 'Save Settings',
        'settings.reset': 'Reset to Defaults',
        'settings.export': 'Export',
        'settings.import': 'Import',
        'settings.users': 'Users',
        'settings.vehicles': 'Vehicles',
        'settings.priceAdjustment': 'Price Adjustment',
        'settings.priceValidation': 'Price Validation',
        'settings.automatedPriceSettings': 'Automated Price Settings',
        'settings.emailNotifications': 'Email Notifications',
        'settings.automatedReports': 'Automated Reports',
        'settings.customization': 'CUSTOMIZATION',
        
        // Page Titles
        'pageTitle.priceAutomationSettings': 'Price Automation Settings',
        'pageTitle.priceValidation': 'Price Validation',
        'pageTitle.vehicleNamesEditor': 'Vehicle Names Editor',
        'pageTitle.brandIdentity': 'Brand Identity',
        
        // Price Automation Settings
        'priceAutomation.description': 'Configure all parameters for price automation. Changes are applied in real-time.',
        'priceAutomation.exportSettings': 'Export All Settings',
        'priceAutomation.importSettings': 'Import All Settings',
        'priceAutomation.globalSettings': 'Global Settings',
        'priceAutomation.brokerCommission': 'Broker Commission (%)',
        'priceAutomation.brokerCommissionHelp': 'NET Price = Final Price / (1 + commission)',
        'priceAutomation.defaultMargin': 'Default Margin (%)',
        'priceAutomation.defaultMarginHelp': 'Default: 0% (no margin when no rule exists)',
        'priceAutomation.rounding': 'Rounding',
        'priceAutomation.roundingCents': 'Cents (0.01€)',
        'priceAutomation.roundingHalfEuro': 'Half Euro (0.50€)',
        'priceAutomation.roundingEuro': 'Euro (1.00€)',
        'priceAutomation.rounding5Euros': '5 Euros (5.00€)',
        'priceAutomation.groupHierarchy': 'Group Hierarchy & Price Validation',
        'priceAutomation.groupHierarchyDesc': 'Define group price dependencies to ensure pricing consistency across vehicle categories.',
        'priceAutomation.addRule': 'Add Rule',
        'priceAutomation.noRules': 'No rules configured',
        'priceAutomation.baseGroup': 'Base Group',
        'priceAutomation.targetGroup': 'Target Group',
        'priceAutomation.margin': 'Margin',
        'priceAutomation.actions': 'Actions',
        'priceAutomation.delete': 'Delete',
        'priceAutomation.saveAll': 'Save All',
        'priceAutomation.alternativeSearch': 'Alternative Search (days ahead)',
        'priceAutomation.alternativeSearchHelp': 'If no prices found, search X days ahead',
        'priceAutomation.autoSaveHistory': 'Auto-save to History',
        'priceAutomation.enabled': 'Enabled',
        'priceAutomation.disabled': 'Disabled',
        'priceAutomation.autoSaveHistoryHelp': 'Automatically save prices to history on download',
        'priceAutomation.enableGroupHierarchy': 'Enable Group Hierarchy Validation',
        'priceAutomation.availableGroups': 'Available Groups',
        'priceAutomation.configureDependencies': 'Configure Dependencies',
        'priceAutomation.ruleInfo': 'Rule: Define price comparison rules between groups.',
        'priceAutomation.operatorsInfo': 'Operators: ≥ (greater or equal), ≤ (less or equal), > (greater than)',
        'priceAutomation.exampleInfo': 'Example: D ≥ B1 AND D ≥ B2 means group D price must be ≥ both B1 and B2',
        'priceAutomation.excludeSuppliers': 'Exclude Suppliers from Calculations',
        'priceAutomation.excludeSuppliersHelp': 'Selected suppliers will be excluded from price calculations',
        'priceAutomation.defaultLocation': 'Default Location',
        'priceAutomation.configuredRules': 'Configured Dependency Rules',
        'priceAutomation.tip': '💡 Tip: You can define multiple dependencies per group. For example, D can be set to be ≥ both B1 and B2.',
        'priceAutomation.referenceSupplier': 'Reference Supplier for Price Calculations (used when reading Current Prices)',
        'priceAutomation.referenceSupplierHelp': 'This supplier\'s prices will be used as base for automated price calculations. Change this if you want to follow a different supplier\'s pricing strategy.',
        'priceAutomation.automatedPriceRules': 'Automated Price Rules',
        'priceAutomation.manualSettings': 'Manual Settings',
        'priceAutomation.aiSettings': 'AI Settings',
        'priceAutomation.configureRules': 'Configure how automated prices are calculated for each location and group',
        'priceAutomation.configureRulesGroup': 'Configure rules for each group:',
        'priceAutomation.selectMonth': 'Select month:',
        'priceAutomation.selectDay': 'Select day to configure:',
        'priceAutomation.changesSavedAuto': '💡 Changes are saved automatically',
        'priceAutomation.resetDefaults': 'Reset to Defaults',
        'priceAutomation.aiLearningSystem': 'AI Learning System',
        'priceAutomation.aiDescription': 'The AI observes your manual price adjustments in the visual interface and learns patterns to suggest automated rules.',
        'priceAutomation.manualAdjustments': 'Manual Adjustments',
        'priceAutomation.patternsDetected': 'Patterns Detected',
        'priceAutomation.suggestionsReady': 'Suggestions Ready',
        'priceAutomation.noSuggestions': 'No suggestions yet. The AI needs more data to detect patterns.',
        'priceAutomation.makeAdjustments': 'Make at least 5-10 manual adjustments to start seeing suggestions.',
        'priceAutomation.recentAdjustments': 'Recent Manual Adjustments',
        'priceAutomation.clearAIData': 'Clear AI Data',
        'priceAutomation.refreshSuggestions': 'Refresh Suggestions',
        'priceAutomation.days': 'days',
        'priceAutomation.day': 'day',
        
        // Vehicle Groups
        'groups.mini4doors': 'Mini 4 Doors',
        'groups.mini': 'Mini',
        'groups.economy': 'Economy',
        'groups.miniAuto': 'Mini Automatic',
        'groups.economyAuto': 'Economy Automatic',
        'groups.suv': 'SUV',
        'groups.premium': 'Premium',
        'groups.crossover': 'Crossover',
        'groups.stationWagon': 'Station Wagon',
        'groups.suvAuto': 'SUV Automatic',
        'groups.swAuto': 'SW Automatic',
        'groups.sevenSeater': '7 Seater',
        'groups.sevenSeaterAuto': '7 Seater Automatic',
        'groups.nineSeater': '9 Seater',
        
        // Price Validation
        'validation.groupRules': 'Group Rules',
        'validation.activeAlerts': 'Active Alerts',
        'validation.history': 'History',
        'validation.addNewRule': 'Add New Rule',
        'validation.baseGroup': 'Base Group',
        'validation.select': 'Select...',
        'validation.condition': 'Condition',
        'validation.mustBeGreater': 'Must be GREATER than',
        'validation.mustBeGreaterEqual': 'Must be GREATER OR EQUAL to',
        'validation.mustBeLess': 'Must be LESS than',
        'validation.mustBeLessEqual': 'Must be LESS OR EQUAL to',
        'validation.cannotExceed': 'Cannot exceed % of',
        'validation.compareGroups': 'Compare Groups (hold Ctrl/Cmd for multiple)',
        'validation.selectMultiple': 'Select multiple groups to compare against all of them',
        'validation.addRule': 'Add Rule',
        'validation.configuredRules': 'Configured Rules',
        'validation.pause': 'Pause',
        'validation.remove': 'Remove',
        'validation.base': 'Base',
        'validation.compare': 'Compare',
        
        // Vehicles Page
        'vehicles.vehicleNamesEditor': 'Vehicle Names Editor',
        'vehicles.allVehicles': 'All Vehicles',
        'vehicles.uncategorized': 'Uncategorized',
        'vehicles.categoryManagement': 'Category & Group Management',
        'vehicles.categoryManagementDesc': 'Create and manage vehicle categories and groups',
        'vehicles.newCategory': 'New Category',
        'vehicles.newGroup': 'New Group',
        'vehicles.allBrands': 'All brands',
        'vehicles.allCategories': 'All categories',
        
        // Price Automation Page
        'automation.priceAutomation': 'Price Automation',
        'automation.description': 'Fill in CarJet prices for comparison and competitiveness analysis',
        'automation.automatedPrices': 'Automated Prices',
        'automation.currentPrices': 'Current Prices',
        'automation.commercialVans': 'Commercial Vans',
        'automation.history': 'History',
        'automation.location': 'Location',
        'automation.dateSelection': 'Date Selection',
        'automation.specificDate': 'Specific Date',
        'automation.byMonth': 'By Month',
        'automation.byYear': 'By Year',
        'automation.byPricePeriod': 'By Price Period',
        'automation.startDate': 'Start Date',
        'automation.view': 'View:',
        'automation.manageColumns': 'Manage columns:',
        'automation.add': 'Add',
        'automation.remove': 'Remove',
        'automation.tariffPeriod': 'Tariff Period:',
        'automation.to': 'to',
        'automation.downloadExcel': 'Download Excel:',
        'automation.fillMethod': 'Fill Method:',
        'automation.auto': 'Auto',
        'automation.ai': 'AI',
        'automation.usingRules': 'Using rules-based automation',
        'automation.group': 'Group',
        
        // Home Page
        'home.searchByParameters': 'Search by Parameters',
        'home.pickupLocation': 'Pickup Location',
        'home.startDate': 'Start Date',
        'home.days': 'Days',
        'home.search': 'Search',
        'home.searchAllDays': 'Search All Days',
        
        // Branding
        'branding.title': 'Brand Identity',
        'branding.brandIdentity': 'Brand Identity',
        'branding.companyName': 'Company Name',
        'branding.defaultSupplier': 'Default Supplier',
        'branding.logoUrl': 'Logo URL',
        'branding.faviconUrl': 'Favicon URL',
        'branding.logoPreview': 'Logo Preview',
        'branding.noLogo': 'No logo set - using default',
        
        // Appearance
        'appearance.title': 'Theme & Colors',
        'appearance.primaryColor': 'Primary Color',
        'appearance.secondaryColor': 'Secondary Color',
        'appearance.preview': 'Preview',
        
        // Company Info
        'company.title': 'Company Information',
        'company.legalName': 'Legal Company Name',
        'company.taxId': 'Tax ID / VAT Number',
        'company.email': 'Email',
        'company.phone': 'Phone',
        'company.address': 'Address',
        'company.website': 'Website',
        'company.supportEmail': 'Support Email',
        
        // Formulas
        'formulas.title': 'Formulas & Calculations',
        'formulas.brokerCommission': 'Broker Commission (%)',
        'formulas.defaultMargin': 'Default Margin (%)',
        'formulas.rounding': 'Price Rounding',
        'formulas.minPricePerDay': 'Minimum Price Per Day (€)',
        'formulas.minPricePerMonth': 'Minimum Price Per Month (€)',
        'formulas.taxRate': 'Tax Rate / VAT (%)',
        'formulas.currency': 'Default Currency',
        
        // Notifications
        'notif.saved': 'Saved successfully!',
        'notif.error': 'Error saving',
        'notif.loading': 'Loading...',
        'notif.settingsSaved': 'Settings saved!',
        'notif.brandingSaved': 'Branding saved!',
        'notif.colorsSaved': 'Colors saved and applied!',
        'notif.companySaved': 'Company info saved!',
        'notif.formulasSaved': 'Formulas saved!',
        
        // Common
        'common.yes': 'Yes',
        'common.no': 'No',
        'common.cancel': 'Cancel',
        'common.confirm': 'Confirm',
        'common.close': 'Close',
        'common.save': 'Save',
        'common.delete': 'Delete',
        'common.edit': 'Edit',
        'common.add': 'Add',
        'common.remove': 'Remove',
        'common.search': 'Search',
        'common.filter': 'Filter',
        'common.sort': 'Sort',
        'common.loading': 'Loading...',
        'common.error': 'Error',
        'common.success': 'Success',
        'common.warning': 'Warning',
        'common.info': 'Information',
    }
};

// Current language (default: Portuguese)
let currentLanguage = localStorage.getItem('siteLanguage') || 'pt';

/**
 * Get translation for a key
 * @param {string} key - Translation key (e.g., 'search.title')
 * @param {string} fallback - Fallback text if translation not found
 * @returns {string} - Translated text
 */
function t(key, fallback = key) {
    const lang = translations[currentLanguage];
    return lang && lang[key] ? lang[key] : (fallback || key);
}

/**
 * Set the current language
 * @param {string} lang - Language code ('pt' or 'en')
 */
function setLanguage(lang) {
    if (translations[lang]) {
        currentLanguage = lang;
        localStorage.setItem('siteLanguage', lang);
        applyTranslations();
        
        // Trigger event for other components
        window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
        
        console.log(`✅ Language changed to: ${lang}`);
    }
}

/**
 * Get current language
 * @returns {string} - Current language code
 */
function getLanguage() {
    return currentLanguage;
}

/**
 * Apply translations to all elements with data-i18n attribute
 */
function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);
        
        // Check if it's an input placeholder
        if (element.hasAttribute('data-i18n-placeholder')) {
            element.placeholder = translation;
        } else if (element.tagName === 'INPUT' && element.type !== 'button' && element.type !== 'submit') {
            element.placeholder = translation;
        } else {
            element.textContent = translation;
        }
    });
}

/**
 * Initialize i18n system
 */
function initI18n() {
    // Load saved language
    const saved = localStorage.getItem('siteLanguage');
    if (saved && translations[saved]) {
        currentLanguage = saved;
    }
    
    // Apply translations when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyTranslations);
    } else {
        applyTranslations();
    }
    
    console.log(`🌍 i18n initialized with language: ${currentLanguage}`);
}

// Auto-initialize
initI18n();

// Export for use in other scripts
window.t = t;
window.setLanguage = setLanguage;
window.getLanguage = getLanguage;
window.applyTranslations = applyTranslations;
