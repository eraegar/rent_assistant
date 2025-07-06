#!/usr/bin/env python3
"""
Тест для проверки автоформатирования телефонных номеров и регистрации с telegram_username
"""
import sys
import os
import requests
import json

# Добавляем путь к app папке
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
sys.path.append(app_dir)

def test_phone_formatting():
    """Тест различных форматов телефонных номеров"""
    
    print("🧪 Тестирование автоформатирования номеров телефонов")
    print("=" * 60)
    
    # Test cases для форматирования
    test_cases = [
        ("89991234567", "+7 (999) 123-45-67"),
        ("79991234567", "+7 (999) 123-45-67"),
        ("+79991234567", "+7 (999) 123-45-67"),
        ("9991234567", "+7 (999) 123-45-67"),
        ("999", "+7 (999"),
        ("9991234", "+7 (999) 123-4"),
        ("999123456", "+7 (999) 123-45-6"),
        ("99912345678", "+7 (999) 123-45-67"),  # Обрезка лишних цифр
        ("", ""),
        ("abc", ""),
        ("123abc456", "+7 (123) 456"),
    ]
    
    print("📋 Проверка форматирования номеров:")
    print("-" * 40)
    
    for input_phone, expected in test_cases:
        # Симулируем логику форматирования с frontend
        formatted = format_phone_number(input_phone)
        status = "✅" if formatted == expected else "❌"
        print(f"{status} '{input_phone}' -> '{formatted}' (ожидалось: '{expected}')")
    
    print("\n" + "=" * 60)

def format_phone_number(value: str) -> str:
    """Имитация форматирования номера телефона из frontend"""
    import re
    
    # Удаляем все нечисловые символы кроме +
    numbers = re.sub(r'[^\d+]', '', value)
    
    # Если пустая строка
    if not numbers:
        return ''
    
    # Если начинается с 8, заменяем на +7
    clean_numbers = numbers
    if clean_numbers.startswith('8'):
        clean_numbers = '+7' + clean_numbers[1:]
    
    # Если не начинается с +7, добавляем +7
    if not clean_numbers.startswith('+7'):
        if clean_numbers.startswith('+'):
            clean_numbers = '+7' + clean_numbers[1:]
        else:
            clean_numbers = '+7' + clean_numbers
    
    # Удаляем лишние символы после +7
    digits = clean_numbers[2:]  # убираем +7
    
    # Ограничиваем до 10 цифр после +7
    limited_digits = digits[:10]
    
    # Форматируем в зависимости от количества введенных цифр
    if len(limited_digits) == 0:
        return '+7'
    elif len(limited_digits) <= 3:
        return f'+7 ({limited_digits}'
    elif len(limited_digits) <= 6:
        return f'+7 ({limited_digits[:3]}) {limited_digits[3:]}'
    else:
        part1 = limited_digits[:3]
        part2 = limited_digits[3:6]
        part3 = limited_digits[6:8]
        part4 = limited_digits[8:10]
        
        formatted = f'+7 ({part1}) {part2}'
        if part3:
            formatted += f'-{part3}'
        if part4:
            formatted += f'-{part4}'
        
        return formatted

def test_client_registration_with_telegram():
    """Тест регистрации клиента с telegram username"""
    
    print("🔧 Тестирование регистрации клиента с Telegram алиасом")
    print("=" * 60)
    
    api_url = "http://127.0.0.1:8000/api/v1"
    
    # Тестовые данные для регистрации
    test_data = {
        "name": "Тестовый Клиент",
        "phone": "+79991234567",
        "password": "password123",
        "telegram_username": "@testuser123"
    }
    
    try:
        # Регистрация клиента
        print(f"📝 Регистрация клиента: {test_data['name']}")
        print(f"   Телефон: {test_data['phone']}")
        print(f"   Telegram: {test_data['telegram_username']}")
        
        response = requests.post(
            f"{api_url}/clients/auth/register",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Регистрация успешна!")
            client_data = response.json()
            print(f"   ID: {client_data['id']}")
            print(f"   Имя: {client_data['name']}")
            print(f"   Телефон: {client_data['phone']}")
            print(f"   Telegram: {client_data['telegram_username']}")
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка подключения: {e}")
        print("   Убедитесь, что сервер запущен на http://127.0.0.1:8000")
    
    print("\n" + "=" * 60)

def test_telegram_username_validation():
    """Тест валидации Telegram username"""
    
    print("🔍 Тестирование валидации Telegram алиасов")
    print("=" * 60)
    
    # Test cases для валидации telegram username
    test_cases = [
        ("@testuser", True),
        ("testuser", True),  # Должен добавиться @
        ("@test_user_123", True),
        ("@TestUser", True),
        ("@test", False),  # Слишком короткий
        ("@test_user_very_long_name_that_exceeds_limit", False),  # Слишком длинный
        ("@test-user", False),  # Дефис не разрешен
        ("@тестовый", False),  # Кириллица не разрешена
        ("@test user", False),  # Пробел не разрешен
        ("", False),  # Пустой
        ("@123test", True),  # Начинается с цифры - разрешено
    ]
    
    print("📋 Проверка валидации Telegram алиасов:")
    print("-" * 40)
    
    for telegram_alias, expected_valid in test_cases:
        is_valid = validate_telegram_username(telegram_alias)
        status = "✅" if is_valid == expected_valid else "❌"
        print(f"{status} '{telegram_alias}' -> валидный: {is_valid} (ожидалось: {expected_valid})")
    
    print("\n" + "=" * 60)

def validate_telegram_username(username: str) -> bool:
    """Валидация Telegram username"""
    import re
    
    if not username.strip():
        return False
    
    # Добавляем @ если его нет
    if not username.startswith('@'):
        username = '@' + username
    
    # Проверяем формат
    telegram_regex = re.compile(r'^@[a-zA-Z0-9_]{5,32}$')
    return bool(telegram_regex.match(username))

if __name__ == "__main__":
    print("🎯 Тестирование функций автоформатирования и регистрации")
    print("=" * 60)
    
    # Тестируем форматирование телефонов
    test_phone_formatting()
    
    # Тестируем валидацию Telegram username
    test_telegram_username_validation()
    
    # Тестируем регистрацию с API
    test_client_registration_with_telegram()
    
    print("✅ Все тесты завершены!") 