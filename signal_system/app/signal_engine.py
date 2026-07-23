# app/signal_engine.py
import logging
import pandas as pd
from sqlalchemy.orm import Session
from app.models import PriceData, Signal
from app.indicators import calculate_indicators

logger = logging.getLogger(__name__)


def generate_signals(db: Session, symbols: list):
    if not symbols:
        return

    logger.info("Sinyal uretim motoru (Signal Engine) calisiyor...")

    for symbol in symbols:
        try:
            query = db.query(PriceData).filter(PriceData.symbol == symbol).order_by(PriceData.date.asc()).limit(
                150).all()

            if len(query) < 30:
                logger.warning(f"{symbol}: Indikator hesaplamak icin yetersiz veri.")
                continue

            data = [{
                "date": q.date,
                "open": q.open,
                "high": q.high,
                "low": q.low,
                "close": q.close,
                "volume": q.volume
            } for q in query]

            df = pd.DataFrame(data)
            df.set_index("date", inplace=True)

            df = calculate_indicators(df)

            if df.empty:
                continue

            last_candle = df.iloc[-1]
            prev_candle = df.iloc[-2]
            signal_date = df.index[-1]

            existing_signal = db.query(Signal).filter(Signal.symbol == symbol, Signal.date == signal_date).first()
            if existing_signal:
                continue

            # --- AL/SAT MANTIGI VE FILTRELER ---
            signal_type = "BEKLE"

            ema_cross_up = (prev_candle['ema_9'] <= prev_candle['ema_21']) and (
                        last_candle['ema_9'] > last_candle['ema_21'])
            ema_cross_down = (prev_candle['ema_9'] >= prev_candle['ema_21']) and (
                        last_candle['ema_9'] < last_candle['ema_21'])

            if ema_cross_up:
                if last_candle['rsi'] < 70:
                    signal_type = "AL"

            elif ema_cross_down:
                if last_candle['rsi'] > 30:
                    signal_type = "SAT"

            new_signal = Signal(
                symbol=symbol,
                date=signal_date,
                signal_type=signal_type,
                rsi=float(last_candle['rsi']),
                ema_9=float(last_candle['ema_9']),
                ema_21=float(last_candle['ema_21']),
                macd=float(last_candle['macd']),
                macd_signal=float(last_candle['macd_signal'])
            )
            db.add(new_signal)
            db.commit()

            logger.info(f"Sinyal Üretildi -> Sembol: {symbol} | Karar: {signal_type}")

        except Exception as e:
            db.rollback()
            logger.error(f"{symbol} sinyal uretiminde hata: {e}")