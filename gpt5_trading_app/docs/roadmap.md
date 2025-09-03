# GPT5 Trading App – Roadmap

## Phase 1 (now)
- Assets: equities/ETFs (GLD example).
- Data: Yahoo Finance (EOD).
- Models: XGBoost operational; LSTM + ARIMA-GARCH scaffolds.
- Backtesting: backtrader long/flat; ATR SL/TP.
- UI: Streamlit quick backtest + OOS metrics (TimeSeriesSplit).
- API: FastAPI `/predict`.
- Risk: confidence ≥ 0.58; max position 10%; daily loss limit 2%.
- Circuit breakers: VIX ≥ 35 OR SPY daily drop ≤ -4% → no new entries.

## Phase 2
- Live/paper via Alpaca; execution module.
- Add symbols/universes; EU/US.
- Fundamentals & options pipeline (Yahoo options first pass).
- Pyfolio/empyrical performance pane in UI.

## Phase 3
- Transformers & RL (policy gradient/Q-learning) added to Algo Manager.
- Multi-asset: FX, crypto, commodities.
- Regime detection, feature importance tracking.

## Phase 4
- Optimization & scaling, Docker, CI/CD, ClickHouse or Postgres, microservices split.
