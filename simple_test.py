#!/usr/bin/env python3
"""Simple test for add_person logic without MCP dependencies"""

import re
from typing import Optional

# Mock PEOPLE data
PEOPLE = {
    "Hang": {
        "age": 18,
        "birthday": "25/10",
        "work_experience_years": 0,
        "email": "hang.dam@email.com",
        "phone": "0123456789",
        "address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "occupation": "Sinh viên",
    },
    "Minh": {
        "age": 22,
        "birthday": "09/04",
        "work_experience_years": 2,
        "email": "minh.tran@company.vn",
        "phone": "0987654321",
        "address": "456 Đường Nguyễn Huệ, Quận 3, TP.HCM",
        "occupation": "Kỹ sư phần mềm",
    },
}

def normalize_name(name: str) -> str:
    return name.strip().lower()

def add_person(
    name: str,
    age: int,
    birthday: str,
    email: str,
    phone: str,
    address: Optional[str] = None,
    occupation: Optional[str] = None,
    work_experience_years: Optional[int] = None,
    father: Optional[str] = None,
    mother: Optional[str] = None,
    siblings: Optional[str] = None,
    hobby: Optional[str] = None,
    quote: Optional[str] = None,
    favorite_color: Optional[str] = None,
) -> dict:
    """Thêm người mới vào hệ thống."""
    # Validate tên không được trống
    if not name or not name.strip():
        return {"success": False, "error": "Tên không được để trống"}
    
    name = name.strip()
    
    # Kiểm tra người đã tồn tại chưa
    normalized_name = normalize_name(name)
    for existing_name in PEOPLE.keys():
        if normalize_name(existing_name) == normalized_name:
            return {
                "success": False, 
                "error": f"Người có tên '{existing_name}' đã tồn tại trong hệ thống"
            }
    
    # Validate birthday format
    birthday_pattern = r'^\d{1,2}/\d{1,2}$'
    if not re.match(birthday_pattern, birthday):
        return {
            "success": False, 
            "error": "Ngày sinh phải theo định dạng dd/mm (ví dụ: 25/10)"
        }
    
    # Validate age
    if age < 0 or age > 150:
        return {
            "success": False, 
            "error": "Tuổi phải từ 0 đến 150"
        }
    
    # Validate email format cơ bản
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not re.match(email_pattern, email):
        return {
            "success": False, 
            "error": "Email không đúng định dạng"
        }
    
    # Validate phone (chỉ số và có độ dài hợp lý)
    phone_clean = re.sub(r'[^\d]', '', phone)
    if len(phone_clean) < 8 or len(phone_clean) > 15:
        return {
            "success": False, 
            "error": "Số điện thoại phải có từ 8-15 chữ số"
        }
    
    # Tạo profile mới
    new_profile = {
        "age": age,
        "birthday": birthday,
        "work_experience_years": work_experience_years if work_experience_years is not None else 0,
        "email": email,
        "phone": phone,
    }
    
    # Thêm các thông tin tùy chọn
    if address:
        new_profile["address"] = address
    if occupation:
        new_profile["occupation"] = occupation
    
    # Thêm thông tin gia đình nếu có
    family_info = {}
    if father:
        family_info["father"] = father
    if mother:
        family_info["mother"] = mother
    if siblings:
        family_info["siblings"] = siblings
    
    if family_info:
        new_profile["family"] = family_info
    
    # Thêm thông tin cá nhân khác
    if hobby:
        new_profile["hobby"] = hobby
    if quote:
        new_profile["quote"] = quote
    if favorite_color:
        new_profile["favorite_color"] = favorite_color
    
    # Thêm vào hệ thống
    PEOPLE[name] = new_profile
    
    return {
        "success": True,
        "message": f"Đã thêm người mới '{name}' thành công vào hệ thống",
        "person_count": len(PEOPLE),
        "profile": new_profile
    }

def test_cases():
    print("=== Test tính năng add_person ===")
    print(f"Danh sách ban đầu: {list(PEOPLE.keys())}")
    print()
    
    # Test 1: Thêm thành công
    print("Test 1: Thêm người mới thành công")
    result = add_person(
        name="Lan Nguyen",
        age=25,
        birthday="15/8",
        email="lan.nguyen@example.com",
        phone="0901234567",
        address="789 Đường ABC, Quận 10, TP.HCM",
        occupation="Thiết kế đồ họa",
        work_experience_years=3,
        father="Nguyen VT",
        mother="Tran TH",
        siblings="Nguyen DL",
        hobby="Vẽ tranh",
        quote="Sáng tạo không có giới hạn",
        favorite_color="Hồng"
    )
    print(f"Kết quả: {result['success']} - {result.get('message', result.get('error'))}")
    print()
    
    # Test 2: Tên trùng lặp
    print("Test 2: Tên trùng lặp")
    result = add_person(
        name="Hang",
        age=20,
        birthday="1/1",
        email="test@example.com",
        phone="0123456789"
    )
    print(f"Kết quả: {result['success']} - {result.get('error')}")
    print()
    
    # Test 3: Email không hợp lệ
    print("Test 3: Email không hợp lệ") 
    result = add_person(
        name="Test Person",
        age=25,
        birthday="15/8",
        email="invalid-email",
        phone="0901234567"
    )
    print(f"Kết quả: {result['success']} - {result.get('error')}")
    print()
    
    # Test 4: Format ngày sinh sai
    print("Test 4: Format ngày sinh sai")
    result = add_person(
        name="Test Person 2",
        age=25,
        birthday="2023-08-15",
        email="test2@example.com",
        phone="0901234567"
    )
    print(f"Kết quả: {result['success']} - {result.get('error')}")
    print()
    
    # Test 5: Thêm với thông tin tối thiểu
    print("Test 5: Thông tin tối thiểu")
    result = add_person(
        name="An Vo",
        age=30,
        birthday="22/12",
        email="an.vo@company.com",
        phone="0912345678"
    )
    print(f"Kết quả: {result['success']} - {result.get('message', result.get('error'))}")
    print()
    
    print(f"Danh sách cuối: {list(PEOPLE.keys())}")
    print(f"Tổng số người: {len(PEOPLE)}")

if __name__ == "__main__":
    test_cases()