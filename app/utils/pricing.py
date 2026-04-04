# app/utils/pricing.py


DISTRICT_PRICING = {
    # ========== HÀ NỘI ==========
    # Quận trung tâm Hà Nội (0-5km từ Hồ Gươm)
    'hoàn kiếm': 0,
    'quận hoàn kiếm': 0,
    'ba đình': 2,
    'quận ba đình': 2,
    'đống đa': 3,
    'quận đống đa': 3,
    'hai bà trưng': 3,
    'quận hai bà trưng': 3,
    'cầu giấy': 5,
    'quận cầu giấy': 5,
    'thanh xuân': 5,
    'quận thanh xuân': 5,
    
    # Quận ngoại ô Hà Nội (5-15km)
    'hoàng mai': 7,
    'quận hoàng mai': 7,
    'long biên': 7,
    'quận long biên': 7,
    'nam từ liêm': 10,
    'quận nam từ liêm': 10,
    'bắc từ liêm': 10,
    'quận bắc từ liêm': 10,
    'tây hồ': 5,
    'quận tây hồ': 5,
    'Hà Đông': 12,
    'quận hà đông': 12,
    
    # Huyện ngoại ô Hà Nội (15-30km)
    'gia lâm': 15,
    'huyện gia lâm': 15,
    'đông anh': 18,
    'huyện đông anh': 18,
    'thanh trì': 12,
    'huyện thanh trì': 12,
    'từ liêm': 10,
    'hoài đức': 20,
    'huyện hoài đức': 20,
    'thường tín': 20,
    'huyện thường tín': 20,
    'thanh oai': 25,
    'huyện thanh oai': 25,
    'phú xuyên': 30,
    'huyện phú xuyên': 30,
    'mê linh': 35,
    'huyện mê linh': 35,
    'sóc sơn': 35,
    'huyện sóc sơn': 35,
    'ba vì': 50,
    'huyện ba vì': 50,
    'thạch thất': 40,
    'huyện thạch thất': 40,
    'quốc oai': 35,
    'huyện quốc oai': 35,
    'chương mỹ': 30,
    'huyện chương mỹ': 30,
    'ứng hòa': 35,
    'huyện ứng hòa': 35,
    'mỹ đức': 40,
    'huyện mỹ đức': 40,
    'đan phượng': 25,
    'huyện đan phượng': 25,
    
    # ========== TP. HỒ CHÍ MINH ==========
    # Quận trung tâm (0-5km từ Bến Thành)
    'quận 1': 0,
    'quận 3': 2,
    'quận 4': 2,
    'quận 5': 3,
    'quận 10': 3,
    'bình thạnh': 5,
    'quận bình thạnh': 5,
    'phú nhuận': 5,
    'quận phú nhuận': 5,
    'tân bình': 7,
    'quận tân bình': 7,
    'quận 6': 5,
    'quận 11': 5,
    
    # Quận ngoại ô gần (5-15km)
    'gò vấp': 10,
    'quận gò vấp': 10,
    'tân phú': 10,
    'quận tân phú': 10,
    'bình tân': 12,
    'quận bình tân': 12,
    'quận 7': 10,
    'quận 8': 8,
    'quận 12': 12,
    'quận 9': 12,
    'thủ đức': 12,
    'thành phố thủ đức': 12,
    
    # Huyện ngoại ô xa (15-50km)
    'nhà bè': 15,
    'huyện nhà bè': 15,
    'hóc môn': 18,
    'huyện hóc môn': 18,
    'bình chánh': 15,
    'huyện bình chánh': 15,
    'củ chi': 30,
    'huyện củ chi': 30,
    'cần giờ': 40,
    'huyện cần giờ': 40,
    
    # ========== CÁC TỈNH THÀNH KHÁC ==========
    # Đà Nẵng
    'đà nẵng': 0,
    'thành phố đà nẵng': 0,
    'hải châu': 0,
    'quận hải châu': 0,
    'thanh khê': 3,
    'quận thanh khê': 3,
    'sơn trà': 5,
    'quận sơn trà': 5,
    'ngũ hành sơn': 7,
    'quận ngũ hành sơn': 7,
    'liêu chiểu': 5,
    'quận liên chiểu': 5,
    'cẩm lệ': 7,
    'quận cẩm lệ': 7,
    'hòa vang': 15,
    'huyện hòa vang': 15,
    
    # Hải Phòng
    'hải phòng': 0,
    'thành phố hải phòng': 0,
    'hồng bàng': 0,
    'quận hồng bàng': 0,
    'ngô quyền': 2,
    'quận ngô quyền': 2,
    'lê chân': 3,
    'quận lê chân': 3,
    'hải an': 5,
    'quận hải an': 5,
    'kiến an': 7,
    'quận kiến an': 7,
    'đồ sơn': 15,
    'quận đồ sơn': 15,
    'dương kinh': 7,
    'quận dương kinh': 7,
    
    # Cần Thơ
    'cần thơ': 0,
    'thành phố cần thơ': 0,
    'ninh kiều': 0,
    'quận ninh kiều': 0,
    'bình thủy': 5,
    'quận bình thủy': 5,
    'cái răng': 7,
    'quận cái răng': 7,
    'ô môn': 12,
    'quận ô môn': 12,
    'thốt nốt': 15,
    'quận thốt nốt': 15,
    
    # ========== CÁC TỈNH ==========
    # Miền Bắc
    'hải dương': 55,
    'tỉnh hải dương': 55,
    'hưng yên': 50,
    'tỉnh hưng yên': 50,
    'bắc ninh': 30,
    'tỉnh bắc ninh': 30,
    'vĩnh phúc': 45,
    'tỉnh vĩnh phúc': 45,
    'phú thọ': 80,
    'tỉnh phú thọ': 80,
    'thái nguyên': 70,
    'tỉnh thái nguyên': 70,
    'bắc giang': 50,
    'tỉnh bắc giang': 50,
    'quảng ninh': 150,
    'tỉnh quảng ninh': 150,
    'hạ long': 150,
    'thành phố hạ long': 150,
    'hà nam': 60,
    'tỉnh hà nam': 60,
    'nam định': 85,
    'tỉnh nam định': 85,
    'thái bình': 90,
    'tỉnh thái bình': 90,
    'ninh bình': 100,
    'tỉnh ninh bình': 100,
    'hòa bình': 75,
    'tỉnh hòa bình': 75,
    'sơn la': 250,
    'tỉnh sơn la': 250,
    'điện biên': 450,
    'tỉnh điện biên': 450,
    'lai châu': 400,
    'tỉnh lai châu': 400,
    'lào cai': 300,
    'tỉnh lào cai': 300,
    'yên bái': 180,
    'tỉnh yên bái': 180,
    'tuyên quang': 150,
    'tỉnh tuyên quang': 150,
    'hà giang': 300,
    'tỉnh hà giang': 300,
    'cao bằng': 270,
    'tỉnh cao bằng': 270,
    'bắc kạn': 160,
    'tỉnh bắc kạn': 160,
    'lạng sơn': 150,
    'tỉnh lạng sơn': 150,
    
    # Miền Trung
    'thanh hóa': 150,
    'tỉnh thanh hóa': 150,
    'nghệ an': 290,
    'tỉnh nghệ an': 290,
    'vinh': 290,
    'thành phố vinh': 290,
    'hà tĩnh': 340,
    'tỉnh hà tĩnh': 340,
    'quảng bình': 450,
    'tỉnh quảng bình': 450,
    'đồng hới': 450,
    'thành phố đồng hới': 450,
    'quảng trị': 580,
    'tỉnh quảng trị': 580,
    'thừa thiên huế': 680,
    'tỉnh thừa thiên huế': 680,
    'huế': 680,
    'thành phố huế': 680,
    
    # Miền Nam
    'bà rịa vũng tàu': 100,
    'tỉnh bà rịa vũng tàu': 100,
    'vũng tàu': 100,
    'thành phố vũng tàu': 100,
    'đồng nai': 30,
    'tỉnh đồng nai': 30,
    'biên hòa': 30,
    'thành phố biên hòa': 30,
    'bình dương': 25,
    'tỉnh bình dương': 25,
    'thủ dầu một': 25,
    'thành phố thủ dầu một': 25,
    'long an': 40,
    'tỉnh long an': 40,
    'tân an': 40,
    'thành phố tân an': 40,
    'tiền giang': 70,
    'tỉnh tiền giang': 70,
    'mỹ tho': 70,
    'thành phố mỹ tho': 70,
    'bến tre': 85,
    'tỉnh bến tre': 85,
    'trà vinh': 130,
    'tỉnh trà vinh': 130,
    'vĩnh long': 135,
    'tỉnh vĩnh long': 135,
    'đồng tháp': 140,
    'tỉnh đồng tháp': 140,
    'cao lãnh': 140,
    'thành phố cao lãnh': 140,
    'an giang': 190,
    'tỉnh an giang': 190,
    'long xuyên': 190,
    'thành phố long xuyên': 190,
    'kiên giang': 250,
    'tỉnh kiên giang': 250,
    'rạch giá': 250,
    'thành phố rạch giá': 250,
    'hậu giang': 100,
    'tỉnh hậu giang': 100,
    'vị thanh': 100,
    'thành phố vị thanh': 100,
    'sóc trăng': 230,
    'tỉnh sóc trăng': 230,
    'bạc liêu': 280,
    'tỉnh bạc liêu': 280,
    'cà mau': 350,
    'tỉnh cà mau': 350,
    
    # Tây Nguyên
    'đắk lắk': 350,
    'tỉnh đắk lắk': 350,
    'buôn ma thuột': 350,
    'thành phố buôn ma thuột': 350,
    'đắk nông': 300,
    'tỉnh đắk nông': 300,
    'gia lai': 450,
    'tỉnh gia lai': 450,
    'pleiku': 450,
    'thành phố pleiku': 450,
    'kon tum': 550,
    'tỉnh kon tum': 550,
    'lâm đồng': 300,
    'tỉnh lâm đồng': 300,
    'đà lạt': 300,
    'thành phố đà lạt': 300,
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