# Endpoints para sistema de e-mail de Damage Reports
# Este código será integrado no main.py

# ==================== HELPER FUNCTIONS ====================

def _detect_language_from_country(country_code):
    """
    Detect language based on country code (ISO 3166-1 alpha-2)
    Returns: language_code (pt, en, es, de, fr, etc.)
    """
    if not country_code:
        return 'pt'  # Default para Portugal
    
    country_code = country_code.upper().strip()
    
    # Mapeamento país → idioma
    language_map = {
        # Português
        'PT': 'pt', 'BR': 'pt', 'AO': 'pt', 'MZ': 'pt',
        # Espanhol
        'ES': 'es', 'AR': 'es', 'CL': 'es', 'CO': 'es', 'MX': 'es',
        'PE': 'es', 'VE': 'es', 'EC': 'es', 'GT': 'es', 'CU': 'es',
        'BO': 'es', 'DO': 'es', 'HN': 'es', 'PY': 'es', 'SV': 'es',
        'NI': 'es', 'CR': 'es', 'PA': 'es', 'UY': 'es',
        # Alemão
        'DE': 'de', 'AT': 'de', 'CH': 'de', 'LU': 'de', 'LI': 'de',
        # Francês
        'FR': 'fr', 'BE': 'fr', 'CA': 'fr', 'MC': 'fr', 'SN': 'fr',
        # Italiano
        'IT': 'it', 'SM': 'it', 'VA': 'it',
        # Holandês
        'NL': 'nl',
        # Inglês (resto do mundo)
        'GB': 'en', 'US': 'en', 'IE': 'en', 'AU': 'en', 'NZ': 'en',
        'CA': 'en', 'ZA': 'en', 'IN': 'en', 'SG': 'en',
    }
    
    detected = language_map.get(country_code, 'en')  # Default inglês
    logging.info(f"🌍 Country '{country_code}' → Language '{detected}'")
    return detected


# ==================== API ENDPOINTS ====================

@app.get("/api/damage-reports/email-templates")
async def get_email_templates(request: Request):
    """List all email templates (all languages)"""
    require_auth(request)
    
    try:
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
                
                if is_postgres:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT id, language_code, language_name, subject_template, body_template, updated_at
                            FROM dr_email_templates
                            ORDER BY language_code
                        """)
                        rows = cur.fetchall()
                else:
                    cursor = conn.execute("""
                        SELECT id, language_code, language_name, subject_template, body_template, updated_at
                        FROM dr_email_templates
                        ORDER BY language_code
                    """)
                    rows = cursor.fetchall()
                
                templates = []
                for row in rows:
                    templates.append({
                        'id': row[0],
                        'language_code': row[1],
                        'language_name': row[2],
                        'subject_template': row[3],
                        'body_template': row[4],
                        'updated_at': row[5]
                    })
                
                return {"ok": True, "templates": templates}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error getting email templates: {e}")
        return {"ok": False, "error": str(e)}


@app.get("/api/damage-reports/email-template/{lang}")
async def get_email_template_by_lang(request: Request, lang: str):
    """Get email template for specific language"""
    require_auth(request)
    
    try:
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
                
                if is_postgres:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT id, language_code, language_name, subject_template, body_template, updated_at
                            FROM dr_email_templates
                            WHERE language_code = %s
                        """, (lang,))
                        row = cur.fetchone()
                else:
                    cursor = conn.execute("""
                        SELECT id, language_code, language_name, subject_template, body_template, updated_at
                        FROM dr_email_templates
                        WHERE language_code = ?
                    """, (lang,))
                    row = cursor.fetchone()
                
                if not row:
                    return {"ok": False, "error": f"Template for language '{lang}' not found"}
                
                template = {
                    'id': row[0],
                    'language_code': row[1],
                    'language_name': row[2],
                    'subject_template': row[3],
                    'body_template': row[4],
                    'updated_at': row[5]
                }
                
                return {"ok": True, "template": template}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error getting email template for {lang}: {e}")
        return {"ok": False, "error": str(e)}


