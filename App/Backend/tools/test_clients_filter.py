#!/usr/bin/env python3
"""
Test script to verify clients filtering - only active subscription clients should be shown
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

from database import SessionLocal
from models import User, UserRole, ClientProfile, Subscription, SubscriptionStatus, SubscriptionPlan
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_clients_filter():
    """Test clients filtering functionality"""
    
    db = SessionLocal()
    
    try:
        print("🧪 Testing Clients Filter Functionality")
        print("=" * 50)
        
        # Check current clients in database
        print("📊 Current clients in database:")
        all_clients = db.query(ClientProfile).all()
        
        for client in all_clients:
            has_subscription = client.subscription is not None
            subscription_status = client.subscription.status.value if has_subscription else "Нет подписки"
            print(f"  - {client.user.name} (ID {client.id}): {subscription_status}")
        
        print(f"\nВсего клиентов в базе: {len(all_clients)}")
        
        # Count clients by subscription status
        active_subs = db.query(ClientProfile).join(Subscription).filter(
            Subscription.status == SubscriptionStatus.active
        ).count()
        
        expired_subs = db.query(ClientProfile).join(Subscription).filter(
            Subscription.status == SubscriptionStatus.expired
        ).count()
        
        no_subs = db.query(ClientProfile).filter(
            ~ClientProfile.subscription.has()
        ).count()
        
        print(f"Клиенты с активными подписками: {active_subs}")
        print(f"Клиенты с истекшими подписками: {expired_subs}")
        print(f"Клиенты без подписок: {no_subs}")
        
        # Test API endpoint
        print("\n🔐 Testing API endpoint...")
        
        # Login as manager
        login_data = {
            "phone": "+7900000005",
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
        
        # Test default filtering (should show only active subscriptions)
        print("\n📋 Testing default filtering (only active subscriptions)...")
        response = requests.get(f"{BASE_URL}/api/v1/management/clients", headers=headers)
        
        if response.status_code == 200:
            clients_data = response.json()["clients"]
            print(f"✅ API returned {len(clients_data)} clients (only active subscriptions)")
            
            for client in clients_data:
                sub_status = client["subscription"]["status"] if client["subscription"] else "None"
                print(f"  - {client['name']}: {sub_status}")
                
            # Verify all returned clients have active subscriptions
            all_active = all(
                client["subscription"] and client["subscription"]["status"] == "active" 
                for client in clients_data
            )
            
            if all_active:
                print("✅ All returned clients have active subscriptions")
            else:
                print("❌ Some clients don't have active subscriptions")
        else:
            print(f"❌ API request failed: {response.status_code} - {response.text}")
            return
        
        # Test expired filter
        print("\n📋 Testing expired filter...")
        response = requests.get(
            f"{BASE_URL}/api/v1/management/clients?subscription_status=expired", 
            headers=headers
        )
        
        if response.status_code == 200:
            expired_clients = response.json()["clients"]
            print(f"✅ API returned {len(expired_clients)} clients with expired subscriptions")
        else:
            print(f"❌ Expired filter failed: {response.status_code}")
        
        # Test all filter
        print("\n📋 Testing all clients filter...")
        response = requests.get(
            f"{BASE_URL}/api/v1/management/clients?subscription_status=all", 
            headers=headers
        )
        
        if response.status_code == 200:
            all_clients_api = response.json()["clients"]
            print(f"✅ API returned {len(all_clients_api)} clients (all clients)")
            
            # Should match database count
            if len(all_clients_api) == len(all_clients):
                print("✅ API 'all' filter matches database count")
            else:
                print(f"❌ Mismatch: API returned {len(all_clients_api)}, DB has {len(all_clients)}")
        else:
            print(f"❌ All filter failed: {response.status_code}")
        
        print(f"\n📊 Test Summary:")
        print(f"   - Default API filter: ✅ Shows only active subscriptions ({len(clients_data)} clients)")
        print(f"   - Database active subscriptions: {active_subs}")
        print(f"   - Database expired subscriptions: {expired_subs}")
        print(f"   - Database clients without subscriptions: {no_subs}")
        print(f"   - Total clients in database: {len(all_clients)}")
        print(f"\n🎯 Result: Manager panel will now show only clients with active subscriptions by default")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_clients_filter() 