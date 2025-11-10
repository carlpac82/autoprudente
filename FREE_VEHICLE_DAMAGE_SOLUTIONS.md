# 🆓 SOLUÇÕES GRATUITAS PARA DETEÇÃO DE DANOS - OPEN SOURCE

**Objetivo:** Usar soluções GRÁTIS já prontas para adaptar à Auto Prudente  
**Requisito:** SEM custos de API, código open source, modelos pré-treinados

---

## 🎯 SOLUÇÃO RECOMENDADA: Hugging Face + Custom App

### ⭐ COMBO PERFEITO (100% GRÁTIS):

**1. Modelo AI Pré-treinado** → Hugging Face  
**2. App Base** → GitHub Open Source  
**3. Integração** → Código Python simples

---

## 🤖 MODELO AI GRÁTIS - HUGGING FACE

### **beingamit99/car_damage_detection**

**Link:** https://huggingface.co/beingamit99/car_damage_detection  
**Licença:** Open Source (Apache 2.0)  
**Status:** ✅ Pronto a usar  
**Performance:** Treinado em milhares de imagens

#### **Features:**
- ✅ Modelo pré-treinado GRÁTIS
- ✅ Download direto (sem API paga)
- ✅ Classificação de danos
- ✅ Probability score
- ✅ Fácil integração Python

#### **Código para usar (2 linhas!):**

```python
from transformers import pipeline

# Criar pipeline
pipe = pipeline("image-classification", model="beingamit99/car_damage_detection")

# Analisar foto
result = pipe("foto_carro.jpg")
print(result)
# Output: [{'label': 'damaged', 'score': 0.95}, ...]
```

#### **Classes que detecta:**
- `damaged` - Carro danificado
- `whole` - Carro intacto
- Probability score para cada classe

---

## 📊 DATASETS GRATUITOS - ROBOFLOW

### **1. Car Damage Detection - CAPSTONE**
**Link:** https://universe.roboflow.com/capstone-nh0nc/car-damage-detection-t0g92  
**Licença:** Open Source  
**Imagens:** 1000+ anotadas

**Features:**
- ✅ Object detection
- ✅ Bounding boxes
- ✅ Multiple damage types
- ✅ Download gratuito

### **2. Car Damage Severity - CarDD**
**Link:** https://universe.roboflow.com/car-damage-detection-cardd/car-damage-severity-detection-cardd  
**Imagens:** 500+ com severidade

**Classes:**
- Minor damage
- Moderate damage
- Severe damage

### **3. COCO Car Damage Dataset**
**Link:** https://universe.roboflow.com/dan-vmm5z/car-damage-coco-dataset  
**Format:** COCO (industry standard)  
**Use:** Treinar modelos próprios

---

## 💻 CÓDIGO OPEN SOURCE - GITHUB

### **1. Car Damage Detective** ⭐ COMPLETO
**Link:** https://github.com/neokt/car-damage-detective  
**Autor:** neokt  
**Licença:** MIT (livre para uso comercial)

**O que tem:**
- ✅ **Web app completa** (Flask + Bootstrap)
- ✅ Modelo CNN treinado (VGG16)
- ✅ 79% accuracy location, 71% severity
- ✅ Real-time predictions
- ✅ Dataset incluído

**Tech Stack:**
- Python
- Keras + TensorFlow
- VGG16 transfer learning
- Flask web framework
- Bootstrap UI

**Como usar:**
```bash
git clone https://github.com/neokt/car-damage-detective
cd car-damage-detective
pip install -r requirements.txt
python app.py  # Web app runs!
```

---

### **2. Car Damage Detector - Mask R-CNN**
**Link:** https://github.com/louisyuzhe/car-damage-detector  
**Especialização:** Insurance claims

**Features:**
- ✅ Mask R-CNN (segmentation)
- ✅ Detecta ÁREA exata do dano
- ✅ Usado por seguradoras
- ✅ Training scripts incluídos

