from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window

#This is to test the GUI using Kivy
# this will be the main gui for the HGN test 
# This program uses the Kivy library to create a GUI
# "python -m pip install --upgrade pip wheel virtualenv"
# "python -m pip install kivy[base] kivy_examples"



class MovingDot(Widget):
    def __init__(self, **kwargs):
        super(MovingDot, self).__init__(**kwargs)
        self.dot_size = 50  # Size of the dot
        self.x_pos = 0  # Initial position of the dot
        self.update_time = 1/60.0  # Update time (60 FPS)
        self.direction = 1  # Direction of movement: 1 for right, -1 for left
        
        # Set the background color to white
        Window.clearcolor = (1, 1, 1, 1)
        
        # Schedule the update method to be called every frame
        Clock.schedule_interval(self.update, self.update_time)

    def update(self, *args):
        self.canvas.clear()  # Clear the canvas
        
        with self.canvas:
            # Draw the black dot
            Color(0, 0, 0)
            Ellipse(pos=(self.x_pos, self.center_y - self.dot_size / 2), size=(self.dot_size, self.dot_size))
        
        # Update the position of the dot
        self.x_pos += 4 * self.direction  # Move the dot
        
        # Change direction if the dot reaches the window boundaries
        if self.x_pos > Window.width - self.dot_size or self.x_pos < 0:
            self.direction *= -1

class MovingDotApp(App):
    def build(self):
        return MovingDot()

if __name__ == '__main__':
    MovingDotApp().run()