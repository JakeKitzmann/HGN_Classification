import customtkinter as ctk
import tkinter as tk

class MovingDotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Moving Dot")
        self.geometry("1920x1080")
        self.configure(bg="white")

        self.canvas = ctk.CTkCanvas(self, width=1920, height=1080, bg="white", highlightthickness=0)
        self.canvas.pack()

        # Initial dot position
        self.dot_x = 10
        self.dot_y = 200
        self.dot_radius = 10

        # Dot's movement speed
        self.speed = 2

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

if __name__ == "__main__":
    app = MovingDotApp()
    app.mainloop()