import requests
import json

# Test registration API
url = "http://127.0.0.1:8000/auth/register"

test_data = {
    "phone": "+1234567890",
    "name": "Test User",
    "password": "testpassword123"
}

print("Testing registration API...")
print(f"URL: {url}")
print(f"Data: {test_data}")

try:
    response = requests.post(url, json=test_data)
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("✅ Registration successful!")
    else:
        print("❌ Registration failed!")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nChecking database after API call...")
# Check database
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
print(f"Users in database: {count}")
conn.close() 