from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc

from core.deps import get_session, get_current_user

from models.transacoes_model import TransactionModel
from models.usuario_model import UserModel

from schemas.transacao_schema import (
    TransacaoSchemaCreate,
    TransacaoSchemaResponse
)

from services.transaction_service import TransactionService


router = APIRouter()



@router.post(
    "/",
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

@router.get(
    "/",
    response_model=list[TransacaoSchemaResponse]
)
async def get_transactions(
    page: int = 1,
    limit: int = 10,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    account = current_user.account

    if not account:
        raise HTTPException(
            status_code=400,
            detail="Usuário não possui conta associada"
        )

    # cálculo de paginação
    offset = (page - 1) * limit

    # query base
    query = select(TransactionModel).where(
        TransactionModel.account_id == account.id
    )

    # filtro por tipo
    if type:
        query = query.where(TransactionModel.transaction_type == type)

    # ordenação + paginação
    query = query.order_by(desc(TransactionModel.id)).offset(offset).limit(limit)

    result = await db.execute(query)
    transactions = result.scalars().all()

    return transactions