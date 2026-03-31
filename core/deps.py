from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload  # <--- IMPORTANTE

from core.configs import settings
from core.database import Session
from models.usuario_model import UserModel

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
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if not user_id:
            raise error
    except JWTError:
        raise error

    # AJUSTE AQUI: Usamos .options(selectinload(...))
    # Isso faz o SQLAlchemy buscar o User E a Account em uma "tacada" só
    query = (
        select(UserModel)
        .where(UserModel.id == int(user_id))
        .options(selectinload(UserModel.account)) 
    )
    
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise error

    return user
