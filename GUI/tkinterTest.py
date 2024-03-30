import customtkinter as ctk
import tkinter as tk



class BaseScene(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()

class MainScene(BaseScene):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="This is the Main Scene").pack(pady=20)
        ctk.CTkButton(self, text="Go to Scene 2", command=lambda: master.switch_scene(SecondScene)).pack()

class SecondScene(BaseScene):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="This is the Second Scene").pack(pady=20)
        ctk.CTkButton(self, text="Back to Main Scene", command=lambda: master.switch_scene(MainScene)).pack()




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scene Switcher")
        self.geometry("400x300")

        self.scenes = {}
        self.current_scene = None
        self.switch_scene(MainScene)

    def switch_scene(self, scene_class):
        if self.current_scene is not None:
            self.current_scene.hide()
        scene = self.scenes.get(scene_class)
        if scene is None:
            scene = scene_class(self)
            self.scenes[scene_class] = scene
        self.current_scene = scene
        self.current_scene.show()

if __name__ == "__main__":
    app = App()
    app.mainloop()












#moving dot animation for second scene 



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

