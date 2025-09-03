from __future__ import annotations
import backtrader as bt
import pandas as pd

from gpt5_trading_app.data.data_sources import get_ohlcv_yahoo
from gpt5_trading_app.features.ta_features import add_indicators
from gpt5_trading_app.features.target import make_labels
from gpt5_trading_app.models.xgb_model import XGBSignalModel
from gpt5_trading_app.backtesting.bt_engine import PandasData, SignalStrategy
from gpt5_trading_app.config.settings import settings


def ensure_single_datetime_index(x: pd.DataFrame) -> pd.DataFrame:
    """Force a 1-level tz-naive DatetimeIndex called 'date'."""
    out = x.copy()
    idx = out.index
    if isinstance(idx, pd.MultiIndex):
        idx = idx.get_level_values(0)
    out.index = pd.to_datetime(idx)
    if getattr(out.index, "tz", None) is not None:
        out.index = out.index.tz_localize(None)
    out.index.name = "date"
    out.sort_index(inplace=True)
    return out


def build_price_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Return OHLCV with exact column names Backtrader expects."""
    d = df.copy()
    # normalize lowercase names
    if hasattr(d.columns, "str"):
        d.columns = d.columns.str.lower()
    else:
        d.columns = [str(c).lower() for c in d.columns]

    # prefer raw close; fall back to adj_close if needed
    if "close" not in d.columns and "adj_close" in d.columns:
        d["close"] = d["adj_close"]

    required = ["open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in d.columns]
    if missing:
        raise ValueError(f"Missing required OHLCV columns: {missing}. Got: {list(d.columns)[:10]}")

    price = d[required]
    price = ensure_single_datetime_index(price)
    return price


def run():
    symbol = "GLD"

    # 1) Data & features
    df = get_ohlcv_yahoo(symbol, "2015-01-01", None)
    df = add_indicators(df)
    df = make_labels(df)

    # 2) Model -> signals
    model = XGBSignalModel()
    model.fit(df)
    signals = model.predict_signal(df, threshold=settings.CONFIDENCE_THRESHOLD)

    # 3) Align signals + risk columns on a clean datetime index
    signals = ensure_single_datetime_index(signals)
    risk = ensure_single_datetime_index(df[["atr_14", "sl_atr_mult", "tp_atr_mult"]])
    signals = pd.concat([signals, risk.reindex(signals.index)], axis=1)

    # 4) Prepare OHLCV for Backtrader
    price = build_price_frame(df)

    # 5) Backtrader run
    cerebro = bt.Cerebro()
    data = PandasData(dataname=price)
    cerebro.adddata(data)
    cerebro.broker.setcash(settings.STARTING_CAPITAL)
    cerebro.addstrategy(SignalStrategy, signals_df=signals)
    cerebro.run(maxcpus=1)

    print(f"Final Portfolio Value: {cerebro.broker.getvalue():,.2f}")


if __name__ == "__main__":
    run()
