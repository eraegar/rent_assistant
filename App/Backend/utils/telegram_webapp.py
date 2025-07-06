from fastapi import Header, HTTPException

def extract_init_data(init_data_raw: str) -> dict:
    # Проверка и парсинг initData, если где-то понадобится дополнительно
    from ..auth import check_init_data
    return check_init_data(init_data_raw)

def telegram_main_button(webapp, text: str):
    # Конфигурирование кнопки «главная» через JS-API
    webapp.MainButton.setText(text)
    webapp.MainButton.show()