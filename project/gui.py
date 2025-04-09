import customtkinter as ctk
import add_Faces
import os  # for checking folder existence

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

    status_label = ctk.CTkLabel(reg_window, text="")
    status_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

    def start_registration():
        username = username_entry.get().strip()
        if not username:
            status_label.configure(text="⚠️ Username cannot be empty!", text_color="red")
            return

        folder_path = os.path.join("project", "faces", username)

        if os.path.exists(folder_path):
            status_label.configure(text="❌ This username already exists!", text_color="orange")
            return

        add_Faces.capture_faces(username)
        status_label.configure(text=f"✅ {username} registered successfully!", text_color="green")

    start_btn = ctk.CTkButton(reg_window, text="Start", command=start_registration)
    start_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


# Main registration button
reg_btn = ctk.CTkButton(app, text="Registration", command=open_registration_window)
reg_btn.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

app.mainloop()
