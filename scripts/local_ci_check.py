#!/usr/bin/env python3
"""
Скрипт для локального запуска всех CI проверок перед push в GitLab.
Помогает избежать неудачных CI pipeline.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description, cwd=None):
    """Запускает команду и обрабатывает результат"""
    print(f"\n🔍 {description}")
    print(f"Команда: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print(f"✅ {description} - УСПЕШНО")
            return True
        else:
            print(f"❌ {description} - НЕУДАЧА (код: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return False

def check_python():
    """Проверяет Python код"""
    print("\n" + "="*60)
    print("🐍 ПРОВЕРКА PYTHON КОДА")
    print("="*60)
    
    app_dir = Path(__file__).parent.parent / "app"
    
    if not app_dir.exists():
        print("❌ Директория app/ не найдена")
        return False
    
    success = True
    
    # Проверка зависимостей
    success &= run_command(
        "pip install -r requirements-dev.txt",
        "Установка зависимостей для разработки",
        cwd=app_dir
    )
    
    # Flake8 проверка
    success &= run_command(
        "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics",
        "Flake8 - критические ошибки",
        cwd=app_dir
    )
    
    success &= run_command(
        "flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics",
        "Flake8 - полная проверка стиля",
        cwd=app_dir
    )
    
    # Black проверка форматирования
    success &= run_command(
        "black --check --diff .",
        "Black - проверка форматирования",
        cwd=app_dir
    )
    
    # isort проверка импортов
    success &= run_command(
        "isort --check-only --diff .",
        "isort - проверка импортов",
        cwd=app_dir
    )
    
    # MyPy проверка типов (опционально)
    run_command(
        "mypy . --ignore-missing-imports",
        "MyPy - проверка типов (опционально)",
        cwd=app_dir
    )
    
    # Запуск тестов
    success &= run_command(
        "pytest tests/ -v --cov=. --cov-report=term-missing",
        "Pytest - запуск тестов",
        cwd=app_dir
    )
    
    return success

def check_flutter():
    """Проверяет Flutter код"""
    print("\n" + "="*60)
    print("💙 ПРОВЕРКА FLUTTER КОДА")
    print("="*60)
    
    success = True
    
    # Flutter доктор
    run_command(
        "flutter doctor -v",
        "Flutter Doctor - диагностика",
    )
    
    # Получение зависимостей
    success &= run_command(
        "flutter pub get",
        "Flutter pub get - зависимости"
    )
    
    # Анализ кода
    success &= run_command(
        "flutter analyze --fatal-infos --fatal-warnings",
        "Flutter analyze - анализ кода"
    )
    
    # Проверка форматирования
    success &= run_command(
        "dart format --set-exit-if-changed .",
        "Dart format - проверка форматирования"
    )
    
    # Запуск тестов
    success &= run_command(
        "flutter test --coverage",
        "Flutter test - запуск тестов"
    )
    
    return success

def auto_fix():
    """Автоматическое исправление некоторых проблем"""
    print("\n" + "="*60)
    print("🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ")
    print("="*60)
    
    app_dir = Path(__file__).parent.parent / "app"
    
    print("\n🐍 Python auto-fix:")
    
    # Автоматическое форматирование Python
    run_command(
        "black .",
        "Black - автоматическое форматирование",
        cwd=app_dir
    )
    
    run_command(
        "isort .",
        "isort - автоматическая сортировка импортов",
        cwd=app_dir
    )
    
    print("\n💙 Flutter auto-fix:")
    
    # Автоматическое форматирование Flutter
    run_command(
        "dart format .",
        "Dart format - автоматическое форматирование"
    )

def main():
    """Основная функция"""
    print("🚀 ЛОКАЛЬНАЯ ПРОВЕРКА CI/CD")
    print("Этот скрипт запускает те же проверки, что и GitLab CI")
    print("="*60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        auto_fix()
        print("\n✅ Автоматические исправления применены!")
        print("Теперь запустите скрипт без --fix для проверки")
        return
    
    # Переходим в корень проекта
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"Рабочая директория: {os.getcwd()}")
    
    python_success = check_python()
    flutter_success = check_flutter()
    
    print("\n" + "="*60)
    print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("="*60)
    
    if python_success:
        print("✅ Python проверки: УСПЕШНО")
    else:
        print("❌ Python проверки: НЕУДАЧА")
    
    if flutter_success:
        print("✅ Flutter проверки: УСПЕШНО")
    else:
        print("❌ Flutter проверки: НЕУДАЧА")
    
    if python_success and flutter_success:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ УСПЕШНО!")
        print("Можно делать commit и push 🚀")
        sys.exit(0)
    else:
        print("\n⚠️  ЕСТЬ ПРОБЛЕМЫ, ТРЕБУЮЩИЕ ИСПРАВЛЕНИЯ")
        print("\n💡 Попробуйте:")
        print("1. Запустить: python scripts/local_ci_check.py --fix")
        print("2. Исправить оставшиеся проблемы вручную")
        print("3. Запустить скрипт еще раз")
        sys.exit(1)

if __name__ == "__main__":
    main() 