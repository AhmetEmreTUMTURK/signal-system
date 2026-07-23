# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL bağlantı URL'si (Kendi kullanıcı adı ve şifrene göre değiştir)(PostgreSQL kuramadığımız için Neon Console  geçtik.)
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_H7pDMIN2UfaS@ep-shy-fog-avdcqj18-pooler.c-11.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
