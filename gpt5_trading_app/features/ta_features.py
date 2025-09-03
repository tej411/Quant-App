import pandas as pd
import numpy as np
import ta

def _to_series(obj, name: str, index):
    """Coerce Series/DataFrame/ndarray to a 1-D pandas Series."""
    if isinstance(obj, pd.Series):
        s = obj
    elif isinstance(obj, pd.DataFrame):
        s = obj.iloc[:, 0]          # take the first column if it's a 1-col DataFrame
    else:
        s = pd.Series(obj, index=index, name=name)
    s.name = name
    return pd.to_numeric(s, errors="coerce")

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # make sure these are 1-D series
    close = _to_series(df["close"], "close", df.index)
    high  = _to_series(df["high"], "high", df.index)
    low   = _to_series(df["low"], "low", df.index)

    # Indicators
    df["rsi_14"] = ta.momentum.RSIIndicator(close=close, window=14).rsi()
    macd = ta.trend.MACD(close=close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    bb = ta.volatility.BollingerBands(close=close, window=20, window_dev=2)
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()
    df["atr_14"] = ta.volatility.AverageTrueRange(high=high, low=low, close=close, window=14).average_true_range()

    # Returns/vol
    df["ret_1d"] = close.pct_change()
    df["ret_5d"] = close.pct_change(5)
    df["vol_10d"] = df["ret_1d"].rolling(10).std() * np.sqrt(252)

    return df.dropna()
