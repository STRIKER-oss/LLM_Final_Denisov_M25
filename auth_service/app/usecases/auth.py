from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from typing import Dict, Any

class AuthUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
    
    async def register(self, email: str, password: str) -> Dict[str, Any]:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError()
        
        password_hash = hash_password(password)
        user = await self.user_repo.create(email, password_hash)
        await self.session.commit()
        
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    
    async def login(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        
        token = create_access_token(user.id, user.role)
        return token
    
    async def me(self, user_id: int) -> Dict[str, Any]:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
