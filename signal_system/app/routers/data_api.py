from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# Kendi dosya yapına göre importları ayarla
from app.database import get_db
from app.models import PriceData, Signal

# API rotasını tanımlıyoruz
router = APIRouter(prefix="/api", tags=["Dashboard Data"])

@router.get("/prices")
def get_latest_prices(limit: int = 100, db: Session = Depends(get_db)):
    """
    Arayüzdeki mum grafiğini (candlestick) çizmek için son N adet fiyat verisini döndürür.
    """
    # Veritabanından tarihe göre en yeni 'limit' kadar veriyi çekiyoruz
    prices = db.query(PriceData).order_by(PriceData.date.desc()).limit(limit).all()
    return prices

@router.get("/signals")
def get_latest_signals(limit: int = 20, db: Session = Depends(get_db)):
    """
    Arayüzdeki son sinyaller tablosunu beslemek için güncel AL/SAT verilerini döndürür.
    """
    signals = db.query(Signal).order_by(Signal.date.desc()).limit(limit).all()
    return signals