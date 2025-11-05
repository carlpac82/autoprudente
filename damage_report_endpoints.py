"""
Endpoints para Damage Reports
Adicionar ao main.py após os endpoints de vehicles
"""

# ============================================================
# DAMAGE REPORTS ENDPOINTS
# ============================================================

@app.post("/api/damage-reports/upload-template")
async def upload_damage_report_template(request: Request, file: UploadFile = File(...)):
    """Upload do template de Damage Report (PDF/Word)"""
    require_auth(request)
    
    try:
        # Ler ficheiro
        contents = await file.read()
        filename = file.filename
        
        # Guardar na BD
        with _db_lock:
            conn = _db_connect()
            try:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS damage_report_templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        file_data BLOB NOT NULL,
                        content_type TEXT,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        uploaded_by TEXT
                    )
                """)
                
                conn.execute("""
                    INSERT INTO damage_report_templates (filename, file_data, content_type, uploaded_by)
                    VALUES (?, ?, ?, ?)
                """, (filename, contents, file.content_type, request.session.get('username', 'unknown')))
                
                conn.commit()
                
                return {"ok": True, "message": "Template uploaded successfully", "filename": filename}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error uploading template: {e}")
        return {"ok": False, "error": str(e)}


@app.post("/api/damage-reports/extract-from-ra")
async def extract_from_rental_agreement(request: Request, file: UploadFile = File(...)):
    """Extrai campos do Rental Agreement PDF"""
    require_auth(request)
    
    try:
        import PyPDF2
        import re
        from io import BytesIO
        
        # Ler PDF
        contents = await file.read()
        pdf_file = BytesIO(contents)
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Extrair texto
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Extrair campos
        fields = {}
        
        # Número do contrato
        contract_match = re.search(r'^(\d+)', text)
        if contract_match:
            fields['contract_number'] = contract_match.group(1)
        
        # Matrícula
        plate_match = re.search(r'([A-Z]{2}\s*-\s*\d{2}\s*-\s*[A-Z]{2})', text)
        if plate_match:
            fields['vehicle_plate'] = plate_match.group(1).replace(' ', '')
        
        # Nome do cliente
        name_match = re.search(r'\d{5}-\d{2}\n([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]+)', text)
        if name_match:
            fields['client_name'] = name_match.group(1).strip()
        
        # Telefone
        phone_match = re.search(r'(\d{9})', text)
        if phone_match:
            fields['client_phone'] = phone_match.group(1)
        
        # Email
        email_match = re.search(r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})', text, re.IGNORECASE)
        if email_match:
            fields['client_email'] = email_match.group(1).lower()
        
        # Modelo do veículo
        model_match = re.search(r'([A-Z]+\s+\d+\s+[A-Z\s]+)\s+[A-Z]{2}\s*-', text)
        if model_match:
            fields['vehicle_model'] = model_match.group(1).strip()
        
        # Datas e horas
        date_pattern = r'(\d{2}\s*-\s*\d{2}\s*-\s*\d{4})'
        time_pattern = r'(\d{2}\s*:\s*\d{2})'
        
        dates = re.findall(date_pattern, text)
        times = re.findall(time_pattern, text)
        
        if len(dates) >= 2:
            fields['pickup_date'] = dates[-2].replace(' ', '')
            fields['return_date'] = dates[-1].replace(' ', '')
        
        if len(times) >= 2:
            fields['pickup_time'] = times[-2].replace(' ', '')
            fields['return_time'] = times[-1].replace(' ', '')
        
        # Locais
        fields['pickup_location'] = 'AUTO PRUDENTE'
        fields['return_location'] = 'AUTO PRUDENTE'
        
        # Morada
        address_match = re.search(r'(URBANIZAÇÃO[^\n]+)\n([A-Z]+\s+\d{4}-\d{3})', text)
        if address_match:
            fields['address'] = address_match.group(1).strip()
            city_postal = address_match.group(2).strip()
            city_match = re.match(r'([A-Z]+)\s+(\d{4}-\d{3})', city_postal)
            if city_match:
                fields['city'] = city_match.group(1)
                fields['postal_code'] = city_match.group(2)
        
        return {"ok": True, "fields": fields}
        
    except Exception as e:
        logging.error(f"Error extracting RA fields: {e}")
        import traceback
        return {"ok": False, "error": str(e), "traceback": traceback.format_exc()}


@app.post("/api/damage-reports/create")
async def create_damage_report(request: Request):
    """Cria um novo Damage Report"""
    require_auth(request)
    
    try:
        data = await request.json()
        
        with _db_lock:
            conn = _db_connect()
            try:
                # Criar tabela se não existir
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS damage_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dr_number TEXT UNIQUE,
                        ra_number TEXT,
                        contract_number TEXT,
                        date DATE,
                        client_name TEXT,
                        client_email TEXT,
                        client_phone TEXT,
                        client_address TEXT,
                        client_city TEXT,
                        client_postal_code TEXT,
                        vehicle_plate TEXT,
                        vehicle_model TEXT,
                        vehicle_brand TEXT,
                        pickup_date DATETIME,
                        pickup_location TEXT,
                        return_date DATETIME,
                        return_location TEXT,
                        inspection_type TEXT,
                        inspector_name TEXT,
                        mileage INTEGER,
                        fuel_level TEXT,
                        damage_description TEXT,
                        observations TEXT,
                        damage_diagram_data TEXT,
                        repair_items TEXT,
                        total_amount REAL,
                        status TEXT DEFAULT 'draft',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_by TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Gerar número DR
                import datetime
                year = datetime.datetime.now().year
                cursor = conn.execute("SELECT COUNT(*) FROM damage_reports WHERE dr_number LIKE ?", (f"%:{year}",))
                count = cursor.fetchone()[0] + 1
                dr_number = f"{count}:{year}"
                
                # Inserir
                conn.execute("""
                    INSERT INTO damage_reports (
                        dr_number, ra_number, contract_number, date,
                        client_name, client_email, client_phone,
                        client_address, client_city, client_postal_code,
                        vehicle_plate, vehicle_model, vehicle_brand,
                        pickup_date, pickup_location, return_date, return_location,
                        inspection_type, inspector_name, mileage, fuel_level,
                        damage_description, observations, damage_diagram_data,
                        created_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dr_number,
                    data.get('ra_number'),
                    data.get('contractNumber'),
                    data.get('date'),
                    data.get('clientName'),
                    data.get('clientEmail'),
                    data.get('clientPhone'),
                    data.get('address'),
                    data.get('city'),
                    data.get('postalCode'),
                    data.get('vehiclePlate'),
                    data.get('vehicleModel'),
                    data.get('vehicleBrand'),
                    data.get('pickupDate'),
                    data.get('pickupLocation'),
                    data.get('returnDate'),
                    data.get('returnLocation'),
                    data.get('inspectionType'),
                    data.get('inspectorName'),
                    data.get('mileage'),
                    data.get('fuelLevel'),
                    data.get('damageDescription'),
                    data.get('observations'),
                    data.get('damageDiagramData'),
                    request.session.get('username', 'unknown')
                ))
                
                conn.commit()
                
                return {"ok": True, "dr_number": dr_number, "message": "Damage Report created successfully"}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error creating damage report: {e}")
        return {"ok": False, "error": str(e)}


