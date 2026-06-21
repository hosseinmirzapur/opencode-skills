"""
Sentiment Analysis for Crypto Algo Trader
Uses CryptoBERT and FinBERT for market sentiment signals.
"""

from transformers import pipeline
from typing import List, Dict, Optional
import yaml


class SentimentAnalyzer:
    """
    Crypto Market Sentiment Analysis using HuggingFace models.
    Primary: kk08/CryptoBERT - fine-tuned on crypto sentiment
    Fallback: ProsusAI/finbert - financial sentiment
    """
    
    def __init__(self, config_path: str = 'scripts/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize sentiment pipelines
        try:
            self.crypto_bert = pipeline(
                'sentiment-analysis',
                model='kk08/CryptoBERT'
            )
        except Exception:
            self.crypto_bert = None
        
        try:
            self.finbert = pipeline(
                'sentiment-analysis',
                model='ProsusAI/finbert'
            )
        except Exception:
            self.finbert = None
    
    def analyze_text(self, text: str, model: str = 'crypto') -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Returns:
        - positive, negative, neutral scores (0-1)
        """
        if model == 'crypto' and self.crypto_bert:
            result = self.crypto_bert(text)[0]
            # CryptoBERT uses LABEL_0=negative, LABEL_1=positive
            label_map = {'LABEL_0': 'negative', 'LABEL_1': 'positive'}
            scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
            scores[label_map.get(result['label'], 'neutral')] = result['score']
            scores['confidence'] = result['score']
            return scores
        
        elif self.finbert:
            result = self.finbert(text)[0]
            scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
            scores[result['label']] = result['score']
            scores['confidence'] = result['score']
            return scores
        
        return {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34, 'confidence': 0.0}
    
    def analyze_multiple(self, texts: List[str], model: str = 'crypto') -> Dict[str, float]:
        """
        Analyze sentiment across multiple texts and aggregate.
        
        Returns:
        - net_sentiment: -1 (bearish) to +1 (bullish)
        - confidence: 0-1
        """
        if not texts:
            return {'net_sentiment': 0.0, 'confidence': 0.0}
        
        results = [self.analyze_text(t, model) for t in texts]
        
        avg_positive = sum(r['positive'] for r in results) / len(results)
        avg_negative = sum(r['negative'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        net = avg_positive - avg_negative
        
        return {
            'net_sentiment': round(net, 3),
            'confidence': round(avg_confidence, 3),
            'positive_pct': round(avg_positive, 3),
            'negative_pct': round(avg_negative, 3)
        }
    
    def detect_divergence(self, price_change: float, sentiment: float) -> bool:
        """
        Detect price-sentiment divergence.
        Price going up but sentiment down = potential reversal.
        """
        return (price_change > 0.02 and sentiment < -0.1) or \
               (price_change < -0.02 and sentiment > 0.1)


if __name__ == '__main__':
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "Bitcoin touches $29k, Ethereum set to explode!",
        "Crypto market crashes as regulation fears grow",
        "Neutral news about blockchain adoption"
    ]
    
    result = analyzer.analyze_multiple(test_texts)
    print(f"Net sentiment: {result['net_sentiment']}")