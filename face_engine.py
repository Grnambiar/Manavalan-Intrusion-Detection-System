import os
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def extract_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))
    if len(faces) == 0:
        return None
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    # Standardize size for comparison
    return cv2.resize(face_roi, (150, 150))

def load_owner_encodings(face_dir="face"):
    owner_faces = []
    if not os.path.exists(face_dir):
        return []
    
    valid_exts = ('.jpg', '.png', '.jpeg')
    for file in os.listdir(face_dir):
        if file.lower().endswith(valid_exts):
            path = os.path.join(face_dir, file)
            img = cv2.imread(path)
            if img is not None:
                face = extract_face(img)
                if face is not None:
                    # Calculate normalized grayscale histogram
                    hist = cv2.calcHist([face], [0], None, [256], [0, 256])
                    cv2.normalize(hist, hist)
                    owner_faces.append(hist)
    return owner_faces

def check_for_owner(owner_encodings, threshold=0.90):
    if not owner_encodings:
        print("[!] No valid owner face found in face/ directory.")
        return False

    cap = cv2.VideoCapture(0)
    frame = None
    for _ in range(8):  # warmup camera frames
        ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("[!] Camera error.")
        return False

    live_face = extract_face(frame)
    if live_face is None:
        print("[!] No face detected in front of screen.")
        return False

    # Calculate live face histogram
    live_hist = cv2.calcHist([live_face], [0], None, [256], [0, 256])
    cv2.normalize(live_hist, live_hist)

    # Compare correlation score (1.0 is exact match, <0.7 is different person)
    best_score = 0.0
    for ref_hist in owner_encodings:
        score = cv2.compareHist(ref_hist, live_hist, cv2.HISTCMP_CORREL)
        if score > best_score:
            best_score = score

    print(f"[DEBUG] Match confidence score: {best_score:.2f} (Threshold: {threshold})")
    return best_score >= threshold
