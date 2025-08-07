import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import random
import wikipedia
import re

# Connection of the Html File.
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['username']
    return f"Hello, {name}!"  # Return response with data from HTML

if __name__ == '__main__':
    app.run(debug=True)

# Backend for the flask
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow JS to call API

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_command = data.get('command', '').lower()

    # Very basic logic (replace this with your AI or logic)
    if 'hello' in user_command:
        response = "Hello Waseem! How can I help you today?"
    elif 'time' in user_command:
        from datetime import datetime
        response = f"The current time is {datetime.now().strftime('%H:%M')}"
    elif 'your name' in user_command:
        response = "I am your Python-powered voice assistant."
    else:
        response = "Sorry, I didn't understand that."

    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)



# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get list of available voices
voices = engine.getProperty('voices')

# Print all available voices
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} ({voice.id})")

# Set voice by index (0 = Male, 1 = Female on many systems)
engine.setProperty('voice', voices[2].id)  # Change index as needed

# Set properties for voice (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")



# Function to greet the user based on the time of day
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!,  Waseem. How can i help you?")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!,  Waseem. How can I help you?")
    else:
        speak("Good evening!,  Waseem. How can I help you?")

def greet1():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning!, . How can i help you?")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!, . How can I help you?")
    else:
        speak("Good evening!, . How can I help you?")



# Function to listen to user's command via microphone
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please repeat.")
        speak("Sorry, I couldn't understand. Please repeat.")
        return None
    except sr.RequestError:
        print("Sorry, there is an issue with the speech service.")
        speak("Sorry, there is an issue with the speech service.")
        return None

# Function to get user input from the terminal
def get_text_input():
    query = input("Please enter your command: ")
    return query.lower()

# Function to fetch Wikipedia summary
def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation Error:"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "The request timed out. Please try again."
    except wikipedia.exceptions.RedirectError as e:
        return f"Redirect Error: {e.args}"
    except Exception as e:
        return f"An error occurred: {e}"

# Function to perform tasks based on user query
def execute_command(query):
    if 'hello' in query:
        speak("Hi. How can I assist you?")
    
    elif 'how are you' in query:
        speak("I'm doing great! Thank you for asking.")
    
    elif 'what is the time' in query:
        speak(f"The current time is {get_time()}")

    elif 'say hi to' in query:
        speak("Hello ! Hope you are having a great day!")

    # Inside your execute_command function:
    elif 'search' in query and 'in youtube' in query:
    # Extract the search term by removing 'search' and 'in youtube'
        search_term = query.replace('search', '').replace('in youtube', '').strip()
        if search_term:
            url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Searching YouTube for {search_term}")
        else:
            speak("Please tell me what to search for on YouTube.")


    elif 'open instagram' in query:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")

    elif 'open facebook' in query:
        webbrowser.open("https://www.facebook.com")
        speak("Opening Facebook.")
    
    elif 'play music' in query:
        music_folder = "D:\\MUSIC\\"  # Ensure this is a valid folder path
        try:
            songs = os.listdir(music_folder)
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_folder, song))
                speak(f"Playing {song}.")
            else:
                speak("No songs found in the folder.")
        except Exception as e:
            speak(f"Could not play music due to: {e}")
    
    elif 'search' in query:
        query = query.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
        else:
            speak("Please tell me what to search for.")

    elif 'what is' in query:
        query = query.replace("what is", "").strip()
        if query:
            summary = get_wikipedia_summary(query)
            speak(summary)
        else:
            speak("Please specify what you want to know.")
    
    # Math Operations
    elif 'add' in query or 'plus' in query:
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            result = sum(int(num) for num in numbers)
            speak(f"The sum is {result}")
        else:
            speak("Please provide two numbers.")

    elif 'subtract' in query or 'minus' in query:
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            result = int(numbers[0]) - int(numbers[1])
            speak(f"The result is {result}")
        else:
            speak("Please provide two numbers.")

    elif 'multiply' in query or 'times' in query:
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            result = 1
            for num in numbers:
                result *= int(num)
            speak(f"The result is {result}")
        else:
            speak("Please provide two numbers.")

    elif 'divide' in query:
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            if int(numbers[1]) == 0:
                speak("Cannot divide by zero.")
            else:
                result = int(numbers[0]) / int(numbers[1])
                speak(f"The result is {result}")
        else:
            speak("Please provide two numbers.")

    elif 'modulus' in query:
        numbers = re.findall(r'\d+', query)
        if len(numbers) >= 2:
            result = int(numbers[0]) % int(numbers[1])
            speak(f"The remainder is {result}")
        else:
            speak("Please provide two numbers.")

    # Opening Apps
    elif 'open whatsapp' in query:
        try:
            os.system("start whatsapp")
            speak("Opening WhatsApp.")
        except Exception as e:
            speak(f"Could not open WhatsApp: {e}")

    elif 'open spotify' in query:
        try:
            os.system("start spotify")
            speak("Opening Spotify.")
        except Exception as e:
            speak(f"Could not open Spotify: {e}")

    # System Commands
    elif 'shutdown' in query or 'power off' in query:
        speak("Shutting down... Shutting down... Shutting down...")
        exit()
    
    else:
        speak("Sorry, I didn't quite get that. Can you please repeat?")

# Main function to run the assistant
def run_assistant():
    """Main function to run the voice assistant."""
    speak("Welcome!")

    # Input Mode Selection (First step)
    input_mode = None
    while True:
        mode_choice = input("Would you like to speak your command or type it? (speak/type): ").strip().lower()
        if mode_choice in ["speak", "type"]:
            input_mode = mode_choice
            break
        else:
            print("Invalid input mode. Please type 'speak' or 'type'.")

    # Account Selection (Now using the selected input mode)
    user_name = None
    while True:
        # Ask the user for their account using the selected input mode
        if input_mode == "speak":
            speak("Are you User or a guest?") # Speak the prompt
            account_choice_raw = listen()      # Listen for the account choice
        else:  # input_mode == "type"
            account_choice_raw = input("Are you User or a guest? (User/guest): ").strip() # Get typed input

        if account_choice_raw: # Check if any input was received
            account_choice = account_choice_raw.lower() # Convert to lowercase for easier comparison

            if account_choice == "user":
                # Get password using the selected input mode
                if input_mode == "speak":
                    speak("Please say the password.")
                    password = listen()
                else: # input_mode == "type"
                    password = input("Please enter the password: ")

                if password and password == "2006": # Check if password was received and is correct
                    user_name = "user"
                    greet()
                    break # Exit the account selection loop
                else:
                    print("Incorrect password or no password received.")
                    speak("Incorrect password.")
            elif account_choice == "guest":
                greet1() # Greet without a name
                break # Exit the account selection loop
            else:
                print("Invalid account choice. Please say or type 'User' or 'guest'.")
                speak("Invalid account choice. Please say or type User or guest.")
        else:
            print("No account choice received. Please try again.")
            speak("No account choice received. Please try again.")


    # Main loop for commands
    while True:
        if input_mode == "speak":
            query = listen()
        else:  # input_mode == "type"
            query = get_text_input()

        if query:
            execute_command(query)

# Run the assistant
if __name__ == "__main__":
    run_assistant()