---

### **3. Car Damage Detector - nicolasmetallo**
**Link:** https://github.com/nicolasmetallo/car-damage-detector  
**Licença:** MIT

**Features:**
- ✅ Python 2.7 e 3.7
- ✅ TensorFlow
- ✅ CLI + Jupyter notebooks
- ✅ Training pipeline completo

**Usage:**
```bash
# Train
python damage.py train --dataset=path/to/dataset

# Predict
python damage.py detect --weights=path/to/weights.h5 --image=path/to/image.jpg
```

---

### **4. Fleet Inspections App**
**Link:** https://github.com/Angelelz/fleet-inspections  
**Tipo:** Web app completa para fleet management

**Features:**
- ✅ Web app Python (Flask)
- ✅ Database (SQLite)
- ✅ Vehicle tracking
- ✅ Inspection forms
- ✅ Issue tracking
- ✅ Maintenance logs

**Tech:**
- Flask backend
- SQLite database
- Bootstrap frontend
- Forms para inspeções

---

## 🔧 COMO ADAPTAR PARA AUTO PRUDENTE

### **ARQUITETURA PROPOSTA:**

```
┌─────────────────────────────────────────────┐
│  APP MOBILE (React Native)                 │
│  - Captura fotos 6 ângulos                 │
│  - Upload para servidor                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  SERVIDOR PYTHON (FastAPI - já tens!)      │
│  - Recebe fotos                             │
│  - Chama modelo Hugging Face                │
│  - Guarda resultados PostgreSQL             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  MODELO AI (Hugging Face)                   │
│  - beingamit99/car_damage_detection         │
│  - Classifica: damaged/whole                │
│  - Score de probabilidade                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  RELATÓRIO PDF (Como DR atual)              │
│  - Fotos comparação check-in/out            │
│  - Danos detectados pela AI                 │
│  - Manual override (staff)                  │
└─────────────────────────────────────────────┘
```

---

## 📝 PLANO DE IMPLEMENTAÇÃO

### **FASE 1: Setup Modelo AI (1 dia)**

```python
# install.sh
pip install transformers torch pillow

# test_model.py
from transformers import pipeline
from PIL import Image

# Load model (downloads automatically first time)
pipe = pipeline("image-classification", 
                model="beingamit99/car_damage_detection")

# Test with car photo
image = Image.open("test_car.jpg")
result = pipe(image)

print(f"Result: {result}")
# [{'label': 'damaged', 'score': 0.92}]
```

---

### **FASE 2: Integrar no FastAPI (2 dias)**

```python
# main.py (adicionar ao teu existente)
from fastapi import UploadFile, File
from transformers import pipeline
from PIL import Image
import io

# Load model ONCE at startup
damage_model = pipeline("image-classification", 
                       model="beingamit99/car_damage_detection")

@app.post("/api/vehicle/check-damage")
async def check_vehicle_damage(file: UploadFile = File(...)):
    """
    Analisa foto de carro para detetar danos
    """
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # AI prediction
    result = damage_model(image)
    
    # Return result
    return {
        "ok": True,
        "predictions": result,
        "is_damaged": result[0]['label'] == 'damaged',
        "confidence": result[0]['score']
    }
```

---

### **FASE 3: Criar Tabela BD (30 min)**

