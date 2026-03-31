from fastapi import APIRouter

from .endpoints import auth, usuario, transacao

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(usuario.router, prefix="/users", tags=["Usuários"])
api_router.include_router(transacao.router, prefix="/transactions", tags=["Transações"])
