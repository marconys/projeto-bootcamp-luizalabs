from sqlalchemy import Column, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.configs import settings


class AccountModel(settings.DB_BASE_MODEL):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    balance = Column(Numeric(10, 2), default=0)

    user = relationship("UserModel", back_populates="account")
    transactions = relationship(
        "TransactionModel", back_populates="account", cascade="all, delete-orphan"
    )
