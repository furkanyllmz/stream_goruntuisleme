from flask import Flask,render_template
from flask_socketio import SocketIO, emit
import cv2
import base64
import numpy as np
import mediapipe as mp
import math

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
@app.route('/')
def index():
    return render_template('index.html')

# Mediapipe el modeli
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

@socketio.on('connect')
def handle_connect():
    print("🟢 WebSocket bağlantısı kuruldu")

@socketio.on('client-frame')
def handle_client_frame(data):
    try:
        # Base64'ten resmi çöz
        image_data = base64.b64decode(data['image'])
        np_array = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # RGB'ye çevirip el algılama
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            thumb_tip = hand.landmark[4]
            index_tip = hand.landmark[8]

            distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
            print(f"👉 Parmaklar arası mesafe: {distance:.4f}")

            if distance < 0.1:
                print("✋ El kapama algılandı → Space gönderiliyor")
                emit('hand-action', {'action': 'space'}, broadcast=True)

    except Exception as e:
        print("⚠️ Görüntü işleme hatası:", e)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
