# Arquivo: app/sentiment_handler.py
from textblob import TextBlob
import emoji
import re

class SentimentHandler:
    def __init__(self):
        # Dicionário de emojis para sentimento
        self.emoji_sentiments = {
            '😊': 1.0, '😃': 1.0, '😄': 1.0, '😁': 0.8,
            '😢': -1.0, '😭': -1.0, '😞': -0.8, '😟': -0.8,
            '😐': 0.0, '🤔': 0.0, '😕': -0.3,
            '❤️': 1.0, '💕': 1.0, '👍': 0.8, '👎': -0.8
        }
        
        # Palavras de sentimento em português
        self.sentiment_words = {
            'positivas': {
                'ótimo': 1.0, 'excelente': 1.0, 'maravilhoso': 1.0,
                'bom': 0.8, 'legal': 0.7, 'bacana': 0.7,
                'feliz': 0.9, 'alegre': 0.8, 'contente': 0.7
            },
            'negativas': {
                'péssimo': -1.0, 'horrível': -1.0, 'terrível': -1.0,
                'ruim': -0.8, 'chato': -0.7, 'triste': -0.8,
                'irritado': -0.9, 'bravo': -0.8, 'furioso': -1.0
            }
        }

    def extract_emojis(self, text):
        """Extrai emojis do texto"""
        return [c for c in text if c in emoji.EMOJI_DATA]

    def analyze_detailed(self, text):
        """Análise detalhada de sentimento"""
        # Análise básica com TextBlob
        blob = TextBlob(text)
        base_sentiment = blob.sentiment.polarity

        # Análise de emojis
        emojis = self.extract_emojis(text)
        emoji_sentiment = sum(self.emoji_sentiments.get(e, 0) for e in emojis)

        # Análise de palavras-chave em português
        text_lower = text.lower()
        words = re.findall(r'\w+', text_lower)
        
        word_sentiment = 0
        for word in words:
            word_sentiment += self.sentiment_words['positivas'].get(word, 0)
            word_sentiment += self.sentiment_words['negativas'].get(word, 0)

        # Combina os diferentes aspectos da análise
        combined_sentiment = (base_sentiment + emoji_sentiment + word_sentiment) / 3

        # Determina a intensidade e categoria
        intensity = abs(combined_sentiment)
        if combined_sentiment > 0:
            category = 'muito positivo' if intensity > 0.7 else 'positivo' if intensity > 0.3 else 'levemente positivo'
        elif combined_sentiment < 0:
            category = 'muito negativo' if intensity > 0.7 else 'negativo' if intensity > 0.3 else 'levemente negativo'
        else:
            category = 'neutro'

        return {
            'score': combined_sentiment,
            'category': category,
            'intensity': intensity,
            'components': {
                'text_sentiment': base_sentiment,
                'emoji_sentiment': emoji_sentiment,
                'word_sentiment': word_sentiment
            },
            'emojis_found': emojis
        }