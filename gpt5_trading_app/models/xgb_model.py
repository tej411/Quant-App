from __future__ import annotations
import pandas as pd, numpy as np
from xgboost import XGBClassifier
FEATURE_COLUMNS = ['rsi_14','macd','macd_signal','bb_high','bb_low','atr_14','ret_1d','ret_5d','vol_10d']
class XGBSignalModel:
    def __init__(self, params: dict | None = None):
        default = dict(n_estimators=300,max_depth=4,learning_rate=0.05,subsample=0.9,colsample_bytree=0.9,objective='binary:logistic',eval_metric='logloss',n_jobs=4,reg_lambda=1.0)
        if params: default.update(params)
        self.model = XGBClassifier(**default)
        self.fitted = False
    def fit(self, df: pd.DataFrame) -> None:
        X, y = df[FEATURE_COLUMNS].values, df['target'].values
        self.model.fit(X, y)
        self.fitted = True
    def predict_proba(self, df: pd.DataFrame) -> pd.Series:
        assert self.fitted, "Model not fitted"
        X = df[FEATURE_COLUMNS].values
        proba = self.model.predict_proba(X)[:, 1]
        return pd.Series(proba, index=df.index, name='prob_up')
    def predict_signal(self, df: pd.DataFrame, threshold: float = 0.58) -> pd.DataFrame:
        proba = self.predict_proba(df)
        signal = (proba >= threshold).astype(int)
        return pd.DataFrame({'prob_up': proba, 'signal_long': signal}, index=df.index)
