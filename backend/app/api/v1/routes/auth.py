from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.rate_limit import limiter
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.services.auth_service import AuthService
from app.services.password_reset_service import PasswordResetService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(data=data)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.refresh(data=data)


@router.post("/change-password", status_code=200)
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AuthService(db)
    await service.change_password(
        user_id=current_user.id,
        current_password=data.current_password,
        new_password=data.new_password,
    )
    return {
        "success": True,
        "data": {"message": "Password changed successfully"},
    }


@router.post("/forgot-password", status_code=202)
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    service = PasswordResetService(db)
    await service.request_reset(data.email)
    return {
        "success": True,
        "data": {"message": "If this email exists, a reset link has been sent"},
    }


@router.post("/reset-password", status_code=200)
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db),
):
    service = PasswordResetService(db)
    await service.reset_password(data.token, data.new_password)
    return {
        "success": True,
        "data": {"message": "Password has been reset successfully"},
    }