/**
 * Global Branding System
 * Applies white-label customization across the entire platform
 */

(function() {
    'use strict';

    // Load branding settings from localStorage
    function loadBrandingSettings() {
        const saved = localStorage.getItem('brandingSettings');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                console.error('Error loading branding settings:', e);
            }
        }
        // Default settings (AutoPrudente)
        return {
            companyName: 'AutoPrudente',
            defaultSupplier: 'AutoPrudente',
            logoUrl: '',
            faviconUrl: '',
            primaryColor: '#009cb6',
            secondaryColor: '#f4ad0f',
            legalName: '',
            taxId: '',
            companyEmail: '',
            companyPhone: '',
            companyAddress: '',
            companyWebsite: '',
            supportEmail: ''
        };
    }

    // Apply colors to the entire site
    function applyColors(settings) {
        const primary = settings.primaryColor || '#009cb6';
        const secondary = settings.secondaryColor || '#f4ad0f';

        // Create or update style element
        let styleEl = document.getElementById('branding-colors');
        if (!styleEl) {
            styleEl = document.createElement('style');
            styleEl.id = 'branding-colors';
            document.head.appendChild(styleEl);
        }

        // CSS with custom properties and specific overrides
        styleEl.textContent = `
            :root {
                --primary-color: ${primary};
                --secondary-color: ${secondary};
                --primary-rgb: ${hexToRgb(primary)};
                --secondary-rgb: ${hexToRgb(secondary)};
            }

            /* Buttons */
            .bg-\\[\\#009cb6\\], 
            button[class*="bg-[#009cb6]"],
            a[class*="bg-[#009cb6]"] {
                background-color: ${primary} !important;
            }

            .bg-\\[\\#f4ad0f\\],
            button[class*="bg-[#f4ad0f]"],
            a[class*="bg-[#f4ad0f]"] {
                background-color: ${secondary} !important;
            }

            /* Hover states */
            .hover\\:bg-\\[\\#009cb6\\]:hover,
            button[class*="hover:bg-[#009cb6]"]:hover {
                background-color: ${primary} !important;
            }

            .hover\\:bg-\\[\\#f4ad0f\\]:hover,
            button[class*="hover:bg-[#f4ad0f]"]:hover {
                background-color: ${secondary} !important;
            }

            /* Text colors */
            .text-\\[\\#009cb6\\],
            [class*="text-[#009cb6]"] {
                color: ${primary} !important;
            }

            .text-\\[\\#f4ad0f\\],
            [class*="text-[#f4ad0f]"] {
                color: ${secondary} !important;
            }

            /* Borders */
            .border-\\[\\#009cb6\\],
            [class*="border-[#009cb6]"] {
                border-color: ${primary} !important;
            }

            .border-\\[\\#f4ad0f\\],
            [class*="border-[#f4ad0f]"] {
                border-color: ${secondary} !important;
            }

            /* Focus rings */
            .focus\\:ring-\\[\\#009cb6\\]:focus,
            [class*="focus:ring-[#009cb6]"]:focus {
                --tw-ring-color: ${primary} !important;
            }

            /* Specific component overrides */
            .bg-gradient-to-r.from-\\[\\#009cb6\\] {
                --tw-gradient-from: ${primary} !important;
            }

            .bg-gradient-to-r.to-\\[\\#f4ad0f\\] {
                --tw-gradient-to: ${secondary} !important;
            }

            /* Navigation background */
            nav[style*="#009cb6"] {
                background: linear-gradient(135deg, ${primary} 0%, ${secondary} 100%) !important;
            }

            /* Custom styled elements */
            [style*="background-color: #009cb6"],
            [style*="background-color:#009cb6"] {
                background-color: ${primary} !important;
            }

            [style*="background-color: #f4ad0f"],
            [style*="background-color:#f4ad0f"] {
                background-color: ${secondary} !important;
            }

            [style*="color: #009cb6"],
            [style*="color:#009cb6"] {
                color: ${primary} !important;
            }

            [style*="color: #f4ad0f"],
            [style*="color:#f4ad0f"] {
                color: ${secondary} !important;
            }

            [style*="border-color: #009cb6"],
            [style*="border-color:#009cb6"] {
                border-color: ${primary} !important;
            }
        `;

        console.log('✅ Colors applied:', { primary, secondary });
    }

    // Apply logo
    function applyLogo(settings) {
        if (!settings.logoUrl || settings.logoUrl.trim() === '') {
            return; // Keep default logo
        }

        // Find all logo elements (adjust selectors as needed)
        const logoSelectors = [
            'img[alt*="Logo"]',
            'img[alt*="logo"]',
            '.logo img',
            'nav img',
            'header img'
        ];

        logoSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(img => {
                // Only replace if it looks like a logo (small height)
                if (img.height < 100 || img.classList.contains('logo')) {
                    img.src = settings.logoUrl;
                    img.alt = `${settings.companyName} Logo`;
                    console.log('✅ Logo replaced:', img);
                }
            });
        });

        // Update company name in navigation
        const companyNameElements = document.querySelectorAll('[data-company-name]');
        companyNameElements.forEach(el => {
            el.textContent = settings.companyName;
        });
    }

    // Apply favicon
    function applyFavicon(settings) {
        if (!settings.faviconUrl || settings.faviconUrl.trim() === '') {
            return; // Keep default favicon
        }

        // Remove existing favicons
        document.querySelectorAll('link[rel*="icon"]').forEach(link => link.remove());

        // Add new favicon
        const link = document.createElement('link');
        link.rel = 'icon';
        link.type = 'image/x-icon';
        link.href = settings.faviconUrl;
        document.head.appendChild(link);

        console.log('✅ Favicon updated:', settings.faviconUrl);
    }

    // Update page title with company name
    function updatePageTitle(settings) {
        const currentTitle = document.title;
        if (settings.companyName && settings.companyName !== 'AutoPrudente') {
            // Replace "AutoPrudente" or add company name
            if (currentTitle.includes('AutoPrudente')) {
                document.title = currentTitle.replace('AutoPrudente', settings.companyName);
            } else if (!currentTitle.includes(settings.companyName)) {
                document.title = `${settings.companyName} - ${currentTitle}`;
            }
        }
    }

    // Helper: Convert hex to RGB
    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result 
            ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
            : '0, 156, 182'; // Default primary RGB
    }

    // Initialize branding on page load
    function initBranding() {
        const settings = loadBrandingSettings();
        
        applyColors(settings);
        applyLogo(settings);
        applyFavicon(settings);
        updatePageTitle(settings);

        console.log('🎨 Branding initialized:', settings.companyName);
    }

    // Listen for settings changes
    window.addEventListener('storage', (e) => {
        if (e.key === 'brandingSettings') {
            console.log('🔄 Branding settings changed, reapplying...');
            initBranding();
        }
    });

    // Custom event for same-page updates
    window.addEventListener('brandingUpdated', () => {
        console.log('🔄 Branding updated event received');
        initBranding();
    });

    // Export for use in other scripts
    window.getBrandingSettings = loadBrandingSettings;
    window.applyBranding = initBranding;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBranding);
    } else {
        initBranding();
    }

    // Re-apply after a short delay to catch dynamically loaded content
    setTimeout(initBranding, 500);
})();
