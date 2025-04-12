import customtkinter as ctk
from tkinter import messagebox
from registerFaces import add_faces
from encoding import generate_random_encodings
import threading
import os
import cv2
import face_recognition
import pickle
import numpy as np
import csv
from datetime import datetime

# Theme setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FaceRecognitionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition Attendance System")
        self.geometry("600x500")
        
        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.attendance_active = False
        self.marked_attendance = set()  # To track already marked attendance
        
    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Title
        ctk.CTkLabel(main_frame, 
                    text="Face Recognition Attendance System",
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        # Register button
        ctk.CTkButton(main_frame,
                     text="Register New Face",
                     command=self.open_register_popup,
                     width=200).pack(pady=10)
        
        # Train Model button
        self.train_btn = ctk.CTkButton(main_frame,
                                     text="Train Model",
                                     command=self.start_training,
                                     width=200)
        self.train_btn.pack(pady=10)
        
        # Take Attendance button
        self.attendance_btn = ctk.CTkButton(main_frame,
                                          text="Take Attendance",
                                          command=self.toggle_attendance,
                                          width=200,
                                          fg_color="green",
                                          hover_color="dark green")
        self.attendance_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(main_frame, width=300)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(main_frame, text="Ready")
        self.status_label.pack(pady=10)
        
        # Exit button
        ctk.CTkButton(main_frame,
                     text="Exit",
                     command=self.destroy,
                     width=200).pack(pady=10)
    
    def open_register_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Register Face")
        popup.geometry("350x250")
        popup.transient(self)
        popup.grab_set()
        
        # Form
        ctk.CTkLabel(popup, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = ctk.CTkEntry(popup, width=200)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(popup, text="Roll Number:").grid(row=1, column=0, padx=10, pady=10)
        self.roll_entry = ctk.CTkEntry(popup, width=200)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkButton(popup, 
                     text="Start Registration", 
                     command=self.start_registration).grid(row=2, column=0, columnspan=2, pady=20)
    
    def start_registration(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        
        if not name or not roll:
            messagebox.showerror("Error", "Please enter both name and roll number")
            return
        
        threading.Thread(target=add_faces, args=(name, roll), daemon=True).start()
        messagebox.showinfo("Started", "Face registration process started!")
    
    def start_training(self):
        if not os.path.exists("faces"):
            messagebox.showerror("Error", "No 'faces' directory found!")
            return
            
        self.train_btn.configure(state="disabled")
        self.status_label.configure(text="Training model...")
        self.progress.start()
        
        threading.Thread(target=self.run_training, daemon=True).start()
    
    def run_training(self):
        try:
            generate_random_encodings()
            self.after(0, lambda: self.status_label.configure(
                text="Training completed successfully!",
                text_color="green"
            ))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(
                text=f"Error: {str(e)}",
                text_color="red"
            ))
        finally:
            self.after(0, lambda: self.train_btn.configure(state="normal"))
            self.after(0, self.progress.stop)
    
    def toggle_attendance(self):
        if not os.path.exists("random_encodings.pkl"):
            messagebox.showerror("Error", "First train the model using 'Train Model' button")
            return
            
        if not self.attendance_active:
            # Initialize attendance file if not exists
            if not os.path.exists("attendance.csv"):
                with open("attendance.csv", mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Roll Number", "Date", "Time"])
            
            self.attendance_active = True
            self.marked_attendance = set()  # Reset marked attendance
            self.attendance_btn.configure(text="Stop Attendance", fg_color="red", hover_color="dark red")
            self.train_btn.configure(state="disabled")
            self.status_label.configure(text="Starting attendance system...")
            threading.Thread(target=self.run_attendance, daemon=True).start()
        else:
            self.attendance_active = False
            self.attendance_btn.configure(text="Take Attendance", fg_color="green", hover_color="dark green")
            self.train_btn.configure(state="normal")
            self.status_label.configure(text="Attendance system stopped")
    
    def run_attendance(self):
        try:
            # Load encodings
            with open("random_encodings.pkl", "rb") as f:
                data = pickle.load(f)
            known_encodings = data["encodings"]
            known_names = data["names"]
            known_roll_numbers = data.get("roll_numbers", ["N/A"]*len(known_names))
            
            # Camera setup
            video_capture = cv2.VideoCapture(0)
            
            while self.attendance_active:
                ret, frame = video_capture.read()
                if not ret:
                    break
                
                # Resize and convert
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                # Face detection
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_info = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_encodings, face_encoding, 0.6)
                    name = "Unknown"
                    roll = "N/A"
                    
                    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                        roll = known_roll_numbers[best_match_index]
                        
                        # Mark attendance if not already marked
                        if name not in self.marked_attendance:
                            now = datetime.now()
                            date = now.strftime("%Y-%m-%d")
                            time = now.strftime("%H:%M:%S")
                            
                            with open("attendance.csv", mode='a', newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow([name, roll, date, time])
                            
                            self.marked_attendance.add(name)
                            self.after(0, lambda: self.status_label.configure(
                                text=f"Attendance marked for {name}",
                                text_color="green"
                            ))
                    
                    face_info.append((name, roll))
                
                # Display results with attendance status
                for (top, right, bottom, left), (name, roll) in zip(face_locations, face_info):
                    top *= 4; right *= 4; bottom *= 4; left *= 4
                    
                    # Draw rectangle and info box
                    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(frame, (left, bottom - 70), (right, bottom), color, cv2.FILLED)
                    
                    # Display name and roll number
                    cv2.putText(frame, f"Name: {name}", (left + 6, bottom - 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(frame, f"Roll: {roll}", (left + 6, bottom - 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    
                    # Display attendance status
                    if name in self.marked_attendance:
                        cv2.putText(frame, "Status: Marked", (left + 6, bottom - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    elif name != "Unknown":
                        cv2.putText(frame, "Status: Not Marked", (left + 6, bottom - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                cv2.imshow('Attendance System', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            video_capture.release()
            cv2.destroyAllWindows()
            self.after(0, lambda: self.status_label.configure(text="Attendance system stopped"))
            
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(
                text=f"Attendance error: {str(e)}",
                text_color="red"
            ))
        finally:
            self.after(0, lambda: self.attendance_btn.configure(
                text="Take Attendance", 
                fg_color="green", 
                hover_color="dark green"
            ))
            self.after(0, lambda: self.train_btn.configure(state="normal"))
            self.attendance_active = False

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.mainloop()