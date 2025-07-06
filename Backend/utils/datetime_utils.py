from datetime import datetime

def format_date_ru(date_obj: datetime) -> str:
    return date_obj.strftime("%d.%m.%Y")