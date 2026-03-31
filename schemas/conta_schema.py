from pydantic import BaseModel
from decimal import Decimal


# Response simples (SEM transações)
class ContaSchemaResponse(BaseModel):
    id: int
    balance: Decimal

    class Config:
        from_attributes = True