#!/usr/bin/env python3

import requests
import json

# Test the corrected auth/register endpoint
url = "http://127.0.0.1:8000/auth/register"

test_data = {
    "phone": "+7900555555",
    "name": "Новый Тест",
    "password": "testpass123"
}

print("Testing NEW auth/register endpoint...")
print(f"URL: {url}")
print(f"Data: {test_data}")

try:
    response = requests.post(url, json=test_data)
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("✅ NEW endpoint works!")
    else:
        print("❌ NEW endpoint failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Also test old endpoint to confirm it doesn't work
print("\n" + "="*50)
print("Testing OLD /register endpoint (should fail)...")

try:
    old_url = "http://127.0.0.1:8000/register"
    response = requests.post(old_url, json=test_data)
    print(f"OLD endpoint Status: {response.status_code}")
    if response.status_code == 404:
        print("✅ OLD endpoint correctly returns 404")
    else:
        print("❌ OLD endpoint still works (unexpected)")
except Exception as e:
    print(f"OLD endpoint error: {e}")

# Test assistant registration
assistant_data = {
    "name": "Анна Тестовая",
    "phone": "+7900555555", 
    "email": "anna.test@example.com",
    "password": "testpass123",
    "specialization": "personal_only",
    "telegram_username": "@anna_test"
}

# Test assistant login  
login_data = {
    "phone": "+7900555555",
    "password": "testpass123"
} 