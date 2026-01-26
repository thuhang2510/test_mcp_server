#!/usr/bin/env python3
"""
Test script for update_person functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_server import update_person, get_contact_info, PEOPLE

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
    
    # Test 8: Check updated values
    print("Test 8: Kiểm tra thông tin liên lạc sau khi cập nhật")
    hang_contact = get_contact_info("Hang")
    minh_contact = get_contact_info("Minh")
    print(f"Hang contact info: {hang_contact}")
    print(f"Minh contact info: {minh_contact}")
    print()
    
    # Test 9: Update hobby and quote
    print("Test 9: Cập nhật sở thích và câu nói của Hang")
    result1 = update_person("Hang", "hobby", "Vẽ tranh và chụp ảnh nghệ thuật")
    result2 = update_person("Hang", "quote", "Cuộc sống đẹp nhất khi ta sống với đam mê")
    print(f"Update hobby: {result1}")
    print(f"Update quote: {result2}")
    print()
    
    print("=== Kết thúc test ===")
    
    # Reset data to original state for consistency
    print("\nReset dữ liệu về trạng thái ban đầu...")
    PEOPLE["Hang"]["email"] = "hang.dam@email.com"
    PEOPLE["Hang"]["address"] = "123 Đường Lê Lợi, Quận 1, TP.HCM"  
    PEOPLE["Hang"]["hobby"] = "Nhiếp ảnh đường phố"
    PEOPLE["Hang"]["quote"] = "Cứ đi rồi sẽ đến."
    PEOPLE["Minh"]["phone"] = "0987654321"
    print("Đã reset dữ liệu!")

if __name__ == "__main__":
    test_update_person()