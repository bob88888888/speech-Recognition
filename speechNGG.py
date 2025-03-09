import random
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')

def speak(text):
    """Speak the given text using the TTS engine."""
    print(f"Saying: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
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
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ("Something is wrong")
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
            return ("Something is extremely wrong")

speak("Welcome to number guessing game. Here you guess the number and if you guess the number within 10 tries, you win! But if you cannot guess the correct number within 10 tries, you lose!")
speak("The number will be between 1 and 100")

comp = random.randint(0, 100)
print (comp)

count = 1
while True:

    while True:
        speak("Please choose a number between 1 and 100")
        user = listen()
        if user == "Something is wrong":
            continue
        if user.isdigit():
            break
        else:
            continue
    
    user = int(user)

    speak("Number of tries: " + str(count))
    if user == comp:
        speak("Congradulations, you win!")
        break

    elif user > comp:
        speak("Your number is too big")
        count += 1

    elif user < comp:
        speak("Your number is too small")
        count += 1

    if count > 10:
        speak("You did not guess the number. You lose!")
        break