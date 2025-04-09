import cv2
import mediapipe as mp  # type: ignore
import os
import sys
import face_recognition  # type: ignore


# ✅ Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# ✅ MediaPipe setup
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# ✅ Drawing style
drawing_spec = mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
no_landmarks_spec = mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=0, circle_radius=0)


def capture_faces(user):
    user = user.strip()
    if not user:
        print("⚠️ Username cannot be empty!")
        return

    path = f'./project/faces/{user}'

    # ✅ Check/create folder
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'📁 Folder created: {path}')
        else:
            print(f'📁 Folder already exists for {user}')
    except Exception as e:
        print(f"❌ Error creating folder: {e}")
        return

    img_count = len(os.listdir(path))
    max_images = 100

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access webcam.")
        return

    try:
        face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
    except Exception as e:
        print(f"❌ Face detection error: {e}")
        cap.release()
        return

    try:
        while img_count < max_images:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Frame capture failed.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_detection.process(rgb)

            if result.detections:
                for detection in result.detections:
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x, y = int(bbox.xmin * w), int(bbox.ymin * h)
                    w_box, h_box = int(bbox.width * w), int(bbox.height * h)

                    face_crop = frame[y:y + h_box, x:x + w_box]

                    try:
                        img_count += 1
                        filename = f"{path}/{img_count}.jpg"
                        cv2.imwrite(filename, face_crop)
                        print(f"✅ Saved ({img_count}/100): {filename}")
                    except Exception as e:
                        print(f"❌ Failed to save image: {e}")
                        img_count -= 1

                    mp_drawing.draw_detection(
                        frame, detection,
                        bbox_drawing_spec=drawing_spec,
                        keypoint_drawing_spec=no_landmarks_spec
                    )
                    cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
                    break

            cv2.imshow('Webcam - Saving Faces', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("⏹️ Quit pressed by user.")
                break

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    finally:
        print("🔚 Releasing resources...")
        cap.release()
        cv2.destroyAllWindows()
        face_detection.close()
        print("🎉 Done.")

if __name__ == "__main__":
    user = input('Username : ')
    capture_faces(user)
