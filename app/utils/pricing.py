# app/utils/pricing.py

# District pricing map (approximate distance from center)
# Format: 'district_name': base_distance_km
DISTRICT_PRICING = {
    # Quận trung tâm (0-5km)
    'quận 1': 0,
    'quận 3': 2,
    'quận bình thạnh': 5,
    'quận phú nhuận': 5,
    'quận 10': 3,
    'quận 5': 3,
    'quận 6': 5,
    'quận 11': 5,
    'quận tân bình': 7,
    
    # Quận ngoại ô gần (5-15km)
    'quận gò vấp': 10,
    'quận 12': 12,
    'quận tân phú': 10,
    'quận bình tân': 12,
    'quận 7': 10,
    'quận 8': 8,
    'quận 4': 2,
    'quận 9': 12,
    'thủ đức': 12,
    
    # Huyện ngoại ô xa (15-30km)
    'nhà bè': 15,
    'hóc môn': 18,
    'bình chánh': 15,
    'củ chi': 30,
    'cần giờ': 40,
}

# Default distance if district not found
DEFAULT_DISTANCE = 10  # km

def extract_district(address):
    """
    Extract district name from address
    Example: "123 Nguyen Van A, Quan 1, TP HCM" -> "quận 1"
    """
    if not address:
        return None
    
    address_lower = address.lower()
    
    # Common district patterns
    district_patterns = [
        'quận 1', 'quận 2', 'quận 3', 'quận 4', 'quận 5',
        'quận 6', 'quận 7', 'quận 8', 'quận 9', 'quận 10',
        'quận 11', 'quận 12', 'quận bình thạnh', 'quận tân bình',
        'quận phú nhuận', 'quận gò vấp', 'quận tân phú',
        'quận bình tân', 'quận thủ đức', 'thủ đức',
        'nhà bè', 'hóc môn', 'bình chánh', 'củ chi', 'cần giờ'
    ]
    
    for district in district_patterns:
        if district in address_lower:
            return district
    
    return None

def calculate_distance_km(pickup_address, delivery_address):
    """
    Calculate estimated distance between two addresses
    Returns distance in km
    """
    pickup_district = extract_district(pickup_address)
    delivery_district = extract_district(delivery_address)
    
    # Get distance from center for each district
    pickup_km = DISTRICT_PRICING.get(pickup_district, DEFAULT_DISTANCE)
    delivery_km = DISTRICT_PRICING.get(delivery_district, DEFAULT_DISTANCE)
    
    # Estimate distance between two points
    # Simple formula: |pickup - delivery| + base_distance
    if pickup_district == delivery_district:
        # Same district: 2-5km
        distance = 3
    else:
        # Different districts: calculate based on distance from center
        distance = abs(delivery_km - pickup_km) + 3  # +3km base
    
    return max(2, distance)  # Minimum 2km

def calculate_delivery_price(pickup_address, delivery_address, weight_kg=1, service_type='hoa_toc'):
    """
    Calculate delivery price based on distance, weight, and service type
    
    Args:
        pickup_address (str): Pickup address
        delivery_address (str): Delivery address
        weight_kg (float): Weight in kg
        service_type (str): 'hoa_toc' or 'trong_ngay'
    
    Returns:
        dict: {
            'base_fare': int,
            'distance_fee': int,
            'weight_fee': int,
            'service_fee': int,
            'total': int,
            'distance_km': float
        }
    """
    
    # Constants
    BASE_FARE = 15000  # 15,000đ for first 2km
    PRICE_PER_KM = 5000  # 5,000đ per km after 2km
    FREE_WEIGHT_KG = 5  # Free for first 5kg
    PRICE_PER_EXTRA_KG = 2000  # 2,000đ per kg after 5kg
    
    # Calculate distance
    distance_km = calculate_distance_km(pickup_address, delivery_address)
    
    # Calculate distance fee
    if distance_km <= 2:
        distance_fee = BASE_FARE
    else:
        distance_fee = BASE_FARE + (distance_km - 2) * PRICE_PER_KM
    
    # Calculate weight fee
    if weight_kg <= FREE_WEIGHT_KG:
        weight_fee = 0
    else:
        weight_fee = (weight_kg - FREE_WEIGHT_KG) * PRICE_PER_EXTRA_KG
    
    # Calculate service fee multiplier
    if service_type == 'hoa_toc':
        service_multiplier = 1.5  # +50% for express
        service_fee = int((distance_fee + weight_fee) * 0.5)
    else:
        service_multiplier = 1.0  # Standard
        service_fee = 0
    
    # Calculate total
    subtotal = distance_fee + weight_fee
    total = int(subtotal * service_multiplier)
    
    return {
        'base_fare': BASE_FARE,
        'distance_km': round(distance_km, 1),
        'distance_fee': distance_fee,
        'weight_fee': weight_fee,
        'service_fee': service_fee,
        'service_multiplier': service_multiplier,
        'subtotal': subtotal,
        'total': total
    }

def format_price(price):
    """Format price as Vietnamese currency string"""
    return f"{price:,.0f}đ"