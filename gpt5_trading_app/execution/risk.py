from gpt5_trading_app.config.settings import settings
from gpt5_trading_app.data.data_sources import get_vix, get_spy
def circuit_breaker(today: str | None = None) -> dict:
    vix = get_vix().tail(2); spy = get_spy().tail(2)
    trig_vix = vix['close'].iloc[-1] >= settings.CIRCUIT_VIX_LEVEL
    spy_drop = (spy['close'].pct_change().iloc[-1]) <= -settings.CIRCUIT_SPY_DROP
    trigger = trig_vix or spy_drop; reason = []
    if trig_vix: reason.append(f"VIX {vix['close'].iloc[-1]:.2f} ≥ {settings.CIRCUIT_VIX_LEVEL}")
    if spy_drop: reason.append(f"SPY daily return {spy['close'].pct_change().iloc[-1]*100:.2f}% ≤ -{settings.CIRCUIT_SPY_DROP*100:.0f}%")
    return {"triggered": bool(trigger), "reason": "; ".join(reason) if reason else "OK"}
