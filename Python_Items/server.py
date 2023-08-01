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
    print("INSIDE THE SAVE AUDIO ROUTEeeeeeee")
    audio_file = request.files.get('audio') #does not get printed
    if audio_file:
        file_name = TEMP_FILE
        file_path = os.path.join(os.path.dirname(__file__), 'prediction_processing', file_name)
        audio_file.save(file_path)
        print(f"LETS GO: {file_path}")
        return f'Audio saved successfully, file path {file_path}'
    print("No audio data received")
    return 'No audio data received'


@app.route('/get_results', methods=['GET'])
def get_results():
    print('INSIDE THE FETCH RESULTS ROUTEeeeeeeee') # does not get printed
    try:
        result = subprocess.run(['python3', os.path.join(os.path.dirname(__file__), "prediction_from_rec.py")], capture_output=True, text=True)
        # os.remove(os.path.join(os.path.dirname(__file__), 'prediction_processing', TEMP_FILE))
        if result.returncode == 0:
            stdout = result.stdout
            return {
                'stdout': stdout,
            }
        else:
            error_message = result.stderr
            return {
                'error': error_message
            }
    except Exception as e:
        return {
            'exception': str(e)
        }

if __name__ == '__main__':
    app.run(host='localhost', port=3500, debug=True)