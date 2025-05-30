import cv2

backends = {
    cv2.CAP_AVFOUNDATION: "AVFOUNDATION",
    cv2.CAP_QT:           "QT"
}

for backend, name in backends.items():
    for idx in range(3):  # 0,1,2’yi dene
        cap = cv2.VideoCapture(idx, backend)
        ret, _ = cap.read()
        print(f"[{name}] index={idx} → ret={ret}")
        cap.release()
