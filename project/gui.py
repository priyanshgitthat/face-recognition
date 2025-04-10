import customtkinter as ctk
import os  # for checking folder existence
from capture_Faces import capture_faces
app = ctk.CTk()
app.geometry("900x500")
app.title("Face Detection")

def open_registration_window():
    reg_window = ctk.CTkToplevel(app)
    reg_window.geometry("400x250")
    reg_window.title("Register Face")
    reg_window.resizable(False, False)
    reg_window.grab_set()         # 👈 Makes popup modal
    reg_window.focus_force()      # 👈 Focus the popup

    # ✅ Center popup on top of main window
    app.update_idletasks()

    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    popup_width = 400
    popup_height = 250

    center_x = app_x + (app_width // 2) - (popup_width // 2)
    center_y = app_y + (app_height // 2) - (popup_height // 2)

    reg_window.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")

    # 👇 UI Components
    username_entry = ctk.CTkEntry(reg_window, placeholder_text="Enter username")
    username_entry.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

    roll_number_entry = ctk.CTkEntry(reg_window, placeholder_text="Enter roll_number")
    roll_number_entry.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    status_label = ctk.CTkLabel(reg_window, text="")
    status_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def start_registration():
        username = username_entry.get().strip()
        roll_number = roll_number_entry.get().strip()

        if not username or not roll_number:
            status_label.configure(text="⚠️ All fields are required!", text_color="red")
            return

        folder_path = os.path.join("project", "faces", f"{roll_number}_{username}")

        if os.path.exists(folder_path):
            status_label.configure(text="❌ This user already exists!", text_color="orange")
            return

        status_label.configure(text="⏳ Starting face capture...", text_color="blue")
        reg_window.update_idletasks()  # Refresh status label

        # 🟢 Start face capture
        reg_window.destroy()  # Close popup
        capture_faces(username, roll_number)

    start_btn = ctk.CTkButton(reg_window, text="Start", command=start_registration)
    start_btn.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)


# Main registration button
reg_btn = ctk.CTkButton(app, text="Registration", command=open_registration_window)
reg_btn.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

app.mainloop()
