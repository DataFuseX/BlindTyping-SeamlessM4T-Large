var audioPlayed = false;
var startTime = 0;
var wordCount = 0;

function startAudio() {
  if (!audioPlayed) {
    const audio = document.getElementById("audioElement");
    // audio.style.display = 'block'; // Show the audio element
    audio.play(); // Autoplay the audio
    audio.muted = false; // Unmute the audio
    audioPlayed = true;
    startTime = new Date().getTime(); // Record start time
    wordCount = 0; // Reset word count
  }
}

// Function to calculate typing speed
function calculateTypingSpeed() {
  if (audioPlayed) {
    const endTime = new Date().getTime();
    const elapsedTime = (endTime - startTime) / 1000; // Convert to seconds
    const text = document.getElementById("text").value;
    const words = text.trim().split(/\s+/); // Split text into words
    wordCount = words.length;
    const typingSpeed = Math.round((wordCount / elapsedTime) * 60); // Calculate WPM
    const typingSpeedDisplay = `Typing Speed: ${typingSpeed} WPM`;
    document.getElementById("typingSpeed").textContent = typingSpeedDisplay;
  }
}

// Add event listener to the textarea for real-time speed calculation
document.getElementById("text").addEventListener("input", calculateTypingSpeed);
