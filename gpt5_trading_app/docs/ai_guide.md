# Guidance for GitHub Copilot / AI assistants

## Project intent
Personal quant trading app. Prioritize correctness, leak-free evaluation, and risk controls.

## Must respect (Phase 1)
- Use EOD Yahoo data; no look-ahead. Labels are T+1.
- Default thresholds: confidence 0.58, max position 10%, daily loss limit 2%, CBs (VIX 35 / SPY −4%).
- Backtests via backtrader; UI “quick backtest” shows **out-of-sample** accuracy with TimeSeriesSplit.

## Style
- Python 3.11+, type hints, small pure functions, docstrings.
- Avoid hidden state; explicit params; deterministic seeds when relevant.

## Where to change things
- New features → `features/`.
- New models → `models/` + register in `models/manager.py`.
- Execution (Alpaca) → `execution/broker_alpaca.py` (Phase 2).
- UI metrics → `ui/streamlit_app.py`.

## Common tasks for you (Copilot)
- Add OOS Sharpe/MaxDD tiles in Streamlit from strategy returns.
- Implement walk-forward backtest: train up to t, trade t+1, rolling.
- Add options data fetcher (Yahoo) and simple covered-call signal stub.
- Write unit tests for `add_indicators`/`make_labels`.

## Things to avoid
- Introducing data leakage.
- Using real keys—read from `.env` only.
