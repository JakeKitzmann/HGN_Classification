import customtkinter as CTk
import tkinter as tk

# Set the theme (optional)
CTk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
CTk.set_default_color_theme("blue")  # Sets the default color theme



#this screen will have the dot moving for the eye tracking test.
class TestingScreen(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        #self.title("Moving Dot")
        #self.geometry("1920x1080")
       # self.configure(bg="white")

        self.canvas = CTk.CTkCanvas(self, width=1920, height=1080, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Initial dot position
        self.dot_x = 10
        self.dot_y = 20
        self.dot_radius = 10

        # Dot's movement speed
        self.speed = 5

        # Draw the initial dot
        self.dot = self.canvas.create_oval(self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                                           self.dot_x + self.dot_radius, self.dot_y + self.dot_radius,
                                           fill="black", outline="black")

        # Start the animation
        self.move_dot()

    def move_dot(self):
        # Update the dot's position
        self.dot_x += self.speed

        # Reverse the direction if the dot hits the canvas edge
        if self.dot_x >= self.canvas.winfo_width() - self.dot_radius or self.dot_x <= self.dot_radius:
            self.speed = -self.speed

        # Move the dot
        self.canvas.coords(self.dot, self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                           self.dot_x + self.dot_radius, self.dot_y + self.dot_radius)

        # Repeat the animation every 10 milliseconds
        self.after(10, self.move_dot)


#main start screen
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
        button.place(anchor="center", relx=0.5, rely=0.5)
      

    def switch_to_testing(self):
        # Hide the main frame and show the testing frame
        self.main_frame.pack_forget()
        self.testing_frame.pack(fill="both", expand=True)

# Main
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()





