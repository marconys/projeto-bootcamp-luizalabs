from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload  # Importante para carregar relacionamentos

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

        # 2. Lógica de criação de senha e objeto Usuário
        hashed_password = hash_password(user_data.senha)
        new_user = UserModel(email=user_data.email, password=hashed_password)
        
        # 3. Adicionar objetos à sessão 
        # Note: Não usamos 'async with db.begin()' aqui porque o 
        # get_session do FastAPI/SQLAlchemy já gerencia a transação.
        db.add(new_user)
        
        # Criar conta vinculada (o saldo inicial é 0 como definido na Model)
        new_account = AccountModel(balance=0, user=new_user)
        db.add(new_account)

        try:
            # 4. Efetivar as mudanças no banco de dados
            await db.commit() 
            
            # 5. RECARREGAR o usuário com a conta (Eager Loading)
            # Isso é vital porque o seu Schema de saída (UsuarioSchemaResponse)
            # espera o campo 'account'. Sem o selectinload, o Pydantic quebra.
            query = (
                select(UserModel)
                .where(UserModel.id == new_user.id)
                .options(selectinload(UserModel.account))
            )
            
            result = await db.execute(query)
            # Retornamos o objeto completo (User + Account)
            return result.scalar_one()

        except Exception as e:
            # Se algo falhar na criação ou no commit, desfazemos tudo
            await db.rollback()
            raise e