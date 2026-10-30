from flask import Flask, request, jsonify, render_template_string
from vessels import route_signal

app = Flask(__name__)

# =============================================================================
# THE FACE (HTML/CSS/JS)
# This is the outer layer that your phone sees. 
# It contains the "Ear" (Microphone) and the "Mouth" (Speaker).
# =============================================================================
HTML_FACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Lyra Virtual Human</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            background: #0a0a0a; 
            color: white; 
            padding: 0; 
            margin: 0;
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            height: 100vh; 
            overflow: hidden;
        }
        
        h1 { 
            font-size: 28px; 
            font-weight: 300; 
            letter-spacing: 2px; 
            margin-bottom: 10px;
            color: #e0e0e0;
        }

        #status { 
            color: #888; 
            margin-bottom: 40px; 
            font-style: italic; 
            font-size: 16px;
        }

        /* The Glowing Orb - Lyra's Physical Presence */
        .call-circle { 
            width: 180px; 
            height: 180px; 
            border-radius: 50%; 
            background: radial-gradient(circle, #00ffcc 0%, #006652 100%); 
            margin: 0 auto; 
            cursor: pointer; 
            box-shadow: 0 0 30px #00ffcc; 
            transition: 0.4s ease; 
            border: 5px solid rgba(0, 255, 204, 0.2);
        }

        /* When Lyra is listening, the orb changes color and pulses */
        .call-circle.active { 
            animation: pulse 1.5s infinite; 
            background: radial-gradient(circle, #ff0055 0%, #660022 100%); 
            box-shadow: 0 0 50px #ff0055; 
            border: 5px solid rgba(255, 0, 85, 0.3);
        }

        @keyframes pulse { 
            0% { transform: scale(1); box-shadow: 0 0 30px #ff0055; } 
            50% { transform: scale(1.1); box-shadow: 0 0 60px #ff0055; } 
            100% { transform: scale(1); box-shadow: 0 0 30px #ff0055; } 
        }

        #reply { 
            margin-top: 40px; 
            font-size: 24px; 
            color: #00ffcc; 
            padding: 0 30px;
            line-height: 1.4;
            min-height: 60px;
            transition: 0.3s;
        }
    </style>
</head>
<body>
    <h1>LYRA</h1>
    <div id="status">Tap the orb to start the call</div>
    <div class="call-circle" id="micBtn" onclick="toggleCall()"></div>
    <div id="reply"></div>

    <script>
        let isCalling = false;
        const micBtn = document.getElementById('micBtn');
        const status = document.getElementById('status');
        const replyDiv = document.getElementById('reply');

        // THE EAR: Setup Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Your browser does not support the 'Ear' (Speech Recognition). Please use Chrome.");
        }
        const recognition = new SpeechRecognition();
        recognition.continuous = false; 
        recognition.lang = 'en-US';

        // THE MOUTH: Setup Text-to-Speech
        const synth = window.speechSynthesis;

        function toggleCall() {
            if (!isCalling) {
                startCall();
            } else {
                stopCall();
            }
        }

        function startCall() {
            isCalling = true;
            micBtn.classList.add('active');
            status.innerText = "Lyra is listening...";
            recognition.start();
        }

        function stopCall() {
            isCalling = false;
            micBtn.classList.remove('active');
            status.innerText = "Call ended. Tap to start again.";
            recognition.stop();
        }

        // This handles the signal flowing from the Ear to the Skin
        recognition.onresult = async (event) => {
            const transcript = event.results[0][0].transcript;
            status.innerText = "You: " + transcript;
            replyDiv.innerText = "...";
            
            try {
                // Sending the voice signal to the Flask /talk route
                const response = await fetch(window.location.origin + "/talk", {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: transcript })
                });
                const data = await response.json();
                const lyraReply = data.reply;
                
                replyDiv.innerText = lyraReply;
                speak(lyraReply);
            } catch (error) {
                replyDiv.innerText = "Error: Nerve Cord connection failed!";
                stopCall();
            }
        };

        // This handles the signal flowing from the Skin to the Mouth
        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Try to find a high-quality female voice
            const voices = synth.getVoices();
            const preferredVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Female') || v.name.includes('Samantha'));
            if (preferredVoice) utterance.voice = preferredVoice;
            
            utterance.onend = () => {
                // If we are still in a call, Lyra starts listening again immediately
                if (isCalling) {
                    status.innerText = "Lyra is listening...";
                    recognition.start();
                }
            };
            synth.speak(utterance);
        }

        recognition.onerror = (event) => {
            console.error("Recognition Error: " + event.error);
            if (event.error === 'no-speech') {
                status.innerText = "No speech detected. Listening again...";
                recognition.start();
            } else {
                stopCall();
                status.innerText = "Ear Error. Try again.";
            }
        };
    </script>
</body>
</html>
"""

# =============================================================================
# THE ROUTES (Signals)
# =============================================================================

@app.route('/')
def home():
    """Returns the 'Face' of Lyra to the browser."""
    return render_template_string(HTML_FACE)

@app.route('/talk', methods=['POST'])
def talk():
    """Receives signals from the phone and routes them through the Vessels."""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"reply": "I didn't feel any signal."}), 400
    
    user_message = data.get("message")
    
    # Pass the message into the Vessels (Veins) to reach the Brain or Stomach
    reply = route_signal(user_message)
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # host='0.0.0.0' allows the Tailscale IP (100.123.177.109) to reach this server
    app.run(host='0.0.0.0', port=5000, debug=True)