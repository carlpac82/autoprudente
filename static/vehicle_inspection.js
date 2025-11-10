/**
 * Vehicle Inspection System - Complete JavaScript
 * Real-time camera capture + AI damage detection
 */

// Global state
let currentStep = 1;
let inspectionData = {
    photos: {},
    aiResults: {},
    vehicleInfo: {}
};

let cameraStream = null;
let currentPhotoType = null;
let autoSequenceMode = false;
let currentPhotoIndex = 0;

// Notification helper
function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Create toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#009cb6'};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10001;
        font-weight: 500;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentNode) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Photo types and instructions
const photoTypes = [
    {type: 'front', label: 'Front View', instruction: 'Center the front of the vehicle, include license plate'},
    {type: 'back', label: 'Rear View', instruction: 'Center the rear of the vehicle, include license plate'},
    {type: 'left', label: 'Left Side', instruction: 'Show the entire left side, include all doors and wheels'},
    {type: 'right', label: 'Right Side', instruction: 'Show the entire right side, include all doors and wheels'},
    {type: 'interior', label: 'Interior', instruction: 'Show seats and dashboard, focus on condition'},
    {type: 'odometer', label: 'Odometer', instruction: 'Clear view of odometer showing mileage'}
];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializePhotoGrid();
    loadInspectorName();
    initializeDiagramInteraction();
});

function initializePhotoGrid() {
    const grid = document.getElementById('photoGrid');
    grid.innerHTML = photoTypes.map((photo, index) => {
        // Number colors matching diagram
        let numberColor = '#10b981'; // green for 1-4
        if (photo.type === 'interior') numberColor = '#f59e0b'; // amber for 5
        if (photo.type === 'odometer') numberColor = '#8b5cf6'; // purple for 6
        
        return `
        <div class="photo-slot" id="slot-${photo.type}" onclick="openCamera('${photo.type}')">
            <div class="photo-slot-number" style="background: ${numberColor}; border-color: ${numberColor}; color: white;">
                ${index + 1}
            </div>
            <div class="absolute inset-0 flex flex-col items-center justify-center p-4 pt-12">
                <svg class="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <div class="text-center">
                    <div class="font-semibold text-gray-700 text-sm">${photo.label}</div>
                    <div class="text-xs text-gray-500 mt-1">Click to capture</div>
                </div>
            </div>
            <div class="absolute top-2 right-2 hidden" id="check-${photo.type}">
                <svg class="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
            </div>
        </div>
    `;
    }).join('');
}

function initializeDiagramInteraction() {
    // Make diagram indicators clickable
    const indicators = document.querySelectorAll('.photo-indicator');
    indicators.forEach(indicator => {
        indicator.addEventListener('click', function() {
            const photoType = this.getAttribute('data-type');
            openCamera(photoType);
        });
    });
}

function updateDiagramIndicator(photoType, captured) {
    // Update diagram indicator when photo is captured
    const indicator = document.querySelector(`.photo-indicator[data-type="${photoType}"]`);
    if (indicator) {
        if (captured) {
            indicator.classList.add('captured');
        } else {
            indicator.classList.remove('captured');
        }
    }
}

function loadInspectorName() {
    const saved = localStorage.getItem('inspectorName');
    if (saved) {
        document.getElementById('inputInspectorName').value = saved;
    }
}

// Step navigation
function nextStep() {
    if (currentStep === 1) {
        if (!validateVehicleInfo()) return;
        saveVehicleInfo();
    } else if (currentStep === 2) {
        if (!validatePhotos()) return;
        startAIAnalysis();
    } else if (currentStep === 3) {
        generateReview();
    }
    
    currentStep++;
    updateStepDisplay();
}

function prevStep() {
    currentStep--;
    updateStepDisplay();
}

