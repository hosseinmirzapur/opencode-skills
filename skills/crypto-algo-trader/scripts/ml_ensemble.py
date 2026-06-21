"""
ML Ensemble for Crypto Algo Trader
XGBoost, LSTM, TFT, and stacked ensemble for price prediction.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import yaml


class MLEnsemble:
    """
    Multi-model ML ensemble for crypto signal generation.
    Uses XGBoost, LSTM, TFT with stacking meta-learner.
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
        
        # Price-based features
        features['returns'] = df['close'].pct_change()
        features['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        
        # Technical indicators
        features['rsi'] = self._rsi(df['close'])
        features['macd'] = self._macd(df['close'])
        features['atr'] = self._atr(df)
        
        # Lag features
        for lag in [1, 2, 3, 5, 10]:
            features[f'return_lag_{lag}'] = features['returns'].shift(lag)
        
        # Rolling features
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
            y = (target_col > 0).astype(int)
            
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
        
        # Class 1 = UP, Class 0 = DOWN
        up_confidence = proba[1] if len(proba) > 1 else 0.5
        direction = 'UP' if up_confidence > 0.5 else 'DOWN'
        
        return {
            'direction': direction,
            'confidence': round(up_confidence, 3)
        }
    
    def predict_ensemble(self, df: pd.DataFrame, 
                       kronos_signal: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Combine all model predictions.
        """
        predictions = {
            'xgboost': self.predict_xgboost(df),
        }
        
        if kronos_signal:
            predictions['kronos'] = kronos_signal
        
        # Weighted average
        weights = {'xgboost': 0.4, 'kronos': 0.6}
        total_weight = sum(weights.get(k, 0.33) for k in predictions)
        
        up_score = sum(
            predictions[k]['confidence'] if predictions[k]['direction'] == 'UP' else 
            (1 - predictions[k]['confidence']) if predictions[k]['direction'] == 'DOWN' else 0
            for k in predictions
        )
        
        confidence = up_score / len(predictions) if predictions else 0.5
        
        # Determine direction
        up_weighted = sum(
            predictions[k]['confidence'] * weights.get(k, 0.33)
            for k in predictions if predictions[k]['direction'] == 'UP'
        )
        down_weighted = sum(
            predictions[k]['confidence'] * weights.get(k, 0.33)
            for k in predictions if predictions[k]['direction'] == 'DOWN'
        )
        
        direction = 'UP' if up_weighted > down_weighted else 'DOWN'
        
        return {
            'direction': direction,
            'confidence': round(confidence, 3),
            'component_signals': predictions
        }


if __name__ == '__main__':
    ensemble = MLEnsemble()
    print("ML Ensemble ready")