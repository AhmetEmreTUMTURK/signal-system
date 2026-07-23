# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Response Modelleri (API'den disari donecek verinin formati)
class SignalResponse(BaseModel):
    symbol: str
    date: datetime
    signal_type: str
    rsi: Optional[float]
    ema_9: Optional[float]
    ema_21: Optional[float]

    class Config:
        from_attributes = True

class PriceHistoryResponse(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        from_attributes = True