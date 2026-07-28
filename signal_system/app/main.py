# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models import Base
from app.scheduler import start_scheduler
from app.routers import signals
from app.routers import data_api # Yukarıdaki dosyayı kaydettiğin isim

# Veritabani tablolarinin varligini garanti altina al (Bulutta zaten var)
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="Hisse ve Kripto Sinyal API",
    description="Algoritmik sinyal uretim ve backtest sistemi",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(signals.router)
app.include_router(data_api.router)

@app.get("/")
def root():
    return {"message": "Sinyal Sistemi API aktif. Dokumantasyon icin /docs adresine gidin."}