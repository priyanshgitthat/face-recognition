import os
import json
import face_recognition  # type: ignore
import cv2
import subprocess
import sys  # 👈 for using current python interpreter

encoding_path = os.path.join("project", "encodings.json")


if not os.path.exists(encoding_path):
    print("⚠️ encodings.json not found. Generating now...")
    try:
        subprocess.run([sys.executable, "project/save_encoding.py"], check=True)
        print("✅ encodings.json created successfully.\n")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to generate encodings.json:", e)
        exit(1)

        
# ✅ Load encodings from JSON
with open("project/encodings.json", "r") as f:
    data = json.load(f)

known_encodings = [face_recognition.face_encodings(face_recognition.load_image_file(img_path))[0] for img_path in data["paths"]]
known_names = data["names"]

# ✅ Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for (top, right, bottom, left), enc in zip(locations, encodings):
        matches = face_recognition.compare_faces(known_encodings, enc, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            idx = matches.index(True)
            name = known_names[idx]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.imshow("Face Match", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
