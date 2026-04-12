import jwt
from datetime import datetime, timezone
from app.core.config import settings
from typing import Dict, Any

def decode_and_validate(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG]
        )
        
        exp = payload.get("exp")
        if exp and isinstance(exp, (int, float)):
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            if exp_datetime < datetime.now(timezone.utc):
                raise ValueError("Token has expired")
        
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.PyJWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
