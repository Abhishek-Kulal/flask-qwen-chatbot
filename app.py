from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

QWEN_API_KEY = "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"
QWEN_API_URL = "https://api.openrouter.ai/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen:7b-chat",
        "messages": [
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        response = requests.post(QWEN_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        if 'choices' in result:
            bot_reply = result["choices"][0]["message"]["content"]
        else:
            bot_reply = "⚠️ No valid response received from the API."
    except requests.exceptions.RequestException as e:
        print("\n⚠️ ERROR contacting Qwen API:", e)
        bot_reply = (
            "❌ Unable to contact Qwen API.\n"
            "Check your internet connection or DNS settings."
        )

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
