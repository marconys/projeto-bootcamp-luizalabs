from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.auth import create_access_token
from core.security import verify_password

from models.usuario_model import UserModel

router = APIRouter()


@router.post("/login")
async def login(
    # O Depends() aqui lê os dados do formulário do Swagger
    user_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_session)
):
    # O OAuth2PasswordRequestForm usa .username no lugar de .email
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.username)
    )
    user = result.scalar_one_or_none()

    # O campo de senha no form é .password
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email ou senha inválidos"
        )

    # O 'sub' deve ser string para evitar bugs em alguns decoders
    access_token = create_access_token(sub=str(user.id))

    return {"access_token": access_token, "token_type": "bearer"}
