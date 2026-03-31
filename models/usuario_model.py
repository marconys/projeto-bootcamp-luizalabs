from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import settings


class UserModel(settings.DB_BASE_MODEL):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    account = relationship("AccountModel", back_populates="user", uselist=False)
