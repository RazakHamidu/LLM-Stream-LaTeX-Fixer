from flask import Flask, render_template, request, Response, stream_with_context
import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv, find_dotenv
import os 
from dotenv import load_dotenv

app = Flask(__name__)

# --- 1. CONFIGURAZIONE API ---
load_dotenv()
api_key = os.getenv("api_key")

genai.configure(api_key=api_key)

# --- 2. CONFIGURAZIONE MODELLO ---
# Definiamo le impostazioni di generazione
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

# Impostazioni di sicurezza (Safety Settings) - Opzionale: qui li lasciamo standard
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    generation_config=generation_config,
    safety_settings=safety_settings
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Se volessi gestire una chat con cronologia (multi-turn), dovresti passare
    # la 'history' dal frontend e usare model.start_chat(history=...)
    # Per questo esempio rimaniamo su single-turn (domanda -> risposta).

    def generate():
        try:
            response = model.generate_content(
                user_message, 
                stream=True
            )
            
            for chunk in response:
                try:
                    if chunk.text:
                        yield chunk.text
                except ValueError:
                    # Se entriamo qui, il chunk è stato bloccato dai filtri di sicurezza
                    print("Chunk bloccato dai filtri di sicurezza")
                    continue

        except Exception as e:
            yield f"\n[Errore API: {str(e)}]"

    # stream_with_context è fondamentale in Flask per mantenere il contesto
    # durante un loop lungo come quello di un LLM
    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)