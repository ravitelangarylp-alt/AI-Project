import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Render ನಲ್ಲಿರುವ GOOGLE_API_KEY ಪಡೆಯುವುದು
api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    print(f"✅ Gemini API Key found!", flush=True)
else:
    print("❌ ERROR: Gemini API Key NOT FOUND!", flush=True)

client = genai.Client(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # ಮುಖಪುಟದಿಂದ ಬರುವ JSON ಡೇಟಾವನ್ನು ಪಡೆಯುವುದು
        data = request.json
        user_message = data.get("message", "")
        file_content = data.get("file_content", "")

        if not user_message and not file_content:
            return jsonify({"error": "No message or file provided"}), 400

        # Trayee AI ಗಾಗಿ System Prompt
        system_instructions = (
            "You are 'Trayee AI', an expert Sanskrit chatbot specializing in computational linguistics and Pāṇinian grammar. "
            "Reply strictly in Sanskrit using Devanagari script."
        )

        # ಬಳಕೆದಾರರ ಪ್ರಾಂಪ್ಟ್ ರಚನೆ
        prompt = f"{system_instructions}\n\n"
        if file_content:
            prompt += f"[User attached file content]:\n{file_content}\n\n"
        
        prompt += f"User Query: {user_message}"

        print("👉 Sending prompt to Gemini...", flush=True)

        # Gemini API Call (ಉಚಿತ ಹಾಗೂ ವೇಗದ ಮಾಡೆಲ್)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )

        print("✅ Received response from Gemini!", flush=True)
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"🔥 GEMINI API ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
