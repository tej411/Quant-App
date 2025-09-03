import pandas as pd

def _to_series(obj, name: str, index):
    """Coerce Series/DataFrame/ndarray to a 1-D pandas Series."""
    if isinstance(obj, pd.Series):
        s = obj
    elif isinstance(obj, pd.DataFrame):
        # if it's a 1-col DataFrame, take that column; otherwise take the first numeric col
        if obj.shape[1] == 1:
            s = obj.iloc[:, 0]
        else:
            num = obj.select_dtypes(include="number")
            s = (num.iloc[:, 0] if not num.empty else obj.iloc[:, 0])
    else:
        s = pd.Series(obj, index=index, name=name)
    s.name = name
    return pd.to_numeric(s, errors="coerce")

def make_labels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Force 'close' to be a 1-D Series and overwrite the column so downstream ops are consistent
    close = _to_series(out["close"], "close", out.index)
    out["close"] = close.values

    # Create future_close from the coerced 1-D series
    future_close = close.shift(-1)
    out["future_close"] = future_close.values

    # Direction label
    out["target"] = (future_close > close).astype(int)

    # Risk params (scalars)
    out["sl_atr_mult"] = 1.5
    out["tp_atr_mult"] = 2.0

    return out.dropna()
