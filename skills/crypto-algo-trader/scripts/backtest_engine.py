"""
Backtesting Engine for Crypto Algo Trader
Implements walk-forward optimization with purged cross-validation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta


class BacktestEngine:
    """
    Professional backtesting with walk-forward optimization.
    Prevents overfitting through proper train/test separation.
    """
    
    def __init__(self, config_path: str = 'scripts/config.yaml'):
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def walk_forward_split(self, data: pd.DataFrame, 
                           train_days: int = 60,
                           test_days: int = 10,
                           purge_days: int = 1) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        Create walk-forward splits with purge to prevent lookahead bias.
        Returns list of (train_df, test_df) tuples.
        """
        splits = []
        start_date = data.index.min()
        end_date = data.index.max()
        
        while start_date + timedelta(days=train_days + test_days + purge_days) <= end_date:
            train_end = start_date + timedelta(days=train_days)
            test_start = train_end + timedelta(days=purge_days)
            test_end = test_start + timedelta(days=test_days)
            
            train_df = data.loc[start_date:train_end]
            test_df = data.loc[test_start:test_end]
            
            splits.append((train_df, test_df))
            
            start_date = test_start
        
        return splits
    
    def run_backtest(self, signals: List[Dict], 
                     price_data: pd.DataFrame) -> Dict[str, float]:
        """
        Run backtest on generated signals.
        
        Args:
            signals: List of signal dicts with entry, sl, tp, action
            price_data: OHLCV data for the period
        
        Returns:
            Performance metrics dict
        """
        trades = []
        position = None
        
        for i, row in enumerate(price_data.itertuples()):
            # Check for open position
            if position:
                if position['action'] == 'BUY':
                    if row.low <= position['stop_loss']:
                        trades.append({'pnl': -position['risk'], 'duration': i - position['entry_idx']})
                        position = None
                    elif row.high >= position['take_profit']:
                        trades.append({'pnl': position['reward'], 'duration': i - position['entry_idx']})
                        position = None
                # Match signal to entry
                for sig in signals:
                    if abs(row.timestamp - pd.Timestamp(sig['timestamp']).to_datetime64()) < np.timedelta64(1, 'h'):
                        if sig['confidence'] > self.config['signals']['confidence_threshold']:
                            position = {
                                'entry_idx': i,
                                'action': sig['action'],
                                'stop_loss': sig['stop_loss'],
                                'take_profit': sig['take_profit'],
                                'risk': sig['entry_price'] - sig['stop_loss'],
                                'reward': sig['take_profit'] - sig['entry_price']
                            }
                        break
        
        return self.calculate_metrics(trades)
    
    def calculate_metrics(self, trades: List[Dict]) -> Dict[str, float]:
        """Calculate performance metrics from trades."""
        if not trades:
            return {'sharpe': 0, 'win_rate': 0, 'profit_factor': 0, 'max_dd': 0}
        
        pnls = [t['pnl'] for t in trades]
        
        # Sharpe Ratio (assuming 0 risk-free rate)
        sharpe = np.mean(pnls) / np.std(pnls) * np.sqrt(252) if np.std(pnls) > 0 else 0
        
        # Win Rate
        wins = sum(1 for p in pnls if p > 0)
        win_rate = wins / len(pnls)
        
        # Profit Factor
        gross_profit = sum(p for p in pnls if p > 0)
        gross_loss = abs(sum(p for p in pnls if p < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Max Drawdown
        equity = np.cumsum(pnls)
        max_dd = 0
        if len(equity) > 1:
            peak = equity[0]
            for e in equity:
                if e > peak:
                    peak = e
                dd = (peak - e) / peak if peak > 0 else 0
                max_dd = max(max_dd, dd)
        
        return {
            'sharpe': round(sharpe, 2),
            'win_rate': round(win_rate, 3),
            'profit_factor': round(profit_factor, 2),
            'max_dd': round(max_dd, 3),
            'total_trades': len(trades),
            'avg_duration': round(np.mean([t['duration'] for t in trades]), 1)
        }
    
    def deflated_sharpe(self, sharpe: float, n_trials: int, 
                        skew: float = 0, kurtosis: float = 3,
                        sr = 0.0) -> float:
        """
        Calculate deflated Sharpe ratio to correct for multiple testing bias.
        Lo (2002) method.
        """
        # Simplified implementation
        # Full formula accounts for skewness, kurtosis, and number of trials
        adjustment = 1 + (skew * sharpe / 6) + ((kurtosis - 3) * sharpe**2 / 24)
        deflated = sharpe - (n_trials ** 0.5) * sr / n_trials
        return round(deflated * adjustment, 2)


if __name__ == '__main__':
    engine = BacktestEngine()
    print("Backtest engine ready")