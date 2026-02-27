import os
import uuid
import subprocess
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows Acode to talk to Render
socketio = SocketIO(app, cors_allowed_origins="*")

STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)

@app.route('/download/<job_id>/<stem>')
def download_stem(job_id, stem):
    # Demucs output path: storage/job_id/htdemucs/input_filename/stem.wav
    # We simplify this for the tutorial
    path = f"{STORAGE}/{job_id}/htdemucs/uploaded_file"
    return send_from_directory(path, f"{stem}.wav")

@socketio.on('start_separation')
def handle_separation(data):
    job_id = str(uuid.uuid4())
    input_path = os.path.join(STORAGE, f"{job_id}_input.mp3")
    
    # In a real app, save the binary data from 'data' to input_path
    # For now, we assume the file is sent via Socket or HTTP
    
    emit('status', {'msg': 'AI Processing started... this takes 1-2 mins.'})
    
    # The Power Move: Calling Demucs
    try:
        subprocess.run(["demucs", "-n", "htdemucs", "-o", f"{STORAGE}/{job_id}", input_path], check=True)
        emit('complete', {
            'job_id': job_id,
            'stems': {
                'vocals': f"https://YOUR-RENDER-URL.onrender.com/download/{job_id}/vocals",
                'drums': f"https://YOUR-RENDER-URL.onrender.com/download/{job_id}/drums",
                'bass': f"https://YOUR-RENDER-URL.onrender.com/download/{job_id}/bass",
                'other': f"https://YOUR-RENDER-URL.onrender.com/download/{job_id}/other"
            }
        })
    except Exception as e:
        emit('error', {'msg': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)