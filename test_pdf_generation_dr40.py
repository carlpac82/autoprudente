#!/usr/bin/env python3
"""
Test PDF Generation for DR40/2025
"""
import sqlite3

def test_pdf_generation():
    print("="*80)
    print("TESTE DE GERAÇÃO DE PDF - DR40/2025")
    print("="*80)
    
    # 1. Buscar DR da BD
    conn = sqlite3.connect('rental_database.db')
    cursor = conn.execute("""
        SELECT * FROM damage_reports 
        WHERE dr_number = 'DR40/2025' 
        AND (is_deleted = 0 OR is_deleted IS NULL)
    """)
    row = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    
    if not row:
        print("❌ DR não encontrado!")
        conn.close()
        return
    
    report = dict(zip(columns, row))
    print(f"✅ DR encontrado: {report['dr_number']}")
    print(f"   Cliente: {report.get('client_name')}")
    print(f"   Veículo: {report.get('vehicle_plate')}")
    
    # 2. Mapear dados
    report_data = {
        'dr_number': report.get('dr_number', ''),
        'contractNumber': report.get('contract_number', ''),
        'date': report.get('date', ''),
        'inspection_date': report.get('date', ''),
        'clientName': report.get('client_name', ''),
        'clientEmail': report.get('client_email', ''),
        'clientPhone': report.get('client_phone', ''),
        'address': report.get('client_address', ''),
        'city': report.get('client_city', ''),
        'postalCode': report.get('client_postal_code', ''),
        'country': report.get('client_country', ''),
        'vehiclePlate': report.get('vehicle_plate', ''),
        'vehicleBrand': report.get('vehicle_brand', ''),
        'vehicleModel': report.get('vehicle_model', ''),
        'vehicleColor': report.get('vehicle_color', ''),
        'vehicleKm': report.get('vehicle_km', ''),
        'pickupDate': report.get('pickup_date', ''),
        'pickupTime': report.get('pickup_time', ''),
        'pickupLocation': report.get('pickup_location', ''),
        'returnDate': report.get('return_date', ''),
        'returnTime': report.get('return_time', ''),
        'returnLocation': report.get('return_location', ''),
        'fuel_level_pickup': report.get('fuel_pickup', ''),
        'fuel_level_return': report.get('fuel_return', ''),
        'total_repair_cost': report.get('total_cost', ''),
        'inspector_name': report.get('inspector_name', ''),
        'inspection_date': report.get('inspection_date', ''),
        'damage_diagram_data': report.get('damage_diagram_data', ''),
        'damageDiagramData': report.get('damage_diagram_data', '')
    }
    
    print(f"✅ Report data preparado: {len(report_data)} campos")
    
    # 3. Verificar template ativo
    cursor = conn.execute("""
        SELECT id, version, filename, num_pages 
        FROM damage_report_templates 
        WHERE is_active = 1 
        ORDER BY version DESC LIMIT 1
    """)
    template = cursor.fetchone()
    
    if not template:
        print("❌ Nenhum template ativo!")
        return
    
    print(f"✅ Template ativo: v{template[1]} - {template[2]} ({template[3]} páginas)")
    
    # 4. Verificar coordenadas
    cursor = conn.execute("SELECT COUNT(*) FROM damage_report_coordinates")
    coord_count = cursor.fetchone()[0]
    print(f"✅ Coordenadas mapeadas: {coord_count}")
    
    # 5. Tentar gerar PDF
    print("\n🔧 Tentando gerar PDF...")
    try:
        from main import _fill_template_pdf_with_data
        pdf_data = _fill_template_pdf_with_data(report_data)
        
        print(f"✅✅✅ PDF GERADO COM SUCESSO!")
        print(f"   Tamanho: {len(pdf_data)} bytes")
        
        # Salvar para testar
        with open('/tmp/dr40_test_generated.pdf', 'wb') as f:
            f.write(pdf_data)
        print(f"   Salvo em: /tmp/dr40_test_generated.pdf")
        
    except Exception as e:
        print(f"❌❌❌ ERRO NA GERAÇÃO:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensagem: {e}")
        import traceback
        print("\nStack trace completo:")
        traceback.print_exc()
    
    conn.close()

if __name__ == '__main__':
    test_pdf_generation()
