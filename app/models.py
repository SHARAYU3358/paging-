from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import DateTime

from .database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(String(36), primary_key=True)

    name = Column(String(255), nullable=False)

    category = Column(String(100), nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime, nullable=False)

    updated_at = Column(DateTime, nullable=False)