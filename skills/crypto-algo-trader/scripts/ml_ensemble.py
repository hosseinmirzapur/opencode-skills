"""
ML Ensemble for Crypto Algo Trader
XGBoost-based price prediction (lightweight, no PyTorch required).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
import yaml


class MLEnsemble:
    """
    ML signal generation using XGBoost.
    Lightweight alternative to LSTM/TFT ensemble.
    """

    def __init__(self, config_path: str = 'scripts/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.models = {}

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features for ML models.
        """
        features = pd.DataFrame(index=df.index)

        features['returns'] = df['close'].pct_change()
        features['log_returns'] = np.log(df['close'] / df['close'].shift(1))

        features['rsi'] = self._rsi(df['close'])
        features['macd'] = self._macd(df['close'])
        features['atr'] = self._atr(df)

        for lag in [1, 2, 3, 5, 10]:
            features[f'return_lag_{lag}'] = features['returns'].shift(lag)

        features['vol_20'] = features['returns'].rolling(20).std()
        features['vol_60'] = features['returns'].rolling(60).std()

        return features.dropna()

    def _rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        up = delta.clip(lower=0).rolling(period).mean()
        down = (-delta.clip(upper=0)).rolling(period).mean()
        rs = up / down
        return 100 - (100 / (1 + rs))

    def _macd(self, series: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
        ema_fast = series.ewm(span=fast).mean()
        ema_slow = series.ewm(span=slow).mean()
        return ema_fast - ema_slow

    def _atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        tr = pd.concat([
            df['high'] - df['low'],
            abs(df['high'] - df['close'].shift()),
            abs(df['low'] - df['close'].shift())
        ], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def train_xgboost(self, train_df: pd.DataFrame, target_col: str = 'returns'):
        """Train XGBoost classifier for direction prediction."""
        try:
            import xgboost as xgb

            features = self.engineer_features(train_df)
            X = features.drop(columns=[target_col, 'log_returns'])
            y = (features[target_col] > 0).astype(int)

            params = self.config['ml_models']['xgboost']
            model = xgb.XGBClassifier(
                n_estimators=params['n_estimators'],
                max_depth=params['max_depth'],
                learning_rate=params['learning_rate']
            )

            model.fit(X, y)
            self.models['xgboost'] = model
            return model
        except ImportError:
            return None

    def predict_xgboost(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Predict using XGBoost."""
        if 'xgboost' not in self.models:
            return {'direction': 'NEUTRAL', 'confidence': 0.5}

        features = self.engineer_features(df)
        X = features.drop(columns=['returns', 'log_returns'], errors='ignore')

        proba = self.models['xgboost'].predict_proba(X.iloc[-1:])[0]

        up_confidence = proba[1] if len(proba) > 1 else 0.5
        direction = 'UP' if up_confidence > 0.5 else 'DOWN'

        return {
            'direction': direction,
            'confidence': round(up_confidence, 3)
        }

    def predict_ensemble(self, df: pd.DataFrame,
                        chronos_signal: Dict = None) -> Dict[str, Any]:
        """
        Combine model predictions.
        """
        predictions = {
            'xgboost': self.predict_xgboost(df),
        }

        if chronos_signal:
            predictions['chronos'] = chronos_signal

        if len(predictions) == 1:
            signal = list(predictions.values())[0]
            return {
                'direction': signal['direction'],
                'confidence': signal['confidence'],
                'component_signals': predictions
            }

        weights = {'xgboost': 0.4, 'chronos': 0.6}

        up_weighted = sum(
            predictions[k]['confidence'] * weights.get(k, 0.5)
            for k in predictions if predictions[k]['direction'] == 'UP'
        )
        down_weighted = sum(
            predictions[k]['confidence'] * weights.get(k, 0.5)
            for k in predictions if predictions[k]['direction'] == 'DOWN'
        )

        direction = 'UP' if up_weighted > down_weighted else 'DOWN'
        confidence = (up_weighted + down_weighted) / len(predictions)

        return {
            'direction': direction,
            'confidence': round(confidence, 3),
            'component_signals': predictions
        }


if __name__ == '__main__':
    ensemble = MLEnsemble()
    print("ML Ensemble ready (XGBoost only)")
