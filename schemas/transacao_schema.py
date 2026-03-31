from pydantic import BaseModel, ConfigDict

from decimal import Decimal

from typing import Literal


# Entrada
class TransacaoSchemaCreate(BaseModel):
    amount: Decimal
    transaction_type: Literal["credit", "debit"]


# Saída
class TransacaoSchemaResponse(BaseModel):
    id: int
    amount: Decimal
    transaction_type: str

    model_config = ConfigDict(from_attributes=True)
