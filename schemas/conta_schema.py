from pydantic import BaseModel, ConfigDict
from decimal import Decimal


# Response simples (SEM transações)
class ContaSchemaResponse(BaseModel):
    id: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)
