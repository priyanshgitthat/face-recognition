import sys
import os
import cv2
import mediapipe as mp
import numpy as np


sys.stderr = open(os.devnull, 'w')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=1,  
    min_detection_confidence=0.7
)

def enhance_face(face_image):
    
 
    lab = cv2.cvtColor(face_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    limg = cv2.merge([clahe.apply(l), a, b])
    enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    return sharpened

def save_face_image(frame, bbox, folder_path, img_count):
    
    h, w = frame.shape[:2]
    x = max(0, int(bbox.xmin * w))
    y = max(0, int(bbox.ymin * h))
    w_box = min(w - x, int(bbox.width * w))
    h_box = min(h - y, int(bbox.height * h))
    
    face_crop = frame[y:y+h_box, x:x+w_box]
    
    if face_crop.size > 0:
     
        enhanced_face = enhance_face(face_crop)
        
        
        if enhanced_face.shape[0] < 200 or enhanced_face.shape[1] < 200:
            enhanced_face = cv2.resize(enhanced_face, (200, 200))
            
        img_path = os.path.join(folder_path, f"{img_count}.jpg")
        cv2.imwrite(img_path, enhanced_face)
        return True
    return False

def add_faces(username, roll_number):
    
    folder_name = f"faces/{roll_number}_{username}"
    os.makedirs(folder_name, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    img_count = 0
    max_images = 100
    quality_threshold = 30  
    
    print("\nface registration start (quality check)")
    print("look into camera straight , and try to register in good light")
    
    while img_count < max_images:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        

        results = face_detection.process(rgb_frame)
        
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                
         
                face_crop = frame[
                    max(0, int(bbox.ymin*frame.shape[0])):min(frame.shape[0], int((bbox.ymin+bbox.height)*frame.shape[0])),
                    max(0, int(bbox.xmin*frame.shape[1])):min(frame.shape[1], int((bbox.xmin+bbox.width)*frame.shape[1]))
                ]
                
                if face_crop.size > 0:
                 
                    gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                    
                    if fm > quality_threshold:  
                        if save_face_image(frame, bbox, folder_name, img_count + 1):
                            img_count += 1
                            print(f"\r✅ Saved Image: {img_count}/{max_images} (quality: {int(fm)})", end="")
                            
                            
                            cv2.putText(frame, f"Saved: {img_count}/{max_images}", (10, 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            cv2.putText(frame, f"Quality: {int(fm)}", (10, 70),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "LOW QUALITY - MOVE CLOSER", (10, 70),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                

                x = int(bbox.xmin * frame.shape[1])
                y = int(bbox.ymin * frame.shape[0])
                w = int(bbox.width * frame.shape[1])
                h = int(bbox.height * frame.shape[0])
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow("Face Registration (Press Q to stop)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"\n\n🎉 {img_count} images saved in high quality '{folder_name}' ")

if __name__ == "__main__":
    username = input("Username: ").strip()
    roll_number = input("Roll Number : ").strip()
    add_faces(username, roll_number)