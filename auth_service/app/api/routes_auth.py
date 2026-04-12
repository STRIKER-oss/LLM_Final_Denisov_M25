from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_uc

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/register", response_model=UserPublic)
async def register(request: RegisterRequest, auth_uc: AuthUseCase = Depends(get_auth_uc)):
    result = await auth_uc.register(request.email, request.password)
    return result

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_uc: AuthUseCase = Depends(get_auth_uc)):
    token = await auth_uc.login(form_data.username, form_data.password)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserPublic)
async def me(credentials: HTTPAuthorizationCredentials = Security(security), auth_uc: AuthUseCase = Depends(get_auth_uc)):
    token = credentials.credentials
    from app.core.security import decode_token
    payload = decode_token(token)
    if not payload:
        from app.core.exceptions import InvalidTokenError
        raise InvalidTokenError()
    user_id = int(payload.get("sub"))
    result = await auth_uc.me(user_id)
    return result
