import face_recognition
import cv2
import pickle
import os
import numpy as np
import csv
from datetime import datetime


with open("random_encodings.pkl", "rb") as f:
    data = pickle.load(f)
known_encodings = data["encodings"]
known_names = data["names"]
known_roll_numbers = data.get("roll_numbers", ["N/A"]*len(known_names))  # रोल नंबर के लिए


ATTENDANCE_FILE = "attendance.csv"
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Roll Number", "Date", "Time"])


marked_attendance = set()


video_capture = cv2.VideoCapture(0)


TOLERANCE = 0.6
FRAME_SKIP = 2

print("🔍 Face recognition start press Q to stop...")

frame_count = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    
    frame_count += 1
    if frame_count % FRAME_SKIP != 0:
        continue
        
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding, TOLERANCE)
        name = "Unknown"
        roll_number = "N/A"
        
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_names[best_match_index]
            roll_number = known_roll_numbers[best_match_index]
            

            if name not in marked_attendance:
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")
                
                with open(ATTENDANCE_FILE, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, roll_number, date, time])
                
                marked_attendance.add(name)
                print(f"✅ Attendance Marked: {name} (Roll NUmber: {roll_number})")
                
        face_names.append((name, roll_number))
    

    for (top, right, bottom, left), (name, roll_number) in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
 
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 70), (right, bottom), (0, 255, 0), cv2.FILLED)
        

        cv2.putText(frame, f"Name: {name}", (left + 6, bottom - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        # cv2.putText(frame, f"Roll: {roll_number}", (left + 6, bottom - 30), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
 
        if name in marked_attendance:
            cv2.putText(frame, "Attendance: Marked", (left + 6, bottom - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()