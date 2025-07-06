from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, database, auth
from typing import Optional

router = APIRouter()

# ... existing code ...

@router.post("/telegram-login", response_model=schemas.Token)
async def telegram_login(telegram_data: schemas.TelegramLogin, db: Session = Depends(database.get_db)):
    """
    Авторизация/регистрация через Telegram WebApp
    """
    try:
        # Проверяем, существует ли пользователь с таким Telegram ID
        user = db.query(models.User).filter(models.User.telegram_id == telegram_data.telegram_id).first()
        
        if not user:
            # Если пользователя нет, создаем нового
            user = models.User(
                username=telegram_data.username or f"tg_{telegram_data.telegram_id}",
                email=f"tg_{telegram_data.telegram_id}@telegram.user",  # Временный email
                telegram_id=telegram_data.telegram_id,
                first_name=telegram_data.first_name,
                last_name=telegram_data.last_name,
                hashed_password=auth.get_password_hash("telegram_user_temp_password")  # Временный пароль
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print(f"✅ New Telegram user created: {user.username} (ID: {user.telegram_id})")
        else:
            # Обновляем данные существующего пользователя
            user.first_name = telegram_data.first_name
            user.last_name = telegram_data.last_name
            if telegram_data.username:
                user.username = telegram_data.username
            db.commit()
            
            print(f"✅ Existing Telegram user logged in: {user.username} (ID: {user.telegram_id})")
        
        # Создаем JWT токен
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        print(f"❌ Telegram login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate with Telegram"
        ) 