function updateStepDisplay() {
    // Hide all steps
    document.querySelectorAll('.step-content').forEach(el => el.classList.add('hidden'));
    
    // Show current step
    const steps = ['stepVehicleInfo', 'stepPhotos', 'stepAnalysis', 'stepReview'];
    document.getElementById(steps[currentStep - 1]).classList.remove('hidden');
    
    // Update step indicators
    for (let i = 1; i <= 4; i++) {
        const dot = document.getElementById(`step${i}`);
        dot.classList.remove('active', 'completed');
        if (i < currentStep) {
            dot.classList.add('completed');
        } else if (i === currentStep) {
            dot.classList.add('active');
        }
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Validation
function validateVehicleInfo() {
    const plate = document.getElementById('inputPlate').value.trim();
    const inspector = document.getElementById('inputInspectorName').value.trim();
    
    if (!plate) {
        showNotification('Please enter vehicle plate', 'error');
        document.getElementById('inputPlate').focus();
        return false;
    }
    
    if (!inspector) {
        showNotification('Please enter inspector name', 'error');
        document.getElementById('inputInspectorName').focus();
        return false;
    }
    
    return true;
}

function validatePhotos() {
    const capturedCount = Object.keys(inspectionData.photos).length;
    if (capturedCount < 6) {
        showNotification(`Please capture all 6 photos (${capturedCount}/6 done)`, 'warning');
        return false;
    }
    return true;
}

function saveVehicleInfo() {
    inspectionData.vehicleInfo = {
        inspection_type: document.getElementById('inputInspectionType').value,
        vehicle_plate: document.getElementById('inputPlate').value.trim(),
        vehicle_brand: document.getElementById('inputBrand').value.trim(),
        vehicle_model: document.getElementById('inputModel').value.trim(),
        contract_number: document.getElementById('inputContract').value.trim(),
        customer_name: document.getElementById('inputCustomerName').value.trim(),
        customer_email: document.getElementById('inputCustomerEmail').value.trim(),
        customer_phone: document.getElementById('inputCustomerPhone').value.trim(),
        odometer_reading: document.getElementById('inputOdometer').value,
        fuel_level: document.getElementById('inputFuelLevel').value,
        inspector_name: document.getElementById('inputInspectorName').value.trim(),
        inspector_notes: document.getElementById('inputNotes').value.trim()
    };
    
    // Save inspector name
    localStorage.setItem('inspectorName', inspectionData.vehicleInfo.inspector_name);
    
    // Update header
    document.getElementById('inspectionType').textContent = 
        inspectionData.vehicleInfo.inspection_type === 'check_in' ? 'Check-in' : 'Check-out';
}

// Auto Sequence Mode
function startAutoSequence() {
    autoSequenceMode = true;
    currentPhotoIndex = 0;
    
    showNotification('Modo automático ativado! Siga as instruções', 'info');
    
    // Start with first photo
    setTimeout(() => {
        openCameraAutoSequence(0);
    }, 1000);
}

async function openCameraAutoSequence(index) {
    if (index >= photoTypes.length) {
        // All photos captured!
        autoSequenceMode = false;
        showNotification('Todas as 6 fotos capturadas! A processar com AI...', 'success');
        document.getElementById('btnNextToAnalysis').disabled = false;
        return;
    }
    
    currentPhotoIndex = index;
    const photoType = photoTypes[index].type;
    
    // Show instruction before opening camera
    const instructions = [
        'Dirija-se à FRENTE do carro',
        'Dirija-se à TRASEIRA do carro', 
        'Dirija-se ao LADO ESQUERDO do carro',
        'Dirija-se ao LADO DIREITO do carro',
        'Entre no carro e aponte para o INTERIOR',
        'Aponte para o ODÓMETRO no painel'
    ];
    
    // Show big instruction overlay
    showBigInstruction(instructions[index], () => {
        openCamera(photoType);
    });
}

function showBigInstruction(text, callback) {
    // Create fullscreen instruction overlay
    const overlay = document.createElement('div');
    overlay.id = 'instructionOverlay';
    overlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0, 156, 182, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(10px);
    `;
    
    overlay.innerHTML = `
        <div style="text-align: center; color: white; padding: 40px;">
            <svg style="width: 96px; height: 96px; margin: 0 auto 30px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <h2 style="font-size: 32px; font-weight: bold; margin-bottom: 20px;">${text}</h2>
            <p style="font-size: 18px; opacity: 0.9; margin-bottom: 40px;">Posicione-se e prepare a câmera</p>
            <div style="font-size: 48px; font-weight: bold;" id="countdown">3</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    // Countdown 3, 2, 1
    let count = 3;
    const countdownEl = document.getElementById('countdown');
    
    const countInterval = setInterval(() => {
        count--;
        if (count > 0) {
            countdownEl.textContent = count;
        } else {
            countdownEl.innerHTML = `
                <svg style="width: 64px; height: 64px; display: inline-block;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
            `;
            clearInterval(countInterval);
            
            // Remove overlay and open camera
            setTimeout(() => {
                document.body.removeChild(overlay);
                callback();
            }, 500);
        }
    }, 1000);
}

// Camera functions
async function openCamera(photoType) {
    currentPhotoType = photoType;
    const photo = photoTypes.find(p => p.type === photoType);
    
    document.getElementById('cameraTitle').textContent = photo.label;
    document.getElementById('cameraInstruction').textContent = photo.instruction;
    document.getElementById('cameraModal').classList.add('active');
    
    // Customize overlay for photo type
    setupCameraOverlay(photoType);
    
    try {
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'environment', // Use back camera on mobile
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            }
        });
        
        document.getElementById('cameraPreview').srcObject = cameraStream;
        
        // Start positioning hints animation
        startPositioningHints(photoType);
    } catch (error) {
        console.error('Camera error:', error);
        showNotification('Could not access camera: ' + error.message, 'error');
        closeCamera();
    }
}

