import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
import pyttsx3
import schedule
import time
import threading
import re
from datetime import datetime
import os
import json

last_reminder_time = 0.0
REMINDER_COOLDOWN = 3.0   # seconds to ignore wake-word after reminder

access_key = "your_pvporcupine_access_key"


# Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
speak_lock = threading.Lock()
# Global flag
reminder_speaking = threading.Event()
stream = None

# Your Picovoice Access Key
# replace with actual key

# Global to-do list
to_do_list = []
DATA_FILE = "todo_data.json"

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(to_do_list, f)

def load_tasks():
    global to_do_list
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                to_do_list = json.load(f)
            except json.JSONDecodeError:
                to_do_list = []

def speak(text):
    global stream
    with speak_lock:
        # pause mic
        if stream is not None:
            try:
                stream.stop_stream()
            except:
                pass

        print("Lisa:", text)
        engine.say(text)
        engine.runAndWait()

        # resume mic
        if stream is not None:
            try:
                stream.start_stream()
            except:
                pass


def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def trigger_reminder():
    def _reminder_job():
        global last_reminder_time
        speak("Hey! It's time to review your to-do list.")
        if to_do_list:
            for task in to_do_list:
                speak(task)
        else:
            speak("You have no tasks in your list.")
        # start cooldown
        last_reminder_time = time.time()

    threading.Thread(target=_reminder_job, daemon=True).start()



def handle_task_input():
    while True:
        command = listen_command()
        if not command:
            continue

        print("Parsed Command:", command)

        stop_words_pattern = r"\b(stop|exit|break|bye|thank you|quit|goodbye|enough|shut up|close)\b"
        
        # Check if the command contains any of the stop words
        if re.search(r"\b(stop|exit|quit|bye|thank you|that's all|enough|no more)\b",command,re.IGNORECASE):
            speak("Stopping task input.")
            break

        tasks_added = False
        
        # Match show command
        if re.search(r"\b(show|display|list|tell|get|see|what(?:'s| is)?)\b", command,re.IGNORECASE):
            if to_do_list:
                speak("Here are your tasks:")
                for task in to_do_list:
                    speak(task)
            else:
                speak("Your to-do list is empty.")
            continue

        # Match multiple add task commands with to-do list
        task_match = re.findall(r"add (.+?) to (my )?(to[- ]?do list|todo list)", command)
        if task_match:
            for match in task_match:
                task = match[0].strip()
                to_do_list.append(task)
                save_tasks()
                tasks_added = True
                speak(f"Added '{task}' to your to-do list.")

        elif "add" in command:
            fallback = command.replace("add", "").strip()
            if fallback:
                to_do_list.append(fallback)
                save_tasks()
                tasks_added = True
                speak(f"Added '{fallback}' to your to-do list.")

        time_match = re.search(r"remind me at (\d{1,2})(?::(\d{2}))?\s?(am|pm)", command)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            meridiem = time_match.group(3).lower()

            if meridiem == "pm" and hour != 12:
                hour += 12
            if meridiem == "am" and hour == 12:
                hour = 0

            reminder_time = f"{hour:02d}:{minute:02d}"
            schedule.every().day.at(reminder_time).do(trigger_reminder)
            speak(f"Reminder set for {hour % 12 or 12}:{minute:02d} {meridiem.upper()}.")
            break

        # Handle reminder after specific time
        time_match_seconds = re.search(r"remind me after (\d+)\s?(seconds?|minutes?)", command)
        if time_match_seconds:
            time_value = int(time_match_seconds.group(1))
            unit = time_match_seconds.group(2)

            if "minute" in unit:
                time_in_seconds = time_value * 60
            else:
                time_in_seconds = time_value

            # Schedule the reminder in a non-blocking manner using threading
            threading.Timer(time_in_seconds, trigger_reminder).start()
            speak(f"Reminder set to alert after {time_value} {unit}.")
            break

        if not tasks_added:
            speak("I didn't understand. Please say something like 'add buy milk to my to-do list', 'remind me at 8 PM', or 'remind me after 10 minutes'.")

def schedule_runner():
    while True:
        schedule.run_pending()
        time.sleep(1)

def wake_word_listener():
    global last_reminder_time
    porcupine = pvporcupine.create(keywords=["hey siri"], access_key=access_key)
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word...")
    try:
        while True:
            # Safely read from mic
            try:
                pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            except OSError:
                # Microphone buffer underflow or stream error; skip this frame
                continue

            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Cooldown after reminders
            if time.time() - last_reminder_time < REMINDER_COOLDOWN:
                continue

            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                speak("Yes?")
                handle_task_input()
                print("Listening for wake word again...")
    except KeyboardInterrupt:
        print("Shutting down Lisa.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


# Start the scheduler in background
threading.Thread(target=schedule_runner, daemon=True).start()

# Start Lisa
load_tasks()
wake_word_listener()
