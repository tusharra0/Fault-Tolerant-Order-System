from sqlalchemy import Column, String, Float, Text
from db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    items = Column(Text, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default="PENDING")
