// Replace with your actual Render URL
const SOCKET_URL = "https://your-moises-clone.onrender.com";
const socket = io(SOCKET_URL);

let audioCtx;
let sources = {}; // To store AudioBufferSourceNodes
let gainNodes = {}; // To store GainNodes (Volume)
let audioBuffers = {}; // To store actual audio data

const statusMsg = document.getElementById('status-msg');

// 1. Handle File Selection and Upload
async function handleUpload() {
    const fileInput = document.getElementById('audio-upload');
    const file = fileInput.files[0];
    if (!file) return alert("Select a file first!");

    statusMsg.innerText = "Reading file...";
    
    const reader = new FileReader();
    reader.onload = function() {
        const bytes = new Uint8Array(reader.result);
        socket.emit('upload_and_process', {
            name: file.name,
            file: bytes
        });
    };
    reader.readAsArrayBuffer(file);
}

socket.on('status', (data) => {
    statusMsg.innerText = data.message;
});

// 2. When AI is done, download and buffer the stems
socket.on('process_complete', async (data) => {
    statusMsg.innerText = "Stems ready! Downloading to mixer...";
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    const stemNames = ['vocals', 'drums', 'bass', 'other'];
    
    for (const name of stemNames) {
        const response = await fetch(data.urls[name]);
        const arrayBuffer = await response.arrayBuffer();
        audioBuffers[name] = await audioCtx.decodeAudioData(arrayBuffer);
        setupTrack(name);
    }
    
    statusMsg.innerText = "All tracks synced. Ready to play!";
    document.getElementById('play-btn').disabled = false;
});

// 3. Setup individual track gain (volume)
function setupTrack(name) {
    gainNodes[name] = audioCtx.createGain();
    const slider = document.getElementById(`${name}-vol`);
    slider.oninput = (e) => {
        gainNodes[name].gain.value = e.target.value;
    };
}

// 4. Synchronized Start/Stop
function togglePlay() {
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const btn = document.getElementById('play-btn');
    
    if (btn.innerText === "Play") {
        const startTime = audioCtx.currentTime + 0.1; // Small buffer for sync
        
        Object.keys(audioBuffers).forEach(name => {
            sources[name] = audioCtx.createBufferSource();
            sources[name].buffer = audioBuffers[name];
            sources[name].connect(gainNodes[name]).connect(audioCtx.destination);
            sources[name].start(startTime);
        });
        
        btn.innerText = "Stop";
    } else {
        Object.keys(sources).forEach(name => sources[name].stop());
        btn.innerText = "Play";
    }
}