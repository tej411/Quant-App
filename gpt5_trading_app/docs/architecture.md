# Architecture Overview

**Packages**
- `gpt5_trading_app/data`: Yahoo loaders; `get_ohlcv_yahoo` returns flat OHLCV.
- `gpt5_trading_app/features`: `add_indicators` (RSI/MACD/BB/ATR), `make_labels` (T+1 dir, ATR SL/TP).
- `gpt5_trading_app/models`: `XGBSignalModel` (+ stubs for LSTM, ARIMA-GARCH); `manager.py` for algo registry.
- `gpt5_trading_app/backtesting`: Backtrader feed/strategy + metrics.
- `gpt5_trading_app/execution`: risk (circuit breakers), sizing, Alpaca placeholder.
- `gpt5_trading_app/ui`: Streamlit dashboard (OOS metrics).
- `gpt5_trading_app/api`: FastAPI `/predict`.

**Flow**
Data → Features → Labels → Model.fit → `predict_proba` → threshold to signal →  
Backtest (Backtrader) or UI preview → Risk checks (CBs, sizing).

**Non-goals (Phase 1)**
- No intraday.
- No live trading yet (Alpaca in Phase 2).
- Transformers/RL deferred to Phase 3.

**Risk Rules (Phase 1)**
- Trade only if `prob_up ≥ 0.58`.
- Max position 10% of equity; daily loss cap 2%.
- Circuit breakers: VIX ≥ 35 or SPY ≤ −4% daily → pause entries.
