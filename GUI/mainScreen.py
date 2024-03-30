import customtkinter as CTk
import tkinter as tk

# Set the theme (optional)
CTk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
CTk.set_default_color_theme("blue")  # Sets the default color theme

class TestingScreen(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = CTk.CTkLabel(self, text="This is the testing screen")
        label.pack()

class MainApplication(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Main Screen')
        self.geometry('1920x1080')  # Set the size of the window

        # Main screen frame
        self.main_frame = CTk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Testing screen frame (initially not visible)
        self.testing_frame = TestingScreen(self)
        self.testing_frame.pack_forget()

        # Button on the main screen to switch to the testing screen
        button = CTk.CTkButton(self.main_frame, text="Testing", command=self.switch_to_testing, width=300, height=80)
        button.pack()

    def switch_to_testing(self):
        # Hide the main frame and show the testing frame
        self.main_frame.pack_forget()
        self.testing_frame.pack(fill="both", expand=True)

# Main
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()





