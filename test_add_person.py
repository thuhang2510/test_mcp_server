#!/usr/bin/env python3
"""Test script for the new add_person tool"""

from mcp_server import mcp, PEOPLE

def test_add_person_success():
    """Test thêm người mới thành công"""
    print("=== Test thêm người mới thành công ===")
    
    result = mcp.get_handler("add_person")(
        name="Lan Nguyen",
        age=25,
        birthday="15/08",
        email="lan.nguyen@example.com", 
        phone="0901234567",
        address="789 Đường Võ Văn Tần, Quận 10, TP.HCM",
        occupation="Thiết kế đồ họa",
        work_experience_years=3,
        father="Nguyen VT",
        mother="Tran TH", 
        siblings="Nguyen DL",
        hobby="Vẽ tranh",
        quote="Sáng tạo không có giới hạn",
        favorite_color="Hồng"
    )
    
    print(f"Kết quả: {result}")
    print(f"Số người trong hệ thống: {len(PEOPLE)}")
    print()

def test_add_person_duplicate():
    """Test thêm người trùng tên"""
    print("=== Test thêm người trùng tên ===")
    
    result = mcp.get_handler("add_person")(
        name="Hang", # Tên đã tồn tại
        age=20,
        birthday="01/01",
        email="test@example.com",
        phone="0123456789"
    )
    
    print(f"Kết quả: {result}")
    print()

def test_add_person_invalid_email():
    """Test thêm với email không hợp lệ"""
    print("=== Test email không hợp lệ ===")
    
    result = mcp.get_handler("add_person")(
        name="Test Person",
        age=25,
        birthday="15/08", 
        email="invalid-email", # Email không hợp lệ
        phone="0901234567"
    )
    
    print(f"Kết quả: {result}")
    print()

def test_add_person_invalid_birthday():
    """Test thêm với ngày sinh không hợp lệ"""
    print("=== Test ngày sinh không hợp lệ ===")
    
    result = mcp.get_handler("add_person")(
        name="Test Person 2",
        age=25,
        birthday="2023-08-15", # Format sai
        email="test2@example.com",
        phone="0901234567"
    )
    
    print(f"Kết quả: {result}")
    print()

def test_add_person_minimal():
    """Test thêm với thông tin tối thiểu"""
    print("=== Test với thông tin tối thiểu ===")
    
    result = mcp.get_handler("add_person")(
        name="An Vo",
        age=30,
        birthday="22/12",
        email="an.vo@company.com",
        phone="0912345678"
    )
    
    print(f"Kết quả: {result}")
    print()

if __name__ == "__main__":
    print("Danh sách người ban đầu:", list(PEOPLE.keys()))
    print()
    
    # Chạy các test
    test_add_person_success()
    test_add_person_duplicate()
    test_add_person_invalid_email()
    test_add_person_invalid_birthday() 
    test_add_person_minimal()
    
    print("Danh sách người sau test:", list(PEOPLE.keys()))
    print(f"Tổng số người: {len(PEOPLE)}")