# app.py (Flask server)
from flask import Flask, request
from flask_cors import CORS
import subprocess
import os
import base64
import time
import logging
TEMP_FILE = "react_rec.wav"
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
CORS(app)  # Enable CORS

@app.route('/save_audio', methods=['POST'])
def save_audio():
    audio_file = request.files.get('audio')
    if audio_file:
        # Generate a unique file name
        file_name = TEMP_FILE
        # Define the file path
        file_path = os.path.join(os.path.dirname(__file__), 'prediction_processing', file_name)
        # Save the audio to a .wav file
        audio_file.save(file_path)
        print(f"LETS GO: {file_path}")
        return f'Audio saved successfully, file path {file_path}'
    print("No audio data received")
    return 'No audio data received'


@app.route('/get_results', methods=['GET'])
def get_results():
    try:
        # Run the Python script using subprocess
        result = subprocess.run(['python3', os.path.join(os.path.dirname(__file__), "prediction_from_rec.py")], capture_output=True, text=True)
        # os.remove(os.path.join(os.path.dirname(__file__), 'prediction_processing', TEMP_FILE))
        # Check if the script executed successfully
        if result.returncode == 0:
            stdout = result.stdout
            # Process the stdout and stderr as needed
            return {
                'stdout': stdout,
            }
        else:
            error_message = result.stderr
            # Handle the case where the script failed to execute
            return {
                'error': error_message
            }
    except Exception as e:
        # Handle any exceptions that may occur during script execution
        return {
            'exception': str(e)
        }

if __name__ == '__main__':
    app.run()