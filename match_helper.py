def match_vehicle_group_by_characteristics(category: str, car_name: str, transmission: str, vehicle_groups: dict, fallback_func) -> str:
    """Match inteligente baseado nas características parametrizadas no Admin Vehicles"""
    if not vehicle_groups:
        return fallback_func(category, car_name)
    
    category_lower = (category or '').lower()
    transmission_lower = (transmission or '').lower()
    car_lower = (car_name or '').lower()
    
    is_automatic = 'auto' in transmission_lower or 'automático' in transmission_lower
    is_manual = 'manual' in transmission_lower
    
    best_match = None
    best_score = 0
    
    for code, group_info in vehicle_groups.items():
        score = 0
        
        # Match categoria (peso 3)
        group_cat = (group_info.get('category') or '').lower()
        if group_cat and group_cat in category_lower:
            score += 3
        elif category_lower and category_lower in group_cat:
            score += 2
        
        # Match transmissão (peso 2)
        group_trans = (group_info.get('transmission') or '').lower()
        if is_automatic and 'auto' in group_trans:
            score += 2
        elif is_manual and 'manual' in group_trans:
            score += 2
        
        # Match brand/model (peso 1)
        brand = (group_info.get('brand') or '').lower()
        model = (group_info.get('model') or '').lower()
        if brand and brand in car_lower:
            score += 1
        if model and model in car_lower:
            score += 1
        
        if score > best_score:
            best_score = score
            best_match = code
    
    # Se encontrou match razoável (score >= 2), usa
    if best_match and best_score >= 2:
        return best_match
    
    # Fallback
    return fallback_func(category, car_name)
