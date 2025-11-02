/**
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
        
        // Settings
        'settings.title': 'Definições & Personalização',
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
        
        // Branding
        'branding.title': 'Identidade da Marca',
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
        
        // Settings
        'settings.title': 'Settings & Customization',
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
        
        // Branding
        'branding.title': 'Brand Identity',
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
