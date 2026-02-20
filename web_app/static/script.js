document.addEventListener('DOMContentLoaded', () => {
    const recordButton = document.getElementById('recordButton');
    const audioUpload = document.getElementById('audioUpload');
    const languageSelect = document.getElementById('language');
    const statusDiv = document.getElementById('status');
    const resultsContainer = document.getElementById('results');
    const originalTextP = document.getElementById('originalText');
    const translatedTextP = document.getElementById('translatedText');
    const audioPlayer = document.getElementById('audioPlayer');

    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // Recording functionality
    recordButton.addEventListener('click', async () => {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    processAudio(audioBlob, "recorded_audio.wav");
                    audioChunks = [];
                });

                isRecording = true;
                recordButton.innerHTML = '<span class="icon">⏹️</span> Stop Recording';
                recordButton.classList.add('recording');
                statusDiv.textContent = "Recording...";
            } catch (err) {
                console.error("Error accessing microphone:", err);
                statusDiv.textContent = "Error accessing microphone. Please allow permissions.";
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;
            recordButton.innerHTML = '<span class="icon">🎙️</span> Start Recording';
            recordButton.classList.remove('recording');
            statusDiv.textContent = "Processing...";
        }
    });

    // File Upload functionality
    audioUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            processAudio(file, file.name);
        }
    });

    async function processAudio(audioData, filename) {
        statusDiv.textContent = "Uploading and processing...";
        resultsContainer.style.display = 'none';

        const formData = new FormData();
        formData.append('audio', audioData, filename);
        formData.append('language', languageSelect.value);

        try {
            const response = await fetch('/process_audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Processing failed');
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            statusDiv.textContent = `Error: ${error.message}`;
        }
    }

    function displayResults(data) {
        statusDiv.textContent = "Translation complete!";
        resultsContainer.style.display = 'block';
        
        originalTextP.textContent = data.original_text;
        translatedTextP.textContent = data.translated_text;
        
        audioPlayer.src = data.audio_url;
        audioPlayer.load();
        audioPlayer.play().catch(e => console.log("Auto-play prevented (browser policy)"));
    }
});
