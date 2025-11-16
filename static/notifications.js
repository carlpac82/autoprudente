/**
 * Unified Notification System
 * Monocromatic design matching progress bar style
 * Popups vermelhos desativados conforme solicitação
 */

// Desativar popups vermelhos
const DISABLE_ERROR_POPUPS = true;

// Add CSS for notifications - Clean monocromatic design
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .app-notification {
        position: fixed;
        top: 24px;
        right: 24px;
        min-width: 360px;
        max-width: 480px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06), 0 2px 8px rgba(0, 0, 0, 0.04);
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10000;
        animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(0, 0, 0, 0.06);
    }
    
    .app-notification.success { background: #f0fdf9; border-color: #009cb6; }
    .app-notification.warning { background: #fffcf5; border-color: #f4ad0f; }
    .app-notification.error { background: #fef2f2; border-color: #ef4444; }
    .app-notification.info { background: #f0f9ff; border-color: #009cb6; }
    
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
    .app-notification-icon.warning { color: #f4ad0f; }
    .app-notification-icon.error { color: #ef4444; }
    .app-notification-icon.info { color: #009cb6; }
    
    .app-notification-close {
        flex-shrink: 0;
        width: 16px;
        height: 16px;
        color: #9ca3af;
        cursor: pointer;
        transition: color 0.15s;
        border-radius: 4px;
        padding: 2px;
        margin-left: 4px;
    }
    
    .app-notification-close:hover {
        color: #374151;
    }
    
    .app-notification-message {
        flex: 1;
        font-size: 13.5px;
        line-height: 1.4;
        color: #374151;
        white-space: pre-line;
        font-weight: 500;
        letter-spacing: -0.01em;
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
    // Desativar popups vermelhos (error) conforme solicitado
    if (DISABLE_ERROR_POPUPS && type === 'error') {
        console.log(`[ERROR POPUP DISABLED] ${message}`);
        return;
    }
    
    // Remove existing notifications
    const existing = document.querySelectorAll('.app-notification');
    existing.forEach(n => n.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `app-notification ${type}`;
    
    // Simple monocromatic icons - clean minimal design
    let iconSVG = '';
    if (type === 'success') {
        iconSVG = `<svg class="app-notification-icon success" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>`;
    } else if (type === 'warning') {
        iconSVG = `<svg class="app-notification-icon warning" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>`;
    } else if (type === 'error') {
        iconSVG = `<svg class="app-notification-icon error" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
        </svg>`;
    } else {
        iconSVG = `<svg class="app-notification-icon info" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
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
