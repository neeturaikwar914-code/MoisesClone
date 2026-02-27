import os
import uuid
import subprocess
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# THE FIX: Increase upload limit from 1MB to 100MB
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=100000000)

STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)

@app.route('/download/<job_id>/<stem>')
def download_stem(job_id, stem):
    path = os.path.join(STORAGE, job_id, "htdemucs", "input")
    return send_from_directory(path, f"{stem}.wav")

@socketio.on('start_separation')
def handle_separation(data):
    job_id = str(uuid.uuid4())
    job_folder = os.path.join(STORAGE, job_id)
    os.makedirs(job_folder, exist_ok=True)
    
    input_path = os.path.join(job_folder, "input.mp3")
    with open(input_path, "wb") as f:
        f.write(data['file'])
    
    # Send update back to phone to move the progress bar
    emit('status', {'msg': 'AI Processing... (3-5 mins)', 'progress': 25})
    
    try:
        subprocess.run(["demucs", "-n", "htdemucs", "-o", job_folder, input_path], check=True)
        emit('complete', {'job_id': job_id})
    except Exception as e:
        emit('error', {'msg': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
