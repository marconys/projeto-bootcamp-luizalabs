from fastapi import FastAPI
from api.v1.api import api_router
from core.configs import settings

app = FastAPI(
    title="Projeto Conta API",
    version="1.0.0",
    description="API para gerenciamento de contas e transações",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
