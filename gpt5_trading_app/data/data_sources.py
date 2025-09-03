from __future__ import annotations
import pandas as pd
import yfinance as yf
def get_ohlcv_yahoo(symbol: str, start: str = "2010-01-01", end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, start=start, end=end, interval=interval, auto_adjust=False, progress=False)

    if not isinstance(df, pd.DataFrame) or df.empty:
        raise RuntimeError(f"No data returned for {symbol}")

    # --- FLATTEN columns to simple strings ---
    if isinstance(df.columns, pd.MultiIndex):
        # take level 0 (field) and normalize
        df.columns = [str(c[0]).lower().replace(" ", "_") for c in df.columns]
    else:
        df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]

    # ensure standard names exist
    if "adj_close" in df.columns and "close" not in df.columns:
        df["close"] = df["adj_close"]

    df.index.name = "date"
    return df
def get_vix(start: str = "2010-01-01", end: str | None = None) -> pd.DataFrame:
    return get_ohlcv_yahoo("^VIX", start=start, end=end)
def get_spy(start: str = "2010-01-01", end: str | None = None) -> pd.DataFrame:
    return get_ohlcv_yahoo("SPY", start=start, end=end)
