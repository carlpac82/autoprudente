/**
 * Unified Notification System
 * Monocromatic design matching progress bar style
 */

// Add CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .app-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        min-width: 320px;
        max-width: 500px;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        padding: 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
    
    .app-notification.hiding {
        animation: slideOut 0.3s ease-out forwards;
    }
    
    .app-notification-icon {
        flex-shrink: 0;
        width: 20px;
        height: 20px;
    }
    
    .app-notification-icon.success { color: #009cb6; }
    .app-notification-icon.warning { color: #f6b511; }
    .app-notification-icon.error { color: #ef4444; }
    .app-notification-icon.info { color: #009cb6; }
    
    .app-notification-close {
        flex-shrink: 0;
        width: 16px;
        height: 16px;
        color: #9ca3af;
        cursor: pointer;
        transition: color 0.2s;
    }
    
    .app-notification-close:hover {
        color: #4b5563;
    }
    
    .app-notification-message {
        flex: 1;
        font-size: 14px;
        color: #1f2937;
        white-space: pre-line;
    }
`;
document.head.appendChild(notificationStyles);

/**
 * Show a notification
 * @param {string} message - The message to display
 * @param {string} type - Type: 'success', 'warning', 'error', 'info'
 * @param {number} duration - Duration in ms (0 = no auto-close)
 */
function showNotification(message, type = 'info', duration = 5000) {
    // Remove existing notifications
    const existing = document.querySelectorAll('.app-notification');
    existing.forEach(n => n.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'app-notification';
    
    // Icon based on type (monocromatic)
    let iconSVG = '';
    if (type === 'success') {
        iconSVG = `<svg class="app-notification-icon success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>`;
    } else if (type === 'warning') {
        iconSVG = `<svg class="app-notification-icon warning" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>`;
    } else if (type === 'error') {
        iconSVG = `<svg class="app-notification-icon error" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>`;
    } else {
        iconSVG = `<svg class="app-notification-icon info" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>`;
    }
    
    notification.innerHTML = `
        ${iconSVG}
        <div class="app-notification-message">${message}</div>
        <svg class="app-notification-close" fill="none" stroke="currentColor" viewBox="0 0 24 24" onclick="this.closest('.app-notification').remove()">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    if (duration > 0) {
        setTimeout(() => {
            notification.classList.add('hiding');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
}

// Make it globally available
window.showNotification = showNotification;
