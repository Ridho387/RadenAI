from flask import Flask, render_template, request, jsonify
from auth import load_users, save_users  # Untuk autentikasi & kuota
from hotel import search_hotels          # Untuk pencarian hotel (via link)
from ai_engines.open_chat import ask_openai # AI default
# import ai_engines.claude_engine, etc.

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_openai():
    return render_template('chat_openai.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/specs')
def specs():
    return render_template('specs.html')

@app.route('/other-ais')
def other_ais():
    return render_template('other_ais.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    user_id = data.get("user_id")
    message = data.get("message")
    ai_choice = data.get("ai") or "openai"

    if "hotel" in message.lower():
        hotel_links = search_hotels(message)
        return jsonify({"response": f"Berikut link hotel:\n" + "\n".join(hotel_links)})

    if ai_choice == "openai":
        reply = ask_openai(message)
    else:
        reply = "Fitur AI tersebut belum diaktifkan."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
