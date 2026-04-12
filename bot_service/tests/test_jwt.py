import pytest
import jwt
from app.core.config import settings
from app.core.jwt import decode_and_validate

def test_decode_and_validate_valid_token():
    payload = {"sub": "123", "role": "user"}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    
    result = decode_and_validate(token)
    
    assert result["sub"] == "123"
    assert result["role"] == "user"

def test_decode_and_validate_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("invalid.token.here")

def test_decode_and_validate_expired_token():
    import time
    payload = {"sub": "123", "exp": int(time.time()) - 100}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    
    with pytest.raises(ValueError, match="Token has expired"):
        decode_and_validate(token)

def test_decode_and_validate_wrong_secret():
    payload = {"sub": "123"}
    token = jwt.encode(payload, "wrong_secret", algorithm="HS256")
    
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate(token)
