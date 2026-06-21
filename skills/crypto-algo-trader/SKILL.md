---
name: crypto-algo-trader
description: Use when generating professional algorithmic trading signals for cryptocurrencies with ML models, technical analysis, risk management, and backtesting. Provides entry points, SL/TP, position sizing, and confidence scores for BTC/ETH day trading.
---

# Crypto Algo Trader — Institutional-Grade Trading Signals

**Professional algorithmic trading skill for cryptocurrency markets with multi-model ML ensemble, market regime detection, and institutional risk management.**

---

## When To Use

- User wants trading signals for BTC or ETH with entry price, stop loss, take profit, and position sizing
- Need ML-powered price predictions using state-of-the-art models (Kronos, XGBoost, LSTM)
- Want to combine technical analysis, sentiment, and market microstructure signals
- Require paper trading or backtesting before live execution
- Risk management is critical (Kelly criterion, VaR, Monte Carlo simulations)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     SIGNAL GENERATION                       │
├───────────────┬───────────────┬───────────────┬─────────────┤
│  Technical    │      ML       │   Sentiment   │   Order     │
│   Analysis    │   Ensemble    │   Analysis    │  Flow/Micro │
└───────────────┴───────────────┴───────────────┴─────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   WEIGHTED CONFLUENCE   │
              │    Multi-timeframe      │
              └────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  RISK MANAGEMENT LAYER                       │
├───────────────┬───────────────┬───────────────┬─────────────┤
│   Position    │     Stop      │   Take Profit │  Portfolio  │
│   Sizing      │     Loss      │               │   Limits    │
│  (Kelly)      │   (ATR-based) │  (RR: 1:2+)  │             │
└───────────────┴───────────────┴───────────────┴─────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKTESTING ENGINE                        │
│          Walk-forward, Purged CV, Deflated Sharpe             │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Market Regime Detection

Before any signal, classify the market state:

| Regime | Detection Method | Impact |
|--------|-----------------|--------|
| **TRENDING_UP** | HMM + Hurst > 0.5 + ADX > 25 | Favor momentum, wider stops |
| **TRENDING_DOWN** | HMM + Hurst > 0.5 + ADX > 25 | Favor shorts/bearish signals |
| **RANGING** | HMM + Hurst < 0.4 + Bollinger squeeze | Favor mean-reversion, tight stops |
| **VOLATILE** | ATR 90th percentile + Volume spike | Reduce position size by 50% |
| **ILLIQUID** | Spread > 0.5% + Book depth < 1k | Wait, don't trade |

**Implementation:** See `scripts/regime_detector.py`

---

## 2. Signal Generation Layer

### 2a. Technical Analysis Signals (TA-Lib)

| Indicator | Purpose | Signal |
|-----------|---------|--------|
| **KAMA** | Adaptive moving average, no lag | Trend direction |
| **VWAP** | Volume-weighted average | Institutional value |
| **CVD** | Cumulative volume delta | Order flow imbalance |
| **Market Profile** | Volume distribution | Support/resistance |
| **Fisher Transform** | Normalized momentum | Overbought/oversold |
| **Schaff Trend Cycle** | Faster MACD-like signal | Trend changes |
| **Chandelier Exit** | Volatility stop | Risk reference |

### 2b. ML Ensemble Signals

| Model | Framework | Output |
|-------|-----------|--------|
| **XGBoost + Bayesian Opt** | Feature-based | Buy/Sell/Hold + confidence |
| **LSTM with Attention** | Sequence modeling | Next price direction |
| **Temporal Fusion Transformer** | Multi-horizon | Probabilistic forecast |
| **LightGBM Quantile** | Uncertainty | Price range (5th–95th) |
| **Stacking Ensemble** | Meta-learner | Weighted signal combination |

**Features used:** OHLCV, returns, volume, technical indicators, on-chain metrics, sentiment, macro data.

### 2c. Kronos Foundation Model (HF: shiyu-coder/Kronos)

- Pre-trained on 45+ exchanges of candlestick data
- Tokenizer converts OHLCV to discrete tokens
- Direction prediction with 58-65% accuracy on hourly crypto
- Used as primary directional signal
- **See `scripts/kronos_predict.py`**

### 2d. Sentiment Signals (HF Models)

| Model | Specialization |
|-------|----------------|
| **kk08/CryptoBERT** | Crypto-specific sentiment |
| **ProsusAI/finbert** | Financial sentiment (fallback) |

Process:
1. Fetch headlines, tweets, Reddit posts
2. Run through CryptoBERT
3. Aggregate hourly sentiment index
4. Detect divergence: price up + sentiment down = reversal

### 2e. Multi-Timeframe Confluence

```
Signal weight matrix:
15m: 0.2  (confirmation)
1h:  0.5  (primary)
4h:  0.3  (context)

Final confidence = Σ(weighted_signal × weight)
Only trade if:
- confidence > 0.65
- minimum 3/5 signal generators agree
- regime allows the signal type
```

---

## 3. Risk Management Layer

### Position Sizing (Fractional Kelly)

