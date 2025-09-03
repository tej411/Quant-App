from datetime import datetime
import pandas as pd, pytz
def to_aware(dt: datetime, tz: str = "Europe/Amsterdam"):
    tzinfo = pytz.timezone(tz)
    if dt.tzinfo is None:
        return tzinfo.localize(dt)
    return dt.astimezone(tzinfo)
def as_utc_index(df: pd.DataFrame) -> pd.DataFrame:
    if df.index.tz is None:
        df.index = df.index.tz_localize('UTC')
    else:
        df.index = df.index.tz_convert('UTC')
    return df
