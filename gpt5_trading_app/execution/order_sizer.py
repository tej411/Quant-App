from gpt5_trading_app.config.settings import settings
def max_position_size(cash: float, price: float) -> int:
    alloc = cash * settings.MAX_POSITION_PCT
    return max(1, int(alloc // price))
