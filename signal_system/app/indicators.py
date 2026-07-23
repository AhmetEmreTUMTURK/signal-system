# app/indicators.py
import pandas_ta as ta
import pandas as pd


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verilen DataFrame'e EMA(9), EMA(21), RSI(14) ve MACD(12,26,9) hesaplayip ekler.
    df icinde 'close' sutunu oldugunu varsayar.
    """
    df.columns = [c.lower() for c in df.columns]

    if len(df) < 30:
        return df

    df.ta.ema(length=9, append=True)
    df.ta.ema(length=21, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)

    # pandas-ta'nin otomatik olusturdugu karmasik sutun isimlerini modellerimize uyduruyoruz
    df.rename(columns={
        'EMA_9': 'ema_9',
        'EMA_21': 'ema_21',
        'RSI_14': 'rsi',
        'MACD_12_26_9': 'macd',
        'MACDs_12_26_9': 'macd_signal'
    }, inplace=True, errors='ignore')

    # NaN degerleri temizle (ilk mumlarda hareketli ortalamalar hesaplanamaz)
    df.dropna(inplace=True)

    return df