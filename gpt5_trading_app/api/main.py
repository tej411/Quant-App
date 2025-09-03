# gpt5_trading_app/api/main.py
from fastapi import FastAPI
from pydantic import BaseModel

from gpt5_trading_app.config.settings import settings
from gpt5_trading_app.data.data_sources import get_ohlcv_yahoo
from gpt5_trading_app.features.ta_features import add_indicators
from gpt5_trading_app.features.target import make_labels
from gpt5_trading_app.models.xgb_model import XGBSignalModel

app = FastAPI(title="GPT5 Trading App API", version="0.1.0")


class PredictRequest(BaseModel):
    symbol: str = "GLD"
    start: str = "2015-01-01"
    end: str | None = None
    threshold: float = settings.CONFIDENCE_THRESHOLD


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    df = get_ohlcv_yahoo(req.symbol, req.start, req.end)
    df = add_indicators(df)
    df = make_labels(df)

    model = XGBSignalModel()
    model.fit(df)
    signals = model.predict_signal(df, threshold=req.threshold).tail(10)
    return signals.reset_index().to_dict(orient="records")
