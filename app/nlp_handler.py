# Arquivo: app/nlp_handler.py
import spacy

class NLPHandler:
    def __init__(self):
        self.nlp = spacy.load('pt_core_news_sm')
        
    def process_message(self, message):
        # Processa a mensagem com spaCy
        doc = self.nlp(message)
        
        # Extrai informações relevantes
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        tokens = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]
        
        return {
            'original': message,
            'entities': entities,
            'tokens': tokens,
            'lemmas': lemmas,
            'sentiment': self._analyze_sentiment(doc)
        }
    
    def _analyze_sentiment(self, doc):
        # Análise de sentimento simples baseada em palavras positivas/negativas
        positive_words = {'bom', 'ótimo', 'excelente', 'feliz', 'alegre', 'legal'}
        negative_words = {'ruim', 'péssimo', 'triste', 'chato', 'difícil'}
        
        text_lower = doc.text.lower()
        
        if any(word in text_lower for word in positive_words):
            return 'positive'
        elif any(word in text_lower for word in negative_words):
            return 'negative'
        return 'neutral'
    
    def get_main_topics(self, message):
        doc = self.nlp(message)
        # Retorna substantivos e entidades nomeadas como tópicos principais
        return [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]