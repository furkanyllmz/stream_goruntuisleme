from flask import Flask
from flask_socketio import SocketIO, emit
import cv2
import base64
import mediapipe as mp

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

@socketio.on('connect')
def handle_connect():
    print("🟢 WebSocket bağlantısı kuruldu")

@socketio.on('start-stream')
def start_stream():
    print("📸 Yayın başlıyor...")
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("❌ Kamera hatası")
            break

        # Mediapipe ile el hareketi algılama
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            thumb_tip = hand.landmark[4]
            index_tip = hand.landmark[8]
            distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

            if distance < 0.05:
                print("✋ El kapandı → 'space' tetiklenecek")
                emit('hand-action', {'action': 'space'})

        # Görüntüyü base64 olarak encode et ve gönder
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        try:
            emit('video-feed', {'image': jpg_as_text})
        except Exception as e:
            print(f"Emit hatası: {e}")
            break

        socketio.sleep(0.05)

@socketio.on('disconnect')
def handle_disconnect():
    print("🔴 Bağlantı kesildi.")
    cap.release()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=9000, debug=False)
