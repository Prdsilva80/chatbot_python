# Arquivo: app/chat_handler.py
from app.nlp_handler import NLPHandler

class ChatHandler:
    def __init__(self):
        from app.responses import responses
        self.responses = responses
        self.nlp_handler = NLPHandler()
    
    def get_response(self, message):
        # Processa a mensagem com NLP
        nlp_result = self.nlp_handler.process_message(message)
        
        # Verifica sentimento
        sentiment = nlp_result['sentiment']
        
        # Procura por entidades nomeadas
        entities = nlp_result['entities']
        
        # Procura por tópicos principais
        topics = self.nlp_handler.get_main_topics(message)
        
        # Lógica de resposta melhorada
        message = message.lower().strip()
        
        # Responde baseado em entidades encontradas
        if entities:
            for entity, label in entities:
                if label == 'PER':  # Pessoa
                    return f"Você mencionou {entity}. Infelizmente não tenho informações específicas sobre pessoas."
                elif label == 'LOC':  # Local
                    return f"Você mencionou o local {entity}. Gostaria de saber algo específico sobre ele?"
        
        # Responde baseado no sentimento
        if sentiment == 'positive' and message not in self.responses:
            return "Que bom que você está com um sentimento positivo! Como posso ajudar a manter esse astral?"
        elif sentiment == 'negative' and message not in self.responses:
            return "Sinto muito por você estar se sentindo assim. Posso tentar ajudar de alguma forma?"
        
        # Verifica se há uma resposta exata
        if message in self.responses:
            return self.responses[message]
        
        # Procura por palavras-chave nas mensagens
        for key in self.responses:
            if key in message:
                return self.responses[key]
        
        # Se encontrou tópicos mas não tem resposta específica
        if topics:
            return f"Vejo que você está falando sobre {', '.join(topics)}. Pode elaborar melhor sua pergunta?"
        
        # Resposta padrão
        return "Desculpe, não entendi completamente. Pode reformular sua pergunta?"