function setupCameraOverlay(photoType) {
    const overlayContainer = document.getElementById('cameraOverlay');
    const hintText = document.getElementById('hintText');
    
    // Clear existing overlay
    overlayContainer.innerHTML = '';
    
    // Car diagrams for each view
    const carDiagrams = {
        'front': getCarFrontSVG(),
        'back': getCarBackSVG(),
        'left': getCarSideSVG(),
        'right': getCarSideSVG(),
        'interior': getInteriorSVG(),
        'odometer': getOdometerSVG()
    };
    
    const hints = {
        'front': 'Alinhe a frente do veículo com o diagrama',
        'back': 'Alinhe a traseira do veículo com o diagrama',
        'left': 'Alinhe o lado esquerdo com o diagrama',
        'right': 'Alinhe o lado direito com o diagrama',
        'interior': 'Centre o interior do veículo',
        'odometer': 'Centre o odómetro para leitura clara'
    };
    
    // Create new overlay with car diagram
    overlayContainer.innerHTML = `
        <svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
            <rect width="100%" height="100%" fill="black" opacity="0.4"/>
            <g transform="translate(50, 50)">
                ${carDiagrams[photoType] || carDiagrams['front']}
            </g>
        </svg>
        <div id="positionHints" style="position: absolute; bottom: 100px; left: 0; right: 0; text-align: center;">
            <div id="hintText" style="display: inline-block; background: rgba(0,0,0,0.7); color: white; padding: 12px 24px; border-radius: 25px; font-size: 16px; font-weight: 600; backdrop-filter: blur(8px);">
                ${hints[photoType]}
            </div>
        </div>
    `;
}

function getCarFrontSVG() {
    return `
        <g opacity="0.8">
            <!-- Car outline - front view -->
            <rect x="150" y="50" width="400" height="300" rx="20" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="10,5"/>
            
            <!-- Hood -->
            <rect x="180" y="80" width="340" height="60" rx="5" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Windshield -->
            <path d="M 200 140 L 220 170 L 480 170 L 500 140 Z" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Headlights -->
            <ellipse cx="220" cy="100" rx="25" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            <ellipse cx="480" cy="100" rx="25" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Grille -->
            <rect x="320" y="85" width="60" height="35" rx="3" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- License plate area -->
            <rect x="300" y="310" width="100" height="30" rx="3" fill="none" stroke="#f59e0b" stroke-width="3"/>
            <text x="350" y="330" text-anchor="middle" fill="#f59e0b" font-size="12" font-weight="bold">MATRÍCULA</text>
        </g>
    `;
}

function getCarBackSVG() {
    return `
        <g opacity="0.8">
            <!-- Car outline - back view -->
            <rect x="150" y="50" width="400" height="300" rx="20" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="10,5"/>
            
            <!-- Trunk -->
            <rect x="180" y="260" width="340" height="60" rx="5" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Rear window -->
            <path d="M 200 210 L 220 180 L 480 180 L 500 210 Z" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Tail lights -->
            <rect x="190" y="270" width="40" height="35" rx="5" fill="none" stroke="#ef4444" stroke-width="2"/>
            <rect x="470" y="270" width="40" height="35" rx="5" fill="none" stroke="#ef4444" stroke-width="2"/>
            
            <!-- License plate area -->
            <rect x="300" y="280" width="100" height="30" rx="3" fill="none" stroke="#f59e0b" stroke-width="3"/>
            <text x="350" y="300" text-anchor="middle" fill="#f59e0b" font-size="12" font-weight="bold">MATRÍCULA</text>
        </g>
    `;
}

