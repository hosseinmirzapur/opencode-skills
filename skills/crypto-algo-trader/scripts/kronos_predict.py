"""
Chronos-Tiny Predictor for Crypto Algo Trader
Uses Amazon Chronos-Tiny foundation model for time series forecasting.
Model: amazon/chronos-tiny (~80MB, runs on CPU)
"""

import numpy as np
from typing import Dict, Any, List


class ChronosPredictor:
    """
    Chronos-Tiny Foundation Model for Crypto Price Prediction.
    Lightweight time series forecasting model from Amazon.
    Pre-trained on diverse time series data including financial data.
    """

    def __init__(self, model_name: str = 'amazon/chronos-tiny'):
        self.model_name = model_name
        self.pipeline = None
        try:
            from chronos import ChronosPipeline
            self.pipeline = ChronosPipeline.from_pretrained(
                model_name,
                device_map='auto',
                torch_dtype='auto'
            )
        except ImportError:
            print("chronos package not installed. Install with: pip install chronos-forecast")
        except Exception as e:
            print(f"Chronos model loading fallback: {e}")

    def predict_direction(self, ohlcv_sequence: List[Dict]) -> Dict[str, Any]:
        """
        Predict price direction (UP/DOWN/SIDEWAYS).

        Returns:
        - direction: 'UP', 'DOWN', or 'SIDEWAYS'
        - confidence: 0-1 confidence score
        """
        prices = np.array([c['close'] for c in ohlcv_sequence[-120:]], dtype=np.float32)

        if self.pipeline is None:
            return self._momentum_fallback(prices)

        try:
            import torch
            context = torch.tensor(prices).unsqueeze(0)
            forecast = self.pipeline.predict(
                context=context,
                prediction_length=12,
                num_samples=20
            )

            median_forecast = forecast.squeeze().median(dim=0).values.numpy()
            current_price = prices[-1]
            predicted_price = float(median_forecast[-1])
            pct_change = (predicted_price - current_price) / current_price

            if pct_change > 0.005:
                direction = 'UP'
                confidence = min(0.5 + abs(pct_change) * 10, 0.85)
            elif pct_change < -0.005:
                direction = 'DOWN'
                confidence = min(0.5 + abs(pct_change) * 10, 0.85)
            else:
                direction = 'SIDEWAYS'
                confidence = 0.55

            return {'direction': direction, 'confidence': round(confidence, 2)}

        except Exception as e:
            print(f"Chronos prediction error: {e}")
            return self._momentum_fallback(prices)

    def _momentum_fallback(self, prices: np.ndarray) -> Dict[str, Any]:
        """Fallback: simple momentum when model unavailable."""
        if len(prices) < 20:
            return {'direction': 'SIDEWAYS', 'confidence': 0.5}

        recent = prices[-20:]
        momentum = (recent[-1] - recent[0]) / recent[0]

        if momentum > 0.02:
            return {'direction': 'UP', 'confidence': 0.6}
        elif momentum < -0.02:
            return {'direction': 'DOWN', 'confidence': 0.6}
        else:
            return {'direction': 'SIDEWAYS', 'confidence': 0.55}

    def predict_4h_range(self, ohlcv_sequence: List[Dict]) -> Dict[str, float]:
        """
        Predict 4-hour price range.
        Returns low and high bounds.
        """
        prices = np.array([c['close'] for c in ohlcv_sequence[-120:]], dtype=np.float32)
        current_price = prices[-1]

        if self.pipeline is None:
            volatility = np.std(np.diff(prices[-20:]) / prices[-20:-1])
            range_percent = volatility * 2
            return {
                'low': current_price * (1 - range_percent),
                'high': current_price * (1 + range_percent)
            }

        try:
            import torch
            context = torch.tensor(prices).unsqueeze(0)
            forecast = self.pipeline.predict(
                context=context,
                prediction_length=12,
                num_samples=20
            )

            all_samples = forecast.squeeze().numpy()
            low = float(np.percentile(all_samples[:, -1], 5))
            high = float(np.percentile(all_samples[:, -1], 95))

            return {'low': low, 'high': high}

        except Exception:
            volatility = np.std(np.diff(prices[-20:]) / prices[-20:-1])
            range_percent = volatility * 2
            return {
                'low': current_price * (1 - range_percent),
                'high': current_price * (1 + range_percent)
            }


if __name__ == '__main__':
    predictor = ChronosPredictor()
    print("Chronos-Tiny predictor ready for inference")
