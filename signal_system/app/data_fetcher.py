# app/data_fetcher.py
import logging
import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import PriceData
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_symbols(filepath="symbols.txt"):
    try:
        with open(filepath, "r") as f:
            return [line.strip().upper() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error(f"{filepath} dosyasi bulunamadi!")
        return []


def fetch_and_save_data(db: Session, symbols: list):
    if not symbols:
        logger.warning("Sembol listesi bos, veri cekme islemi iptal edildi.")
        return

    logger.info(f"{len(symbols)} sembol icin veriler cekiliyor...")

    try:
        data = yf.download(symbols, period="5d", interval="15m", group_by="ticker", threads=True)
    except Exception as e:
        logger.error(f"yfinance ile toplu veri cekilirken kritik hata olustu: {e}")
        return

    for symbol in symbols:
        try:
            if len(symbols) == 1:
                df = data.copy()
            else:
                if symbol not in data.columns.levels[0]:
                    logger.warning(f"{symbol} icin veri donmedi (Borsa kapali veya sembol hatali olabilir).")
                    continue
                df = data[symbol].copy()

            df.dropna(how="all", inplace=True)
            if df.empty:
                logger.warning(f"{symbol} tablosu temizlendikten sonra bombos kaldi! (Veriler NaN gelmis olabilir)")
                continue

            # DB'de bu sembole ait en guncel kaydin tarihini bul (Tekrar yazmayi onlemek icin)
            last_record = db.query(func.max(PriceData.date)).filter(PriceData.symbol == symbol).scalar()

            new_records = []
            for index, row in df.iterrows():
                record_date = index.to_pydatetime()

                if record_date.tzinfo is not None:
                    record_date = record_date.replace(tzinfo=None)

                # DB'deki kayittan daha eskiyse veya ayniysa atla
                if last_record and record_date <= last_record:
                    continue

                price_entry = PriceData(
                    symbol=symbol,
                    date=record_date,
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume'])
                )
                new_records.append(price_entry)

            if new_records:
                db.bulk_save_objects(new_records)
                db.commit()
                logger.info(f"{symbol}: {len(new_records)} yeni fiyat kaydi eklendi.")
            else:
                logger.info(f"{symbol}: Yeni kayit bulunamadi, veritabaniniz guncel.")

        except Exception as e:
            db.rollback()
            logger.error(f"{symbol} dongusunde islenirken veritabani hatasi: {e}")