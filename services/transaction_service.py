from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from decimal import Decimal

from models.conta_model import AccountModel
from models.transacoes_model import TransactionModel



class TransactionService:
    async def create_transaction(self, db: AsyncSession, account_id: int, amount: Decimal, transaction_type: str):
        
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        
        async with db.begin():
            # Verificar se a conta existe
            result = await db.execute(select(AccountModel).where(AccountModel.id == account_id).with_for_update())
            account = result.scalar_one_or_none()
            
            if not account:
                raise ValueError("Conta não encontrada.")
            
            # Lógica do negócio para débito ou crédito
            if transaction_type == "debit":
                if Decimal(account.balance) < amount:
                    raise ValueError("Saldo insuficiente para débito.")
                account.balance -= amount
            
            elif transaction_type == "credit":
                account.balance += amount
            else:
                raise ValueError("Tipo de transação inválido. Use 'debit' ou 'credit'.")
            
            transaction = TransactionModel(
                account_id=account.id,
                amount=amount,
                transaction_type=transaction_type
            )
            
            db.add(transaction)
            # O commit/flush acontece automaticamente ao sair do bloco 'begin'
            return transaction        