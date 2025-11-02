// Custom Notification System with Monochromatic SVG Icons
// Colors: #009cb6 (primary), #f4ad0f (secondary/warning), red-500 (error)

let confirmResolve = null;

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type: 'success', 'error', 'warning', 'info'
 */
function showNotification(message, type = 'info') {
    let container = document.getElementById('notificationContainer');
    
    // Create container if it doesn't exist
    if (!container) {
        container = document.createElement('div');
        container.id = 'notificationContainer';
        container.className = 'fixed top-4 right-4 z-[100] space-y-2';
        document.body.appendChild(container);
    }
    
    const notification = document.createElement('div');
    
    const icons = {
        success: '<svg class="w-6 h-6 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        error: '<svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
        warning: '<svg class="w-6 h-6 text-[#f4ad0f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
        info: '<svg class="w-6 h-6 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    };
    
    notification.className = 'bg-white rounded-lg shadow-lg p-4 flex items-start gap-3 min-w-[300px] max-w-md transform transition-all duration-300 translate-x-full';
    notification.innerHTML = `
        ${icons[type]}
        <div class="flex-1">
            <p class="text-sm text-gray-800">${message}</p>
        </div>
        <button onclick="this.parentElement.remove()" class="text-gray-400 hover:text-gray-600">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        </button>
    `;
    
    container.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 10);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

/**
 * Show a custom confirm modal
 * @param {string} title - Modal title
 * @param {string} message - Modal message
 * @param {string} type - Type: 'info', 'warning', 'search', 'danger'
 * @returns {Promise<boolean>} - True if confirmed, false if cancelled
 */
function customConfirm(title, message, type = 'info') {
    return new Promise((resolve) => {
        confirmResolve = resolve;
        
        let modal = document.getElementById('customConfirmModal');
        
        // Create modal if it doesn't exist
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'customConfirmModal';
            modal.className = 'hidden fixed inset-0 bg-black bg-opacity-50 z-[100] flex items-center justify-center p-4';
            modal.innerHTML = `
                <div class="bg-white rounded-lg max-w-md w-full p-6 shadow-xl">
                    <div class="flex items-start gap-3 mb-4">
                        <div id="confirmIcon" class="flex-shrink-0"></div>
                        <div class="flex-1">
                            <h3 id="confirmTitle" class="text-lg font-semibold text-gray-900 mb-2"></h3>
                            <p id="confirmMessage" class="text-sm text-gray-600 whitespace-pre-line"></p>
                        </div>
                    </div>
                    <div class="flex gap-3 justify-end">
                        <button onclick="resolveConfirm(false)" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                            Cancel
                        </button>
                        <button onclick="resolveConfirm(true)" id="confirmButton" class="px-4 py-2 bg-[#009cb6] text-white rounded-lg hover:bg-[#007a91] transition-colors">
                            Confirm
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
        
        const iconContainer = document.getElementById('confirmIcon');
        const titleElement = document.getElementById('confirmTitle');
        const messageElement = document.getElementById('confirmMessage');
        const confirmButton = document.getElementById('confirmButton');
        
        const icons = {
            info: '<svg class="w-8 h-8 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
            warning: '<svg class="w-8 h-8 text-[#f4ad0f]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>',
            search: '<svg class="w-8 h-8 text-[#009cb6]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>',
            danger: '<svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>'
        };
        
        iconContainer.innerHTML = icons[type] || icons.info;
        titleElement.textContent = title;
        messageElement.textContent = message;
        
        // Set button color based on type
        if (type === 'warning' || type === 'danger') {
            confirmButton.className = 'px-4 py-2 bg-[#f4ad0f] text-white rounded-lg hover:bg-[#e39e0e] transition-colors';
        } else {
            confirmButton.className = 'px-4 py-2 bg-[#009cb6] text-white rounded-lg hover:bg-[#007a91] transition-colors';
        }
        
        modal.classList.remove('hidden');
    });
}

/**
 * Resolve the confirm modal
 * @param {boolean} result - True if confirmed, false if cancelled
 */
function resolveConfirm(result) {
    const modal = document.getElementById('customConfirmModal');
    if (modal) {
        modal.classList.add('hidden');
    }
    if (confirmResolve) {
        confirmResolve(result);
        confirmResolve = null;
    }
}

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('customConfirmModal');
        if (modal && !modal.classList.contains('hidden')) {
            resolveConfirm(false);
        }
    }
});
