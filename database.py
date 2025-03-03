from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ایجاد اتصال به دیتابیس SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# ایجاد کلاس پایه برای مدل‌ها
Base = declarative_base()
metadata = MetaData()

# تعریف مدل برای جدول کاربران
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    age = Column(Integer)

# ایجاد جلسه برای دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تابع کمکی برای دریافت دیتابیس
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ایجاد جداول در دیتابیس
def create_tables():
    Base.metadata.create_all(bind=engine) 