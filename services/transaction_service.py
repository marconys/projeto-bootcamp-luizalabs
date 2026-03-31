from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from decimal import Decimal

from models.conta_model import AccountModel
from models.transacoes_model import TransactionModel


class TransactionService:
    async def create_transaction(
        self, db: AsyncSession, account_id: int, amount: Decimal, transaction_type: str
    ):
        # 1. Validação básica fora do banco
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        try:
            # 2. SELECT com LOCK (Pessimistic Locking)
            # Isso garante que ninguém altere a conta até você dar o commit
            query = select(AccountModel).where(AccountModel.id == account_id).with_for_update()
            result = await db.execute(query)
            account = result.scalar_one_or_none()

            if not account:
                raise ValueError("Conta não encontrada.")

            # 3. Lógica de Negócio
            if transaction_type == "debit":
                if Decimal(account.balance) < amount:
                    raise ValueError("Saldo insuficiente.")
                account.balance -= amount
            elif transaction_type == "credit":
                account.balance += amount
            else:
                raise ValueError("Tipo inválido.")

            # 4. Registrar a transação no histórico
            new_transaction = TransactionModel(
                account_id=account.id, 
                amount=amount, 
                transaction_type=transaction_type
            )
            db.add(new_transaction)

            # 5. Efetivar tudo de uma vez
            await db.commit() 
            await db.refresh(new_transaction)
            
            return new_transaction

        except Exception as e:
            # Se der qualquer erro (saldo insuficiente, erro de rede, etc)
            # o rollback garante que o saldo NÃO seja alterado
            await db.rollback()
            raise e