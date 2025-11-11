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
    // Auto-fill Rececionista from logged-in user
    const userName = localStorage.getItem('userName') || 'Rececionista';
    const receptionistField = document.getElementById('inputReceptionist');
    if (receptionistField) {
        receptionistField.value = userName;
    }
    
    // Set user initials in avatar
    const userInitials = document.getElementById('userInitials');
    const userNameDisplay = document.getElementById('userNameDisplay');
    if (userInitials && userName) {
        const nameParts = userName.split(' ');
        const initials = nameParts.length > 1 
            ? nameParts[0][0] + nameParts[nameParts.length - 1][0]
            : userName.substring(0, 2);
        userInitials.textContent = initials.toUpperCase();
    }
    if (userNameDisplay) {
        userNameDisplay.textContent = userName;
    }
    
    // Auto-fill current Date
    const now = new Date();
    const dateStr = now.toLocaleDateString('pt-PT', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
    });
    const dateField = document.getElementById('inputDate');
    if (dateField) {
        dateField.value = dateStr;
    }
    
    // Auto-fill current Time
    const timeStr = now.toLocaleTimeString('pt-PT', { 
        hour: '2-digit', 
        minute: '2-digit'
    });
    const timeField = document.getElementById('inputTime');
    if (timeField) {
        timeField.value = timeStr;
    }
    
    // Auto-format RA field: 5 digits + "-09"
    const raField = document.getElementById('inputRA');
    if (raField) {
        raField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/[^0-9-]/g, ''); // Only numbers and dash
            
            // Remove any existing dash
            value = value.replace(/-/g, '');
            
            // Limit to 5 digits
            if (value.length > 5) {
                value = value.substring(0, 5);
            }
            
            // Auto-add -09 after 5 digits
            if (value.length === 5) {
                value = value + '-09';
            }
            
            e.target.value = value;
        });
        
        // Also format on blur if user enters exactly 5 digits
        raField.addEventListener('blur', function(e) {
            let value = e.target.value.replace(/[^0-9-]/g, '');
            value = value.replace(/-/g, '');
            
            if (value.length === 5) {
                e.target.value = value + '-09';
            }
        });
    }
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
    // Diagram was removed, keeping function for compatibility
}

// Step navigation (4 steps: Photos -> Diagram -> Analysis -> Review)
function nextStep() {
    if (currentStep === 1) {
        // Go to diagram after photos
        if (!validatePhotos()) return;
        showDiagramStep();
    } else if (currentStep === 2) {
        // Go to analysis after diagram
        startAIAnalysis();
    } else if (currentStep === 3) {
        // Go to review after analysis
        generateReview();
    }
    
    currentStep++;
    updateStepDisplay();
}

function showDiagramStep() {
    // Navigate to diagram from photos
    document.getElementById('stepPhotos').classList.add('hidden');
    document.getElementById('stepDiagram').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    console.log('✅ Showing diagram step');
}

function prevStep() {
    currentStep--;
    updateStepDisplay();
}

