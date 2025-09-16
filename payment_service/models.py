from sqlalchemy import Column, String, Boolean
from db import Base

class Payment(Base):
    __tablename__ = "payments"

    order_id = Column(String, primary_key=True, index=True)
    authorized = Column(Boolean, default=True)


from db import engine, Base

Base.metadata.create_all(bind=engine)
