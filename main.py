import speech_recognition as sr
import pyttsx3
from datetime import datetime
import json
import os

# Initialize the speech engine only once
# himanshu Start
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5   # Reduce pause threshold for faster response
        r.energy_threshold = 200  # Adjust sensitivity for quicker response
        print("Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Add timeout and limit to make it faster
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            print("Speech service unavailable")
            return ""

def save_message(name, message, delivery_date, delivery_time):
    messages = load_messages()
    messages.append({"name": name, "message": message, "delivery_date": delivery_date, "delivery_time": delivery_time})
    with open("legacy_messages.json", "w") as f:
        json.dump(messages, f)

def load_messages():
    if os.path.exists("legacy_messages.json"):
        with open("legacy_messages.json", "r") as f:
            return json.load(f)
    return []

def check_messages():
    now = datetime.now()
    messages = load_messages()
    for msg in messages:
        message_datetime = datetime.strptime(f"{msg['delivery_date']} {msg['delivery_time']}", "%Y-%m-%d %H:%M")
        if message_datetime <= now:
            say(f"Message for {msg['name']}: {msg['message']}")
            messages.remove(msg)
    with open("legacy_messages.json", "w") as f:
        json.dump(messages, f)

def handle_general_queries(query):
    responses = {
        "how are you": "I am good, what about you?",
        "me too": "That's great, wanna know me more?",
        "your name": "I am Pushpendra, your virtual assistant.",
        "what can you do": "I can help you with your horoscope, leave messages, and answer your questions.",
        "hello": "Hello! How can I assist you today?",
        "bye": "Goodbye! Have a great day!",
        "GL bajaj":"it is a fucking college fuck you ",
        
    }
    for key in responses:
        if key in query:
            return responses[key]
    return "Sorry, I don't understand."

def determine_zodiac(month, day):
    # Simplified zodiac calculation
    zodiac = {
        (3, 21): "aries", (4, 20): "taurus", (5, 21): "gemini", (6, 21): "cancer",
        (7, 23): "leo", (8, 23): "virgo", (9, 23): "libra", (10, 23): "scorpio",
        (11, 22): "sagittarius", (12, 22): "capricorn", (1, 20): "aquarius", (2, 19): "pisces"
    }
    return next((z for (m, d), z in zodiac.items() if (month, day) >= (m, d)), "pisces")

if __name__ == '__main__':
    say("Hello, I am your assistant.")
    name = ""

    while True:
        query = takeCommand()

        if "my name is" in query:
            name = query.replace("my name is", "").strip()
            say(f"Nice to meet you, {name}!")

        elif "tell me my horoscope" in query:
            say("Please tell me your birth date in the format DD-MM-YYYY.")
            dob = takeCommand()
            try:
                dob_date = datetime.strptime(dob, "%d-%m-%Y")
                sign = determine_zodiac(dob_date.month, dob_date.day)
                say(f"{name}, your zodiac sign is {sign}.")
            except ValueError:
                say("Sorry, I didn't understand your birth date. Please try again.")

        elif "leave a message" in query:
            say("What message would you like to leave?")
            message = takeCommand()
            say("Please tell me the delivery date in the format year-month-day.")
            delivery_date = takeCommand()
            say("Please tell me the delivery time in the format hour and minutes.")
            delivery_time = takeCommand()
            try:
                datetime.strptime(f"{delivery_date} {delivery_time}", "%Y-%m-%d %H:%M")
                save_message(name, message, delivery_date, delivery_time)
                say("Your message has been saved.")
            except ValueError:
                say("Sorry, I didn't understand the date or time format.")

        elif "check my messages" in query:
            check_messages()

        elif "exit" in query or "stop" in query:
            say("Goodbye!")
            break

        else:
            response = handle_general_queries(query)
            say(response)
