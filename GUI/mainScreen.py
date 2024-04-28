import customtkinter as CTk
import tkinter as tk
from record import recordVideo
import threading 
from PIL import ImageFont
import firebase_admin   # pip install firebase_admin
from firebase_admin import db as firebase_db, credentials
import socket
import json
import time


# Load the font file
font_path = "GUI/fonts/sofiapro-light.otf"
sofiaPro = ImageFont.truetype(font_path, size=16)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("GUI/ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://iot-term-project-4c046-default-rtdb.firebaseio.com/'})

# Now you can use the font in your project
# Set the theme (optional)
CTk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
CTk.set_default_color_theme("blue")  # Sets the default color theme

 
screenWidth = 1920
screenHeight = 1080
currentTime = 0
move = None

################
# REMOVE LATER #
################
eye_positions = [960, 973, 975, 987, 998, 1004, 1020, 1025, 1030, 1032, 1038, 1044, 1050, 1059, 1060, 1066, 1070]

################################################################################################################################################
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

        #Search frame(intially not visivle)
        self.search_frame = SearchScreen(self)
        self.search_frame.pack_forget()

        #wait for resutls frame( initially not visible)
        self.caseResult_frame = caseResult(self)
        self.caseResult_frame.pack_forget()


        # Create a frame to act as the box
        intro_box = CTk.CTkFrame(self.main_frame, fg_color="#3b8ed0")
        intro_box.place(anchor="center", relx=0.25, rely=0.5)
        intro_box.place_configure(width=screenWidth/1.98, height=screenHeight+5)

        #Title 
        title_text = CTk.CTkLabel(intro_box, text="The HNG Test", font = (sofiaPro, 48, "bold"), text_color = "white")
        title_text.pack(side = "top", pady = (screenHeight*.35, 10))
        #intro
        directionsText = "Directions: Keep head 4-6 inches away from webcam and keep "
        HNGintro = "The Horizontal Gaze Nystagmus Test (HGN) is a screening method commonly utilized in various contexts to assess eye movement patterns. It involves tracking the movement of an object with the eyes, observing for any irregularities in the smoothness and continuity of gaze. In a typical HGN test, the subject is instructed to follow a moving target horizontally across their field of vision while maintaining a stable head position. The test aims to identify any deviations from normal eye movement patterns, which may indicate underlying physiological or neurological conditions. By analyzing the quality and consistency of gaze tracking, HGN testing can provide valuable insights into visual function and ocular health."
        directions_text = CTk.CTkLabel(intro_box, text=HNGintro, wraplength= 850, font = (sofiaPro, 24), text_color = "white", justify = "left")
        directions_text.pack(fill = "both", pady = 10, padx = 10)
        

        # Button on the main screen to switch to the testing screen
        button = CTk.CTkButton(self.main_frame, text="HNG Testing", command=self.switch_to_testing, width=300, height=80, font=(sofiaPro, 18))
        button.place(anchor="center", relx=0.75, rely=0.5)

        # Button to switch to search screen 
        button = CTk.CTkButton(self.main_frame, text="Search Cases", command=self.switch_to_search, width=300, height=80, font=(sofiaPro, 18))
        button.place(anchor="center", relx=0.75, rely=0.6)
        
      
    #switch to testing scene 
    def switch_to_testing(self):
        # Hide the main frame and show the testing frame
        self.main_frame.pack_forget()
        self.testing_frame.pack(fill="both", expand=True)
        self.testing_frame.update_idletasks()

    #switch to search scene
    def switch_to_search(self):
        self.main_frame.pack_forget()
        self.search_frame.pack(fill="both", expand=True)
        self.search_frame.update_idletasks()
   

###########################################################################################################################################
#this screen will have the dot moving for the eye tracking test.
caseNumber = 0
class TestingScreen(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize socket connection to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 4000)
        self.client_socket.connect(self.server_address)

        #GET NEXT AVAILABLE CASE NUMBER FROM FIRE BASE HERE &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&           *******         *************       *********
        caseNumber = 111
     
        self.canvas = CTk.CTkCanvas(self, width=1920, height=1080, highlightthickness=0)

        #directions frame 
        directionsBox = CTk.CTkFrame(self, fg_color="#3b8ed0")
        directionsBox.place(anchor="center", relx=0.5, rely=0.75)
        directionsBox.place_configure(width=400, height=250)


        #user directions %%%% need to adjsut 
        directions = "\n \n- Keep eyes level with webcam \n- Keep head forward and track dot with eyes only \n - Remain 2-4 inches away from webcam \n- Continue for duration of test \n- Press Begin Test when ready"
        directions_text = CTk.CTkLabel(directionsBox, text=directions, wraplength= 850, font = (sofiaPro, 18), text_color = "white", justify = "left")
        directions_text.place(anchor = "s", relx = .5, rely = .85)
        
        self.canvas.pack()

        # Initial dot position
        screenWidth = 1920/2
        self.dot_x = 960
        self.dot_y = 20
        self.dot_radius = 10

        # Dot's movement speed
        self.speed = 6

        self.is_moving = False
        # Draw the initial dot
        
        self.dot = self.canvas.create_oval(self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                                           self.dot_x + self.dot_radius, self.dot_y + self.dot_radius,
                                           fill="black", outline="black")
      

        #button to return to the main screen
        self.button = CTk.CTkButton(self, text="Return to Main", command=self.return_to_main, width=100, height=60,font=(sofiaPro, 18))
        self.button.place(anchor="s", relx=0.05, rely=0.95)
        
        #button to begin test
        self.button2 = CTk.CTkButton(self, text="Begin Test", command=self.start_test, width=400, height=60,font=(sofiaPro, 18))
        self.button2.place(anchor="s", relx=0.5, rely=0.4)
        #self.button2.place()  # Place the button back
        # Start the animation
        #self.move_dot()

    # Function to send eye tracking data to the server
    def send_eye_tracking_data(self, x_position):
        data = {
            'x_position': x_position
        }
        message = json.dumps(data)
        self.client_socket.sendall(message.encode())

    # Function to send eye tracking data continously
    def send_eye_tracking_data_continously(self):
        # Simulate sending eye tracking data after updating dot's position
        for x_position in eye_positions:
            self.send_eye_tracking_data(x_position)
            # Sleep for short time to simulate eye movement
            time.sleep(1)

    
    #start the test and flag is_moving as true 
    def start_test(self):
        
        self.button2.configure(state="disabled")
        #print("start test")
        self.is_moving = True
        self.speed = 8
    
        self.start_time = time.time()
        self.recording_duration = 24 # Duration in seconds, there is a delay before the test starts so we can make the dot move a little extra 

        #record = threading.Thread(target=recordVideo).start()
        time.sleep(2)
        self.move_dot()
     
        
    def move_dot(self):
        #move = True
        
        
        # Update the dot's position
        self.dot_x += self.speed

        # Reverse the direction if the dot hits the canvas edge
        if self.dot_x >= self.canvas.winfo_width() - self.dot_radius or self.dot_x <= self.dot_radius:
            self.speed = -self.speed
            

        # Move the dot
        self.canvas.coords(self.dot, self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                           self.dot_x + self.dot_radius, self.dot_y + self.dot_radius)
        
        #turn off after 20 seconds
        elapsed_time = time.time() - currentTime

        # Convert elapsed time to integer to truncate the decimal part

        # Repeat the animation every 10 milliseconds    
        if self.is_moving and time.time() - self.start_time < self.recording_duration:
            self.after(10, self.move_dot)
        else:
            self.switch_to_results()
    

    def reset_screen(self):
        # Reset all attributes to their initial values
        self.is_moving = False
        self.button2.configure(state="normal")
        self.dot_x = 960
        self.dot_y = 20
        self.speed = 0
        self.canvas.coords(self.dot, self.dot_x - self.dot_radius, self.dot_y - self.dot_radius,
                           self.dot_x + self.dot_radius, self.dot_y + self.dot_radius)  # Reset dot position
        
    #swap to main scene 
    def return_to_main(self):
        
        self.reset_screen()
        
        self.master.testing_frame.pack_forget()
       # self.pack_forget()
       
        self.master.main_frame.pack(fill="both", expand=True)
        #self.master.main_frame.update()
        self.master.main_frame.update_idletasks()

    def switch_to_results(self):
        # Hide the main frame and show the testing frame
        self.reset_screen()
        self.master.testing_frame.pack_forget()
        self.master.caseResult_frame.pack(fill="both", expand=True)
        self.master.caseResult_frame.update_idletasks()

##################################################################################################################################
global caseFound
class SearchScreen(CTk.CTkFrame):
    caseFound = False 
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = CTk.CTkCanvas(self, width=screenWidth, height=screenHeight, highlightthickness=0)
        self.canvas.pack()

        
        #search box label 
        searchLabel = CTk.CTkLabel(self, text = "Search by case", font = (sofiaPro, 34, "bold"), bg_color= "#f0f0f0", fg_color= "#f0f0f0")
        searchLabel.place(anchor = "s", relx = .5, rely = .45)

        #search field 
        self.search_field = CTk.CTkEntry(self, width = 250, font = (sofiaPro, 16), placeholder_text="Enter case number here")
        self.search_field.place(anchor = "s", relx = .5, rely = .5)

        #is case number in data base?
       
      
        #return to main button 
        self.button = CTk.CTkButton(self, text="Return to Main", command=self.return_to_main, width=100, height=60,font=(sofiaPro, 18))
        self.button.place(anchor="s", relx=0.05, rely=0.95)

        def on_enter_pressed(event):
            user_input = self.search_field.get()
            # search database for case number
            caseResults(user_input)

        # Bind the <Return> key event to the search field
        self.search_field.bind("<Return>", on_enter_pressed)


        #handle what the database sends about the case number 
        def caseResults(user_input):
            ref = firebase_db.reference('/Case Numbers')
            snapshot = ref.order_by_key().equal_to(user_input).get()
            if snapshot:
                print("Case number found. Data: ", snapshot[user_input])
                results = CTk.CTkLabel(self, text=("Case number found. Data: ", snapshot[user_input]), wraplength= 850, font = (sofiaPro, 18), text_color = "black", justify = "left")
                results.place(anchor = "s", relx = .5, rely = .85)

            else:
                print("Case number not found.")


            #print("Case number =", user_input)

    def return_to_main(self):
       # self.reset_screen()
        self.search_field.delete(0, 'end')
        self.search_field._placeholder_text = "Enter case number here"
        self.master.search_frame.pack_forget()
       # self.pack_forget()
       
        self.master.main_frame.pack(fill="both", expand=True)
        #self.master.main_frame.update()
        self.master.main_frame.update_idletasks()
        
#===============================================================================================================================
class caseResult(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = CTk.CTkCanvas(self, width=screenWidth, height=screenHeight, highlightthickness=0)
        self.canvas.pack()

        intro_box = CTk.CTkFrame(self, fg_color="#3b8ed0")
        intro_box.place(anchor="center", relx=0.5, rely=0.5)
        intro_box.place_configure(width=600, height=250)



        #search box label 
        searchLabel = CTk.CTkLabel(intro_box, text = "Waiting for results of case: " + str(caseNumber), font = (sofiaPro, 34, "bold"))
        searchLabel.place(anchor = "s", relx = .5, rely = .45)

        #label for case results 

        #MIGHT NOT BE ABLE TO GET CASE TO SHOW UP HERE THIS WINDOW MIGHT BE FOR ONLY SHOWING THE CASE NUMBER IF WE DONT HAVE TIME TO FIGURE THAT OUT 

        
        #return to main button 
        self.button = CTk.CTkButton(self, text="Return to Main", command=self.return_to_main, width=100, height=60,font=(sofiaPro, 18))
        self.button.place(anchor="s", relx=0.05, rely=0.95)


    def return_to_main(self):

        self.master.caseResult_frame.pack_forget()
        self.master.main_frame.pack(fill="both", expand=True)
        #self.master.main_frame.update()
        self.master.main_frame.update_idletasks()


# Main
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()





