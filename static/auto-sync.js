/**
 * Auto-Sync System
 * Automatically syncs localStorage to database to prevent data loss on Render
 */

(function() {
    'use strict';

    const SYNC_INTERVAL = 60000; // Sync every 60 seconds (reduced frequency)
    const KEYS_TO_SYNC = [
        // Branding & Appearance
        'brandingSettings',
        'formulaSettings',
        
        // Price Automation
        'priceAutomationSettings',
        'automatedPriceRules',
        'pricingStrategies',
        'priceAIData',
        'customDias',
        'vansPricing',
        
        // User Settings
        'userSettings',
        'priceAutomationAISettings',
        
        // Validation Rules
        'priceValidationRules',
        
        // Language
        'selectedLanguage',
        
        // Any other settings
        'companyInfo',
        'emailSettings',
        'reportSettings'
    ];

    let syncInProgress = false;
    let lastSyncTime = 0;
    let hasUnsyncedChanges = false; // Track if there are changes to sync
    let lastDataSnapshot = {}; // Track last synced data

    // Sync all localStorage keys to database
    async function syncToDatabase(force = false) {
        if (syncInProgress) {
            console.log('⏳ Sync already in progress, skipping...');
            return;
        }

        // Skip if no unsynced changes (unless forced)
        if (!force && !hasUnsyncedChanges) {
            console.log('✨ No changes to sync');
            return;
        }

        syncInProgress = true;
        const now = Date.now();
        
        try {
            const dataToSync = {};
            let hasData = false;

            // Collect all data from localStorage
            KEYS_TO_SYNC.forEach(key => {
                const value = localStorage.getItem(key);
                if (value) {
                    dataToSync[key] = value;
                    hasData = true;
                }
            });

            if (!hasData) {
                console.log('📭 No data to sync');
                hasUnsyncedChanges = false;
                syncInProgress = false;
                return;
            }

            // Send to server
            const response = await fetch('/api/settings/sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSync)
            });

            if (response.ok) {
                lastSyncTime = now;
                lastDataSnapshot = JSON.parse(JSON.stringify(dataToSync)); // Deep copy
                hasUnsyncedChanges = false;
                console.log('✅ Settings synced to database at', new Date().toLocaleTimeString());
            } else {
                console.error('❌ Sync failed:', response.status);
            }
        } catch (error) {
            console.error('❌ Sync error:', error);
        } finally {
            syncInProgress = false;
        }
    }

    // Load all settings from database on page load
    async function loadFromDatabase() {
        try {
            const response = await fetch('/api/settings/load-all');
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.settings) {
                    let loadedCount = 0;
                    
                    Object.keys(data.settings).forEach(key => {
                        if (data.settings[key]) {
                            // Only load if localStorage is empty or older
                            const existing = localStorage.getItem(key);
                            if (!existing || existing === '{}' || existing === '[]') {
                                localStorage.setItem(key, data.settings[key]);
                                loadedCount++;
                            }
                        }
                    });
                    
                    if (loadedCount > 0) {
                        console.log(`✅ Loaded ${loadedCount} settings from database`);
                        // Trigger branding update if loaded
                        if (data.settings.brandingSettings) {
                            window.dispatchEvent(new Event('brandingUpdated'));
                        }
                    }
                }
            }
        } catch (error) {
            console.error('❌ Error loading settings:', error);
        }
    }

    // Monitor localStorage changes and trigger sync
    function setupStorageMonitor() {
        const originalSetItem = localStorage.setItem;
        
        localStorage.setItem = function(key, value) {
            const oldValue = localStorage.getItem(key);
            originalSetItem.apply(this, arguments);
            
            // If it's a key we care about and value actually changed
            if (KEYS_TO_SYNC.includes(key) && oldValue !== value) {
                hasUnsyncedChanges = true;
                
                // Debounce: only sync if 10 seconds have passed since last sync
                const timeSinceLastSync = Date.now() - lastSyncTime;
                if (timeSinceLastSync > 10000) {
                    setTimeout(syncToDatabase, 2000); // Sync after 2 seconds
                }
            }
        };
    }

    // Initialize
    async function init() {
        console.log('🔄 Auto-Sync System initialized');
        
        // Load settings from database first
        await loadFromDatabase();
        
        // Setup storage monitor
        setupStorageMonitor();
        
        // Initial sync
        setTimeout(syncToDatabase, 2000);
        
        // Periodic sync
        setInterval(syncToDatabase, SYNC_INTERVAL);
        
        // Sync before page unload (only if there are changes)
        window.addEventListener('beforeunload', () => {
            // Only sync if there are unsynced changes
            if (!hasUnsyncedChanges) {
                console.log('✨ No changes on unload, skip sync');
                return;
            }
            
            // Use sendBeacon for reliable non-blocking sync on page close
            const dataToSync = {};
            KEYS_TO_SYNC.forEach(key => {
                const value = localStorage.getItem(key);
                if (value) dataToSync[key] = value;
            });
            
            if (Object.keys(dataToSync).length > 0) {
                // sendBeacon requires Blob with correct content-type
                const blob = new Blob([JSON.stringify(dataToSync)], {
                    type: 'application/json'
                });
                navigator.sendBeacon('/api/settings/sync', blob);
                console.log('📤 Sent beacon sync on page unload');
            }
        });
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for manual sync
    window.syncSettings = syncToDatabase;
    window.loadSettings = loadFromDatabase;
})();
