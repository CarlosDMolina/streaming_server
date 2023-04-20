// playback.js
let frameIndex = 0;
let playbackInterval;

function updateFrame() {
    const totalFrames = 150
    const img = document.getElementById('framePlayer');
    img.src = 'static/frames/frame_' + String(frameIndex).padStart(4, '0') + '.jpg';
    frameIndex = (frameIndex + 1) % totalFrames;
}

function startPlayback() {
    if (playbackInterval) {
        clearInterval(playbackInterval);
    }
    frameIndex = 0;
    playbackInterval = setInterval(updateFrame, 1000 / 30); // Adjust the number 30 to match your desired frame rate
}

function stopPlayback() {
    if (playbackInterval) {
        clearInterval(playbackInterval);
    }
}
