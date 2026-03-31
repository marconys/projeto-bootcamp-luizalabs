from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session
from schemas.usuario_schema import UsuarioSchemaCreate, UsuarioSchemaResponse
from services.user_service import UserService


router = APIRouter()


@router.post(
    "/",
    response_model=UsuarioSchemaResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UsuarioSchemaCreate,
    db: AsyncSession = Depends(get_session)
):
    service = UserService()

    try:
        user = await service.create_user(db, user_data)
        return UsuarioSchemaResponse.model_validate(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )