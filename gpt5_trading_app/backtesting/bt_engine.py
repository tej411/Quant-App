from __future__ import annotations
import backtrader as bt, pandas as pd
from dataclasses import dataclass
from gpt5_trading_app.config.settings import settings
class PandasData(bt.feeds.PandasData):
    params = (('datetime', None),('open','open'),('high','high'),('low','low'),('close','close'),('volume','volume'),('openinterest', None),)
class SignalStrategy(bt.Strategy):
    params = dict(signals_df=None, atr_col='atr_14', max_position_pct=settings.MAX_POSITION_PCT, confidence_threshold=settings.CONFIDENCE_THRESHOLD, sl_mult_col='sl_atr_mult', tp_mult_col='tp_atr_mult')
    def __init__(self):
        if self.p.signals_df is None: raise ValueError("signals_df must be provided")
        self.signals = self.p.signals_df; self.data_close = self.datas[0].close; self.order=None; self.entry_price=None
    def next(self):
        dt = self.datas[0].datetime.datetime(0)
        if dt not in self.signals.index: return
        sig = int(self.signals.loc[dt,'signal_long']); prob=float(self.signals.loc[dt,'prob_up'])
        atr = float(self.signals.loc[dt,self.p.atr_col]) if self.p.atr_col in self.signals.columns else None
        sl_mult = float(self.signals.loc[dt,self.p.sl_mult_col]) if self.p.sl_mult_col in self.signals.columns else 1.5
        tp_mult = float(self.signals.loc[dt,self.p.tp_mult_col]) if self.p.tp_mult_col in self.signals.columns else 2.0
        if not self.position and sig==1 and prob>=self.p.confidence_threshold:
            cash = self.broker.getcash(); size_cash = cash*self.p.max_position_pct; size = max(1, int(size_cash/self.data_close[0]))
            if size>0:
                self.order = self.buy(size=size); self.entry_price = self.data_close[0]
                if atr is not None and atr>0:
                    sl_price = self.entry_price - sl_mult*atr; tp_price = self.entry_price + tp_mult*atr
                    self.sell(exectype=bt.Order.Stop, price=sl_price, size=size, oco=self.sell(price=tp_price, exectype=bt.Order.Limit, size=size))
        elif self.position and sig==0: self.close()
from dataclasses import dataclass
@dataclass
class BTResult: cerebro: bt.Cerebro; strat: SignalStrategy
