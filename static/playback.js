// playback.js
let frameCount = 150;
let frameIndex = 0;
let playbackInterval;
const frameRate = 30;
let framePath = "static/processed_frames/";

function playFrame() {
    const framePlayer = document.getElementById("framePlayer");
    framePlayer.src = framePath + "frame_" + String(frameIndex).padStart(4, "0") + ".jpg";
    frameIndex = (frameIndex + 1) % frameCount;
}

function startPlayback() {
    if (!videoProcessed) {
        alert("Please process the video first or allow video to finish processing.");
        return;
    }

    clearInterval(playbackInterval);
    playbackInterval = setInterval(playFrame, 1000 / frameRate);
}

function stopPlayback() {
    clearInterval(playbackInterval);
}
