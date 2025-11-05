🐍 Hand-Gesture Controlled Snake Game

An advanced, interactive, and augmented-reality style Snake Game controlled entirely using hand gestures.  
Built with Python, OpenCV, MediaPipe, Pygame, and NumPy.

This project uses your webcam to track your hand in real time — your index finger controls the snake, an open palm pauses/resumes, and a thumbs-up gesture restarts the game.  
Featuring smooth animations, dynamic levels, AR-style visuals, particle explosions, and custom synthesized sound effects.

---

✨ Features

🎮 Gesture-Based Controls  
- Index finger → Move the snake  
- Open palm → Pause / Resume  
- Thumbs-up → Restart the game  

🎥 AR-Style Webcam Background  
- Live webcam feed displayed behind gameplay  
- Semi-transparent overlay for a futuristic look  

💥 Particle Effects  
- Explosion particles when food is eaten  
- Colorful snake trail  
- Glowing food effects  

 🔊 Synthesized Sound Effects  
- No external audio files  
- Procedurally generated tones (eat, pause, restart, explosion)

⚡ Smooth Gameplay  
- Movement smoothing using buffers  
- Stable controls  
- Increasing difficulty with levels  
- Self-collision detection and reset  

---

 🧰 Tech Stack

| Component     | Technology |
|--------------|------------|
| Hand Tracking | MediaPipe Hands |
| Camera Input  | OpenCV |
| Game Engine   | Pygame |
| Math / Arrays | NumPy |
| Language      | Python 3.10 |

---

📦 Installation

✅ 1. Install Python 3.10  
MediaPipe requires Python 3.10 for compatibility.

✅ 2. Install Dependencies
Run:

```bash
pip install -r requirements.txt
