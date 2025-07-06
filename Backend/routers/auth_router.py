# app/routers/auth_router.py

from fastapi import APIRouter, HTTPException, Body, FastAPI
from pydantic import BaseModel, Field
from ..auth import check_init_data, create_jwt


router = APIRouter(prefix="/auth", tags=["auth"])


class InitDataRequest(BaseModel):
    """
    Схема входящего JSON для верификации Telegram WebApp.
    """
    initData: str = Field(
        ...,
        title="initData",
    )


class AuthResponse(BaseModel):  
    """
    Схема ответа: JWT-токен и ID пользователя.
    """
    token: str = Field(..., description="JWT для дальнейшей авторизации")
    user_id: int = Field(..., description="ID пользователя в Telegram")


@router.post(
    "/verify",
    response_model=AuthResponse,
    summary="Verify Telegram WebApp initData and return JWT",
)
async def verify_telegram_user(
    body: InitDataRequest = Body(
        ...,
        media_type="application/json",
    )
) -> AuthResponse:
    # 1. Получаем и проверяем initData
    parsed = check_init_data(body.initData)

    # 2. Извлекаем вложенный объект user
    user_info = parsed.get("user", {})
    telegram_user_id = user_info.get("id")
    if telegram_user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Cannot extract user ID from initData"
        )

    # 3. Генерируем JWT и возвращаем
    token = create_jwt(str(telegram_user_id))
    return AuthResponse(token=token, user_id=telegram_user_id)
