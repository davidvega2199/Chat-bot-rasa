from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Ruta para servir el archivo HTML (index.html).
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para manejar las interacciones con el chatbot.
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Envía el mensaje del usuario al servidor de Rasa a través de una solicitud POST.
    rasa_response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "user", "message": user_message}
    )

    # Procesa la respuesta de Rasa
    if rasa_response.status_code == 200:
        rasa_responses = rasa_response.json()
        
        # Inicializa las variables para almacenar el texto de respuesta y los botones
        bot_response = ""
        buttons = []

        # Recorre la respuesta de Rasa para extraer el texto y los botones
        for rasa_response in rasa_responses:
            if "text" in rasa_response:
                bot_response += rasa_response["text"] + " "
            if "buttons" in rasa_response:
                buttons = rasa_response["buttons"]

        # Devuelve la respuesta en el formato esperado por el frontend
        return jsonify({
            "bot_response": bot_response.strip(),
            "buttons": buttons
        })
    else:
        # Maneja los errores si Rasa no responde correctamente
        return jsonify({"error": "Error connecting to Rasa"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)