from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from core.configs import settings
from core.database import Session
from models.usuario_model import UserModel

# Onde o FastAPI busca o token no Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> UserModel:
    # busca e valida o usuário logado
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token gerado pelo seu auth.py
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if not user_id:
            raise error
    except JWTError:
        raise error

    # Busca o usuário no banco de dados
    result = await db.execute(select(UserModel).where(UserModel.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise error

    return user
