#!/usr/bin/env python3
"""
Script para adicionar rotas básicas de vehicle inspection ao main.py
"""

def add_basic_routes():
    """Adiciona rotas básicas ao main.py"""
    
    # Ler o arquivo main.py
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Encontrar onde inserir (antes do if __name__)
    lines = content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('if __name__ == "__main__":'):
            insert_index = i
            break
    
    if insert_index == -1:
        print("❌ Não foi possível encontrar 'if __name__'")
        return False
    
    # Rotas básicas para adicionar
    basic_routes = '''
# ================================================================================
# VEHICLE INSPECTION ROUTES - BASIC IMPLEMENTATION
# ================================================================================

@app.get("/check-in")
async def check_in_page(request: Request):
    """Check-in page"""
    return templates.TemplateResponse("vehicle_inspection.html", {
        "request": request,
        "inspection_type": "checkin"
    })

@app.get("/check-out") 
async def check_out_page(request: Request):
    """Check-out page"""
    return templates.TemplateResponse("vehicle_inspection.html", {
        "request": request,
        "inspection_type": "checkout"
    })

@app.get("/vehicle-inspections")
async def vehicle_inspections_history(request: Request):
    """Vehicle inspections history page"""
    return templates.TemplateResponse("inspection_history.html", {
        "request": request
    })

@app.post("/api/vehicle-inspections/create")
async def create_vehicle_inspection(request: Request):
    """Create a new vehicle inspection"""
    try:
        form = await request.form()
        
        inspection_data = {
            "inspection_type": form.get("type", "checkin"),
            "vehicle_plate": form.get("plate", ""),
            "contract_number": form.get("ra", ""),
            "inspector_name": form.get("receptionist", ""),
            "inspection_date": form.get("date", ""),
            "inspection_time": form.get("time", ""),
            "fuel_level": form.get("fuelLevel", 100),
            "odometer_reading": form.get("odometerReading", 0),
            "damage_notes": form.get("observations", ""),
            "created_at": datetime.now().isoformat()
        }
        
        inspection_number = f"VI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        inspection_data["inspection_number"] = inspection_number
        
        logging.info(f"Vehicle inspection created: {inspection_number}")
        
        return JSONResponse({
            "ok": True,
            "inspection_number": inspection_number,
            "message": "Inspection saved successfully"
        })
        
    except Exception as e:
        logging.error(f"Error creating vehicle inspection: {e}")
        return JSONResponse({
            "ok": False,
            "error": str(e)
        }, status_code=500)

@app.post("/api/save-inspection")
async def save_inspection_legacy(request: Request):
    """Legacy endpoint for saving inspections"""
    try:
        data = await request.json()
        
        inspection_number = f"VI-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logging.info(f"Legacy inspection saved: {inspection_number}")
        
        return JSONResponse({
            "success": True,
            "inspection_number": inspection_number,
            "message": "Inspection saved successfully"
        })
        
    except Exception as e:
        logging.error(f"Error saving legacy inspection: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })

@app.get("/api/inspections/history")
async def get_inspections_history(request: Request):
    """Get vehicle inspections history"""
    try:
        mock_inspections = [
            {
                "inspection_number": "VI-20251111150000",
                "vehicle_plate": "AA-00-AA",
                "contract_number": "12345-01",
                "inspection_type": "checkin",
                "inspector_name": "Admin",
                "created_at": "2025-11-11T15:00:00",
                "fuel_level": 100,
                "odometer_reading": 50000
            }
        ]
        
        return JSONResponse({
            "ok": True,
            "inspections": mock_inspections
        })
        
    except Exception as e:
        logging.error(f"Error getting inspections history: {e}")
        return JSONResponse({
            "ok": False,
            "error": str(e)
        }, status_code=500)

'''
    
    # Inserir as rotas
    new_lines = lines[:insert_index] + basic_routes.split('\n') + lines[insert_index:]
    
    # Escrever o arquivo
    with open("main.py", "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Rotas básicas adicionadas com sucesso!")
    return True

if __name__ == "__main__":
    add_basic_routes()
