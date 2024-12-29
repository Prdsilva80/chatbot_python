# Arquivo: app/chat_handler.py
from app.nlp_handler import NLPHandler
from app.ml_handler import MLHandler
from app.sentiment_handler import SentimentHandler

class ChatHandler:
    def __init__(self):
        from app.responses import responses
        self.responses = responses
        self.nlp_handler = NLPHandler()
        self.ml_handler = MLHandler()
        self.sentiment_handler = SentimentHandler()
        
        # Respostas baseadas em intenções
        self.intent_responses = {
            "greeting": [
                "Olá! Como posso ajudar você hoje?",
                "Oi! Em que posso ser útil?",
                "Olá! É um prazer conversar com você!"
            ],
            "goodbye": [
                "Até logo! Foi um prazer conversar com você!",
                "Tchau! Tenha um ótimo dia!",
                "Até mais! Volte sempre que precisar!"
            ],
            "thanks": [
                "Por nada! Estou aqui para ajudar!",
                "É um prazer poder ajudar!",
                "Fico feliz em ser útil!"
            ],
            "help": [
                "Claro! Me diga como posso ajudar.",
                "Estou aqui para isso! Qual sua dúvida?",
                "Vou fazer o possível para ajudar. O que você precisa?"
            ],
            "about_bot": [
                "Sou um chatbot com recursos de ML e NLP, criado para ajudar e aprender!",
                "Sou um assistente virtual que usa inteligência artificial para conversar e ajudar!",
                "Sou um programa desenvolvido para interagir e auxiliar de forma inteligente!"
            ],
            "technical": [
                "Posso ajudar com informações técnicas. Qual é sua dúvida específica?",
                "Tenho conhecimento técnico para compartilhar. O que quer saber?",
                "Estou preparado para discutir assuntos técnicos. Em que posso ajudar?"
            ]
        }
        
        # Respostas baseadas em sentimento
        self.sentiment_responses = {
            "muito_positivo": [
                "Que maravilha ver você tão animado! Seu entusiasmo é contagiante!",
                "Adorei seu alto astral! Vamos manter essa energia positiva!",
                "Sua alegria é inspiradora! Como posso contribuir para esse momento?"
            ],
            "positivo": [
                "Que bom que você está bem! Posso ajudar em algo?",
                "É ótimo ver você com esse ânimo! Como posso ser útil?",
                "Seu humor positivo torna nossa conversa ainda melhor!"
            ],
            "neutro": [
                "Como posso tornar seu dia melhor?",
                "Estou aqui para ajudar no que precisar.",
                "Em que posso ser útil hoje?"
            ],
            "negativo": [
                "Sinto que algo não está bem. Quer conversar sobre isso?",
                "Posso tentar ajudar a melhorar seu dia. O que está acontecendo?",
                "Estou aqui para ouvir e tentar ajudar no que puder."
            ],
            "muito_negativo": [
                "Sinto muito que você esteja passando por isso. Estou aqui para ajudar.",
                "Sua situação parece difícil. Quer compartilhar mais sobre o que está sentindo?",
                "Compreendo sua frustração. Como posso tentar ajudar?"
            ]
        }

    def get_response(self, message):
        # Análise completa
        nlp_result = self.nlp_handler.process_message(message)
        ml_result = self.ml_handler.predict_intent(message)
        sentiment_result = self.sentiment_handler.analyze_detailed(message)
        
        # Extrai informações principais
        sentiment_category = sentiment_result['category']
        sentiment_intensity = sentiment_result['intensity']
        intent = ml_result['intent']
        confidence = ml_result['confidence']
        
        # 1. Verifica sentimentos fortes
        if sentiment_intensity > 0.7:
            if 'muito positivo' in sentiment_category:
                from random import choice
                return choice(self.sentiment_responses["muito_positivo"])
            elif 'muito negativo' in sentiment_category:
                from random import choice
                return choice(self.sentiment_responses["muito_negativo"])
        
        # 2. Verifica intenções com alta confiança
        if confidence > 0.6:
            if intent in self.intent_responses:
                from random import choice
                return choice(self.intent_responses[intent])
        
        # 3. Verifica entidades nomeadas
        entities = nlp_result.get('entities', [])
        for entity, label in entities:
            if label == 'PER':
                return f"Você mencionou {entity}. Infelizmente não tenho informações específicas sobre pessoas."
            elif label == 'LOC':
                return f"Você mencionou o local {entity}. Gostaria de saber algo específico sobre ele?"
            elif label == 'ORG':
                return f"Você mencionou {entity}. Posso tentar buscar informações sobre essa organização."
        
        # 4. Verifica respostas exatas
        message_lower = message.lower().strip()
        if message_lower in self.responses:
            return self.responses[message_lower]
        
        # 5. Busca por palavras-chave
        for key in self.responses:
            if key in message_lower:
                return self.responses[key]
        
        # 6. Resposta baseada no sentimento geral
        if 'positivo' in sentiment_category:
            from random import choice
            return choice(self.sentiment_responses["positivo"])
        elif 'negativo' in sentiment_category:
            from random import choice
            return choice(self.sentiment_responses["negativo"])
        
        # 7. Resposta padrão
        return "Entendi sua mensagem, mas não tenho uma resposta específica. Pode reformular de outra forma?"

    def get_detailed_analysis(self, message):
        """Retorna análise detalhada da mensagem"""
        return {
            'nlp': self.nlp_handler.process_message(message),
            'ml': self.ml_handler.predict_intent(message),
            'sentiment': self.sentiment_handler.analyze_detailed(message)
        }