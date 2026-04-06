from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase
from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError
import jwt

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_auth_uc(db: AsyncSession = Depends(get_db)) -> AuthUseCase:
    return AuthUseCase(db)

async def get_current_user_id(authorization: Optional[str] = Header(None, alias="Authorization")) -> int:
    if not authorization:
        raise InvalidTokenError()
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise InvalidTokenError()
    
    payload = decode_token(token)
    if payload is None:
        raise InvalidTokenError()
    
    try:
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise InvalidTokenError()
        return int(user_id_str)
    except (ValueError, KeyError):
        raise InvalidTokenError()
