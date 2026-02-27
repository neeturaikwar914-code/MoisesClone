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
    path = f"{STORAGE}/{job_id}/htdemucs/uploaded_file"
    return send_from_directory(path, f"{stem}.wav")

@socketio.on('start_separation')
def handle_separation(data):
    job_id = str(uuid.uuid4())
    input_path = os.path.join(STORAGE, f"{job_id}_input.mp3")
    emit('status', {'msg': 'AI Processing started...'})
    try:
        subprocess.run(["demucs", "-n", "htdemucs", "-o", f"{STORAGE}/{job_id}", input_path], check=True)
        emit('complete', {'job_id': job_id})
    except Exception as e:
        emit('error', {'msg': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port)
