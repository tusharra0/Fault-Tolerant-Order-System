from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:postgres123@postgres:5432/orders"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# 👇 Add this line to auto-create tables if missing
def init_db():
    from models import Order  # import your models
    Base.metadata.create_all(bind=engine)
