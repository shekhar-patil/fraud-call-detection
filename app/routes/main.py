from flask import Blueprint, request, jsonify, render_template
import speech_recognition as sr
import pandas as pd
from app.models.fraud_detection import load_data, preprocess_data, train_model, preprocess_input, predict_label

main = Blueprint('main', __name__)

recognizer = sr.Recognizer()

file_path = "./data/fraud_call.file"
data = load_data(file_path)
corpus = preprocess_data(data)
labels = pd.get_dummies(data['label']).iloc[:, 1].values  # Selecting the 'fraud' column as target
model = train_model(corpus, labels)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict', methods=['POST'])
def predict():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                prediction = predict_label(text, model)
                return jsonify({'text': text, 'prediction': prediction})
            except sr.UnknownValueError:
                return jsonify({'error': 'Google Speech Recognition could not understand audio'})
            except sr.RequestError as e:
                return jsonify({'error': f'Could not request results from Google Speech Recognition service; {e}'})
    return jsonify({'error': 'No audio file found'})
    