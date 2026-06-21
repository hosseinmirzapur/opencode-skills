"""
Risk Management Layer for Crypto Algo Trader
Implements Fractional Kelly position sizing, VaR, Monte Carlo simulations.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from scipy.stats import norm
import yaml


class RiskManager:
    def __init__(self, config_path: str = 'scripts/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.daily_pnl = 0.0
        self.current_drawdown = 0.0
    
    def fractional_kelly(self, win_probability: float, win_loss_ratio: float) -> float:
        """
        Calculate fractional Kelly position size.
        
        f* = (bp - q) / b * k
        Where:
        - b = win_loss_ratio
        - p = win_probability
        - q = 1 - p
        - k = fractional coefficient (0.25 for safety)
        """
        k = self.config['risk']['kelly_fraction']
        p = win_probability
        b = win_loss_ratio
        q = 1 - p
        
        if b == 0:
            return 0.0
        
        f_star = (b * p - q) / b
        f_star = max(0, min(f_star * k, self.config['risk']['max_position_percent']))
        
        return f_star
    
    def calculate_atr_stop(self, atr: float, entry_price: float, 
                           regime: str, direction: str) -> float:
        """Calculate ATR-based stop loss."""
        multipliers = self.config['risk']['stop_loss_atr_multipliers']
        multiplier = multipliers.get(regime, 1.5)
        
        stop_distance = atr * multiplier
        if direction == 'BUY':
            return entry_price - stop_distance
        else:
            return entry_price + stop_distance
    
    def calculate_take_profit(self, entry_price: float, stop_loss: float,
                            confidence: float, direction: str) -> float:
        """Calculate take profit based on risk-reward ratio and confidence."""
        risk = abs(entry_price - stop_loss)
        
        # Select R:R based on confidence
        if confidence >= 0.9:
            rr = self.config['risk']['risk_reward_ratios']['high_confidence']
        elif confidence >= 0.7:
            rr = self.config['risk']['risk_reward_ratios']['medium_confidence']
        else:
            rr = self.config['risk']['risk_reward_ratios']['low_confidence']
        
        target = risk * rr
        
        if direction == 'BUY':
            return entry_price + target
        else:
            return entry_price - target
    
    def value_at_risk(self, returns: pd.Series, confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR) using parametric method.
        """
        mu = returns.mean()
        sigma = returns.std()
        var = -(mu + sigma * norm.ppf(1 - confidence))
        return var
    
    def monte_carlo_simulation(self, entry_price: float, stop_loss: float,
                               take_profit: float, mu: float, sigma: float,
                               n_simulations: int = 10000) -> Dict[str, float]:
        """
        Run Monte Carlo simulation to estimate SL/TP hit probabilities.
        Returns probability of hitting SL vs TP.
        """
        sl_hit = 0
        tp_hit = 0
        neither = 0
        
        for _ in range(n_simulations):
            # Simulate price path
            final_price = np.random.lognormal(mu, sigma)
            
            if final_price <= stop_loss:
                sl_hit += 1
            elif final_price >= take_profit:
                tp_hit += 1
            else:
                neither += 1
        
        return {
            'sl_probability': sl_hit / n_simulations,
            'tp_probability': tp_hit / n_simulations,
            'uncertainty': neither / n_simulations
        }
    
    def check_circuit_breaker(self, daily_loss: float, total_capital: float) -> bool:
        """Check if daily circuit breaker is triggered."""
        loss_pct = (daily_loss / total_capital) * 100
        
        if loss_pct <= -self.config['risk']['portfolio_limits']['daily_loss_limit_percent']:
            return True
        return False
    
    def calculate_position_size(self, signal_confidence: float, 
                                historical_data: pd.DataFrame,
                                current_price: float) -> float:
        """
        Full position sizing workflow.
        Returns position size as percentage of capital.
        """
        returns = historical_data['close'].pct_change().dropna()
        
        # Win probability (simplified: using positive return frequency)
        win_prob = (returns > 0).mean()
        # Average win/loss ratio
        avg_win = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0.01
        avg_loss = abs(returns[returns < 0].mean()) if len(returns[returns < 0]) > 0 else 0.01
        win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 1.0
        
        # Adjust for signal confidence
        adjusted_win_prob = min(1.0, win_prob * (1 + signal_confidence))
        
        return self.fractional_kelly(adjusted_win_prob, win_loss_ratio)


if __name__ == '__main__':
    rm = RiskManager()
    print("Risk Manager initialized with config")
    
    # Test Kelly calculation
    size = rm.fractional_kelly(0.55, 1.5)
    print(f"Sample position size: {size:.2f}%")