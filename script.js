// static/js/script.js

let countdown; // Declare countdown variable
let timeLeft = 10800; // 3 hours in seconds
const timerDisplay = document.getElementById('timer');
const popup = document.getElementById('popup');
const safeButton = document.getElementById('safeButton');
const sosButton = document.getElementById('sosButton');

// Function to start the countdown
function startCountdown() {
    countdown = setInterval(() => {
        const hours = Math.floor(timeLeft / 3600);
        const minutes = Math.floor((timeLeft % 3600) / 60);
        const seconds = timeLeft % 60;

        // Format time as HH:MM:SS
        timerDisplay.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        // Check if time is up
        if (timeLeft <= 0) {
            clearInterval(countdown);
            alarm(); // Trigger alarm
        } else if (timeLeft === 15) {
            showPopup