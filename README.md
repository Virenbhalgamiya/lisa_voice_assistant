# 🎙️ Lisa: Voice-to-Voice AI Assistant

Lisa is an offline, voice-based assistant built with Python. It listens for a wake word ("Hey Siri"), understands your voice commands like setting reminders or managing a to-do list, and responds using speech — all locally on your machine.

---

## ✅ Features

- Wake word detection using Porcupine ("Hey Siri")
- Voice-to-text command parsing
- Add to-do tasks by speaking
- Set voice-triggered reminders (e.g., "remind me after 10 seconds")
- Voice feedback and confirmation
- Continues listening after reminders (non-blocking design)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/lisa_voice_assistant.git
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

Paste your key in main.py file on accesss_key variable at top
