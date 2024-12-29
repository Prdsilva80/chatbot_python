# Arquivo: app/routes.py
from flask import Blueprint, request, jsonify
from app.chat_handler import ChatHandler
from flask import render_template_string

main = Blueprint('main', __name__)
chat_handler = ChatHandler()

# Arquivo: app/routes.py
@main.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Mensagem não fornecida'
            }), 400
        
        message = data['message']
        response = chat_handler.get_response(message)
        
        # Análises completas
        nlp_info = chat_handler.nlp_handler.process_message(message)
        ml_info = chat_handler.ml_handler.predict_intent(message)
        sentiment_info = chat_handler.sentiment_handler.analyze_detailed(message)
        
        return jsonify({
            'response': response,
            'analysis': {
                'nlp': {
                    'entities': nlp_info['entities'],
                    'tokens': nlp_info['tokens'][:5]
                },
                'ml': {
                    'intent': ml_info['intent'],
                    'confidence': ml_info['confidence']
                },
                'sentiment': {
                    'category': sentiment_info['category'],
                    'score': sentiment_info['score'],
                    'intensity': sentiment_info['intensity'],
                    'emojis': sentiment_info['emojis_found']
                }
            }
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Serviço está funcionando corretamente'
    })

@main.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chatbot Python</title>
        <style>
            #chat-container { margin: 20px; max-width: 600px; }
            #messages { height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
            #input-container { display: flex; }
            #message-input { flex-grow: 1; margin-right: 10px; padding: 5px; }
        </style>
    </head>
    <body>
        <div id="chat-container">
            <div id="messages"></div>
            <div id="input-container">
                <input type="text" id="message-input" placeholder="Digite sua mensagem...">
                <button onclick="sendMessage()">Enviar</button>
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                if (!message) return;

                displayMessage('Você: ' + message);
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    displayMessage('Bot: ' + data.response);
                })
                .catch(error => {
                    displayMessage('Erro: ' + error);
                });

                input.value = '';
            }

            function displayMessage(message) {
                const messages = document.getElementById('messages');
                messages.innerHTML += '<div>' + message + '</div>';
                messages.scrollTop = messages.scrollHeight;
            }

            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)