import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st, pandas as pd
from datetime import date
from sklearn.model_selection import TimeSeriesSplit  # <-- NEW

from gpt5_trading_app.config.settings import settings
from gpt5_trading_app.data.data_sources import get_ohlcv_yahoo
from gpt5_trading_app.features.ta_features import add_indicators
from gpt5_trading_app.features.target import make_labels
from gpt5_trading_app.models.xgb_model import XGBSignalModel
from gpt5_trading_app.execution.risk import circuit_breaker

st.set_page_config(page_title="GPT5 Trading App", layout="wide")
st.title("GPT5 Trading App — MVP")
st.caption("Gold-first EOD trading (GLD). XGBoost operational; LSTM/ARIMA scaffolds.")

# --------- helper: out-of-sample probabilities via time-series CV ---------
def cv_probs_timeseries(df_lbl: pd.DataFrame, n_splits: int = 5, gap: int = 5) -> pd.Series:
    """
    Returns OOS probabilities for 'prob_up' using walk-forward CV.
    'gap' purges last 'gap' bars from train and first 'gap' bars from test to reduce leakage.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    probs = pd.Series(index=df_lbl.index, dtype=float)

    for train_idx, test_idx in tscv.split(df_lbl):
        # Purge/embargo
        if gap > 0:
            if len(train_idx) <= gap or len(test_idx) <= gap:
                continue
            train_idx = train_idx[:-gap]
            test_idx = test_idx[gap:]

        train_df = df_lbl.iloc[train_idx]
        test_df  = df_lbl.iloc[test_idx]

        model = XGBSignalModel()
        model.fit(train_df)
        p = model.predict_proba(test_df)
        probs.iloc[test_idx] = p.values

    return probs.dropna()
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("Controls")
    symbol = st.text_input("Symbol", "GLD")
    start = st.date_input("Start", date(2015,1,1))
    end = st.date_input("End", date.today())
    threshold = st.slider("Confidence threshold", 0.5, 0.9, float(settings.CONFIDENCE_THRESHOLD), 0.01)
    if st.button("Run backtest (quick)"):
        st.session_state["run"] = True

cb = circuit_breaker()
if cb["triggered"]:
    st.warning(f"⛔ Circuit breaker active: {cb['reason']} (no new entries)")
else:
    st.success("✅ Circuit breakers: OK")

if st.session_state.get("run"):
    st.subheader(f"Backtest (quick) — {symbol}")

    # 1) Data + features + labels
    df = get_ohlcv_yahoo(symbol, str(start), str(end))
    df_feat = add_indicators(df)
    df_lbl  = make_labels(df_feat)

    # 2) Out-of-sample probabilities via walk-forward CV
    probs_oos = cv_probs_timeseries(df_lbl, n_splits=5, gap=5)
    y_true_oos = df_lbl.loc[probs_oos.index, "target"].astype(int)
    pred_dir_oos = (probs_oos >= 0.5).astype(int)
    trade_mask_oos = (probs_oos >= float(threshold))

    oos_dir_acc   = float((pred_dir_oos == y_true_oos).mean())
    oos_trade_cnt = int(trade_mask_oos.sum())
    oos_trade_acc = float((pred_dir_oos[trade_mask_oos] == y_true_oos[trade_mask_oos]).mean()) if oos_trade_cnt else None

    # Baseline: always predict the majority class in OOS
    base_acc = max(y_true_oos.mean(), 1 - y_true_oos.mean())

    # 3) Compose the preview table aligned to OOS index
    view = pd.concat(
        [
            df_lbl.loc[probs_oos.index, ["close", "atr_14", "sl_atr_mult", "tp_atr_mult"]],
            probs_oos.rename("prob_up"),
            trade_mask_oos.astype(int).rename("signal_long"),
        ],
        axis=1
    ).dropna()

    # 4) Metrics tiles (OOS)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("OOS directional accuracy (0.5)", f"{oos_dir_acc:.1%}")
    c2.metric(f"OOS trade accuracy (≥ {threshold:.2f})", f"{oos_trade_acc:.1%}" if oos_trade_cnt else "—")
    c3.metric("OOS number of trades", oos_trade_cnt)
    c4.metric("Baseline (always-up)", f"{base_acc:.1%}")

    st.line_chart(view[["close"]])
    st.dataframe(view.tail(20))
    st.info(
        "Metrics shown are OUT-OF-SAMPLE via time-series cross-validation with a small embargo. "
        "Use the Backtrader script for P&L, Sharpe, drawdown, and costs."
    )
