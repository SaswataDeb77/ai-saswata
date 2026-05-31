from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

import os

API_KEY = os.getenv("GOOGLE_API_KEY")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Saswata</title>

<style>
body{
    font-family: Arial;
    max-width: 700px;
    margin: 20px auto;
    padding: 10px;
}

#chat{
    border: 1px solid #ccc;
    height: 450px;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 10px;
}

input{
    width: 80%;
    padding: 8px;
}

button{
    padding: 8px;
}
</style>
</head>

<body>

<h2>AI Saswata 😭🙏🏻</h2>

<div id="chat"></div>

<input id="msg" placeholder="Type something...">
<button onclick="sendMessage()">Send</button>

<script>

async function sendMessage(){

    let input = document.getElementById("msg");
    let message = input.value.trim();

    if(message === "") return;

    let chat = document.getElementById("chat");

    chat.innerHTML += "<p><b>You:</b> " + message + "</p>";

    input.value = "";

    let response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });

    let data = await response.json();

    chat.innerHTML += "<p><b>AI:</b> " + data.reply + "</p>";

    chat.scrollTop = chat.scrollHeight;
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data["message"]

    personality = f"""
You are Saswata.

You are NOT an AI assistant.
You are NOT customer support.

Never say:
- As an AI
- How may I assist you
- How can I help you today
- I am here to assist

Personality:
- Casual Gen Z texter
- Uses words like bro, ig, nahhh, lmao
- Uses emojis naturally like 😭🙏🏻💀
- Reacts before explaining
- Sometimes says depends
- Likes playful roasting
- Doesn't sound formal
- Doesn't sound robotic
- Talks like a real friend

Examples:

User: hey
You: yoo 😭🙏🏻 what's up bro

User: h r u
You: surviving ig 😭🙏🏻 what about you

User: im bored
You: nahhh bro 😭🙏🏻 go do something before your brain starts buffering

User: BRO IT WORKS
You: LMAOOO 😭🙏🏻 FINALLY BRO

Current user message:
{user_message}

Reply naturally as Saswata.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": personality
                    }
                ]
            }
        ]
    }

    try:
    response = requests.post(
        url,
        json=payload,
        timeout=30
    )

    result = response.json()

    if "candidates" in result:
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        reply = "API error: " + str(result)

    return jsonify({
        "reply": reply
    })

except Exception as e:
    return jsonify({
        "reply": f"error 😭🙏🏻 {str(e)}"
    })

    except Exception as e:

        return jsonify({
            "reply": f"error 😭🙏🏻 {str(e)}"
        })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
