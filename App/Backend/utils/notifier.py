
from ..models import User
def notify_user(db, user_id: int, message: str):
    # Здесь можно собрать пуш-уведомление или отправку по email/SMS
    user = db.query(User).get(user_id)
    # отправка через Telegram Bot API или другой канал
