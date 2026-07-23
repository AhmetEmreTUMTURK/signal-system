# app/scheduler.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.data_fetcher import fetch_and_save_data, get_symbols
from app.signal_engine import generate_signals
from datetime import datetime

logger = logging.getLogger(__name__)


def job_pipeline():
    logger.info("--- Zamanlanmis Gorev Basladi ---")
    db = SessionLocal()
    try:
        symbols = get_symbols("symbols.txt")
        if symbols:
            fetch_and_save_data(db, symbols)
            generate_signals(db, symbols)
    except Exception as e:
        logger.error(f"Zamanlanmis gorev sirasinda beklenmeyen hata: {e}")
    finally:
        db.close()
        logger.info("--- Zamanlanmis Gorev Tamamlandi ---")


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(job_pipeline, 'interval', minutes=15, next_run_time=datetime.now())

    scheduler.start()
    logger.info("APScheduler basariyla baslatildi. Sistem her 15 dakikada bir otonom calisacak.")
    return scheduler