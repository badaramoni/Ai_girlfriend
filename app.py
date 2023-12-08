from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from elevenlabs import generate, set_api_key
import os
from datetime import datetime
import hashlib
import requests

app = Flask(__name__)
CORS(app)

# ElevenLabs API key and voice ID
set_api_key("7692db7429062230e4a68649261046ab")
cloned_voice_id = "Samantha"

# Directory for audio files
AUDIO_FOLDER = 'audio_files'
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    try:
        audio = generate(data['text'], voice=cloned_voice_id)
    except Exception as e:
        print(f"Error generating audio: {e}")
        return jsonify({"error": "Error generating audio"})

    audio_url = save_audio(audio)
    return jsonify({"audioUrl": audio_url})


def save_audio(audio):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{hashlib.md5(timestamp.encode()).hexdigest()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)
    with open(filepath, 'wb') as audio_file:
        audio_file.write(audio)
    return f'http://127.0.0.1:5000/{AUDIO_FOLDER}/{filename}'


@app.route('/chat', methods=['POST'])
def chat():
    print("Received request data:", request.json)  # Log the incoming request data
    user_input = request.json.get("text")

    try:
        hugging_face_response = requests.post("https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
        headers={"Authorization": "Bearer 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"}, json={"inputs": user_input})
    except Exception as e:
        print(f"Error calling Hugging Face API: {e}")
        return jsonify({"error": "Error generating response"})

    if hugging_face_response.status_code == 200:
        chat_response = hugging_face_response.json().get("generated_text", "")
        try:
            audio = generate(chat_response, voice=cloned_voice_id)
        except Exception as e:
            print(f"Error generating audio: {e}")
            return jsonify({"error": "Error generating response"})

        audio_url = save_audio(audio)
        return jsonify({"audioUrl": audio_url})
    else:
        return jsonify({"error": "Error generating response"}), hugging_face_response.status_code


@app.route(f'/{AUDIO_FOLDER}/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
