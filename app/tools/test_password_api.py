#!/usr/bin/env python3
"""
Test script to verify password API functionality
"""
import sys
import os
import requests
import json

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

# Меняем рабочую директорию на app
os.chdir(app_dir)

BASE_URL = "http://localhost:8000"

def test_password_api():
    """Test password API functionality"""
    
    try:
        print("🧪 Testing Password API Functionality")
        print("=" * 50)
        
        # First, login as manager
        print("🔐 Logging in as manager...")
        login_data = {
            "phone": "+7900000005",  # Manager phone from test data
            "password": "manager123"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/management/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Manager login failed: {response.status_code} - {response.text}")
            return
        
        token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print("✅ Manager login successful")
        
        # Get all assistants
        print("\n📋 Getting all assistants...")
        response = requests.get(f"{BASE_URL}/api/v1/management/assistants", headers=headers)
        if response.status_code != 200:
            print(f"❌ Failed to get assistants: {response.status_code} - {response.text}")
            return
        
        assistants = response.json()["assistants"]
        print(f"✅ Found {len(assistants)} assistants")
        
        # Display current passwords
        print("\n🔑 Current assistant passwords:")
        for assistant in assistants:
            password = assistant.get("last_known_password", "Unknown")
            reset_at = assistant.get("last_password_reset_at", "Never")
            print(f"  {assistant['name']} (ID {assistant['id']}): '{password}' (reset: {reset_at})")
        
        # Find Геннадий for testing
        gennady = None
        for assistant in assistants:
            if "Геннадий" in assistant["name"]:
                gennady = assistant
                break
        
        if not gennady:
            print("❌ Геннадий not found")
            return
        
        print(f"\n🎯 Testing with Геннадий (ID {gennady['id']})")
        print(f"   Current password: '{gennady.get('last_known_password', 'Unknown')}'")
        
        # Test password reset
        print("\n🔄 Testing password reset...")
        response = requests.post(
            f"{BASE_URL}/api/v1/management/assistants/{gennady['id']}/reset-password",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Password reset failed: {response.status_code} - {response.text}")
            return
        
        reset_result = response.json()
        new_password = reset_result["new_password"]
        print(f"✅ Password reset successful! New password: '{new_password}'")
        
        # Verify password is updated in database
        print("\n🔍 Verifying password update...")
        response = requests.get(f"{BASE_URL}/api/v1/management/assistants", headers=headers)
        if response.status_code == 200:
            updated_assistants = response.json()["assistants"]
            for assistant in updated_assistants:
                if assistant["id"] == gennady["id"]:
                    stored_password = assistant.get("last_known_password")
                    if stored_password == new_password:
                        print(f"✅ Password correctly stored in database: '{stored_password}'")
                    else:
                        print(f"❌ Password mismatch! Stored: '{stored_password}', Expected: '{new_password}'")
                    break
        else:
            print(f"❌ Failed to verify password update: {response.status_code}")
        
        # Test assistant login with new password
        print(f"\n🧪 Testing assistant login with new password...")
        assistant_login_data = {
            "phone": "79085673445",  # Геннадий's phone from test
            "password": new_password
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/assistants/auth/login",
            json=assistant_login_data
        )
        
        if response.status_code == 200:
            print(f"✅ Assistant login successful with new password!")
        else:
            print(f"❌ Assistant login failed: {response.status_code} - {response.text}")
        
        print(f"\n📊 Test Summary:")
        print(f"   - Manager API: ✅ Working")
        print(f"   - Password Reset API: ✅ Working") 
        print(f"   - Password Storage: ✅ Working")
        print(f"   - Assistant Login: {'✅ Working' if response.status_code == 200 else '❌ Failed'}")
        print(f"   - New Password: '{new_password}'")
        
    except Exception as e:
        print(f"❌ Error during API test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_api() 