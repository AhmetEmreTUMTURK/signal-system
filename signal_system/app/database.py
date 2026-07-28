# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL bağlantı URL'si (Kendi kullanıcı adı ve şifrene göre değiştir)(PostgreSQL kuramadığımız için Neon Console  geçtik.)
# Format: postgresql://kullanici_adi:sifren@localhost:5432/veritabani_adi
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:(sizinşifreniz)@localhost:5432/signal_db"

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
