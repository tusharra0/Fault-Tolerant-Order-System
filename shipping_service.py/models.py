from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from db import Base

class Shipment(Base):
    __tablename__ = "shipments"

    order_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    tracking_number = Column(String, nullable=False)
    status = Column(String, default="READY")
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_delivery = Column(DateTime)


from db import engine, Base

Base.metadata.create_all(bind=engine)