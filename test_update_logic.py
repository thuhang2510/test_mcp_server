#!/usr/bin/env python3
"""
Test script for update_person logic only (without MCP dependencies)
"""

# Test data (copy from mcp_server.py)
PEOPLE = {
    "Hang": {
        "age": 18,
        "birthday": "25/10",
        "work_experience_years": 0,
        "email": "hang.dam@email.com",
        "phone": "0123456789",
        "address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "occupation": "Sinh viên",
        "family": {
            "father": "Dam VT",
            "mother": "La TT",
            "sister": "Dam HG",
        },
        "hobby": "Nhiếp ảnh đường phố",
        "quote": "Cứ đi rồi sẽ đến.",
        "favorite_color": "Tím",
    },
    "Minh": {
        "age": 22,
        "birthday": "09/04", 
        "work_experience_years": 2,
        "email": "minh.tran@company.vn",
        "phone": "0987654321",
        "address": "456 Đường Nguyễn Huệ, Quận 3, TP.HCM",
        "occupation": "Kỹ sư phần mềm",
        "family": {
            "father": "Tran TL",
            "mother": "Nguyen MT",
            "brother": "Tran QH",
        },
        "hobby": "Chạy bộ buổi sáng",
        "quote": "Bền bỉ tạo nên khác biệt.",
        "favorite_color": "Xanh dương",
    },
}

def find_person_key(name: str):
    """Find person key (simplified version)"""
    needle = name.strip().lower()
    for key in PEOPLE:
        if key.lower() in needle:
            return key
    return None

# Helper functions for update_person
UPDATABLE_FIELDS = {
    "email": str,
    "phone": str, 
    "address": str,
    "occupation": str,
    "hobby": str,
    "quote": str,
    "favorite_color": str,
}

def validate_field_and_value(field: str, value: str):
    """Validate if field is updatable and value is valid."""
    field_lower = field.strip().lower()
    
    # Normalize field names
    field_aliases = {
        "email": "email",
        "mail": "email",
        "e-mail": "email",
        "phone": "phone",
        "telephone": "phone",
        "tel": "phone",
        "sdt": "phone",
        "so_dien_thoai": "phone",
        "số điện thoại": "phone",
        "address": "address",
        "dia_chi": "address",
        "địa chỉ": "address",
        "occupation": "occupation",
        "job": "occupation",
        "work": "occupation",
        "nghe_nghiep": "occupation",
        "nghề nghiệp": "occupation",
        "hobby": "hobby",
        "so_thich": "hobby",
        "sở thích": "hobby",
        "quote": "quote",
        "cau_noi": "quote",
        "câu nói": "quote",
        "favorite_color": "favorite_color",
        "mau_yeu_thich": "favorite_color",
        "màu yêu thích": "favorite_color",
        "color": "favorite_color",
    }
    
    # Get canonical field name
    canonical_field = field_aliases.get(field_lower)
    if not canonical_field:
        return None, f"Field '{field}' không thể cập nhật. Các field hỗ trợ: {', '.join(UPDATABLE_FIELDS.keys())}"
    
    # Validate value
    if not value or not value.strip():
        return None, f"Giá trị cho field '{field}' không thể rỗng"
    
    # Basic validation for specific fields
    if canonical_field == "email":
        # Simple email validation
        if "@" not in value or "." not in value.split("@")[-1]:
            return None, f"Email '{value}' không hợp lệ"
    elif canonical_field == "phone":
        # Remove spaces and check if it contains digits
        phone_clean = value.replace(" ", "").replace("-", "")
        if not any(c.isdigit() for c in phone_clean):
            return None, f"Số điện thoại '{value}' không hợp lệ"
    
    return canonical_field, None

def update_person(name: str, field: str, new_value: str):
    """Test version of update_person function"""
    
    # Find person
    key = find_person_key(name)
    if not key:
        return {
            "success": False,
            "message": f"Không tìm thấy người có tên '{name}' trong hệ thống",
            "available_people": list(PEOPLE.keys())
        }
    
    # Validate field and value
    canonical_field, error = validate_field_and_value(field, new_value)
    if error:
        return {
            "success": False,
            "message": error,
            "person": key,
            "field_requested": field
        }
    
    # Get old value for comparison
    old_value = PEOPLE[key].get(canonical_field, "")
    
    # Update the value
    PEOPLE[key][canonical_field] = new_value.strip()
    
    return {
        "success": True,
        "message": f"Đã cập nhật {canonical_field} của {key}",
        "person": key,
        "field": canonical_field,
        "old_value": old_value,
        "new_value": new_value.strip()
    }

def test_update_person():
    """Test the update_person function with various scenarios"""
    
    print("=== Testing update_person functionality ===\n")
    
    # Test 1: Update email
    print("Test 1: Cập nhật email của Hang")
    result = update_person("Hang", "email", "hang.updated@gmail.com")
    print(f"Result: {result}")
    print()
    
    # Test 2: Update phone with Vietnamese field name
    print("Test 2: Cập nhật số điện thoại của Minh")
    result = update_person("Minh", "số điện thoại", "0901234567")
    print(f"Result: {result}")
    print()
    
    # Test 3: Update address
    print("Test 3: Cập nhật địa chỉ của Hang")
    result = update_person("Hang", "address", "789 Đường Võ Văn Tần, Quận 3, TP.HCM")
    print(f"Result: {result}")
    print()
    
    # Test 4: Invalid person name
    print("Test 4: Thử cập nhật người không tồn tại")
    result = update_person("Unknown", "email", "test@email.com")
    print(f"Result: {result}")
    print()
    
    # Test 5: Invalid field
    print("Test 5: Thử cập nhật field không hỗ trợ")
    result = update_person("Hang", "age", "19")
    print(f"Result: {result}")
    print()
    
    # Test 6: Invalid email
    print("Test 6: Thử cập nhật email không hợp lệ")
    result = update_person("Hang", "email", "invalid-email")
    print(f"Result: {result}")
    print()
    
    # Test 7: Empty value
    print("Test 7: Thử cập nhật với giá trị rỗng")
    result = update_person("Hang", "phone", "")
    print(f"Result: {result}")
    print()
    
    # Test 8: Update hobby and quote
    print("Test 8: Cập nhật sở thích và câu nói của Hang")
    result1 = update_person("Hang", "hobby", "Vẽ tranh và chụp ảnh nghệ thuật")
    result2 = update_person("Hang", "quote", "Cuộc sống đẹp nhất khi ta sống với đam mê")
    print(f"Update hobby: {result1}")
    print(f"Update quote: {result2}")
    print()
    
    # Test 9: Check final data
    print("Test 9: Kiểm tra dữ liệu cuối cùng")
    print(f"Hang data: {PEOPLE['Hang']}")
    print(f"Minh data: {PEOPLE['Minh']}")
    print()
    
    print("=== Kết thúc test ===")

if __name__ == "__main__":
    test_update_person()