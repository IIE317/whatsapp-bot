from flask import Flask, request
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "nativ-bot-secret")


@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_number = message["from"]
        text = message["text"]["body"]

        # Bot logic
        reply = "Please send a number (1-5)"
        if text == "1":
            reply = "🧒 Please send your child's name and age."
        elif text == "2":
            reply = "👪 We offer parent coaching and adult support."
        elif text == "3":
            reply = "⌚ Please give the name of the child on the waitlist."
        elif text == "4":
            reply = "💳 Send us your full name and we'll assist with billing."
        elif text == "5":
            reply = "📝 Please write your message and we’ll reply shortly."

        # Send reply via WhatsApp
        send_message(user_number, reply)

    except Exception as e:
        print("Error:", e)

    return "ok", 200

def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