function updateStepDisplay() {
    // Hide all steps
    document.querySelectorAll('.step-content').forEach(el => el.classList.add('hidden'));
    
    // Show current step (now: stepPhotos, stepDiagram, stepAnalysis, stepReview)
    const steps = ['stepPhotos', 'stepDiagram', 'stepAnalysis', 'stepReview'];
    const currentStepElement = document.getElementById(steps[currentStep - 1]);
    if (currentStepElement) {
        currentStepElement.classList.remove('hidden');
    }
    
    // Update step indicators (3 steps only)
    const indicators = document.querySelectorAll('.step-indicator');
    indicators.forEach((indicator, index) => {
        const stepNum = index + 1;
        indicator.classList.remove('active', 'completed');
        if (stepNum < currentStep) {
            indicator.classList.add('completed'); // Blue
        } else if (stepNum === currentStep) {
            indicator.classList.add('active'); // Yellow
        }
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Validation
function validateInspectionInfo() {
    const plate = document.getElementById('inputPlate').value.trim();
    const ra = document.getElementById('inputRA').value.trim();
    
    if (!plate) {
        showNotification('Por favor insira a matrícula', 'error');
        document.getElementById('inputPlate').focus();
        return false;
    }
    
    if (!ra) {
        showNotification('Por favor insira o RA (Rental Agreement)', 'error');
        document.getElementById('inputRA').focus();
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
    // Validate inspection info first
    if (!validateInspectionInfo()) {
        return;
    }
    
    autoSequenceMode = true;
    currentPhotoIndex = 0;
    
    showNotification('Modo automático ativado! Siga as instruções', 'info');
    
    // Start with first photo
    setTimeout(() => {
        capturePhotoSequence(0);
    }, 1000);
}

function capturePhotoSequence(index) {
    if (index >= photoTypes.length) {
        console.log('All photos captured');
        return;
    }
    
    const photoType = photoTypes[index].type;
    
    // Open camera directly - countdown will happen inside modal
    openCamera(photoType);
}

// Countdown removed - now happens in camera modal

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
        
        // Start countdown animation (3, 2, 1, then capture)
        startCameraCountdown();
        
        // Start positioning hints animation
        startPositioningHints(photoType);
    } catch (error) {
        console.error('Camera error:', error);
        showNotification('Could not access camera: ' + error.message, 'error');
        closeCamera();
    }
}

function startCameraCountdown() {
    // Create fullscreen countdown overlay
    const countdownOverlay = document.createElement('div');
    countdownOverlay.id = 'cameraCountdown';
    countdownOverlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;
    
    // Get photo label
    const photo = photoTypes.find(p => p.type === currentPhotoType);
    const photoLabel = photo ? photo.label : 'Foto';
    
    countdownOverlay.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            <h3 style="font-size: 20px; font-weight: 500; color: white; opacity: 0.9; position: absolute; top: 60px; left: 50%; transform: translateX(-50%);">${photoLabel}</h3>
            <div style="text-align: center; position: relative;">
                <svg width="160" height="160" viewBox="0 0 160 160" style="transform: rotate(-90deg);">
                    <circle cx="80" cy="80" r="70" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="10"/>
                    <circle id="countdownCircle" cx="80" cy="80" r="70" fill="none" stroke="#009cb6" stroke-width="10" 
                        stroke-dasharray="440" stroke-dashoffset="0" 
                        style="transition: stroke-dashoffset 1s linear;"/>
                </svg>
                <div id="countdownNumber" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 72px; font-weight: 800; color: white;">3</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(countdownOverlay);
    
    // Countdown animation
    let count = 3;
    const circle = document.getElementById('countdownCircle');
    const numberEl = document.getElementById('countdownNumber');
    const circumference = 440; // 2 * PI * 70
    
    const countInterval = setInterval(() => {
        count--;
        const progress = count / 3;
        circle.style.strokeDashoffset = circumference * (1 - progress);
        
        if (count > 0) {
            numberEl.textContent = count;
        } else {
            clearInterval(countInterval);
            countdownOverlay.remove();
            // Auto-capture photo
            setTimeout(() => {
                capturePhoto();
            }, 200);
        }
    }, 1000);
}

let scene, camera3D, renderer, carModel, animationId;

function setupCameraOverlay(photoType) {
    // Clean camera view - no 3D overlay
    const overlayContainer = document.getElementById('cameraOverlay');
    if (overlayContainer) {
        overlayContainer.innerHTML = '';
    }
    return; // Exit early - no overlay needed
    
    const hints = {
        'front': 'Frente do veículo',
        'back': 'Traseira do veículo',
        'left': 'Lado esquerdo',
        'right': 'Lado direito',
        'interior': 'Interior do veículo',
        'odometer': 'Odómetro'
    };
    
    const isInteriorOrOdo = photoType === 'interior' || photoType === 'odometer';
    
    // Check if THREE.js is loaded
    if (typeof THREE === 'undefined') {
        console.error('THREE.js not loaded! Showing fallback.');
        overlayContainer.innerHTML = `
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <div style="text-align: center; color: white;">
                    <div style="display: inline-flex; align-items: center; gap: 10px; background: rgba(0,156,182,0.95); padding: 12px 24px; backdrop-filter: blur(10px);">
                        <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span style="font-size: 16px; font-weight: 600;">${hints[photoType]}</span>
                    </div>
                </div>
            </div>
        `;
        return;
    }
    
    // Create container for 3D scene
    overlayContainer.innerHTML = `
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.3); display: flex; flex-direction: column; align-items: center; justify-content: center;">
            
            <!-- Three.js 3D Container -->
            <div id="threejs-container" style="width: 100%; height: 400px; margin-bottom: 40px;"></div>
            
            <!-- Direction hint with icon -->
            <div style="text-align: center; color: white;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 12px; background: rgba(0,156,182,0.9); padding: 16px 32px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
                    <svg style="width: 32px; height: 32px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        ${isInteriorOrOdo ? 
                            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>' :
                            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>'
                        }
                    </svg>
                    <span style="font-size: 20px; font-weight: 700;">${hints[photoType]}</span>
                </div>
                <p style="margin-top: 16px; font-size: 14px; opacity: 0.9;">Posicione-se e alinhe o veículo</p>
            </div>
        </div>
    `;
    
    // Initialize Three.js 3D car
    setTimeout(() => init3DCar(photoType), 100);
}

let targetRotation = 0;
let currentRotation = 0;
let isRotating = false;

function init3DCar(photoType) {
    console.log('init3DCar called for:', photoType);
    
    const container = document.getElementById('threejs-container');
    console.log('Container found:', !!container);
    
    if (!container) {
        console.error('threejs-container not found!');
        return;
    }
    
    // Target rotation based on photo type
    const rotations = {
        'front': 0,
        'left': Math.PI / 2,
        'back': Math.PI,
        'right': -Math.PI / 2,
        'interior': 0,
        'odometer': 0
    };
    
    targetRotation = rotations[photoType] || 0;
    console.log('Target rotation:', targetRotation);
    
    // If scene already exists, just animate to new rotation
    if (renderer && carModel) {
        console.log('Reusing existing scene, animating to new rotation');
        isRotating = true;
        return;
    }
    
    console.log('Creating new Three.js scene...');
    
    // Create scene (first time only)
    scene = new THREE.Scene();
    
    // Create camera
    camera3D = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera3D.position.set(0, 3, 8);
    camera3D.lookAt(0, 0, 0);
    
    // Create renderer
    renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);
    
    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    scene.add(directionalLight);
    
    // Add point lights for more drama
    const pointLight1 = new THREE.PointLight(0xffffff, 0.5);
    pointLight1.position.set(-5, 3, 5);
    scene.add(pointLight1);
    
    const pointLight2 = new THREE.PointLight(0xffffff, 0.5);
    pointLight2.position.set(5, 3, -5);
    scene.add(pointLight2);
    
    try {
        // Create 3D car model
        console.log('Creating 3D car model...');
        carModel = create3DCarModel();
        scene.add(carModel);
        
        // Set initial rotation
        currentRotation = targetRotation;
        carModel.rotation.y = currentRotation;
        
        console.log('3D car created successfully!');
        console.log('Starting animation loop...');
        
        // Animate
        animate3DCar();
    } catch (error) {
        console.error('Error creating 3D car:', error);
        alert('Erro ao criar carro 3D: ' + error.message);
    }
}

function create3DCarModel() {
    const carGroup = new THREE.Group();
    
    // Car body (main)
    const bodyGeometry = new THREE.BoxGeometry(4, 1.2, 2);
    const bodyMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x10b981,
        shininess: 100,
        specular: 0x444444
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.position.y = 0.6;
    carGroup.add(body);
    
    // Car cabin (roof)
    const cabinGeometry = new THREE.BoxGeometry(2.5, 1, 1.8);
    const cabin = new THREE.Mesh(cabinGeometry, bodyMaterial);
    cabin.position.set(-0.3, 1.7, 0);
    carGroup.add(cabin);
    
    // Windows
    const windowMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x64b5f6,
        transparent: true,
        opacity: 0.5,
        shininess: 100
    });
    
    // Front window
    const frontWindowGeometry = new THREE.BoxGeometry(0.1, 0.8, 1.6);
    const frontWindow = new THREE.Mesh(frontWindowGeometry, windowMaterial);
    frontWindow.position.set(0.95, 1.7, 0);
    carGroup.add(frontWindow);
    
    // Rear window
    const rearWindow = new THREE.Mesh(frontWindowGeometry, windowMaterial);
    rearWindow.position.set(-1.55, 1.7, 0);
    carGroup.add(rearWindow);
    
    // Wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.4, 0.4, 0.3, 16);
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x1f2937 });
    
    // Front left wheel
    const wheel1 = new THREE.Mesh(wheelGeometry, wheelMaterial);
    wheel1.position.set(1.2, 0.4, 1.1);
    wheel1.rotation.z = Math.PI / 2;
    carGroup.add(wheel1);
    
    // Front right wheel
    const wheel2 = new THREE.Mesh(wheelGeometry, wheelMaterial);
    wheel2.position.set(1.2, 0.4, -1.1);
    wheel2.rotation.z = Math.PI / 2;
    carGroup.add(wheel2);
    
    // Rear left wheel
    const wheel3 = new THREE.Mesh(wheelGeometry, wheelMaterial);
    wheel3.position.set(-1.2, 0.4, 1.1);
    wheel3.rotation.z = Math.PI / 2;
    carGroup.add(wheel3);
    
    // Rear right wheel
    const wheel4 = new THREE.Mesh(wheelGeometry, wheelMaterial);
    wheel4.position.set(-1.2, 0.4, -1.1);
    wheel4.rotation.z = Math.PI / 2;
    carGroup.add(wheel4);
    
    // Headlights
    const headlightGeometry = new THREE.SphereGeometry(0.2, 16, 16);
    const headlightMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xffffaa,
        emissive: 0xffff00,
        emissiveIntensity: 0.5
    });
    
    const headlight1 = new THREE.Mesh(headlightGeometry, headlightMaterial);
    headlight1.position.set(2.1, 0.8, 0.7);
    carGroup.add(headlight1);
    
    const headlight2 = new THREE.Mesh(headlightGeometry, headlightMaterial);
    headlight2.position.set(2.1, 0.8, -0.7);
    carGroup.add(headlight2);
    
    // Tail lights
    const taillightMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xff0000,
        emissive: 0xff0000,
        emissiveIntensity: 0.3
    });
    
    const taillight1 = new THREE.Mesh(headlightGeometry, taillightMaterial);
    taillight1.position.set(-2.1, 0.8, 0.7);
    carGroup.add(taillight1);
    
    const taillight2 = new THREE.Mesh(headlightGeometry, taillightMaterial);
    taillight2.position.set(-2.1, 0.8, -0.7);
    carGroup.add(taillight2);
    
    return carGroup;
}