```
f* = (bp - q) / b * k
Where:
- b = win/loss ratio
- p = win probability
- q = 1 - p
- k = 0.25 (fractional for safety)

Position % = min(f*, 5%)  # Max 5% per trade
```

### Stop Loss

```
ATR(14) × multiplier
Multiplier by regime:
- Trending: 1.5
- Ranging: 1.0
- Volatile: 2.0
```

### Take Profit

```
Minimum R:R = 1:2
Position-based:
- 70-80% confidence: 1:2 R:R
- 80-90% confidence: 1:3 R:R
- 90%+ confidence: 1:4 R:R + trailing
```

### Portfolio-Level Protection

| Rule | Threshold |
|------|-----------|
| Max open positions | 2 (BTC/ETH) |
| Daily circuit breaker | -5% → halt 24h |
| Drawdown kill switch | -15% → halt 7 days |
| Max correlated exposure | 1 long + 1 short max |

---

## 4. Backtesting Engine

### Methodology

```
1. Walk-Forward Optimization:
   - Train: 60 days
   - Test: 10 days
   - Slide forward, repeat
   
2. Purged Cross-Validation:
   - No data leakage between train/test
   - 1-day purge between windows
   
3. Deflated Sharpe Ratio:
   - Corrects for multiple-testing bias
   - Realistic performance expectation
```

### Metrics Computed

- Sharpe Ratio (risk-adjusted returns)
- Sortino Ratio (downside risk)
- Calmar Ratio (drawdown-adjusted)
- Win Rate (%)
- Profit Factor
- Max Drawdown
- Average Hold Time

**See `scripts/backtest_engine.py`**

---

## 5. Output Format

### Structured JSON

```json
{
  "symbol": "BTC/USDT",
  "action": "BUY",
  "entry_price": 68420.50,
  "stop_loss": 67210.00,
  "take_profit": 70840.00,
  "position_size_percent": 12.5,
  "confidence": 0.73,
  "risk_reward_ratio": 2.1,
  "regime": "TRENDING_UP",
  "timeframe": "1h",
  "signals": {
    "kronos": {"direction": "UP", "confidence": 0.68},
    "xgboost": {"direction": "UP", "confidence": 0.71},
    "lstm": {"direction": "UP", "confidence": 0.65},
    "technical": {"direction": "UP", "confidence": 0.60}
  },
  "reasoning": "Kronos (68%), XGBoost (71%), LSTM (65%) all agree on bullish direction...",
  "timestamp": "2026-06-22T01:00:00Z"
}
```

---

## 6. Scripts Directory

```
scripts/
  data_pipeline.py        # OHLCV, news, on-chain data fetch
  regime_detector.py      # HMM + Hurst + Liquidity detection
  ta_signals.py          # Technical indicators (TA-Lib)
  ml_ensemble.py         # XGBoost + LSTM + TFT training/inference
  kronos_predict.py      # HF Kronos model inference
  sentiment.py           # CryptoBERT sentiment analysis
  risk_manager.py        # Kelly, VaR, Monte Carlo, circuit breakers
  backtest_engine.py     # Walk-forward, purged CV, metrics
  config.yaml           # Parameters file
  requirements.txt       # Dependencies
```

---

## 7. HuggingFace Models Reference

| Model | Use Case | HF Link |
|-------|----------|---------|
| **shiyu-coder/Kronos** | Candlestick pattern prediction | https://huggingface.co/shiyu-coder/Kronos |
| **kk08/CryptoBERT** | Crypto sentiment analysis | https://huggingface.co/kk08/CryptoBERT |
| **ProsusAI/finbert** | Financial sentiment (fallback) | https://huggingface.co/ProsusAI/finbert |
| **amazon/chronos-2** | Time series forecasting | https://huggingface.co/amazon/chronos-2 |
| **ibm-granite/TTM-R1** | Time series transformer | https://huggingface.co/ibm-granite/TTM-R1 |

---

## 8. Common Mistakes to Avoid

1. **Trading without regime detection** — same strategy in all market conditions
2. **Ignoring execution costs** — slippage and fees destroy backtest profits
3. **Overfitting to historical data** — walk-forward prevents this
4. **Position sizing too large** — Kelly means you survive to compound
5. **No daily stop loss** — emotions kill trading accounts
6. **Blindly following ML signals** — always check confluence across models

---

## Quick Reference Card

| Step | Action |
|------|--------|
| 1 | Detect market regime (HMM + Hurst) |
| 2 | Generate 5 parallel signals (TA+ML+Sentiment) |
| 3 | Weigh by timeframe (15m/1h/4h) |
| 4 | Check confluence (min 3/5 agreement) |
| 5 | Calculate position size (fractional Kelly) |
| 6 | Set SL (ATR-based) |
| 7 | Set TP (R:R 1:2+ based on confidence) |
| 8 | Validate portfolio limits |
| 9 | Output structured JSON + explanation |
| 10 | Log for backtesting/review |

---

*This skill uses institutional-grade methods: HMM regime detection, Fractional Kelly sizing, walk-forward optimization, and HF foundation models. Test thoroughly with paper trading before live deployment.*