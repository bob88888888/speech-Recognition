import speech_recognition as sr
import pyttsx3
import pandas as pd
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')

class basicOp:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        """Speak the given text using the TTS engine."""
        print(f"Saying: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Capture and recognize speech from the microphone."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                print(f"User: {command}")
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return ""
            except sr.RequestError:
                self.speak("There seems to be an issue with the speech recognition service.")
                return ""

class mainOp:
    def __init__(self, file_path):
        self.basic = basicOp()
        self.dir = file_path

    def intro(self):
        self.basic.speak("Hi, welcome to the smart event list app. What do you want to do today?")

    def addEvent(self):
        self.basic.speak("What is the name of the event you want to add?")
        eventName = self.basic.listen()

        self.basic.speak("What is the date for the event?")
        eventDate = self.basic.listen()

        self.basic.speak("What time does the event occur?")
        eventTime = self.basic.listen()

        if eventName and eventDate and eventTime:
            new_event = {"Event": eventName, "Date": eventDate, "Time": eventTime}
        # Append event to CSV
            self.save_event(new_event)
            self.basic.speak("Event has been added successfully.")
        else:
            self.basic.speak("I couldn't get all the details. Please try again.")

    def save_event(self, event):
        """Saves the event to a CSV file"""
        if os.path.exists(self.dir):
            df = pd.read_csv(self.dir)
            df = pd.concat([df, pd.DataFrame([event])], ignore_index=True)
        else:
            df = pd.DataFrame([event])

        df.to_csv(self.dir, index=False)
        print("Event saved:", event)

    def readEvent(self):
        #Reads events from the CSV file and speaks them.
        if os.path.exists(self.dir):
            df = pd.read_csv(self.dir)
            if df.empty:
                self.basic.speak("There are no events scheduled.")
                return

            numEvent = len(df)
            counter = 1
            for _, row in df.iterrows():
                event_details = f"Event {counter}: {row['Event']}, Date: {row['Date']}, Time: {row['Time']}"
                print(event_details)  # Print for debugging
                counter += 1
                self.basic.speak(event_details)
        else:
            self.basic.speak("No event file found. Please add an event first.")

    def countEvent(self):
        df = pd.read_csv(self.dir)
        self.basic.speak("There are total of " + str(len(df)) + " events in the list")

    def delEvent(self):
        if not os.path.exists(self.dir) or os.stat(self.dir).st_size == 0:
            self.basic.speak("There are no events to delete.")
            return
        
        df = pd.read_csv(self.dir)
        self.basic.speak("Which event would you like to remove?")
        
        for index, row in df.iterrows():
            event_details = f"Event {index + 1}: {row['Event']}, Date: {row['Date']}, Time: {row['Time']}"
            print(event_details)
            self.basic.speak(event_details)

        event_name = self.basic.listen()
        
        if event_name:
            df_filtered = df[df["Event"].str.lower() != event_name.lower()]  # Case-insensitive match
            if len(df_filtered) < len(df):
                df_filtered.to_csv(self.dir, index=False)
                self.basic.speak("The event has been removed.")
                
            else:
                self.basic.speak("No matching event found. Please try again")
            
        
def main_loop(fp):
    basic = basicOp()
    main = mainOp(fp)
    main.intro()
    count = 0

    while True:
        command = basic.listen()
        if command in ["exit", "no"]:
            basic.speak("Goodbye, have a nice day!")
            break
        elif "add" in command:
            main.addEvent()
            count += 1
        elif ("show" and "all") in command:
            main.readEvent()
            count += 1
        elif ("How" and "many") in command:
            main.countEvent()
            count += 1
        elif "remove" in command:
            main.delEvent()

        basic.speak("Is there anything else you would like to do?")
        
        
if __name__ == '__main__':
    # Load CSV Safely
    file_path = "C:/Users/bobya/Documents/University/society/speechRecognition/smartCalender/Events.csv"
    if not(os.path.exists(file_path)):
        print(f"Warning: '{file_path}' not found. A new file will be created when an event is added.")

    main_loop(file_path)

