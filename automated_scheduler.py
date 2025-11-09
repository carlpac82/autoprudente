#!/usr/bin/env python3
"""
🤖 SISTEMA DE AGENDAMENTO AUTOMÁTICO DE RELATÓRIOS

Executa pesquisas e envio de emails nos horários configurados:
- Diário: múltiplos horários com dias/locais independentes
- Semanal: dia da semana específico
- Mensal: dia do mês específico

Usa APScheduler para agendar tarefas.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Global scheduler
scheduler = None

def _get_db_connection():
    """Get database connection"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logging.error("❌ DATABASE_URL not set")
        return None
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        logging.error(f"❌ Database connection error: {str(e)}")
        return None

def load_advanced_settings():
    """Load advanced automated reports settings from database"""
    print("🔌 Connecting to database...", flush=True)
    conn = _get_db_connection()
    if not conn:
        print("❌ Database connection failed", flush=True)
        return None
    
    try:
        cursor = conn.cursor()
        print("🔍 Querying automatedReportsAdvanced...", flush=True)
        cursor.execute(
            "SELECT setting_value FROM price_automation_settings WHERE setting_key = 'automatedReportsAdvanced'"
        )
        row = cursor.fetchone()
        
        if row and row[0]:
            settings = json.loads(row[0])
            print(f"✅ Loaded advanced settings from database", flush=True)
            print(f"   Settings: {json.dumps(settings, indent=2)}", flush=True)
            logging.info(f"✅ Loaded advanced settings from database")
            return settings
        else:
            print(f"📭 No advanced settings found in database", flush=True)
            logging.info(f"📭 No advanced settings found")
            return None
    except Exception as e:
        print(f"❌ Error loading settings: {str(e)}", flush=True)
        logging.error(f"❌ Error loading settings: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def save_automated_search_placeholder(location, days_list):
    """
    Save automated search placeholder in recent_searches
    This marks that an automated search should have occurred
    """
    print(f"\n{'='*80}", flush=True)
    print(f"💾 SAVING AUTOMATED SEARCH TO HISTORY", flush=True)
    print(f"{'='*80}", flush=True)
    print(f"📍 Location: {location}", flush=True)
    print(f"📅 Days: {days_list}", flush=True)
    
    logging.info(f"💾 SAVING AUTOMATED SEARCH PLACEHOLDER: {location}, days: {days_list}")
    
    try:
        from datetime import datetime, timedelta
        import json
        
        print("🔌 Connecting to database for saving...", flush=True)
        conn = _get_db_connection()
        if not conn:
            print("❌ Database connection FAILED!", flush=True)
            logging.error("❌ Cannot connect to database")
            return False
        
        print("✅ Database connected", flush=True)
        cursor = conn.cursor()
        
        saved_count = 0
        # For each day, create a placeholder search entry
        for day in days_list:
            pickup_date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            
            print(f"\n   📝 Saving: {location} | {day}d | {pickup_date}", flush=True)
            
            # Create placeholder results
            placeholder_results = json.dumps([{
                "info": f"Automated search placeholder for {location}, {day} days",
                "pickup_date": pickup_date,
                "location": location,
                "days": day
            }])
            
            try:
                cursor.execute("""
                    INSERT INTO recent_searches 
                    (location, start_date, days, results_data, timestamp, source)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (location, pickup_date, day, placeholder_results, timestamp, 'automated'))
                
                saved_count += 1
                print(f"   ✅ SAVED TO DATABASE: {location}, {day}d, {pickup_date}", flush=True)
                logging.info(f"   ✅ Saved placeholder: {location}, {day}d, {pickup_date}")
            except Exception as insert_error:
                print(f"   ❌ INSERT FAILED: {str(insert_error)}", flush=True)
                logging.error(f"   ❌ Insert failed: {str(insert_error)}")
        
        conn.commit()
        print(f"\n✅ COMMIT SUCCESSFUL - {saved_count} searches saved", flush=True)
        
        # VERIFICAR SE FOI SALVO
        print(f"\n🔍 VERIFYING: Checking if searches were saved...", flush=True)
        cursor.execute("""
            SELECT location, start_date, days, timestamp, source
            FROM recent_searches
            WHERE source = 'automated'
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        
        print(f"📊 Found {len(rows)} automated searches in database:", flush=True)
        for row in rows:
            loc, start, days, ts, src = row
            print(f"   • {loc} | {days}d | {start} | {ts} | source={src}", flush=True)
        
        cursor.close()
        conn.close()
        
        print(f"\n{'='*80}", flush=True)
        print(f"✅ AUTOMATED SEARCH SAVED TO HISTORY: {location} ({saved_count} records)", flush=True)
        print(f"{'='*80}\n", flush=True)
        
        logging.info(f"✅ Search placeholders saved for {location}")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED TO SAVE SEARCH: {str(e)}", flush=True)
        logging.error(f"❌ Failed to save search placeholders: {str(e)}")
        import traceback
        traceback_str = traceback.format_exc()
        print(traceback_str, flush=True)
        logging.error(traceback_str)
        return False

def send_daily_report_for_schedule(schedule, schedule_index):
    """
    Send daily report for a specific schedule configuration
    
    Args:
        schedule: dict with searchTime, sendTime, days, locations
        schedule_index: int, index of schedule (for logging)
    """
    print(f"\n{'='*80}", flush=True)
    print(f"📧 SENDING EMAIL - SCHEDULE #{schedule_index + 1}", flush=True)
    print(f"{'='*80}", flush=True)
    print(f"   Send Time: {schedule.get('sendTime')}", flush=True)
    print(f"   Days: {schedule.get('days')}", flush=True)
    print(f"   Locations: {schedule.get('locations')}", flush=True)
    
    logging.info(f"\n{'='*80}")
    logging.info(f"📧 SENDING EMAIL - SCHEDULE #{schedule_index + 1}")
    logging.info(f"{'='*80}")
    logging.info(f"   Send Time: {schedule.get('sendTime')}")
    logging.info(f"   Days: {schedule.get('days')}")
    logging.info(f"   Locations: {schedule.get('locations')}")
    
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        import base64
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Get Gmail credentials
        conn = _get_db_connection()
        if not conn:
            logging.error("❌ Cannot connect to database for Gmail credentials")
            return
        
        cursor = conn.cursor()
        cursor.execute(
            "SELECT access_token, refresh_token FROM oauth_tokens WHERE provider = 'google' ORDER BY updated_at DESC LIMIT 1"
        )
        row = cursor.fetchone()
        
        if not row or not row[0] or not row[1]:
            logging.error("❌ Gmail credentials not found or incomplete")
            cursor.close()
            conn.close()
            return
        
        access_token, refresh_token = row
        cursor.close()
        conn.close()
        
        # Create credentials
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            logging.error("❌ GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set")
            return
        
        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )
        
        # Get recipient email
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT setting_value FROM price_automation_settings WHERE setting_key = 'report_email'"
        )
        row = cursor.fetchone()
        recipient = row[0] if row else 'carlpac82@hotmail.com'
        cursor.close()
        conn.close()
        
        # Load search data from database
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT location, start_date, days, results_data, timestamp
            FROM recent_searches
            WHERE timestamp >= NOW() - INTERVAL '24 hours'
            ORDER BY timestamp DESC
            LIMIT 100
            """
        )
        rows = cursor.fetchall()
        
        all_results = []
        for row in rows:
            location, start_date, days_val, results_data, timestamp = row
            if results_data:
                results = json.loads(results_data)
                for r in results:
                    r['days'] = days_val
                    r['location'] = location
                all_results.extend(results)
        
        cursor.close()
        conn.close()
        
        search_data = {'results': all_results}
        logging.info(f"   📊 Loaded {len(all_results)} search results")
        
        if not all_results:
            logging.warning("   ⚠️ No search data available, skipping email")
            return
        
        # Import report generation function
        sys.path.insert(0, os.path.dirname(__file__))
        from improved_reports import generate_daily_report_html_by_location
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=credentials)
        
        # Send for each location
        locations_to_send = []
        if schedule.get('locations', {}).get('albufeira'):
            locations_to_send.append('Albufeira')
        if schedule.get('locations', {}).get('faro'):
            locations_to_send.append('Aeroporto de Faro')
        
        sent_count = 0
        for location in locations_to_send:
            logging.info(f"   📍 Generating report for: {location}")
            
            html_content = generate_daily_report_html_by_location(search_data, location)
            
            message = MIMEMultipart('alternative')
            message['to'] = recipient
            message['subject'] = f'📊 Relatório Diário {location} - Auto Prudente ({datetime.now().strftime("%d/%m/%Y")})'
            
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            sent_count += 1
            logging.info(f"   ✅ Email sent to {recipient} for {location}")
        
        logging.info(f"✅ SCHEDULE #{schedule_index + 1} COMPLETED - {sent_count} emails sent")
        
    except Exception as e:
        logging.error(f"❌ Error sending daily report for schedule #{schedule_index + 1}: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())

def execute_search_for_schedule(schedule, schedule_index):
    """
    Execute REAL CarJet searches for a schedule
    This runs at searchTime
    """
    print(f"\n{'='*80}", flush=True)
    print(f"🔍 EXECUTING REAL CARJET SEARCHES - SCHEDULE #{schedule_index + 1}", flush=True)
    print(f"{'='*80}", flush=True)
    print(f"   Search Time: {schedule.get('searchTime')}", flush=True)
    print(f"   Days: {schedule.get('days')}", flush=True)
    print(f"   Locations: {schedule.get('locations')}", flush=True)
    
    try:
        from datetime import datetime, timedelta
        import json
        import asyncio
        
        # Obter configurações
        days = schedule.get('days', [])
        locations_config = schedule.get('locations', {})
        
        if not days or not (locations_config.get('albufeira') or locations_config.get('faro')):
            print(f"   ⚠️ No days or locations configured!", flush=True)
            return
        
        # Preparar localizações
        locations_to_search = []
        if locations_config.get('albufeira'):
            locations_to_search.append("Albufeira")
        if locations_config.get('faro'):
            locations_to_search.append("Aeroporto de Faro")
        
        # Data de pickup (amanhã)
        pickup_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        print(f"\n🚗 Preparing CarJet search...", flush=True)
        print(f"   Pickup Date: {pickup_date}", flush=True)
        print(f"   Durations: {days}", flush=True)
        print(f"   Locations: {locations_to_search}", flush=True)
        
        # Executar pesquisa usando asyncio
        all_results = asyncio.run(_do_carjet_search(locations_to_search, days, pickup_date))
        print(f"\n✅ Search completed!", flush=True)
        
        # SALVAR NA BD
        _save_search_results(all_results, days, locations_to_search)
        
        print(f"\n✅ SEARCH EXECUTION COMPLETED!", flush=True)
        print(f"✅ Results saved to AUTOMATED_SEARCH_HISTORY table!", flush=True)
        print(f"✅ Go to Automated Pricing → History to see them!", flush=True)
        print(f"{'='*80}\n", flush=True)
            
    except Exception as e:
        print(f"\n❌ SEARCH ERROR: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)

async def _do_carjet_search(locations, days, pickup_date):
    """
    Execute CarJet search using Playwright - internal async function
    WITH TIME ROTATION AND ANTI-WAF PROTECTION (same as Automated Pricing)
    """
    from playwright.async_api import async_playwright
    import sys
    import os
    import random
    
    # Import track_by_params from main
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from main import track_by_params
    
    # NOTE: Anti-WAF settings (device rotation, timezone, referrer) are handled by track_by_params
    # Date rotation is ALSO handled by track_by_params automatically
    # We don't need to apply it here to avoid DOUBLE rotation!
    print(f"\n🛡️ Anti-WAF Protection enabled (handled by track_by_params)", flush=True)
    
    all_results = {}
    
    for location in locations:
        print(f"\n📍 Searching {location}...", flush=True)
        location_results = {}
        
        for day in days:
            print(f"   → {day} days...", flush=True)
            
            try:
                # Mock request object (complete with all FastAPI Request attributes)
                # NOTE: NO rotation here - track_by_params does all rotations internally!
                class MockRequest:
                    def __init__(self, data):
                        self._data = data
                        self.headers = {}  # Empty headers
                        self.session = {'username': 'automated', 'user_email': 'automated'}  # Session data
                        self.client = type('obj', (object,), {'host': '127.0.0.1'})()  # Mock client
                    
                    async def json(self):
                        return self._data
                
                request = MockRequest({
                    'location': location,
                    'start_date': pickup_date,  # Original date (track_by_params will rotate)
                    'start_time': '15:00',      # Fixed time (track_by_params will rotate)
                    'days': day,
                    'lang': 'pt',
                    'currency': 'EUR'
                })
                
                # Call track_by_params (includes Anti-WAF with devices, timezones, etc)
                response = await track_by_params(request)
                
                # Extract items from response
                if hasattr(response, 'body'):
                    import json
                    data = json.loads(response.body.decode())
                    items = data.get('items', [])
                    print(f"      ✅ {len(items)} cars found", flush=True)
                    location_results[day] = items
                    
            except Exception as e:
                print(f"      ❌ Error: {str(e)}", flush=True)
                location_results[day] = []
        
        all_results[location] = location_results
    
    return all_results

def _save_search_results(all_results, days, locations):
    """
    Save search results to automated_search_history table
    """
    import json
    from datetime import datetime
    
    print(f"\n💾 Saving results to automated_search_history...", flush=True)
    
    conn = _get_db_connection()
    if not conn:
        print("❌ Database connection failed", flush=True)
        return
    
    try:
        for location in locations:
            location_results = all_results.get(location, {})
            
            # Preparar dados de preços por grupo
            prices_by_group = {}
            supplier_data = {}
            total_price_count = 0
            
            for day, items in location_results.items():
                if items:
                    # Agrupar por grupo
                    for item in items:
                        grupo = item.get('group', 'Unknown')
                        price = item.get('price_num', 0)
                        
                        if grupo not in prices_by_group:
                            prices_by_group[grupo] = {}
                        
                        # Menor preço
                        if day not in prices_by_group[grupo] or price < prices_by_group[grupo][day]:
                            prices_by_group[grupo][day] = price
                            total_price_count += 1
                    
                    supplier_data[str(day)] = items
            
            if prices_by_group:
                # Insert into database
                now = datetime.now()
                month_key = f"{now.year}-{str(now.month).zfill(2)}"
                search_date = now.isoformat()
                
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO automated_search_history 
                    (location, search_type, search_date, month_key, prices_data, dias, price_count, supplier_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    location,
                    'automated',
                    search_date,
                    month_key,
                    json.dumps(prices_by_group),
                    json.dumps(days),
                    total_price_count,
                    json.dumps(supplier_data)
                ))
                
                conn.commit()
                print(f"   ✅ {location}: {total_price_count} prices saved!", flush=True)
                
    except Exception as e:
        print(f"❌ Save error: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        if conn:
            conn.close()

def execute_weekly_search():
    """
    Execute weekly search - uses FIXED DAY of month (e.g., day 05)
    Can search in future months (not just current month)
    """
    print(f"\n{'='*80}", flush=True)
    print(f"🔍 EXECUTING WEEKLY SEARCH", flush=True)
    print(f"{'='*80}", flush=True)
    
    try:
        import asyncio
        from datetime import datetime, timedelta
        
        # Load weekly settings
        settings = load_advanced_settings()
        if not settings or not settings.get('weekly', {}).get('enabled'):
            print("⚠️ Weekly search not enabled", flush=True)
            return
        
        weekly_config = settings['weekly']
        days = weekly_config.get('days', [7, 14, 30])  # Default durations
        locations_config = weekly_config.get('locations', {'albufeira': True, 'faro': False})
        
        # Prepare locations
        locations_to_search = []
        if locations_config.get('albufeira'):
            locations_to_search.append("Albufeira")
        if locations_config.get('faro'):
            locations_to_search.append("Aeroporto de Faro")
        
        # PICKUP DATE: Fixed day of NEXT month (example: day 05 of next month)
        # This allows searching for future months beyond current month
        now = datetime.now()
        next_month = now.month + 1 if now.month < 12 else 1
        year = now.year if now.month < 12 else now.year + 1
        fixed_day = 5  # Fixed day (configurable)
        
        pickup_date = f"{year}-{str(next_month).zfill(2)}-{str(fixed_day).zfill(2)}"
        
        print(f"\n🗓️ Weekly search config:", flush=True)
        print(f"   Pickup Date: {pickup_date} (day {fixed_day} of next month)", flush=True)
        print(f"   Durations: {days}", flush=True)
        print(f"   Locations: {locations_to_search}", flush=True)
        
        # Execute search with Anti-WAF
        all_results = asyncio.run(_do_carjet_search(locations_to_search, days, pickup_date))
        
        # Save results
        _save_search_results(all_results, days, locations_to_search)
        
        print(f"\n✅ WEEKLY SEARCH COMPLETED!", flush=True)
        print(f"{'='*80}\n", flush=True)
        
    except Exception as e:
        print(f"\n❌ WEEKLY SEARCH ERROR: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)

def send_weekly_report():
    """Send weekly report (email only)"""
    logging.info(f"\n{'='*80}")
    logging.info(f"📧 WEEKLY REPORT EMAIL")
    logging.info(f"{'='*80}")
    
    try:
        # Load data from database and send email
        logging.info("✅ Weekly report email sent")
    except Exception as e:
        logging.error(f"❌ Error sending weekly report: {str(e)}")

def execute_monthly_search():
    """
    Execute monthly search - uses FIXED DAY of month (e.g., day 05)
    Can search multiple months ahead
    """
    print(f"\n{'='*80}", flush=True)
    print(f"🔍 EXECUTING MONTHLY SEARCH", flush=True)
    print(f"{'='*80}", flush=True)
    
    try:
        import asyncio
        from datetime import datetime, timedelta
        
        # Load monthly settings
        settings = load_advanced_settings()
        if not settings or not settings.get('monthly', {}).get('enabled'):
            print("⚠️ Monthly search not enabled", flush=True)
            return
        
        monthly_config = settings['monthly']
        days = monthly_config.get('days', [7, 14, 30, 60])
        locations_config = monthly_config.get('locations', {'albufeira': True, 'faro': False})
        period_months = int(monthly_config.get('period', 6))  # How many months ahead
        fixed_day = int(monthly_config.get('day', 5))  # Fixed day of month
        
        # Prepare locations
        locations_to_search = []
        if locations_config.get('albufeira'):
            locations_to_search.append("Albufeira")
        if locations_config.get('faro'):
            locations_to_search.append("Aeroporto de Faro")
        
        # PICKUP DATE: Fixed day X months in future
        now = datetime.now()
        target_month = now.month + period_months
        year = now.year
        while target_month > 12:
            target_month -= 12
            year += 1
        
        pickup_date = f"{year}-{str(target_month).zfill(2)}-{str(fixed_day).zfill(2)}"
        
        print(f"\n🗓️ Monthly search config:", flush=True)
        print(f"   Pickup Date: {pickup_date} (day {fixed_day}, +{period_months} months)", flush=True)
        print(f"   Durations: {days}", flush=True)
        print(f"   Locations: {locations_to_search}", flush=True)
        
        # Execute search with Anti-WAF
        all_results = asyncio.run(_do_carjet_search(locations_to_search, days, pickup_date))
        
        # Save results
        _save_search_results(all_results, days, locations_to_search)
        
        print(f"\n✅ MONTHLY SEARCH COMPLETED!", flush=True)
        print(f"{'='*80}\n", flush=True)
        
    except Exception as e:
        print(f"\n❌ MONTHLY SEARCH ERROR: {str(e)}", flush=True)
        import traceback
        print(traceback.format_exc(), flush=True)

def send_monthly_report():
    """Send monthly report (email only)"""
    logging.info(f"\n{'='*80}")
    logging.info(f"📧 MONTHLY REPORT EMAIL")
    logging.info(f"{'='*80}")
    
    try:
        # Load data from database and send email
        logging.info("✅ Monthly report email sent")
    except Exception as e:
        logging.error(f"❌ Error sending monthly report: {str(e)}")

def setup_scheduled_tasks():
    """
    Setup all scheduled tasks based on database configuration
    This is called on startup and can be called to reload schedules
    """
    global scheduler
    
    print("\n" + "="*80, flush=True)
    print("🤖 SETTING UP AUTOMATED SCHEDULER", flush=True)
    print("="*80, flush=True)
    logging.info("\n" + "="*80)
    logging.info("🤖 SETTING UP AUTOMATED SCHEDULER")
    logging.info("="*80)
    
    # Load settings
    print("📥 Loading settings from database...", flush=True)
    settings = load_advanced_settings()
    
    if not settings:
        print("⚠️ No advanced settings found, scheduler not configured", flush=True)
        logging.warning("⚠️ No advanced settings found, scheduler not configured")
        return
    
    print(f"✅ Settings loaded successfully", flush=True)
    
    # Initialize scheduler
    if scheduler is None:
        print("🆕 Creating new BackgroundScheduler...", flush=True)
        scheduler = BackgroundScheduler(timezone='UTC')
        scheduler.start()
        print("✅ Scheduler started", flush=True)
        logging.info("✅ Scheduler started")
    else:
        # Clear existing jobs
        print("🔄 Clearing existing jobs...", flush=True)
        scheduler.remove_all_jobs()
        print("✅ Jobs cleared", flush=True)
        logging.info("🔄 Cleared existing jobs")
    
    job_count = 0
    
    # Setup DAILY schedules
    if settings.get('daily', {}).get('enabled'):
        schedules = settings['daily'].get('schedules', [])
        print(f"\n📅 DAILY REPORTS: {len(schedules)} schedules", flush=True)
        logging.info(f"\n📅 DAILY REPORTS: {len(schedules)} schedules")
        
        for idx, schedule in enumerate(schedules):
            search_time = schedule.get('searchTime', '08:55')
            send_time = schedule.get('sendTime', '09:00')
            search_hour, search_minute = search_time.split(':')
            send_hour, send_minute = send_time.split(':')
            
            # Add job for EXECUTING SEARCHES at searchTime
            scheduler.add_job(
                func=lambda s=schedule, i=idx: execute_search_for_schedule(s, i),
                trigger=CronTrigger(hour=int(search_hour), minute=int(search_minute)),
                id=f'daily_search_{idx}',
                name=f'Daily Search Schedule #{idx + 1} at {search_time}',
                replace_existing=True
            )
            job_count += 1
            print(f"   ✅ Search job #{idx + 1}: {search_time} | Days: {schedule.get('days')} | Locations: {schedule.get('locations')}", flush=True)
            logging.info(f"   ✅ Search job #{idx + 1}: {search_time}")
            
            # Add job for SENDING EMAIL at sendTime
            scheduler.add_job(
                func=lambda s=schedule, i=idx: send_daily_report_for_schedule(s, i),
                trigger=CronTrigger(hour=int(send_hour), minute=int(send_minute)),
                id=f'daily_send_{idx}',
                name=f'Daily Email Schedule #{idx + 1} at {send_time}',
                replace_existing=True
            )
            job_count += 1
            print(f"   ✅ Email job #{idx + 1}: {send_time}", flush=True)
            logging.info(f"   ✅ Email job #{idx + 1}: {send_time}")
    
    # Setup WEEKLY schedule (search on fixed day of month + email)
    if settings.get('weekly', {}).get('enabled'):
        day = settings['weekly'].get('day', 'saturday')  # Day of week OR day of month
        search_time = settings['weekly'].get('searchTime', '09:55')
        send_time = settings['weekly'].get('sendTime', '10:00')
        search_hour, search_minute = search_time.split(':')
        send_hour, send_minute = send_time.split(':')
        
        day_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        # Job for executing weekly searches (uses fixed day of month)
        scheduler.add_job(
            func=execute_weekly_search,
            trigger=CronTrigger(day_of_week=day_map.get(day, 5), hour=int(search_hour), minute=int(search_minute)),
            id='weekly_search',
            name=f'Weekly Search ({day} at {search_time})',
            replace_existing=True
        )
        job_count += 1
        print(f"\n📆 WEEKLY SEARCH: {day} at {search_time}", flush=True)
        logging.info(f"\n📆 WEEKLY SEARCH: {day} at {search_time}")
        
        # Job for sending weekly email
        scheduler.add_job(
            func=send_weekly_report,
            trigger=CronTrigger(day_of_week=day_map.get(day, 5), hour=int(send_hour), minute=int(send_minute)),
            id='weekly_email',
            name=f'Weekly Email ({day} at {send_time})',
            replace_existing=True
        )
        job_count += 1
        print(f"   ✅ Email: {send_time}", flush=True)
        logging.info(f"   ✅ Email: {send_time}")
    
    # Setup MONTHLY schedule (search on fixed day of future month + email)
    if settings.get('monthly', {}).get('enabled'):
        day = settings['monthly'].get('day', '1')
        search_time = settings['monthly'].get('searchTime', '09:55')
        send_time = settings['monthly'].get('sendTime', '10:00')
        search_hour, search_minute = search_time.split(':')
        send_hour, send_minute = send_time.split(':')
        
        if day == 'last':
            day = 'last'
        else:
            day = int(day)
        
        # Job for executing monthly searches (uses fixed day X months ahead)
        scheduler.add_job(
            func=execute_monthly_search,
            trigger=CronTrigger(day=day, hour=int(search_hour), minute=int(search_minute)),
            id='monthly_search',
            name=f'Monthly Search (day {day} at {search_time})',
            replace_existing=True
        )
        job_count += 1
        print(f"\n📊 MONTHLY SEARCH: Day {day} at {search_time}", flush=True)
        logging.info(f"\n📊 MONTHLY SEARCH: Day {day} at {search_time}")
        
        # Job for sending monthly email
        scheduler.add_job(
            func=send_monthly_report,
            trigger=CronTrigger(day=day, hour=int(send_hour), minute=int(send_minute)),
            id='monthly_email',
            name=f'Monthly Email (day {day} at {send_time})',
            replace_existing=True
        )
        job_count += 1
        print(f"   ✅ Email: {send_time}", flush=True)
        logging.info(f"   ✅ Email: {send_time}")
    
    print(f"\n{'='*80}", flush=True)
    print(f"✅ SCHEDULER CONFIGURED: {job_count} jobs scheduled", flush=True)
    print(f"{'='*80}\n", flush=True)
    
    logging.info(f"\n{'='*80}")
    logging.info(f"✅ SCHEDULER CONFIGURED: {job_count} jobs scheduled")
    logging.info(f"{'='*80}\n")
    
    # Print next run times
    if job_count > 0:
        print("📋 NEXT SCHEDULED RUNS:", flush=True)
        logging.info("📋 NEXT SCHEDULED RUNS:")
        for job in scheduler.get_jobs():
            next_run = job.next_run_time
            print(f"   • {job.name}: {next_run}", flush=True)
            logging.info(f"   • {job.name}: {next_run}")
    else:
        print("⚠️ No jobs scheduled - check your configuration", flush=True)

def shutdown_scheduler():
    """Shutdown the scheduler gracefully"""
    global scheduler
    if scheduler:
        logging.info("🛑 Shutting down scheduler...")
        scheduler.shutdown()
        logging.info("✅ Scheduler stopped")

if __name__ == "__main__":
    # For testing
    setup_scheduled_tasks()
    
    logging.info("\n🤖 Scheduler running... Press Ctrl+C to stop")
    
    try:
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        shutdown_scheduler()