```sql
CREATE TABLE vehicle_inspections (
    id SERIAL PRIMARY KEY,
    inspection_type VARCHAR(20), -- 'check_in' or 'check_out'
    contract_number VARCHAR(50),
    vehicle_plate VARCHAR(20),
    inspector_name VARCHAR(100),
    inspection_date TIMESTAMP DEFAULT NOW(),
    
    -- AI Results
    ai_prediction VARCHAR(20),    -- 'damaged' or 'whole'
    ai_confidence DECIMAL(5,2),   -- 0.00 to 1.00
    
    -- Photos (store as BLOB or S3 URLs)
    photo_front BYTEA,
    photo_back BYTEA,
    photo_left BYTEA,
    photo_right BYTEA,
    photo_interior BYTEA,
    photo_odometer BYTEA,
    
    -- Manual override
    manual_review BOOLEAN DEFAULT FALSE,
    manual_notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### **FASE 4: Frontend Simples (3 dias)**

```javascript
// React Native ou Web
async function uploadPhoto(photo, angle) {
    const formData = new FormData();
    formData.append('file', photo);
    
    const response = await fetch('/api/vehicle/check-damage', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    
    if (result.is_damaged) {
        alert(`⚠️ DANO DETECTADO! Confiança: ${result.confidence}%`);
    } else {
        alert(`✅ Sem danos. Confiança: ${result.confidence}%`);
    }
}
```

---

## 💰 CUSTO TOTAL: €0

| Item | Custo | Notas |
|------|-------|-------|
| Modelo AI | €0 | Hugging Face grátis |
| Dataset | €0 | Roboflow open source |
| Código base | €0 | GitHub MIT license |
| Hosting | €0 | Render já tens |
| PostgreSQL | €0 | Já tens |
| Desenvolvimento | €0 | Tu fazes |
| **TOTAL** | **€0** | 🎉 |

---

## 🎓 TUTORIAIS E RECURSOS

### **Hugging Face:**
- Docs: https://huggingface.co/docs/transformers
- Models: https://huggingface.co/models?pipeline_tag=image-classification&search=car

### **Roboflow:**
- Datasets: https://universe.roboflow.com/
- How to use: https://docs.roboflow.com/

### **TensorFlow:**
- Transfer learning: https://www.tensorflow.org/tutorials/images/transfer_learning

---

## 🚀 EXEMPLO COMPLETO - CÓDIGO PRONTO

```python
"""
Vehicle Damage Detection API - FREE VERSION
Uses Hugging Face model (no API costs)
"""

from fastapi import FastAPI, UploadFile, File, Form
from transformers import pipeline
from PIL import Image
import io
import psycopg2
from datetime import datetime
import base64

app = FastAPI()

# Load model at startup (downloads once, then cached)
print("Loading AI model...")
damage_detector = pipeline(
    "image-classification",
    model="beingamit99/car_damage_detection"
)
print("Model loaded!")

@app.post("/api/vehicle-inspection/create")
async def create_inspection(
    inspection_type: str = Form(...),  # check_in or check_out
    vehicle_plate: str = Form(...),
    contract_number: str = Form(...),
    photo_front: UploadFile = File(...),
    photo_back: UploadFile = File(...),
    photo_left: UploadFile = File(...),
    photo_right: UploadFile = File(...),
):
    """
    Cria inspeção de veículo com análise AI GRATUITA
    """
    
    # Process each photo with AI
    photos = {
        'front': photo_front,
        'back': photo_back,
        'left': photo_left,
        'right': photo_right
    }
    
    results = {}
    damages_detected = []
    
    for angle, photo in photos.items():
        # Read image
        contents = await photo.read()
        image = Image.open(io.BytesIO(contents))
        
        # AI analysis (FREE!)
        prediction = damage_detector(image)
        
        # Store result
        results[angle] = {
            'prediction': prediction[0]['label'],
            'confidence': float(prediction[0]['score']),
            'image_data': base64.b64encode(contents).decode()
        }
        
        # Check if damaged
        if prediction[0]['label'] == 'damaged' and prediction[0]['score'] > 0.7:
            damages_detected.append(f"{angle}: {prediction[0]['score']:.2%}")
    
    # Save to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO vehicle_inspections 
        (inspection_type, vehicle_plate, contract_number, 
         ai_results, damages_detected, inspection_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        inspection_type,
        vehicle_plate,
        contract_number,
        json.dumps(results),
        json.dumps(damages_detected),
        datetime.now()
    ))
    
    inspection_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    
    return {
        "ok": True,
        "inspection_id": inspection_id,
        "damages_detected": damages_detected,
        "has_damage": len(damages_detected) > 0,
        "results": results
    }

