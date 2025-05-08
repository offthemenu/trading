import yfinance as yf
from signals.indicator_logic import calculate_ema, calculate_rsi, calculate_atr
import pandas as pd

def generate_signals(ticker): # for simulation
    df = yf.download(ticker, period='100d', auto_adjust=True)

    if df.empty:
        return _empty_signal(ticker)

    buy, sell, close = evaluate_signal_from_df(df)
    latest = df.iloc[-1]

    return {
        'ticker': ticker,
        'buy': buy,
        'sell': sell,
        'price': close,
        'rsi': float(latest['RSI']),
        'atr': float(latest['ATR']),
        'volume': int(latest['Volume']),
        'volume_avg': float(latest['Volume_SMA']),
    }    

def evaluate_signal_from_df(df: pd.DataFrame):
    """
    Calculates buy/sell signal from a dataframe.
    Assumes 'Close', 'High', 'Low', 'Volume' columns exist.
    """
    if df.shape[0] < 60:
        print("⚠️ Not enough rows for indicator calculation. Skipping.")
        return False, False, None

    df['EMA10'] = calculate_ema(df, 10)
    df['EMA50'] = calculate_ema(df, 50)
    df['ATR'] = calculate_atr(df, 14)
    df['RSI'] = calculate_rsi(df, 14)
    df['Volume_SMA'] = df['Volume'].rolling(20).mean()
    df.dropna(inplace=True)

    if df.empty:
        return False, False, None

    latest = df.iloc[-1]

    try:
        ema10 = float(latest['EMA10'])
        ema50 = float(latest['EMA50'])
        atr = float(latest['ATR'])
        close = float(latest['Close'])
        volume = int(latest['Volume'])
        volume_sma = float(latest['Volume_SMA'])
        rsi = float(latest['RSI'])
    except Exception as e:
        print(f"⚠️ Failed to extract indicators: {e}")
        return False, False, None

    atr_ratio = atr / close

    buy = (
        ema10 > ema50 and
        volume > volume_sma and
        40 < rsi < 70 and
        atr_ratio < 0.03
    )

    sell = (
        ema10 < ema50 or
        rsi < 30 or
        atr_ratio > 0.03
    )

    return buy, sell, close

def _empty_signal(ticker):
    return {
        'ticker': ticker,
        'buy': False,
        'sell': False,
        'price': 0.0,
        'rsi': 0.0,
        'atr': 0.0,
        'volume': 0.0,
        'volume_avg': 0.0,
    }