function getCarSideSVG() {
    return `
        <g opacity="0.8">
            <!-- Car outline - side view -->
            <rect x="100" y="100" width="500" height="200" rx="15" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="10,5"/>
            
            <!-- Roof line -->
            <path d="M 150 150 L 200 120 L 400 120 L 450 150" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Windows -->
            <rect x="210" y="125" width="80" height="40" rx="3" fill="none" stroke="#10b981" stroke-width="2"/>
            <rect x="310" y="125" width="80" height="40" rx="3" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Doors -->
            <line x1="295" y1="150" x2="295" y2="280" stroke="#10b981" stroke-width="2"/>
            
            <!-- Wheels -->
            <circle cx="200" cy="285" r="35" fill="none" stroke="#10b981" stroke-width="3"/>
            <circle cx="200" cy="285" r="20" fill="none" stroke="#10b981" stroke-width="2"/>
            <circle cx="500" cy="285" r="35" fill="none" stroke="#10b981" stroke-width="3"/>
            <circle cx="500" cy="285" r="20" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Bumpers -->
            <rect x="90" y="220" width="15" height="50" rx="3" fill="none" stroke="#10b981" stroke-width="2"/>
            <rect x="595" y="220" width="15" height="50" rx="3" fill="none" stroke="#10b981" stroke-width="2"/>
        </g>
    `;
}

function getInteriorSVG() {
    return `
        <g opacity="0.8">
            <!-- Interior outline -->
            <rect x="200" y="100" width="300" height="200" rx="10" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="10,5"/>
            
            <!-- Dashboard -->
            <rect x="220" y="120" width="260" height="60" rx="5" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Steering wheel -->
            <circle cx="280" cy="150" r="25" fill="none" stroke="#10b981" stroke-width="3"/>
            <circle cx="280" cy="150" r="15" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Seats -->
            <rect x="350" y="200" width="50" height="70" rx="8" fill="none" stroke="#10b981" stroke-width="2"/>
            <rect x="420" y="200" width="50" height="70" rx="8" fill="none" stroke="#10b981" stroke-width="2"/>
        </g>
    `;
}

function getOdometerSVG() {
    return `
        <g opacity="0.8">
            <!-- Odometer outline -->
            <rect x="250" y="150" width="200" height="100" rx="8" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="10,5"/>
            
            <!-- Display -->
            <rect x="270" y="170" width="160" height="60" rx="5" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Digital numbers placeholder -->
            <text x="350" y="210" text-anchor="middle" fill="#10b981" font-size="24" font-family="monospace" font-weight="bold">88888</text>
            <text x="350" y="230" text-anchor="middle" fill="#10b981" font-size="10">KM</text>
        </g>
    `;
}

let hintInterval;
const hints = [
    'Mova para cima',
    'Mova para baixo',
    'Mova para a esquerda',
    'Mova para a direita',
    'Ajuste o ângulo',
    'Afaste-se um pouco',
    'Aproxime-se mais',
    'Posicionamento correto'
];

function startPositioningHints(photoType) {
    // Clear previous interval
    if (hintInterval) clearInterval(hintInterval);
    
    const hintText = document.getElementById('hintText');
    let hintIndex = 0;
    let changeCount = 0;
    
    // Change hints every 3 seconds to simulate positioning feedback
    hintInterval = setInterval(() => {
        changeCount++;
        
        // After a few changes, show "perfect" hint
        if (changeCount > 3) {
            hintText.innerHTML = '✨ Perfeito! Pode tirar a foto';
            hintText.style.background = 'rgba(16, 185, 129, 0.9)'; // Green
            clearInterval(hintInterval);
            return;
        }
        
        // Show random positioning hint
        const randomHint = hints[Math.floor(Math.random() * (hints.length - 1))];
        hintText.innerHTML = randomHint;
        hintText.style.background = 'rgba(0, 0, 0, 0.7)'; // Dark
        
    }, 3000);
}

function closeCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    // Stop positioning hints
    if (hintInterval) {
        clearInterval(hintInterval);
        hintInterval = null;
    }
    
    document.getElementById('cameraModal').classList.remove('active');
}

