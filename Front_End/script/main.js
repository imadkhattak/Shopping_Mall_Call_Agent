let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let audioContext;
let analyser;
let microphone;
let silenceStart = Date.now();
let silenceTimer = null;

// Configuration for silence detection
const SILENCE_THRESHOLD = 0.02; // Adjust based on testing
const SILENCE_DURATION = 1500; // ms to wait before stopping
const CHECK_INTERVAL = 100; // ms

const talkButton = document.getElementById('talkButton');
const buttonText = document.getElementById('buttonText');
const micIcon = document.getElementById('micIcon');
const statusIndicator = document.getElementById('statusIndicator');

talkButton.addEventListener('click', async () => {
    if (!isRecording) {
        startConversation();
    } else {
        stopRecording(); // Manual stop still available
    }
});

async function startConversation() {
    // 1. Play Welcome Message
    updateStatus('playing', 'Initializing...');
    try {
        const response = await fetch('/start_conversation', { method: 'POST' });
        const blob = await response.blob();
        await playAudio(blob);
        
        // 2. Start Recording after welcome message
        startRecording();
    } catch (err) {
        console.error("Error starting conversation:", err);
        updateStatus('error', 'Error');
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Setup Audio Analysis for Silence Detection
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        analyser.fftSize = 256;
        
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            // Clean up audio context
            if (audioContext && audioContext.state !== 'closed') {
                audioContext.close();
            }
            if (silenceTimer) clearInterval(silenceTimer);

            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            processAudio(audioBlob);
        };

        mediaRecorder.start();
        isRecording = true;
        updateStatus('listening', 'Listening...');
        buttonText.innerText = "Listening...";
        micIcon.className = "fas fa-microphone-lines";

        // Start Silence Detection Loop
        silenceStart = Date.now();
        silenceTimer = setInterval(() => {
            analyser.getByteFrequencyData(dataArray);
            
            // Calculate average volume
            let sum = 0;
            for(let i = 0; i < bufferLength; i++) {
                sum += dataArray[i];
            }
            let average = sum / bufferLength;
            // Normalize to 0-1 (approx, usually byte data is 0-255)
            let volume = average / 255;

            // Visualizer update (simple)
            // You could map `volume` to the CSS bars here if desired

            if (volume > SILENCE_THRESHOLD) {
                silenceStart = Date.now(); // Reset timer if noise detected
            } else {
                if (Date.now() - silenceStart > SILENCE_DURATION) {
                    stopRecording();
                }
            }
        }, CHECK_INTERVAL);

    } catch (err) {
        console.error("Error accessing microphone:", err);
        alert("Microphone access is required.");
        updateStatus('error', 'Mic Error');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        isRecording = false;
        buttonText.innerText = "Processing...";
        micIcon.className = "fas fa-spinner fa-spin";
        updateStatus('processing', 'Processing...');
        
        // Stop all tracks to release mic
        if (mediaRecorder.stream) {
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
}

async function processAudio(audioBlob) {
    // Don't send empty/too short audio? 
    // For now, send everything.
    const formData = new FormData();
    formData.append('file', audioBlob);

    try {
        const response = await fetch('/process_audio', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            await playAudio(blob);
            
            // Auto-record again after response
            // Add a small delay
            setTimeout(startRecording, 500); 
        } else {
            console.error("Server error");
            updateStatus('error', 'Server Error');
        }
    } catch (err) {
        console.error("Error sending audio:", err);
        updateStatus('error', 'Network Error');
    }
}

function playAudio(blob) {
    return new Promise((resolve) => {
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        
        updateStatus('speaking', 'Agent Speaking...');
        buttonText.innerText = "Agent Speaking...";
        
        audio.onended = () => {
             // resolve immediately to allow next step
             resolve();
        };
        
        audio.play();
    });
}

function updateStatus(state, text) {
    statusIndicator.className = 'status-indicator'; // Reset
    if (state === 'listening') {
        statusIndicator.classList.add('active', 'listening');
        buttonText.innerText = text;
    } else if (state === 'speaking') {
        statusIndicator.classList.add('active', 'speaking');
        buttonText.innerText = text;
    } else if (state === 'processing') {
        statusIndicator.classList.add('active');
        buttonText.innerText = text;
    } else if (state === 'playing') {
        statusIndicator.classList.add('active');
         buttonText.innerText = text;
    } else {
        // Idle / Error
        buttonText.innerText = text || "Start Conversation";
        micIcon.className = "fas fa-microphone";
    }
}