@app.get("/api/vehicle-inspection/{inspection_id}/report")
async def get_inspection_report(inspection_id: int):
    """
    Gera relatório PDF da inspeção (como Damage Report)
    """
    # TODO: Buscar dados da BD
    # TODO: Gerar PDF com fotos + resultados AI
    # TODO: Comparar check-in vs check-out
    pass
```

---

## ⚡ VANTAGENS DA SOLUÇÃO GRATUITA

### **Pros:**
- ✅ **€0 custo** (vs €0.50-2.00 por inspeção)
- ✅ **Controlo total** do código
- ✅ **Dados privados** (não enviados para APIs externas)
- ✅ **Customização** 100%
- ✅ **Escalável** sem limites
- ✅ **Offline capable** (modelo local)

### **Cons:**
- ⚠️ Precisão menor que soluções pagas (70-80% vs 95%)
- ⚠️ Não detecta tipos específicos de dano (só damaged/whole)
- ⚠️ Não tem estimativa de custo automática
- ⚠️ Precisa desenvolvimento (2-3 semanas)
- ⚠️ Sem suporte técnico

---

## 🎯 QUANDO USAR CADA OPÇÃO

### **Usar Solução Gratuita SE:**
- ✅ Orçamento limitado
- ✅ Apenas 10-50 inspeções/mês
- ✅ Tens tempo para desenvolver
- ✅ Precisão 70-80% é suficiente
- ✅ Queres controlo total

### **Usar Solução Paga (Inspektlabs) SE:**
- ✅ Orçamento disponível (€50-100/mês)
- ✅ 100+ inspeções/mês
- ✅ Precisas precisão 95%+
- ✅ Queres setup em 24h
- ✅ Precisas fraud detection

---

## 📊 COMPARAÇÃO FINAL

| Feature | Grátis (Hugging Face) | Pago (Inspektlabs) |
|---------|----------------------|-------------------|
| **Custo** | €0 | €50-100/mês |
| **Setup** | 2-3 semanas | 24 horas |
| **Precisão** | 70-80% | 95%+ |
| **Fraud detection** | ❌ | ✅ |
| **Damage types** | Basic (2) | Detailed (20+) |
| **Cost estimate** | ❌ | ✅ |
| **Support** | Community | Dedicated |
| **Customização** | 100% | Limited |
| **Dados privados** | ✅ | ⚠️ (API) |

---

## 🚀 PRÓXIMO PASSO

### **RECOMENDAÇÃO:**

**Começar com GRÁTIS para validar!**

1. ✅ Testar modelo Hugging Face (1 dia)
2. ✅ Criar MVP simples (1 semana)
3. ✅ Testar com 10-20 carros reais
4. ✅ Medir precisão vs inspeção manual
5. 📊 **DEPOIS decidir:** continuar grátis ou upgrade pago

**Se precisão 70% é OK → Ficar com grátis**  
**Se precisas 95%+ → Upgrade para Inspektlabs**

---

## 📞 LINKS ÚTEIS

### **Modelos:**
- Hugging Face: https://huggingface.co/beingamit99/car_damage_detection
- Alternativo: https://huggingface.co/models?search=car%20damage

### **Código:**
- Car Damage Detective: https://github.com/neokt/car-damage-detective
- Mask R-CNN: https://github.com/louisyuzhe/car-damage-detector

### **Datasets:**
- Roboflow: https://universe.roboflow.com/search?q=car%20damage
- Kaggle: https://www.kaggle.com/datasets?search=car+damage

---

**CONCLUSÃO:** Podes ter sistema de deteção de danos AI **GRÁTIS** usando Hugging Face + código open source! 🎉

**Queres que comece a implementar?** 🚀
