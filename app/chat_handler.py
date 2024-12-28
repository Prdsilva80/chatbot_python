# Arquivo: app/chat_handler.py
from app.nlp_handler import NLPHandler
from app.ml_handler import MLHandler

class ChatHandler:
    def __init__(self):
        from app.responses import responses
        self.responses = responses
        self.nlp_handler = NLPHandler()
        self.ml_handler = MLHandler()
    
    def get_response(self, message):
        # Processa a mensagem com NLP
        nlp_result = self.nlp_handler.process_message(message)
        
        # Obtém a intenção usando ML
        ml_result = self.ml_handler.predict_intent(message)
        
        # Lógica de resposta baseada na intenção
        intent = ml_result['intent']
        confidence = ml_result['confidence']
        
        # Se a confiança for alta, usa resposta baseada na intenção
        if confidence > 0.6:
            if intent == "greeting":
                return "Olá! Como posso ajudar você hoje?"
            elif intent == "goodbye":
                return "Até logo! Tenha um ótimo dia!"
            elif intent == "about_bot":
                return "Sou um chatbot com recursos de ML e NLP, criado para ajudar e aprender!"
            elif intent == "thanks":
                return "Por nada! Fico feliz em ajudar!"
            elif intent == "help":
                return "Claro! Me diga mais especificamente como posso ajudar."
            elif intent == "mood":
                sentiment = nlp_result['sentiment']
                if sentiment == 'positive':
                    return "Que bom que você está bem! Posso ajudar em algo?"
                elif sentiment == 'negative':
                    return "Sinto muito que você não esteja bem. Quer conversar sobre isso?"
                else:
                    return "Entendo. Como posso ajudar você hoje?"
            elif intent == "technical":
                return "Posso ajudar com informações técnicas. Qual é sua dúvida específica?"
        
        # Se a confiança for baixa, usa a lógica anterior
        message = message.lower().strip()
        
        if message in self.responses:
            return self.responses[message]
        
        # Procura por palavras-chave nas mensagens
        for key in self.responses:
            if key in message:
                return self.responses[key]
        
        # Resposta padrão
        return "Desculpe, não entendi completamente. Pode reformular sua pergunta?"