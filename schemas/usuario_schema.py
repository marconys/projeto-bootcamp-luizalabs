from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

from schemas.conta_schema import ContaSchemaResponse


# Base
class UsuarioSchemaBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# Entrada
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


# Saída
class UsuarioSchemaResponse(UsuarioSchemaBase):
    id: int
    account: Optional[ContaSchemaResponse] = None


# Login
class UsuarioSchemaLogin(BaseModel):
    email: EmailStr
    senha: str
