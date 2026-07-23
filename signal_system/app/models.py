# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    date = Column(DateTime, index=True, nullable=False)
    signal_type = Column(String, nullable=False)  # 'AL', 'SAT', 'BEKLE'
    rsi = Column(Float)
    ema_9 = Column(Float)
    ema_21 = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)