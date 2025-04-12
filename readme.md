# Face Recognition Attendance System 👨💻📊

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-orange)
![Face_Recognition](https://img.shields.io/badge/Face_Recognition-1.3%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

An automated attendance system using facial recognition technology that marks attendance by detecting and recognizing faces in real-time.

## Features ✨

- **Face Registration**: Capture and store multiple face images with name and roll number
- **Model Training**: Generate facial encodings for recognition
- **Attendance Marking**: Automatically records attendance with timestamp
- **Duplicate Prevention**: Ensures each person is marked only once per session
- **CSV Export**: Saves attendance records in spreadsheet format
- **Real-time Preview**: Displays recognition results with visual feedback

## Screenshots 🖼️

<div align="center">
  <img src="./assets/Screenshot (38).png" width="45%">
  <img src="./assets/Screenshot (39).png" width="45%">
  <img src="./assets/Screenshot (40).png" width="45%">
  <img src="./assets/Screenshot (41).png" width="45%">
  <img src="./assets/Screenshot (42).png" width="45%">
  <img src="./assets/Screenshot (43).png" width="45%">
  <img src="./assets/Screenshot (44).png" width="45%">
  <img src="./assets/Screenshot (45).png" width="45%">
  <img src="./assets/Screenshot (46).png" width="45%">

</div>

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/priyanshgitthat/face-recognition.git
cd face-recognition

    Create and activate virtual environment:



python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

    Install dependencies:



pip install -r requirements.txt

Usage 🚀

    Register New Faces:



python registerFaces.py

    Enter name and roll number when prompted

    System will capture 100 high-quality face images

    Press 'Q' to stop early

    Train the Model:


python encoding.py

    Generates facial encodings from captured images

    Saves to random_encodings.pkl

    Run Attendance System:



python recognizeFaces.py

    Detects faces and marks attendance automatically

    Records to attendance.csv with timestamp

    Press 'Q' to exit

File Structure 📂


face-recognition/
├── faces/                  # Folder containing registered face images
├── attendance.csv          # Attendance records
├── random_encodings.pkl    # Trained facial encodings
├── encoding.py             # Model training script
├── registerFaces.py        # Face registration script
├── recognizeFaces.py       # Attendance marking script
├── gui.py                  # Graphical user interface
└── requirements.txt        # Dependencies

Technical Details 🔧

    Uses MediaPipe for high-accuracy face detection

    Implements face_recognition library for facial feature extraction

    Applies CLAHE and sharpening filters for image enhancement

    CSV output includes: Name, Roll Number, Date, Time

    Optimized for real-time performance with frame skipping

Contributing 🤝

Contributions are welcome! Please open an issue or PR for any:

    Bug fixes

    Feature enhancements

    Performance improvements

Connect with Me 📬
## 📩 Contact
📧 **Your Name** – [priyanshverma157@gmail.com](mailto:priyanshverma157@gmail.com)  
🔗 **GitHub** – [github.com/priyanshgitthat](https://github.com/priyanshgitthat)  
🔗 **LinkedIn** – [linkedin.com/in/Priyansh Verma](https://www.linkedin.com/in/priyanshv/)  
🔗 **Portfolio** – [priyanshverma.netlify.app](https://priyanshverma.netlify.app/)  
License 📜

This project is licensed under the MIT License - see the LICENSE file for details.

Developed with ❤️ by Priyansh