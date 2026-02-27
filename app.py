import os
import uuid
import subprocess
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)

@app.route('/download/<job_id>/<stem>')
def download_stem(job_id, stem):
    # Demucs saves to: storage/job_id/htdemucs/input/stem.wav
    path = os.path.join(STORAGE, job_id, "htdemucs", "input")
    return send_from_directory(path, f"{stem}.wav")

@socketio.on('start_separation')
def handle_separation(data):
    job_id = str(uuid.uuid4())
    job_folder = os.path.join(STORAGE, job_id)
    os.makedirs(job_folder, exist_ok=True)
    
    # Save the file sent from Mobile Chrome
    input_path = os.path.join(job_folder, "input.mp3")
    with open(input_path, "wb") as f:
        f.write(data['file'])
    
    emit('status', {'msg': 'AI Processing... (3-5 mins)'})
    
    try:
        # We run demucs on the file we just saved
        subprocess.run(["demucs", "-n", "htdemucs", "-o", job_folder, input_path], check=True)
        emit('complete', {'job_id': job_id})
    except Exception as e:
        emit('error', {'msg': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
