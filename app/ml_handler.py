# Arquivo: app/ml_handler.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

class MLHandler:
    def __init__(self):
        self.model_path = 'models/intent_classifier.joblib'
        self.pipeline = None
        self.initialize_model()
    
    def initialize_model(self):
        # Dados de treinamento inicial
        training_data = [
            # Saudações
            ("olá", "greeting"),
            ("oi", "greeting"),
            ("bom dia", "greeting"),
            ("boa tarde", "greeting"),
            ("boa noite", "greeting"),
            
            # Despedidas
            ("tchau", "goodbye"),
            ("até logo", "goodbye"),
            ("adeus", "goodbye"),
            
            # Perguntas sobre o bot
            ("quem é você", "about_bot"),
            ("o que você faz", "about_bot"),
            ("como você funciona", "about_bot"),
            
            # Agradecimentos
            ("obrigado", "thanks"),
            ("valeu", "thanks"),
            ("agradeço", "thanks"),
            
            # Ajuda
            ("preciso de ajuda", "help"),
            ("pode me ajudar", "help"),
            ("como faço para", "help"),
            
            # Humor
            ("estou feliz", "mood"),
            ("estou triste", "mood"),
            ("tudo bem", "mood"),
            
            # Informações técnicas
            ("como programar", "technical"),
            ("o que é python", "technical"),
            ("machine learning", "technical")
        ]
        
        X, y = zip(*training_data)
        
        # Cria o pipeline de ML
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
            ('clf', MultinomialNB())
        ])
        
        # Treina o modelo
        self.pipeline.fit(X, y)
        
        # Salva o modelo
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.pipeline, self.model_path)
    
    def predict_intent(self, text):
        if self.pipeline is None:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
            else:
                self.initialize_model()
        
        # Prediz a intenção
        intent = self.pipeline.predict([text])[0]
        
        # Obtém probabilidades
        proba = self.pipeline.predict_proba([text])[0]
        confidence = max(proba)
        
        return {
            'intent': intent,
            'confidence': float(confidence)
        }
    
    def train(self, texts, labels):
        """
        Treina o modelo com novos dados
        """
        if self.pipeline is None:
            self.initialize_model()
        
        # Treina com novos dados
        self.pipeline.fit(texts, labels)
        
        # Salva o modelo atualizado
        joblib.dump(self.pipeline, self.model_path)