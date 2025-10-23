import jwt
from datetime import timedelta, datetime, timezone

from core.config import settings

def create_jwt_token(
    data: dict,
    expires_delta: timedelta | None = None,
):
    """Encode JWT token"""
    to_encode = data.copy()
    
    if 'sub' in to_encode:
        to_encode['sub'] = str(to_encode['sub'])
        
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access.expire_at
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.access.secret_key, 
        algorithm=settings.access.algorithm
    )
    
    return encoded_jwt

def verify_token(token: str, expected_type: str = None) -> dict | None:
    """Verifies the JWT token and returns the payload"""
    try: 
        payload = jwt.decode(
            token,
            settings.access.secret_key,
            algorithms=[settings.access.algorithm],
        )
        
        if expected_type and payload.get("type") != expected_type:
            return None 
        
        return payload
    
    except jwt.PyJWTError:
        return None