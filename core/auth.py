from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import jwt


from core.configs import settings


def create_access_token(sub: Any, expires_delta: Optional[timedelta] = None) -> str:
    # Gera o Token JWT assinado
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Payload: 'sub' é o identificador único do usuário (ID ou Email)
    to_encode = {"sub": str(sub), "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
