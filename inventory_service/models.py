from sqlalchemy import Column, String, Boolean, Integer
from db import Base

class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"

    order_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    reserved = Column(Boolean, default=True)
    stock_available = Column(Integer, default=100)  # Simulated stock level


from db import engine, Base

Base.metadata.create_all(bind=engine)