import json
import os
import face_recognition  # type: ignore

def save_encodings(folder_path='project/faces', max_images_per_user=10):
    data = {"paths": [], "names": []}

    for user in os.listdir(folder_path):
        user_dir = os.path.join(folder_path, user)
        if not os.path.isdir(user_dir):
            continue

        images_loaded = 0
        for filename in sorted(os.listdir(user_dir)):
            if images_loaded >= max_images_per_user:
                break

            img_path = os.path.join(user_dir, filename)
            try:
                image = face_recognition.load_image_file(img_path)
                locs = face_recognition.face_locations(image)
                encodings = face_recognition.face_encodings(image, locs)
                if encodings:
                    data["paths"].append(img_path)
                    data["names"].append(user)
                    images_loaded += 1
            except Exception as e:
                print(f"⚠️ Error: {e}")

    with open("project/encodings.json", "w") as f:
        json.dump(data, f)

    print("✅ Encodings saved.")

if __name__ == "__main__":
    save_encodings()
