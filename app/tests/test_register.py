import requests
import json

# Test data
test_user = {
    "name": "Тест Юзер",
    "phone": "+7 (999) 123-45-67",
    "password": "test123"
}

def test_server():
    print("🚀 Тестируем сервер...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Сервер работает! Статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Сервер не запущен: {e}")
        return
    
    # Test 2: Check API docs
    try:
        response = requests.get("http://localhost:8000/docs")
        print(f"✅ API документация доступна! Статус: {response.status_code}")
    except Exception as e:
        print(f"❌ API документация недоступна: {e}")
    
    # Test 3: Try registration
    try:
        print(f"\n📝 Тестируем регистрацию с данными: {test_user}")
        response = requests.post(
            "http://localhost:8000/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📄 Заголовки ответа: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Регистрация успешна!")
            print(f"👤 Данные пользователя: {response.json()}")
        else:
            print(f"❌ Ошибка регистрации!")
            print(f"📝 Текст ошибки: {response.text}")
            
            # Try to parse error as JSON
            try:
                error_data = response.json()
                print(f"🔍 Детали ошибки: {error_data}")
            except:
                print("⚠️ Ответ не в формате JSON")
                
    except Exception as e:
        print(f"💥 Исключение при регистрации: {e}")

if __name__ == "__main__":
    test_server() 