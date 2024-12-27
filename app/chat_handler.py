# Arquivo: app/chat_handler.py
class ChatHandler:
    def __init__(self):
        from app.responses import responses
        self.responses = responses
    
    def get_response(self, message):
        message = message.lower().strip()
        
        # Verifica se há uma resposta exata para a mensagem
        if message in self.responses:
            return self.responses[message]
        
        # Procura por palavras-chave nas mensagens
        for key in self.responses:
            if key in message:
                return self.responses[key]
        
        # Resposta padrão se nenhuma correspondência for encontrada
        return "Desculpe, não entendi. Pode reformular sua pergunta?"