@app.post("/api/damage-reports/email-template/{lang}")
async def save_email_template(request: Request, lang: str):
    """Create or update email template for language"""
    require_auth(request)
    
    try:
        data = await request.json()
        language_name = data.get('language_name', '')
        subject_template = data.get('subject_template', '')
        body_template = data.get('body_template', '')
        
        if not language_name or not subject_template or not body_template:
            return {"ok": False, "error": "Missing required fields"}
        
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
                
                if is_postgres:
                    with conn.cursor() as cur:
                        # Upsert (INSERT ON CONFLICT UPDATE)
                        cur.execute("""
                            INSERT INTO dr_email_templates (language_code, language_name, subject_template, body_template, updated_at)
                            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                            ON CONFLICT (language_code) DO UPDATE SET
                                language_name = EXCLUDED.language_name,
                                subject_template = EXCLUDED.subject_template,
                                body_template = EXCLUDED.body_template,
                                updated_at = CURRENT_TIMESTAMP
                        """, (lang, language_name, subject_template, body_template))
                else:
                    # SQLite - usar INSERT OR REPLACE
                    conn.execute("""
                        INSERT OR REPLACE INTO dr_email_templates (language_code, language_name, subject_template, body_template, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, (lang, language_name, subject_template, body_template))
                
                conn.commit()
                logging.info(f"✅ Email template '{lang}' saved successfully")
                return {"ok": True, "message": f"Template for '{language_name}' saved successfully"}
            finally:
                conn.close()
    except Exception as e:
        logging.error(f"Error saving email template for {lang}: {e}")
        return {"ok": False, "error": str(e)}


@app.post("/api/damage-reports/send-email")
async def send_damage_report_email(request: Request):
    """
    Send Damage Report via email using Gmail OAuth
    Detects language automatically from client country
    Supports attachments (PDF + images, max 20MB total)
    """
    require_auth(request)
    
    try:
        import base64
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        
        data = await request.json()
        
        # Dados do DR
        dr_number = data.get('drNumber', '')
        client_email = data.get('clientEmail', '')
        client_name = data.get('clientName', '')
        first_name = client_name.split()[0] if client_name else ''
        contract_number = data.get('contractNumber', '')
        vehicle_plate = data.get('vehiclePlate', '')
        date = data.get('date', '')
        country = data.get('country', 'PT')  # ISO 3166-1 code
        
        # Anexos
        pdf_data_base64 = data.get('pdfData', '')  # Base64 do PDF
        attachments = data.get('attachments', [])  # Array de {name, data_base64, type}
        
        # Validações
        if not client_email:
            return {"ok": False, "error": "Client email is required"}
        
        if not dr_number:
            return {"ok": False, "error": "DR number is required"}
        
        # 1. Detectar idioma baseado no país
        language_code = _detect_language_from_country(country)
        logging.info(f"📧 Sending DR email: {dr_number} to {client_email} (language: {language_code})")
        
        # 2. Obter template de email
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
                
                if is_postgres:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT subject_template, body_template
                            FROM dr_email_templates
                            WHERE language_code = %s
                        """, (language_code,))
                        row = cur.fetchone()
                else:
                    cursor = conn.execute("""
                        SELECT subject_template, body_template
                        FROM dr_email_templates
                        WHERE language_code = ?
                    """, (language_code,))
                    row = cursor.fetchone()
                
                if not row:
                    # Fallback para inglês se idioma não encontrado
                    logging.warning(f"⚠️ Template for '{language_code}' not found, using 'en'")
                    language_code = 'en'
                    if is_postgres:
                        with conn.cursor() as cur:
                            cur.execute("SELECT subject_template, body_template FROM dr_email_templates WHERE language_code = %s", (language_code,))
                            row = cur.fetchone()
                    else:
                        cursor = conn.execute("SELECT subject_template, body_template FROM dr_email_templates WHERE language_code = ?", (language_code,))
                        row = cursor.fetchone()
                
                if not row:
                    return {"ok": False, "error": "No email templates configured"}
                
                subject_template = row[0]
                body_template = row[1]
            finally:
                conn.close()
        
        # 3. Substituir parâmetros nos templates
        params = {
            'drNumber': dr_number,
            'firstName': first_name,
            'contractNumber': contract_number,
            'vehiclePlate': vehicle_plate,
            'date': date,
            'email': client_email
        }
        
        subject = subject_template
        body = body_template
        for key, value in params.items():
            subject = subject.replace(f'{{{key}}}', value or '')
            body = body.replace(f'{{{key}}}', value or '')
        
        # 4. Carregar token OAuth do Gmail
        with _db_lock:
            conn = _db_connect()
            try:
                is_postgres = conn.__class__.__module__ == 'psycopg2.extensions'
                
                if is_postgres:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT access_token, refresh_token, expires_at
                            FROM oauth_tokens
                            WHERE provider = 'google'
                            ORDER BY id DESC LIMIT 1
                        """)
                        token_row = cur.fetchone()
                else:
                    cursor = conn.execute("""
                        SELECT access_token, refresh_token, expires_at
                        FROM oauth_tokens
                        WHERE provider = 'google'
                        ORDER BY id DESC LIMIT 1
                    """)
                    token_row = cursor.fetchone()
                
                if not token_row:
                    return {"ok": False, "error": "Gmail not connected. Please configure OAuth in Admin Settings."}
                
                access_token = token_row[0]
                refresh_token = token_row[1]
            finally:
                conn.close()
        
        # 5. Criar mensagem MIME
        message = MIMEMultipart()
        message['To'] = client_email
        message['Subject'] = subject
        
        # Corpo do email (HTML com quebras de linha)
        html_body = body.replace('\n', '<br>')
        message.attach(MIMEText(html_body, 'html'))
        
        # 6. Anexar PDF do DR
        if pdf_data_base64:
            try:
                # Remover prefixo data:application/pdf;base64, se houver
                if ',' in pdf_data_base64:
                    pdf_data_base64 = pdf_data_base64.split(',')[1]
                
                pdf_bytes = base64.b64decode(pdf_data_base64)
                
                part = MIMEBase('application', 'pdf')
                part.set_payload(pdf_bytes)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="Damage_Report_{dr_number.replace("/", "_")}.pdf"')
                message.attach(part)
                
                logging.info(f"📎 PDF attached: {len(pdf_bytes)} bytes")
            except Exception as e:
                logging.error(f"Error attaching PDF: {e}")
        
        # 7. Anexar outros arquivos (imagens, etc)
        for att in attachments:
            try:
                att_name = att.get('name', 'attachment')
                att_data = att.get('data', '')
                att_type = att.get('type', 'application/octet-stream')
                
                if ',' in att_data:
                    att_data = att_data.split(',')[1]
                
                att_bytes = base64.b64decode(att_data)
                
                # Validar tamanho (máx 20MB por anexo)
                if len(att_bytes) > 20 * 1024 * 1024:
                    logging.warning(f"⚠️ Attachment '{att_name}' too large ({len(att_bytes)} bytes), skipping")
                    continue
                
                main_type, sub_type = att_type.split('/')
                part = MIMEBase(main_type, sub_type)
                part.set_payload(att_bytes)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{att_name}"')
                message.attach(part)
                
                logging.info(f"📎 Attachment added: {att_name} ({len(att_bytes)} bytes)")
            except Exception as e:
                logging.error(f"Error attaching file '{att.get('name')}': {e}")
        
        # 8. Enviar via Gmail API
        try:
            credentials = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
            )
            
            service = build('gmail', 'v1', credentials=credentials)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}
            
            result = service.users().messages().send(userId='me', body=send_message).execute()
            
            logging.info(f"✅ Email sent successfully to {client_email} (Message ID: {result['id']})")
            return {
                "ok": True,
                "message": f"Email sent to {client_email}",
                "message_id": result['id'],
                "language": language_code
            }
        except Exception as e:
            logging.error(f"❌ Error sending email via Gmail API: {e}")
            return {"ok": False, "error": f"Failed to send email: {str(e)}"}
    
    except Exception as e:
        logging.error(f"Error in send_damage_report_email: {e}", exc_info=True)
        return {"ok": False, "error": str(e)}
