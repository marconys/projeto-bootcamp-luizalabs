from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session
from core.auth import create_access_token
from core.security import verify_password

from models.usuario_model import UserModel
from schemas.usuario_schema import UsuarioSchemaLogin

router = APIRouter()


@router.post("/login")
async def login(user_data: UsuarioSchemaLogin, db: AsyncSession = Depends(get_session)):
    # Buscar usuário pelo email
    result = await db.execute(
        select(UserModel).where(UserModel.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    # Se não existir ou senha inválida
    if not user or not verify_password(user_data.senha, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos"
        )

    # Gerar token
    access_token = create_access_token(sub=user.id)

    return {"access_token": access_token, "token_type": "bearer"}