function capturePhoto() {
    const video = document.getElementById('cameraPreview');
    
    // Validate video is ready
    if (!video || !video.videoWidth || !video.videoHeight) {
        alert('Câmera ainda não está pronta. Aguarde um momento.');
        console.error('Video not ready:', video);
        return;
    }
    
    if (!currentPhotoType) {
        alert('Erro: Tipo de foto não definido.');
        console.error('currentPhotoType is null');
        return;
    }
    
    console.log('Capturing photo:', currentPhotoType, `${video.videoWidth}x${video.videoHeight}`);
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    // Mirror image back for display
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0);
    
    console.log('Canvas created, converting to blob...');
    
    // Convert to blob
    canvas.toBlob(blob => {
        if (!blob) {
            alert('Erro ao criar imagem. Tente novamente.');
            console.error('Blob creation failed');
            return;
        }
        
        console.log('Photo blob created:', blob.size, 'bytes');
        
        // Show preview with options
        showPhotoPreview(blob, currentPhotoType);
        
    }, 'image/jpeg', 0.9);
}

function showPhotoPreview(blob, photoType) {
    // Hide camera video
    document.getElementById('cameraPreview').style.display = 'none';
    document.getElementById('cameraOverlay').style.display = 'none';
    
    // Create preview overlay
    const cameraModal = document.getElementById('cameraModal');
    const previewContainer = document.createElement('div');
    previewContainer.id = 'photoPreviewContainer';
    previewContainer.style.cssText = `
        position: absolute;
        inset: 0;
        background: rgba(0,0,0,0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10001;
    `;
    
    const photoLabel = photoTypes.find(p => p.type === photoType).label;
    
    previewContainer.innerHTML = `
        <div style="text-align: center; color: white; margin-bottom: 20px;">
            <h3 style="font-size: 24px; font-weight: 600;">${photoLabel}</h3>
            <p style="font-size: 14px; opacity: 0.8; margin-top: 8px;">Verifique a qualidade da foto</p>
        </div>
        
        <div style="position: relative; max-width: 90%; max-height: 60vh;">
            <img src="${URL.createObjectURL(blob)}" style="max-width: 100%; max-height: 60vh; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.5);">
        </div>
        
        <div style="display: flex; gap: 16px; margin-top: 32px;">
            <button onclick="retakePhoto()" style="display: flex; align-items: center; gap: 8px; background: #ef4444; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Repetir
            </button>
            <button onclick="acceptPhoto('${photoType}', ${Date.now()})" style="display: flex; align-items: center; gap: 8px; background: #10b981; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Próxima
            </button>
        </div>
    `;
    
    cameraModal.querySelector('.flex').appendChild(previewContainer);
    
    // Store blob temporarily
    window.tempPhotoBlob = blob;
}

function retakePhoto() {
    // Remove preview
    const preview = document.getElementById('photoPreviewContainer');
    if (preview) preview.remove();
    
    // Show camera again
    document.getElementById('cameraPreview').style.display = 'block';
    document.getElementById('cameraOverlay').style.display = 'block';
    
    // Clear temp blob
    window.tempPhotoBlob = null;
}

function acceptPhoto(photoType, timestamp) {
    const blob = window.tempPhotoBlob;
    
    if (!blob) {
        alert('Erro: Foto não encontrada');
        return;
    }
    
    // Store photo
    inspectionData.photos[photoType] = blob;
    
    // Update UI
    const slot = document.getElementById(`slot-${photoType}`);
    slot.innerHTML = `<img src="${URL.createObjectURL(blob)}" alt="${photoType}">`;
    slot.classList.add('captured');
    document.getElementById(`check-${photoType}`).classList.remove('hidden');
    
    // Update diagram indicator
    updateDiagramIndicator(photoType, true);
    
    // Show animation
    slot.classList.add('shutter-animation');
    setTimeout(() => slot.classList.remove('shutter-animation'), 300);
    
    showNotification(`${photoTypes.find(p => p.type === photoType).label} guardada`, 'success');
    
    // Enable next button if all photos captured
    if (Object.keys(inspectionData.photos).length === 6) {
        document.getElementById('btnNextToAnalysis').disabled = false;
        
        // Show completion message if in auto mode
        if (autoSequenceMode) {
            showCompletionMessage();
            return;
        }
    }
    
    // Remove preview
    const preview = document.getElementById('photoPreviewContainer');
    if (preview) preview.remove();
    
    // Clear temp blob
    window.tempPhotoBlob = null;
    
    closeCamera();
    
    // If in auto sequence mode, move to next photo
    if (autoSequenceMode) {
        setTimeout(() => {
            openCameraAutoSequence(currentPhotoIndex + 1);
        }, 800);
    }
}

