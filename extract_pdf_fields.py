#!/usr/bin/env python3
"""
Extrai campos do Rental Agreement e mapeia para o Damage Report
"""
import PyPDF2
import re

def extract_ra_fields(pdf_path):
    """Extrai campos do Rental Agreement"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    # Extrair campos usando regex
    fields = {}
    
    # Número do contrato (primeira linha)
    contract_match = re.search(r'^(\d+)', text)
    if contract_match:
        fields['contract_number'] = contract_match.group(1)
    
    # Matrícula
    plate_match = re.search(r'([A-Z]{2}\s*-\s*\d{2}\s*-\s*[A-Z]{2})', text)
    if plate_match:
        fields['vehicle_plate'] = plate_match.group(1).replace(' ', '')
    
    # Nome do cliente (após o número do contrato)
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
    
    # Local (AUTO PRUDENTE aparece 2x)
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
    
    return fields

def print_fields(fields):
    """Imprime campos extraídos"""
    print("\n" + "="*80)
    print("CAMPOS EXTRAÍDOS DO RENTAL AGREEMENT")
    print("="*80)
    for key, value in sorted(fields.items()):
        print(f"{key:20s}: {value}")
    print("="*80)

if __name__ == "__main__":
    # Extrair do RA exemplo
    print("📄 Extraindo campos do Rental Agreement...")
    fields = extract_ra_fields('report_23653.pdf')
    print_fields(fields)
    
    # Salvar em JSON para usar na API
    import json
    with open('ra_fields_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(fields, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Campos salvos em ra_fields_mapping.json")
