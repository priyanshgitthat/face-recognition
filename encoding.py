import face_recognition
import pickle
import cv2
import os
import numpy as np
import random
from pathlib import Path

RANDOM_IMAGES_PER_PERSON = 15
MIN_FACE_SIZE = 100
GPU_MODE = True

def init_gpu():
    if GPU_MODE:
        os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def get_random_images(person_dir):
 
    all_images = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        all_images.extend(person_dir.glob(ext))
    return random.sample(all_images, min(RANDOM_IMAGES_PER_PERSON, len(all_images))) if all_images else []

def fast_encode_image(img_path):
    
    try:
        image = cv2.imread(str(img_path))
        if image is None: 
            print(f"⚠️ Can't Load Images : {img_path.name}")
            return None
        

        image = cv2.resize(image, (200, 200))
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
       
        face_locations = face_recognition.face_locations(rgb_image, model="hog", number_of_times_to_upsample=1)
        if not face_locations:
            print(f"⚠️ Face Not Found: {img_path.name}")
            return None
        
 
        encodings = face_recognition.face_encodings(rgb_image, face_locations, num_jitters=1)
        return encodings[0] if encodings else None
    except Exception as e:
        print(f"❌ Error {img_path.name}: {str(e)}")
        return None

def generate_random_encodings():
    init_gpu()
    encodings = []
    names = []
    

    
    for person_dir in Path("faces").iterdir():
        if person_dir.is_dir():
            person_name = person_dir.name
            selected_images = get_random_images(person_dir)
            
            for img_path in selected_images:
                encoding = fast_encode_image(img_path)
                if encoding is not None:  
                    encodings.append(encoding)
                    names.append(person_name)
                    print(f"✅ {person_name}: {img_path.name}")
    

    if encodings:
        with open("random_encodings.pkl", "wb") as f:
            pickle.dump({"encodings": encodings, "names": names}, f)
        print(f"\n🎉 Done! Generated {len(encodings)} face encodings for {len(set(names))} unique people")
        print(f"output: random_encodings.pkl")
    else:
        print("❌ No encoding found ")

if __name__ == "__main__":
    generate_random_encodings()