function showCompletionMessage() {
    // Close camera
    closeCamera();
    
    // Show completion screen
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(16, 185, 129, 0.95);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        backdrop-filter: blur(10px);
    `;
    
    overlay.innerHTML = `
        <div style="text-align: center; color: white; padding: 40px;">
            <svg style="width: 120px; height: 120px; margin: 0 auto 30px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <h2 style="font-size: 36px; font-weight: bold; margin-bottom: 16px;">Inspeção Terminada</h2>
            <p style="font-size: 18px; opacity: 0.9;">Todas as 6 fotos foram capturadas com sucesso</p>
            <p style="font-size: 16px; opacity: 0.8; margin-top: 12px;">A processar com AI...</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    setTimeout(() => {
        document.body.removeChild(overlay);
        autoSequenceMode = false;
    }, 3000);
}

// AI Analysis
async function startAIAnalysis() {
    const resultsDiv = document.getElementById('analysisResults');
    const progressDiv = document.getElementById('analysisProgress');
    resultsDiv.innerHTML = '';
    resultsDiv.classList.add('hidden');
    progressDiv.classList.remove('hidden');
    
    let analyzed = 0;
    const total = Object.keys(inspectionData.photos).length;
    
    for (const [photoType, photoBlob] of Object.entries(inspectionData.photos)) {
        try {
            // Create form data
            const formData = new FormData();
            formData.append('file', photoBlob, `${photoType}.jpg`);
            
            // Call AI API
            const response = await fetch('/api/vehicle/detect-damage', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            // Store result
            inspectionData.aiResults[photoType] = result;
            
            // Update progress
            analyzed++;
            const percent = Math.round((analyzed / total) * 100);
            document.getElementById('analysisPercent').textContent = `${percent}%`;
            document.getElementById('analysisBar').style.width = `${percent}%`;
            
            // Add result to display
            addAnalysisResult(photoType, result);
            
        } catch (error) {
            console.error(`Error analyzing ${photoType}:`, error);
            inspectionData.aiResults[photoType] = {ok: false, error: error.message};
        }
    }
    
    // Hide progress, show results
    progressDiv.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    document.getElementById('btnNextToReview').disabled = false;
    
    showNotification('AI analysis complete!', 'success');
}

function addAnalysisResult(photoType, result) {
    const photo = photoTypes.find(p => p.type === photoType);
    const resultsDiv = document.getElementById('analysisResults');
    
    let badgeClass = 'bg-green-100 text-green-800';
    let badgeText = 'No Damage';
    let icon = '';
    
    if (result.ok && result.has_damage) {
        if (result.confidence_percent > 70) {
            badgeClass = 'bg-red-100 text-red-800';
            badgeText = `${result.damage_type} (${result.confidence_percent}%)`;
            icon = '';
        } else {
            badgeClass = 'bg-yellow-100 text-yellow-800';
            badgeText = `Possible ${result.damage_type} (${result.confidence_percent}%)`;
            icon = '';
        }
    }
    
    const resultHtml = `
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center gap-3">
                <img src="${URL.createObjectURL(inspectionData.photos[photoType])}" 
                     class="w-16 h-16 object-cover rounded" alt="${photo.label}">
                <div>
                    <div class="font-medium text-gray-900">${photo.label}</div>
                    <div class="text-sm text-gray-600">${result.verdict || 'Analysis complete'}</div>
                </div>
            </div>
            <div class="px-3 py-1 ${badgeClass} rounded-full text-xs font-semibold flex items-center gap-1">
                <span>${icon}</span>
                <span>${badgeText}</span>
            </div>
        </div>
    `;
    
    resultsDiv.insertAdjacentHTML('beforeend', resultHtml);
}

// Review
function generateReview() {
    const summary = document.getElementById('reviewSummary');
    
    // Count damages
    let damageCount = 0;
    let highConfidenceDamages = [];
    
    for (const [photoType, result] of Object.entries(inspectionData.aiResults)) {
        if (result.ok && result.has_damage) {
            damageCount++;
            if (result.confidence_percent > 70) {
                highConfidenceDamages.push({
                    photo: photoTypes.find(p => p.type === photoType).label,
                    type: result.damage_type,
                    confidence: result.confidence_percent
                });
            }
        }
    }
    
    const hasDamage = damageCount > 0;
    
    summary.innerHTML = `
        <div class="space-y-6">
            <!-- Vehicle Info -->
            <div>
                <h3 class="font-semibold text-gray-900 mb-3">Vehicle Information</h3>
                <div class="grid grid-cols-2 gap-3 text-sm">
                    <div><span class="text-gray-600">Plate:</span> <span class="font-medium">${inspectionData.vehicleInfo.vehicle_plate}</span></div>
                    <div><span class="text-gray-600">Type:</span> <span class="font-medium">${inspectionData.vehicleInfo.inspection_type === 'check_in' ? 'Check-in' : 'Check-out'}</span></div>
                    <div><span class="text-gray-600">Brand:</span> <span class="font-medium">${inspectionData.vehicleInfo.vehicle_brand || 'N/A'}</span></div>
                    <div><span class="text-gray-600">Model:</span> <span class="font-medium">${inspectionData.vehicleInfo.vehicle_model || 'N/A'}</span></div>
                    <div><span class="text-gray-600">Contract:</span> <span class="font-medium">${inspectionData.vehicleInfo.contract_number || 'N/A'}</span></div>
                    <div><span class="text-gray-600">Odometer:</span> <span class="font-medium">${inspectionData.vehicleInfo.odometer_reading || 'N/A'} km</span></div>
                    <div><span class="text-gray-600">Fuel:</span> <span class="font-medium">${inspectionData.vehicleInfo.fuel_level || 'N/A'}</span></div>
                    <div><span class="text-gray-600">Inspector:</span> <span class="font-medium">${inspectionData.vehicleInfo.inspector_name}</span></div>
                </div>
            </div>

            <!-- Damage Status -->
            <div>
                <h3 class="font-semibold text-gray-900 mb-3">Damage Assessment</h3>
                <div class="p-4 rounded-lg ${hasDamage ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-2xl"></span>
                        <span class="font-bold text-lg">${hasDamage ? `${damageCount} Damage(s) Detected` : 'No Damage Detected'}</span>
                    </div>
                    ${highConfidenceDamages.length > 0 ? `
                        <div class="mt-3 space-y-1">
                            ${highConfidenceDamages.map(d => `
                                <div class="text-sm">• ${d.photo}: <strong>${d.type}</strong> (${d.confidence}% confidence)</div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            </div>

            <!-- Photos -->
            <div>
                <h3 class="font-semibold text-gray-900 mb-3">Captured Photos (${Object.keys(inspectionData.photos).length})</h3>
                <div class="grid grid-cols-3 gap-2">
                    ${Object.keys(inspectionData.photos).map(type => `
                        <img src="${URL.createObjectURL(inspectionData.photos[type])}" 
                             class="w-full h-24 object-cover rounded" 
                             alt="${photoTypes.find(p => p.type === type).label}">
                    `).join('')}
                </div>
            </div>

            ${inspectionData.vehicleInfo.inspector_notes ? `
                <div>
                    <h3 class="font-semibold text-gray-900 mb-2">Inspector Notes</h3>
                    <p class="text-sm text-gray-700 bg-gray-50 p-3 rounded">${inspectionData.vehicleInfo.inspector_notes}</p>
                </div>
            ` : ''}
        </div>
    `;
}

// Save inspection
async function saveInspection() {
    showNotification('Saving inspection...', 'info');
    
    try {
        // Create form data with all information
        const formData = new FormData();
        
        // Add vehicle info
        for (const [key, value] of Object.entries(inspectionData.vehicleInfo)) {
            formData.append(key, value || '');
        }
        
        // Add photos
        for (const [photoType, photoBlob] of Object.entries(inspectionData.photos)) {
            formData.append(`photo_${photoType}`, photoBlob, `${photoType}.jpg`);
        }
        
        // Add AI results as JSON
        formData.append('ai_results', JSON.stringify(inspectionData.aiResults));
        
        // Save to API
        const response = await fetch('/api/vehicle-inspections/create', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.ok) {
            showNotification('Inspection saved successfully!', 'success');
            
            // Redirect to inspections list after 2 seconds
            setTimeout(() => {
                window.location.href = '/vehicle-inspections';
            }, 2000);
        } else {
            throw new Error(result.error || 'Save failed');
        }
        
    } catch (error) {
        console.error('Save error:', error);
        showNotification('Error saving inspection: ' + error.message, 'error');
    }
}
