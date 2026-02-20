import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'generated_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

def transcribe_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text

def text_to_speech(text, language):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)
    tts = gTTS(text=text, lang=language)
    tts.save(filepath)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    target_lang = request.form.get('language', 'en')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save uploaded audio
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(filepath)

    try:
        # 1. Transcribe
        original_text = transcribe_audio(filepath)
        if not original_text:
            return jsonify({'error': 'Could not understand audio'}), 400

        # 2. Translate
        translated_text = translate_text(original_text, target_lang)

        # 3. Text to Speech
        audio_filename = text_to_speech(translated_text, target_lang)

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify({
            'original_text': original_text,
            'translated_text': translated_text,
            'audio_url':f"/audio/{audio_filename}"
        })

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