function animate3DCar() {
    animationId = requestAnimationFrame(animate3DCar);
    
    if (carModel) {
        // Smooth rotation to target angle
        if (isRotating || Math.abs(targetRotation - currentRotation) > 0.01) {
            // Calculate shortest rotation path
            let diff = targetRotation - currentRotation;
            
            // Normalize to -PI to PI range
            while (diff > Math.PI) diff -= Math.PI * 2;
            while (diff < -Math.PI) diff += Math.PI * 2;
            
            // Smooth easing (ease-out cubic)
            const rotationSpeed = diff * 0.08;
            currentRotation += rotationSpeed;
            
            // Stop rotating when close enough
            if (Math.abs(diff) < 0.01) {
                currentRotation = targetRotation;
                isRotating = false;
            }
            
            carModel.rotation.y = currentRotation;
        } else {
            // Slow idle rotation when not transitioning
            carModel.rotation.y += 0.003;
            currentRotation = carModel.rotation.y;
        }
    }
    
    renderer.render(scene, camera3D);
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
    
    // Change hints every 3 seconds to simulate positioning feedback
    hintInterval = setInterval(() => {
        const hintText = document.getElementById('hintText');
        if (!hintText) {
            clearInterval(hintInterval);
            return;
        }
        
        changeCount++;
        
        // After a few changes, show "perfect" hint
        if (changeCount > 3) {
            hintText.innerHTML = 'Posicionamento correto - Pode tirar a foto';
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

let changeCount = 0;

// OCR License Plate Detection
async function detectLicensePlate(blob) {
    console.log('🔍 Detectando matrícula com OCR...');
    
    // Check if license plate field is already filled
    const plateField = document.getElementById('inputPlate');
    if (plateField && plateField.value.trim()) {
        console.log('Matrícula já preenchida, saltando OCR');
        return;
    }
    
    showNotification('🔍 A detectar matrícula...', 'info');
    
    try {
        // Convert blob to image URL
        const imageUrl = URL.createObjectURL(blob);
        
        // Process with Tesseract OCR
        const result = await Tesseract.recognize(
            imageUrl,
            'eng', // English works better for alphanumeric
            {
                logger: info => {
                    if (info.status === 'recognizing text') {
                        console.log(`OCR Progress: ${Math.round(info.progress * 100)}%`);
                    }
                }
            }
        );
        
        console.log('OCR Text detected:', result.data.text);
        
        // Extract license plate pattern
        // Portuguese format: XX-XX-XX or XX-00-XX or 00-XX-00
        const text = result.data.text.toUpperCase();
        
        // Try multiple patterns
        const patterns = [
            /([A-Z0-9]{2}[-\s]?[A-Z0-9]{2}[-\s]?[A-Z0-9]{2})/g,  // XX-XX-XX
            /([A-Z]{2}[-\s]?\d{2}[-\s]?[A-Z]{2})/g,              // AA-00-AA
            /(\d{2}[-\s]?[A-Z]{2}[-\s]?\d{2})/g,                // 00-AA-00
            /([A-Z]{2}[-\s]?\d{2}[-\s]?\d{2})/g,                // AA-00-00
        ];
        
        let detectedPlate = null;
        for (const pattern of patterns) {
            const matches = text.match(pattern);
            if (matches && matches.length > 0) {
                // Get the match and format it
                detectedPlate = matches[0].replace(/\s+/g, '-');
                // Ensure format XX-XX-XX
                if (detectedPlate.length >= 6 && detectedPlate.length <= 10) {
                    break;
                }
            }
        }
        
        if (detectedPlate) {
            // Format properly: XX-XX-XX
            detectedPlate = detectedPlate.replace(/[^A-Z0-9]/g, '');
            if (detectedPlate.length >= 6) {
                const formatted = `${detectedPlate.slice(0,2)}-${detectedPlate.slice(2,4)}-${detectedPlate.slice(4,6)}`;
                
                // Fill the field
                if (plateField) {
                    plateField.value = formatted;
                    plateField.style.background = '#fef3c7'; // Highlight yellow
                    setTimeout(() => {
                        plateField.style.background = '';
                    }, 2000);
                }
                
                showNotification(`✅ Matrícula detectada: ${formatted}`, 'success');
                console.log('✅ License plate detected:', formatted);
            } else {
                throw new Error('Formato inválido');
            }
        } else {
            throw new Error('Matrícula não encontrada');
        }
        
        // Clean up
        URL.revokeObjectURL(imageUrl);
        
    } catch (error) {
        console.warn('OCR failed:', error);
        showNotification('⚠️ Não foi possível detectar a matrícula automaticamente. Por favor, insira manualmente.', 'warning');
    }
}

function closeCamera() {
    // Stop camera stream
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    
    // Clear camera preview
    const video = document.getElementById('cameraPreview');
    if (video) {
        video.srcObject = null;
    }
    
    // Hide modal
    document.getElementById('cameraModal').classList.remove('active');
}

// Functions for new button layout
function retakePhoto() {
    // Remove preview if exists
    const preview = document.getElementById('photoPreviewContainer');
    if (preview) preview.remove();
    
    // Show camera again
    document.getElementById('cameraPreview').style.display = 'block';
    document.getElementById('cameraOverlay').style.display = 'block';
    
    // Restart countdown
    startCameraCountdown();
}

function acceptPhoto() {
    // Save the photo
    if (window.tempPhotoBlob && currentPhotoType) {
        savePhotoToInspection(window.tempPhotoBlob, currentPhotoType);
    }
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
            <button id="btnRetake" onclick="window.retakePhotoAction()" style="display: flex; align-items: center; gap: 8px; background: #009cb6; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                Repetir
            </button>
            <button id="btnAccept" onclick="window.acceptPhotoAction()" style="display: flex; align-items: center; gap: 8px; background: #f59e0b; color: white; padding: 14px 28px; border-radius: 8px; border: none; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <svg style="width: 20px; height: 20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
                Próxima
            </button>
        </div>
    `;
    
    cameraModal.querySelector('.flex').appendChild(previewContainer);
    
    // Store blob temporarily and photo type
    window.tempPhotoBlob = blob;
    window.tempPhotoType = photoType;
    
    // Create global functions for onclick handlers
    window.retakePhotoAction = function() {
        console.log('Retake button clicked via onclick!');
        retakePhoto();
    };
    
    window.acceptPhotoAction = function() {
        console.log('Accept button clicked via onclick! PhotoType:', photoType);
        acceptPhoto(photoType);
    };
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

function showSavingAnimation() {
    // Create saving overlay
    const savingOverlay = document.createElement('div');
    savingOverlay.id = 'savingOverlay';
    savingOverlay.style.cssText = `
        position: fixed;
        inset: 0;
        background: rgba(0, 156, 182, 0.95);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10001;
        animation: fadeIn 0.2s ease-in;
    `;
    
    savingOverlay.innerHTML = `
        <div style="text-align: center; color: white;">
            <svg style="width: 64px; height: 64px; margin: 0 auto 20px; animation: spin 1s linear infinite;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <h3 style="font-size: 24px; font-weight: 600; margin: 0;">A guardar foto...</h3>
        </div>
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    `;
    
    document.body.appendChild(savingOverlay);
    
    // Remove after 1.5 seconds
    setTimeout(() => {
        savingOverlay.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => savingOverlay.remove(), 300);
    }, 1500);
}

function acceptPhoto(photoType) {
    console.log('acceptPhoto called for:', photoType);
    const blob = window.tempPhotoBlob;
    
    if (!blob) {
        alert('Erro: Foto não encontrada');
        console.error('No blob found in window.tempPhotoBlob');
        return;
    }
    
    // Show saving animation
    showSavingAnimation();
    
    // Store photo
    inspectionData.photos[photoType] = blob;
    
    // Update UI
    const slot = document.getElementById(`slot-${photoType}`);
    if (slot) {
        slot.innerHTML = `<img src="${URL.createObjectURL(blob)}" alt="${photoType}">`;
        slot.classList.add('captured');
        
        // Show animation
        slot.classList.add('shutter-animation');
        setTimeout(() => slot.classList.remove('shutter-animation'), 300);
    }
    
    // Update check icon if exists
    const checkIcon = document.getElementById(`check-${photoType}`);
    if (checkIcon) {
        checkIcon.classList.remove('hidden');
    }
    
    // Update diagram indicator if function exists
    if (typeof updateDiagramIndicator === 'function') {
        updateDiagramIndicator(photoType, true);
    }
    
    showNotification(`${photoTypes.find(p => p.type === photoType).label} guardada`, 'success');
    
    // OCR: Auto-detect license plate from front photo
    if (photoType === 'front') {
        detectLicensePlate(blob);
    }
    
    // Auto-open diagram if all photos captured
    if (Object.keys(inspectionData.photos).length === 6) {
        showNotification('Todas as fotos capturadas! A abrir marcação de danos...', 'success');
        
        // Wait a bit then auto-navigate to diagram
        setTimeout(() => {
            console.log('🔵 Auto-opening diagram after 6 photos');
            showDiagramStep();
            // Also initialize canvas
            const canvasEl = document.getElementById('drawingCanvas');
            if (canvasEl && window.canvas) {
                const img = document.querySelector('#carDiagram img');
                if (img) {
                    canvasEl.width = img.offsetWidth;
                    canvasEl.height = img.offsetHeight;
                    console.log('✅ Canvas auto-initialized');
                }
            }
        }, 1500);
    }
    
    // Remove preview
    const preview = document.getElementById('photoPreviewContainer');
    if (preview) preview.remove();
    
    // Clear temp blob
    window.tempPhotoBlob = null;
    
    // Check if we need to capture more photos
    const totalPhotos = Object.keys(inspectionData.photos).length;
    console.log(`Photos captured: ${totalPhotos}/6`);
    
    if (totalPhotos < 6) {
        // Find next photo type to capture
        const nextPhotoType = photoTypes.find(pt => !inspectionData.photos[pt.type]);
        
        if (nextPhotoType) {
            console.log('Opening next photo:', nextPhotoType.type);
            
            // Close current camera
            closeCamera();
            
            // Open camera for next photo after short delay
            setTimeout(() => {
                openCamera(nextPhotoType.type);
            }, 1800); // Wait for saving animation to finish
        }
    } else {
        // All photos captured, close camera
        closeCamera();
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

// Logout function
function logout() {
    // Clear user data
    localStorage.removeItem('userName');
    localStorage.removeItem('userToken');
    
    // Show confirmation
    if (confirm('Tem a certeza que deseja terminar a sessão?')) {
        // Redirect to login page
        window.location.href = '/login';
    }
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
        
        // Add diagram data if exists
        if (window.diagramData) {
            formData.append('diagram_data', JSON.stringify(window.diagramData));
        }
        
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
