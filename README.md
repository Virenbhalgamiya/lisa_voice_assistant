# 🎙️ Lisa: Voice-to-Voice AI Assistant

Lisa is an offline, voice-based assistant built with Python. It listens for a wake word ("Hey Siri"), understands your voice commands like setting reminders or managing a to-do list, and responds using speech — all locally on your machine.

---

## ✅ Features

- Wake word detection using Porcupine ("Hey Siri")
- Voice-to-text command parsing
- Add to-do tasks by speaking
- Set voice-triggered reminders (e.g., "remind me after 10 seconds")
- Show you previous to-do's by saying ("show|display|list|tell|get|see|what")
- You can stop it by saying ("stop|exit|break|bye|thank you|quit|goodbye|enough|shut up|close") 

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Virenbhalgamiya/lisa_voice_assistant.git
cd lisa_voice_assistant
```
### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
```
#### 🔄 Activate the Environment

##### 🪟 Windows

```bash
venv\Scripts\activate
```
##### 🐧 macOS/Linux
```bash
source venv/bin/activate
```
### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```
If pyaudio throws errors, try:
```bash
pip install pipwin
pipwin install pyaudio
```
🔑 Porcupine Access Key Setup

Go to https://console.picovoice.ai/

Sign in and generate a free Access Key

Paste your key in main.py file on access_key variable at top

### ▶️ Run Lisa
Once setup is complete:
```bash
python main.py
```
# Additional markdown content for the remaining sections
additional_markdown = """
## 🗣️ Example Commands

- `Add call mum`
- `Add homework`
- `Remind me after 5 seconds`
- `Remind me after 10 minutes`

---

## 📁 Project Structure
```plaintext
lisa_voice_assistant/
├── main.py          # Main program file
├── requirements.txt # Required packages
└── README.md        # This file
```

## 📦 Example requirements.txt
If it's missing, create a file `requirements.txt` with:

```plaintext
nginx
pvporcupine
speechrecognition
pyttsx3
pyaudio
```

## 🧪 Sample Interaction
```plaintext
Listening for wake word...
Wake word detected!
Lisa: Yes?
Listening for your command...
You said: remind me after 5 seconds
Parsed Command: remind me after 5 seconds
Lisa: Reminder set to alert after 5 seconds.
Lisa: Hey! It's time to review your to-do list.
Lisa will continue listening after this — no blocking or deadlock occurs.
```
##  👾Challenges
- Need to wake up the assistant again after setting a reminder.
- Application needs to be restarted to after getting alerts.


## 👨‍💻 Author
**Viren Bhalgamiya**
Smart reminder & task management using voice

## 📄 License
For educational use only. Do not distribute commercially without permission

