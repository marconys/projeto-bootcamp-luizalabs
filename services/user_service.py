from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UserModel
from models.conta_model import AccountModel

from schemas.usuario_schema import UsuarioSchemaCreate
from core.security import hash_password


class UserService:

    async def create_user(self, db: AsyncSession, user_data: UsuarioSchemaCreate):
        
        # Verificar se email já existe
        result = await db.execute(
            select(UserModel).where(UserModel.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError("Email já cadastrado")

        # Hash da senha
        hashed_password = hash_password(user_data.senha)

        #  Criar usuário
        new_user = UserModel(
            email=user_data.email,
            password=hashed_password
        )

        # Criar conta automaticamente
        new_account = AccountModel(
            balance=0,
            user=new_user  # relação direta
        )

        # Persistir no banco
        async with db.begin():
            db.add(new_user)
            db.add(new_account)
            # Fazemos o flush/commit implícito aqui ao sair do bloco
            # Mas o refresh idealmente deve ser solicitado para carregar os IDs
            await db.flush()  # Envia pro DB para gerar o ID
            # Carrega os dados gerados
            await db.refresh(new_user)  
        # Retornar usuário (com account via relationship)
        return new_user
        