
# GPT5 Trading App (MVP)

Personal quantitative trading application — modular, extensible, and focused on continuous learning.
Initial scope targets **EOD equities/ETFs** with a gold-first example using **GLD** from Yahoo Finance.

**Your selections (frozen Aug 17, 2025):**
- Markets: US + EU (US-first), Paper-trading MVP.
- Go-live target: **Sep 17, 2025**.
- Data: Yahoo Finance (EOD) + Alpaca credentials (for later live). 
- Models (Phase 1): **XGBoost**, **LSTM/GRU**, **ARIMA-GARCH** (skeletons included; XGBoost wired for backtests).
- Backtesting engine: **backtrader**.
- Risk: daily loss limit **2%** of equity; trade only when **confidence ≥ 58%**.
- Circuit breakers (MVP): 
  - **VIX ≥ 35** OR **SPY daily drop ≤ -4%** → block new entries for next session.

## Quickstart

1) Create and activate a virtualenv (Python 3.10+ recommended), then:
```bash
pip install -r requirements.txt
```

2) Copy env template and fill secrets:
```bash
cp .env.example .env
# Fill ALPACA_API_KEY / ALPACA_API_SECRET for later live/paper trading
```

### Before running, ensure you have activated the venv root in the powershell:
.venv\Scripts\Activate.ps1

3) Run a GLD backtest (XGBoost):
```bash
python scripts/backtest_gld.py
```

4) Launch the dashboard:
```bash
streamlit run ui/streamlit_app.py
```

5) (Optional) Start the API:
```bash
uvicorn api.main:app --reload
```

### Notes
- Database is SQLite by default (`gpt5_trading_app.db`) for simplicity. 
- The **XGBoost** pipeline is fully operational; LSTM/ARIMA are scaffolded for Phase 1 iteration.
- Feature set: OHLCV + RSI/MACD/Bollinger/ATR + rolling returns/vol.
- Labels: T+1 direction; stop-loss/take-profit suggested from ATR multiples (1.5× SL, 2.0× TP).

---

## Project Structure

```
gpt5_trading_app/
  api/                 # FastAPI service
  backtesting/         # Backtrader integration & metrics
  config/              # Settings and env
  data/                # Data sources and universe
  execution/           # Risk, sizing, brokers
  features/            # Feature engineering and targets
  models/              # ML models and manager
  ui/                  # Streamlit dashboard
  utils/               # Logging, time, persistence
  scripts/             # Example scripts
```

---

## Roadmap
- Phase 1: solidify XGBoost; wire LSTM + ARIMA-GARCH; expand metrics & regime detection.
- Phase 2: add fundamentals & sentiment; paper/live hooks via Alpaca; options data pipeline.
- Phase 3: Transformers & RL; multi-asset expansion (FX/crypto/commodities).
- Phase 4: Optimization & scaling.
