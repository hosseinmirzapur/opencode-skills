"""
Sentiment Analysis for Crypto Algo Trader
Uses VADER + TextBlob for lightweight, CPU-only sentiment analysis.
No GPU or large model downloads required.
"""

from typing import List, Dict
import yaml


class SentimentAnalyzer:
    """
    Crypto Market Sentiment Analysis using VADER + TextBlob.
    Primary: VADER - rule-based, optimized for social media text
    Secondary: TextBlob - pattern-based sentiment with subjectivity
    """

    def __init__(self, config_path: str = 'scripts/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.vader = None
        self.textblob = None

        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader = SentimentIntensityAnalyzer()
        except ImportError:
            print("vaderSentiment not installed. Install with: pip install vaderSentiment")

        try:
            from textblob import TextBlob
            self.textblob = TextBlob
        except ImportError:
            print("textblob not installed. Install with: pip install textblob")

    def analyze_text(self, text: str, model: str = 'vader') -> Dict[str, float]:
        """
        Analyze sentiment of a single text.

        Returns:
        - positive, negative, neutral scores (0-1)
        - compound: -1 to +1 overall sentiment
        """
        scores = {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34, 'confidence': 0.0}

        if self.vader:
            vader_scores = self.vader.polarity_scores(text)
            compound = vader_scores['compound']

            if compound >= 0.05:
                scores['positive'] = min(0.5 + compound * 0.5, 1.0)
                scores['negative'] = 0.0
                scores['neutral'] = 1.0 - scores['positive']
            elif compound <= -0.05:
                scores['negative'] = min(0.5 + abs(compound) * 0.5, 1.0)
                scores['positive'] = 0.0
                scores['neutral'] = 1.0 - scores['negative']
            else:
                scores['neutral'] = 0.7
                scores['positive'] = 0.15
                scores['negative'] = 0.15

            scores['compound'] = compound
            scores['confidence'] = abs(compound)

        if self.textblob:
            blob = self.textblob(text)
            tb_polarity = blob.sentiment.polarity

            if self.vader:
                blended = (scores['compound'] + tb_polarity) / 2
                scores['compound'] = blended
                scores['confidence'] = (scores['confidence'] + abs(tb_polarity)) / 2
            else:
                scores['compound'] = tb_polarity
                scores['confidence'] = abs(tb_polarity)

                if tb_polarity > 0.05:
                    scores['positive'] = min(0.5 + tb_polarity * 0.5, 1.0)
                    scores['negative'] = 0.0
                    scores['neutral'] = 1.0 - scores['positive']
                elif tb_polarity < -0.05:
                    scores['negative'] = min(0.5 + abs(tb_polarity) * 0.5, 1.0)
                    scores['positive'] = 0.0
                    scores['neutral'] = 1.0 - scores['negative']
                else:
                    scores['neutral'] = 0.7
                    scores['positive'] = 0.15
                    scores['negative'] = 0.15

        return scores

    def analyze_multiple(self, texts: List[str], model: str = 'vader') -> Dict[str, float]:
        """
        Analyze sentiment across multiple texts and aggregate.

        Returns:
        - net_sentiment: -1 (bearish) to +1 (bullish)
        - confidence: 0-1
        """
        if not texts:
            return {'net_sentiment': 0.0, 'confidence': 0.0}

        results = [self.analyze_text(t, model) for t in texts]

        avg_compound = sum(r.get('compound', 0) for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        avg_positive = sum(r['positive'] for r in results) / len(results)
        avg_negative = sum(r['negative'] for r in results) / len(results)

        return {
            'net_sentiment': round(avg_compound, 3),
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
