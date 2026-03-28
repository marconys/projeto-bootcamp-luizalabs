from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from core.configs import settings

class TransactionModel(settings.DB_BASE_MODEL):
    __tablename__ = "transacoes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String, nullable=False)
    
    account = relationship("AccountModel", back_populates="transactions")