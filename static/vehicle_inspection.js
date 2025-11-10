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
        <g opacity="0.9" transform="scale(0.9)">
            <!-- Main car body outline -->
            <path d="M 200 100 L 200 280 Q 200 320 240 320 L 460 320 Q 500 320 500 280 L 500 100 Q 500 80 480 80 L 220 80 Q 200 80 200 100 Z" 
                  fill="none" stroke="#10b981" stroke-width="4" stroke-dasharray="12,8"/>
            
            <!-- Hood -->
            <path d="M 230 110 L 230 160 L 470 160 L 470 110 Q 470 100 460 100 L 240 100 Q 230 100 230 110 Z" 
                  fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Headlights (detailed) -->
            <g>
                <path d="M 240 120 Q 250 120 255 125 L 255 145 Q 255 150 250 150 L 240 150 Q 235 150 235 145 L 235 125 Q 235 120 240 120 Z" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
                <circle cx="247" cy="135" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
                
                <path d="M 460 120 Q 450 120 445 125 L 445 145 Q 445 150 450 150 L 460 150 Q 465 150 465 145 L 465 125 Q 465 120 460 120 Z" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
                <circle cx="453" cy="135" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
            </g>
            
            <!-- Grille (detailed) -->
            <rect x="310" y="125" width="80" height="40" rx="4" fill="none" stroke="#10b981" stroke-width="2.5"/>
            <line x1="320" y1="135" x2="380" y2="135" stroke="#10b981" stroke-width="1"/>
            <line x1="320" y1="145" x2="380" y2="145" stroke="#10b981" stroke-width="1"/>
            <line x1="320" y1="155" x2="380" y2="155" stroke="#10b981" stroke-width="1"/>
            
            <!-- Windshield -->
            <path d="M 240 170 L 250 190 Q 250 195 255 195 L 445 195 Q 450 195 450 190 L 460 170" 
                  fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Roof line -->
            <path d="M 250 200 L 255 220 L 445 220 L 450 200" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Side mirrors -->
            <ellipse cx="215" cy="210" rx="10" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            <ellipse cx="485" cy="210" rx="10" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Front bumper -->
            <path d="M 220 290 L 210 305 L 490 305 L 480 290" fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- License plate (highlighted) -->
            <rect x="310" y="285" width="80" height="25" rx="3" fill="rgba(245, 158, 11, 0.1)" stroke="#f59e0b" stroke-width="3"/>
            <text x="350" y="302" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="bold">XX-XX-XX</text>
            
            <!-- Wheel wells -->
            <ellipse cx="260" cy="310" rx="35" ry="20" fill="none" stroke="#10b981" stroke-width="2"/>
            <ellipse cx="440" cy="310" rx="35" ry="20" fill="none" stroke="#10b981" stroke-width="2"/>
        </g>
    `;
}

function getCarBackSVG() {
    return `
        <g opacity="0.9" transform="scale(0.9)">
            <!-- Main car body outline -->
            <path d="M 200 100 L 200 280 Q 200 320 240 320 L 460 320 Q 500 320 500 280 L 500 100 Q 500 80 480 80 L 220 80 Q 200 80 200 100 Z" 
                  fill="none" stroke="#10b981" stroke-width="4" stroke-dasharray="12,8"/>
            
            <!-- Roof line -->
            <path d="M 250 100 L 255 120 L 445 120 L 450 100" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Rear window -->
            <path d="M 240 130 L 250 150 Q 250 155 255 155 L 445 155 Q 450 155 450 150 L 460 130" 
                  fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Trunk/Boot -->
            <path d="M 230 165 L 230 270 L 470 270 L 470 165" fill="none" stroke="#10b981" stroke-width="2.5"/>
            <line x1="240" y1="180" x2="460" y2="180" stroke="#10b981" stroke-width="1.5"/>
            
            <!-- Tail lights (detailed) -->
            <g>
                <!-- Left tail light -->
                <rect x="235" y="245" width="45" height="50" rx="4" fill="rgba(239, 68, 68, 0.1)" stroke="#ef4444" stroke-width="2.5"/>
                <rect x="240" y="250" width="35" height="18" rx="2" fill="none" stroke="#ef4444" stroke-width="1.5"/>
                <rect x="240" y="272" width="35" height="18" rx="2" fill="none" stroke="#ef4444" stroke-width="1.5"/>
                
                <!-- Right tail light -->
                <rect x="420" y="245" width="45" height="50" rx="4" fill="rgba(239, 68, 68, 0.1)" stroke="#ef4444" stroke-width="2.5"/>
                <rect x="425" y="250" width="35" height="18" rx="2" fill="none" stroke="#ef4444" stroke-width="1.5"/>
                <rect x="425" y="272" width="35" height="18" rx="2" fill="none" stroke="#ef4444" stroke-width="1.5"/>
            </g>
            
            <!-- License plate (highlighted) -->
            <rect x="310" y="255" width="80" height="28" rx="3" fill="rgba(245, 158, 11, 0.1)" stroke="#f59e0b" stroke-width="3"/>
            <text x="350" y="274" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="bold">XX-XX-XX</text>
            
            <!-- Side mirrors -->
            <ellipse cx="215" cy="160" rx="10" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            <ellipse cx="485" cy="160" rx="10" ry="15" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Rear bumper -->
            <path d="M 220 300 L 210 315 L 490 315 L 480 300" fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Wheel wells -->
            <ellipse cx="260" cy="310" rx="35" ry="20" fill="none" stroke="#10b981" stroke-width="2"/>
            <ellipse cx="440" cy="310" rx="35" ry="20" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Exhaust -->
            <ellipse cx="420" cy="313" rx="8" ry="5" fill="none" stroke="#10b981" stroke-width="1.5"/>
        </g>
    `;
}

function getCarSideSVG() {
    return `
        <g opacity="0.9" transform="scale(0.85)">
            <!-- Main body outline -->
            <path d="M 120 240 L 120 200 Q 120 190 130 185 L 160 180 L 180 150 Q 185 140 195 135 L 250 120 L 450 120 Q 460 120 465 130 L 485 155 L 515 165 Q 525 170 525 180 L 550 185 Q 560 190 560 200 L 560 240 Q 560 255 550 260 L 530 265 L 150 265 Q 130 260 120 250 Z" 
                  fill="none" stroke="#10b981" stroke-width="4" stroke-dasharray="12,8"/>
            
            <!-- Roof line -->
            <path d="M 190 140 L 250 125 L 450 125 L 470 140" fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Windows -->
            <g>
                <!-- Front window -->
                <path d="M 195 145 L 205 135 L 265 130 L 275 145 L 270 175 L 200 175 Z" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
                
                <!-- Rear window -->
                <path d="M 425 145 L 445 130 L 465 135 L 475 145 L 470 175 L 430 175 Z" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
            </g>
            
            <!-- Door lines -->
            <g>
                <!-- Front door -->
                <path d="M 280 150 L 280 250" stroke="#10b981" stroke-width="2.5"/>
                <ellipse cx="290" cy="200" rx="5" ry="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
                
                <!-- Rear door -->
                <path d="M 420 150 L 420 250" stroke="#10b981" stroke-width="2.5"/>
                <ellipse cx="410" cy="200" rx="5" ry="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
            </g>
            
            <!-- Side skirts -->
            <path d="M 150 260 L 145 265 L 535 265 L 530 260" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Wheels (detailed) -->
            <g>
                <!-- Front wheel -->
                <circle cx="210" cy="275" r="42" fill="none" stroke="#10b981" stroke-width="3"/>
                <circle cx="210" cy="275" r="28" fill="none" stroke="#10b981" stroke-width="2.5"/>
                <circle cx="210" cy="275" r="15" fill="none" stroke="#10b981" stroke-width="2"/>
                <!-- Spokes -->
                <line x1="210" y1="260" x2="210" y2="290" stroke="#10b981" stroke-width="1.5"/>
                <line x1="195" y1="275" x2="225" y2="275" stroke="#10b981" stroke-width="1.5"/>
                
                <!-- Rear wheel -->
                <circle cx="470" cy="275" r="42" fill="none" stroke="#10b981" stroke-width="3"/>
                <circle cx="470" cy="275" r="28" fill="none" stroke="#10b981" stroke-width="2.5"/>
                <circle cx="470" cy="275" r="15" fill="none" stroke="#10b981" stroke-width="2"/>
                <!-- Spokes -->
                <line x1="470" y1="260" x2="470" y2="290" stroke="#10b981" stroke-width="1.5"/>
                <line x1="455" y1="275" x2="485" y2="275" stroke="#10b981" stroke-width="1.5"/>
            </g>
            
            <!-- Bumpers -->
            <g>
                <!-- Front bumper -->
                <path d="M 115 230 L 110 235 L 110 255 L 115 260" fill="none" stroke="#10b981" stroke-width="2.5"/>
                
                <!-- Rear bumper -->
                <path d="M 565 230 L 570 235 L 570 255 L 565 260" fill="none" stroke="#10b981" stroke-width="2.5"/>
            </g>
            
            <!-- Side mirror -->
            <ellipse cx="185" cy="175" rx="15" ry="10" fill="none" stroke="#10b981" stroke-width="2"/>
            
            <!-- Headlight & taillight indicators -->
            <ellipse cx="125" cy="220" rx="8" ry="12" fill="none" stroke="#10b981" stroke-width="1.5"/>
            <rect x="545" y="215" width="15" height="25" rx="2" fill="rgba(239, 68, 68, 0.1)" stroke="#ef4444" stroke-width="2"/>
        </g>
    `;
}

function getInteriorSVG() {
    return `
        <g opacity="0.9" transform="scale(0.9)">
            <!-- Main interior frame -->
            <rect x="180" y="80" width="340" height="260" rx="12" fill="none" stroke="#10b981" stroke-width="4" stroke-dasharray="12,8"/>
            
            <!-- Dashboard (detailed) -->
            <path d="M 200 120 L 200 180 Q 200 190 210 190 L 490 190 Q 500 190 500 180 L 500 120 Q 500 110 490 110 L 210 110 Q 200 110 200 120 Z" 
                  fill="none" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Instrument cluster -->
            <g>
                <circle cx="350" cy="145" r="28" fill="none" stroke="#10b981" stroke-width="2"/>
                <circle cx="350" cy="145" r="20" fill="none" stroke="#10b981" stroke-width="1.5"/>
                <text x="350" y="152" text-anchor="middle" fill="#10b981" font-size="14" font-weight="bold">km/h</text>
            </g>
            
            <!-- Center console -->
            <rect x="290" y="195" width="120" height="35" rx="4" fill="none" stroke="#10b981" stroke-width="2"/>
            <circle cx="325" cy="212" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
            <circle cx="350" cy="212" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
            <circle cx="375" cy="212" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
            
            <!-- Steering wheel (detailed) -->
            <g>
                <circle cx="260" cy="160" r="32" fill="none" stroke="#10b981" stroke-width="3"/>
                <circle cx="260" cy="160" r="22" fill="none" stroke="#10b981" stroke-width="2.5"/>
                <circle cx="260" cy="160" r="10" fill="none" stroke="#10b981" stroke-width="2"/>
                <line x1="240" y1="160" x2="228" y2="160" stroke="#10b981" stroke-width="2.5"/>
                <line x1="280" y1="160" x2="292" y2="160" stroke="#10b981" stroke-width="2.5"/>
            </g>
            
            <!-- Front seats (detailed) -->
            <g>
                <!-- Driver seat -->
                <path d="M 220 240 L 220 260 Q 220 270 230 270 L 270 270 Q 280 270 280 260 L 280 240 Q 280 235 275 235 L 225 235 Q 220 235 220 240 Z" 
                      fill="none" stroke="#10b981" stroke-width="2.5"/>
                <path d="M 225 235 L 225 210 Q 225 200 235 200 L 265 200 Q 275 200 275 210 L 275 235" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
                
                <!-- Passenger seat -->
                <path d="M 420 240 L 420 260 Q 420 270 430 270 L 470 270 Q 480 270 480 260 L 480 240 Q 480 235 475 235 L 425 235 Q 420 235 420 240 Z" 
                      fill="none" stroke="#10b981" stroke-width="2.5"/>
                <path d="M 425 235 L 425 210 Q 425 200 435 200 L 465 200 Q 475 200 475 210 L 475 235" 
                      fill="none" stroke="#10b981" stroke-width="2"/>
            </g>
            
            <!-- Gear shift -->
            <ellipse cx="320" cy="245" rx="12" ry="20" fill="none" stroke="#10b981" stroke-width="2"/>
        </g>
    `;
}

function getOdometerSVG() {
    return `
        <g opacity="0.9" transform="scale(0.95)">
            <!-- Instrument cluster frame -->
            <rect x="220" y="130" width="260" height="140" rx="12" fill="none" stroke="#10b981" stroke-width="4" stroke-dasharray="12,8"/>
            
            <!-- Main display background -->
            <rect x="240" y="150" width="220" height="100" rx="8" fill="rgba(16, 185, 129, 0.05)" stroke="#10b981" stroke-width="2.5"/>
            
            <!-- Digital display -->
            <g>
                <rect x="255" y="165" width="190" height="50" rx="6" fill="rgba(0, 0, 0, 0.1)" stroke="#10b981" stroke-width="2"/>
                
                <!-- Digital numbers (7-segment style) -->
                <text x="350" y="200" text-anchor="middle" fill="#10b981" font-size="32" font-family="monospace" font-weight="bold" letter-spacing="4">123456</text>
            </g>
            
            <!-- KM label -->
            <rect x="320" y="220" width="60" height="22" rx="4" fill="none" stroke="#10b981" stroke-width="1.5"/>
            <text x="350" y="236" text-anchor="middle" fill="#10b981" font-size="14" font-weight="bold">km</text>
            
            <!-- Side indicators -->
            <g>
                <!-- Fuel indicator -->
                <circle cx="260" cy="185" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
                <text x="260" y="190" text-anchor="middle" fill="#10b981" font-size="10" font-weight="bold">F</text>
                
                <!-- Temperature indicator -->
                <circle cx="440" cy="185" r="8" fill="none" stroke="#10b981" stroke-width="1.5"/>
                <text x="440" y="190" text-anchor="middle" fill="#10b981" font-size="10" font-weight="bold">T</text>
            </g>
            
            <!-- Border detail lines -->
            <line x1="250" y1="220" x2="310" y2="220" stroke="#10b981" stroke-width="1"/>
            <line x1="390" y1="220" x2="450" y2="220" stroke="#10b981" stroke-width="1"/>
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
            <button id="btnRetake" style="display: flex; align-items: center; gap: 8px; background: #ef4444; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Repetir
            </button>
            <button id="btnAccept" style="display: flex; align-items: center; gap: 8px; background: #10b981; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s;">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Próxima
            </button>
        </div>
    `;
    
    cameraModal.querySelector('.flex').appendChild(previewContainer);
    
    // Store blob temporarily and photo type
    window.tempPhotoBlob = blob;
    window.tempPhotoType = photoType;
    
    // Add event listeners to buttons
    document.getElementById('btnRetake').addEventListener('click', retakePhoto);
    document.getElementById('btnAccept').addEventListener('click', () => acceptPhoto(photoType));
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
