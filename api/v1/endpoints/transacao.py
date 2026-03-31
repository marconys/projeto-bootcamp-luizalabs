from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_session, get_current_user

from models.usuario_model import UserModel

from schemas.transacao_schema import (
    TransacaoSchemaCreate,
    TransacaoSchemaResponse
)

from services.transaction_service import TransactionService


router = APIRouter()



@router.post(
    "/transactions",
    response_model=TransacaoSchemaResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: TransacaoSchemaCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    service = TransactionService()
    try:
        # pega a conta do usuário logado
        account = current_user.account

        result = await service.create_transaction(
            db=db,
            account_id=account.id,
            amount=transaction_data.amount,
            transaction_type=transaction_data.transaction_type
        )

        return result["transaction"]

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )