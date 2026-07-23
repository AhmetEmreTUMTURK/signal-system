# app/routers/signals.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Signal, PriceData
from app.schemas import SignalResponse, PriceHistoryResponse

router = APIRouter(prefix="/signals", tags=["Signals"])

@router.get("/latest", response_model=List[SignalResponse])
def get_latest_signals(db: Session = Depends(get_db)):

    signals = db.query(Signal).distinct(Signal.symbol).order_by(Signal.symbol, Signal.date.desc()).all()
    return signals

@router.get("/{symbol}", response_model=SignalResponse)
def get_signal_by_symbol(symbol: str, db: Session = Depends(get_db)):
    signal = db.query(Signal).filter(Signal.symbol == symbol.upper()).order_by(Signal.date.desc()).first()
    if not signal:
        raise HTTPException(status_code=404, detail="Bu sembol icin sinyal bulunamadi.")
    return signal

@router.get("/history/{symbol}", response_model=List[PriceHistoryResponse])
def get_price_history(symbol: str, limit: int = 100, db: Session = Depends(get_db)):
    history = db.query(PriceData).filter(PriceData.symbol == symbol.upper()).order_by(PriceData.date.desc()).limit(limit).all()
    if not history:
        raise HTTPException(status_code=404, detail="Gecmis veri bulunamadi.")
    return history