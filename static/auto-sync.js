/**
 * Auto-Sync System
 * Automatically syncs localStorage to database to prevent data loss on Render
 */

(function() {
    'use strict';

    const SYNC_INTERVAL = 30000; // Sync every 30 seconds
    const KEYS_TO_SYNC = [
        'brandingSettings',
        'priceAutomationSettings',
        'automatedPriceRules',
        'pricingStrategies',
        'userSettings',
        'priceAutomationAISettings'
    ];

    let syncInProgress = false;
    let lastSyncTime = 0;

    // Sync all localStorage keys to database
    async function syncToDatabase() {
        if (syncInProgress) {
            console.log('⏳ Sync already in progress, skipping...');
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
            originalSetItem.apply(this, arguments);
            
            // If it's a key we care about, schedule a sync
            if (KEYS_TO_SYNC.includes(key)) {
                // Debounce: only sync if 5 seconds have passed since last sync
                const timeSinceLastSync = Date.now() - lastSyncTime;
                if (timeSinceLastSync > 5000) {
                    setTimeout(syncToDatabase, 1000); // Sync after 1 second
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
        
        // Sync before page unload
        window.addEventListener('beforeunload', () => {
            // Use sendBeacon for reliable sync on page close
            const dataToSync = {};
            KEYS_TO_SYNC.forEach(key => {
                const value = localStorage.getItem(key);
                if (value) dataToSync[key] = value;
            });
            
            if (Object.keys(dataToSync).length > 0) {
                navigator.sendBeacon('/api/settings/sync', JSON.stringify(dataToSync));
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
