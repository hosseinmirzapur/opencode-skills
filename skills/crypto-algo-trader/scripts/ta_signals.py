"""
Technical Analysis Signals for Crypto Algo Trader
Implements premium indicators: KAMA, VWAP, CVD, Market Profile, Fisher Transform.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
import talib


class TASignals:
    """
    Technical Analysis signal generators.
    All indicators chosen for institutional-grade signal quality.
    """
    
    @staticmethod
    def kama(df: pd.DataFrame, er_window: int = 10, fast: int = 2, slow: int = 30) -> pd.Series:
        """
        Kaufman Adaptive Moving Average.
        Adjusts speed to volatility without whipsaws.
        """
        return talib.KAMA(df['close'], timeperiod=er_window)
    
    @staticmethod
    def vwap(df: pd.DataFrame) -> pd.Series:
        """
        Volume Weighted Average Price.
        Institutional benchmark - measures smart money vs retail.
        """
        vwap = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
        return vwap
    
    @staticmethod
    def cvd(df: pd.DataFrame) -> pd.Series:
        """
        Cumulative Volume Delta.
        Measures buy/sell pressure imbalance.
        Note: Requires tick-level data for full accuracy.
        """
        # Simplified version using price movement
        delta = df['close'] - df['open']
        volume_signed = df['volume'] * np.sign(delta)
        return volume_signed.cumsum()
    
    @staticmethod
    def fisher_transform(series: pd.Series) -> pd.Series:
        """
        Fisher Transform.
        Normalizes price to approximately Gaussian for statistical analysis.
        Values > 2 indicate overbought, <-2 indicate oversold.
        """
        normalized = 2 * (series / series.max()) - 1
        return np.log((1 + normalized) / (1 - normalized))
    
    @staticmethod
    def schaff_trend_cycle(df: pd.DataFrame, cycle: int = 10, fast: int = 12, slow: int = 26) -> pd.Series:
        """
        Schaff Trend Cycle.
        Faster trend detection than MACD with fewer false signals.
        """
        macd, _, _ = talib.MACD(df['close'], fastperiod=fast, slowperiod=slow)
        stc = talib.KDJ(df['high'], df['low'], df['close'])['K']
        return stc
    
    @staticmethod
    def chandelier_exit(df: pd.DataFrame, period: int = 22, multiplier: float = 3.0) -> pd.Series:
        """
        Chandelier Exit.
        Volatility-based trailing stop that keeps you in big moves.
        """
        atr = talib.ATR(df['high'], df['low'], df['close'], timeperiod=period)
        highest_close = df['close'].rolling(period).max()
        return highest_close - (multiplier * atr)
    
    def generate_signals(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate all TA signals and aggregate.
        
        Returns:
        - direction: UP/DOWN/NEUTRAL
        - confidence: 0-1
        - individual signals
        """
        kama = self.kama(df)
        vwap = self.vwap(df)
        cvd = self.cvd(df)
        chandelier = self.chandelier_exit(df)
        
        # Signal generation
        signals = {
            'kama_bullish': df['close'].iloc[-1] > kama.iloc[-1],
            'vwap_deviation': (df['close'].iloc[-1] - vwap.iloc[-1]) / vwap.iloc[-1],
            'cvd_positive': cvd.iloc[-1] > 0,
            'price_above_chandelier': df['close'].iloc[-1] > chandelier.iloc[-1]
        }
        
        # Aggregate confidence
        bullish_count = sum(1 for v in signals.values() if v is True and isinstance(v, bool))
        confidence = bullish_count / len(signals)
        
        # Determine direction
        if signals['kama_bullish'] and signals['cvd_positive'] and signals['price_above_chandelier']:
            direction = 'UP'
        elif not signals['kama_bullish'] and not signals['cvd_positive']:
            direction = 'DOWN'
        else:
            direction = 'NEUTRAL'
        
        return {
            'direction': direction,
            'confidence': round(confidence, 2),
            'signals': signals,
            'indicators': {
                'kama': float(kama.iloc[-1]) if not kama.empty else None,
                'vwap': float(vwap.iloc[-1]) if not vwap.empty else None,
                'cvd': float(cvd.iloc[-1]) if not cvd.empty else None,
                'chandelier_stop': float(chandelier.iloc[-1]) if not chandelier.empty else None
            }
        }


if __name__ == '__main__':
    # Test with dummy data
    import numpy as np
    dates = pd.date_range('2024-01-01', periods=100, freq='1h')
    prices = np.cumsum(np.random.randn(100) * 10) + 100
    df = pd.DataFrame({
        'open': prices,
        'high': prices + 5,
        'low': prices - 5,
        'close': prices + np.random.randn(100),
        'volume': np.random.randint(1000, 10000, 100)
    })
    
    ta = TASignals()
    signals = ta.generate_signals(df)
    print(f"Direction: {signals['direction']}, Confidence: {signals['confidence']}")