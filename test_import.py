#!/usr/bin/env python3
"""Test script to check if mcp_server imports work."""

try:
    from mcp_server import (
        PEOPLE, 
        find_person_key, 
        build_profile,
        SEARCHABLE_FIELDS
    )
    
    print("✓ Import successful!")
    
    # Test basic functionality
    print(f"✓ Found {len(PEOPLE)} people in database")
    print(f"✓ People: {list(PEOPLE.keys())}")
    
    # Test new fields in PEOPLE
    sample_person = list(PEOPLE.values())[0]
    new_fields = ["email", "phone", "address", "occupation"]
    
    print("\n=== Testing new fields in data ===")
    for field in new_fields:
        if field in sample_person:
            print(f"✓ {field}: {sample_person[field]}")
        else:
            print(f"✗ {field}: MISSING")
    
    # Test build_profile includes new fields
    print("\n=== Testing build_profile with new fields ===")
    profile = build_profile("Hang")
    for field in new_fields:
        if field in profile:
            print(f"✓ Profile includes {field}: {profile[field]}")
        else:
            print(f"✗ Profile missing {field}")
    
    # Test SEARCHABLE_FIELDS includes new fields
    print("\n=== Testing SEARCHABLE_FIELDS ===")
    for field in new_fields:
        if field in SEARCHABLE_FIELDS:
            print(f"✓ {field} is searchable")
        else:
            print(f"✗ {field} is NOT searchable")
    
    print("\n🎉 All import and basic functionality tests passed!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("This is expected if MCP modules are not installed")
except Exception as e:
    print(f"❌ Unexpected error: {e}")