@app.get("/api/damage-reports/list")
async def list_damage_reports(request: Request):
    """Lista todos os Damage Reports"""
    require_auth(request)
    
    try:
        with _db_lock:
            conn = _db_connect()
            try:
                cursor = conn.execute("""
                    SELECT 
                        id, dr_number, ra_number, contract_number, date,
                        client_name, vehicle_plate, vehicle_model,
                        status, created_at, created_by
                    FROM damage_reports
                    ORDER BY created_at DESC
                """)
                
                reports = []
                for row in cursor.fetchall():
                    reports.append({
                        'id': row[0],
                        'dr_number': row[1],
                        'ra_number': row[2],
                        'contract_number': row[3],
                        'date': row[4],
                        'client_name': row[5],
                        'vehicle_plate': row[6],
                        'vehicle_model': row[7],
                        'status': row[8],
                        'created_at': row[9],
                        'created_by': row[10]
                    })
                
                return {"ok": True, "reports": reports}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error listing damage reports: {e}")
        return {"ok": False, "error": str(e)}


@app.get("/api/damage-reports/{dr_number}")
async def get_damage_report(request: Request, dr_number: str):
    """Obtém um Damage Report específico"""
    require_auth(request)
    
    try:
        with _db_lock:
            conn = _db_connect()
            try:
                cursor = conn.execute("SELECT * FROM damage_reports WHERE dr_number = ?", (dr_number,))
                row = cursor.fetchone()
                
                if not row:
                    return {"ok": False, "error": "Damage Report not found"}
                
                # Mapear colunas
                columns = [desc[0] for desc in cursor.description]
                report = dict(zip(columns, row))
                
                return {"ok": True, "report": report}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error getting damage report: {e}")
        return {"ok": False, "error": str(e)}
