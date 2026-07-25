import os
from flask import Flask, request
import requests

app = Flask(__name__)

# ======== CONFIGURACION (rellena esto con tus datos) ========
VERIFY_TOKEN = "camino2026"  # este lo inventas tu, luego lo usaras en el panel de Meta
# ==============================================================


@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    """
    Facebook llama a esta ruta UNA VEZ cuando configuras el webhook
    en el panel de Meta, para confirmar que el servidor es tuyo.
    """
    modo = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if modo == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado correctamente.")
        return challenge, 200
    else:
        return "Token de verificacion invalido", 403


@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    """
    Aqui llegan los mensajes reales de los clientes desde Messenger.
    """
    data = request.get_json()
    print("Mensaje recibido:", data)

    if data.get("object") == "page":
        for entrada in data.get("entry", []):
            for evento in entrada.get("messaging", []):
                sender_id = evento["sender"]["id"]

                if "message" in evento and "text" in evento["message"]:
                    texto_cliente = evento["message"]["text"]
                    print(f"Cliente {sender_id} escribio: {texto_cliente}")

                    # --- ACA VA LA LOGICA DE RESPUESTA ---
                    # Por ahora, un "echo" simple de prueba:
                    respuesta = f"Recibi tu mensaje: {texto_cliente}"
                    enviar_mensaje(sender_id, respuesta)

    return "ok", 200


def enviar_mensaje(destinatario_id, texto):
    """
    Envia un mensaje de texto a un cliente usando el Send API de Meta.
    """
    url = "https://graph.facebook.com/v21.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": destinatario_id},
        "message": {"text": texto},
    }
    respuesta = requests.post(url, params=params, json=payload)
    print("Respuesta de Facebook:", respuesta.status_code, respuesta.text)



if __name__ == "__main__":
    app.run(port=5000, debug=True)


