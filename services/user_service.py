from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UserModel
from models.conta_model import AccountModel

from schemas.usuario_schema import UsuarioSchemaCreate
from core.security import hash_password


class UserService:

    async def create_user(self, db: AsyncSession, user_data: UsuarioSchemaCreate):
        # 1. Verificar se email já existe
        result = await db.execute(
            select(UserModel).where(UserModel.email == user_data.email)
        )
        if result.scalar_one_or_none():
            raise ValueError("Email já cadastrado")

        # 2. Lógica de criação
        hashed_password = hash_password(user_data.senha)
        new_user = UserModel(email=user_data.email, password=hashed_password)
        
        # 3. Adicionar objetos à sessão (sem abrir novo begin)
        db.add(new_user)
        
        # Criar conta vinculada
        new_account = AccountModel(balance=0, user=new_user)
        db.add(new_account)

        try:
            # 4. Efetivar as mudanças que já estão na sessão
            await db.commit() 
            await db.refresh(new_user)
            return new_user
        except Exception as e:
            await db.rollback()
            raise e
        