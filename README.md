# Victo_AI
Victo AI is a voice-activated smart assistant built with Streamlit, Speech Recognition, Google Gemini AI, and WeatherStack API. It allows users to set and manage alarms using voice commands, fetch real-time weather updates, and receive AI-powered bedtime advice. 🚀🎤⏰  

# 🌁️ Victo AI - Smart Assistant

Victo AI is a **voice-controlled assistant** that allows users to **set and manage alarms using voice commands**. It also provides **real-time weather updates** and **AI-powered bedtime advice** based on the user’s alarm time. Built using **Streamlit, Speech Recognition, Google Gemini AI, and WeatherStack API**, this project creates a seamless and intelligent user experience.

Features
👉 **Voice Activation** - Say `"Hey Victo"` to wake up the assistant.  
👉 **Speech-to-Text Processing** - Converts voice commands into text.  
👉 **Alarm Management** - Set, delete, and list alarms using voice commands.  
👉 **Persistent Storage** - Alarms are stored in a JSON file and persist after restarts.  
👉 **Real-Time Weather Updates** - Fetches the current weather using the WeatherStack API.  
👉 **AI-Powered Sleep Advice** - Uses Gemini AI to recommend optimal bedtimes based on your alarm.  
👉 **Streamlit UI** - A clean and interactive web-based interface.  

---

## 📆 Project Structure
```
Victo-AI/
│── .env                  # Stores API keys securely
│── alarms.json            # Stores alarm data persistently
│── app.py                 # Main application file
│── requirements.txt       # Required Python dependencies

Installation & Setup

### 1️⃣ Clone the Repository (If Using GitHub)
```bash
git clone https://github.com/yourusername/victo-ai.git
cd victo-ai
```

### 2️⃣ Install Dependencies
Make sure you have **Python 3.8+** installed, then run:
```bash
pip install -r requirements.txt
```
If `requirements.txt` is missing, install dependencies manually:
```bash
pip install streamlit google-generativeai sounddevice speechrecognition numpy pyttsx3 requests python-dotenv wave
```

### 3️⃣ Create a `.env` File  
Create a **`.env`** file in the project root and add:
```
GOOGLE_API_KEY=your_google_api_key
WEATHER_API_KEY=your_weatherstack_api_key
```
🔹 **Replace `your_google_api_key` and `your_weatherstack_api_key` with actual API keys.**  

---

## 🎤 How to Run the Assistant  
Run the following command:
```bash
streamlit run app.py
```
🔹 Replace `app.py` with your actual script name if different.

---

## 🗣️ Supported Voice Commands
| **Command** | **Functionality** |
|------------|------------------|
| `"Hey Victo, set an alarm for tomorrow at 7 AM."` | Sets an alarm for 7 AM. |
| `"Hey Victo, delete alarm 1."` | Deletes the first alarm. |
| `"Hey Victo, delete all alarms."` | Clears all alarms. |

---

## 🛠️ Troubleshooting
🔹 **If the assistant doesn’t recognize your voice:**  
- Ensure your **microphone is working** and properly configured.  
- Speak **clearly and loudly enough**.  
- Try restarting the script.  

🔹 **If the weather API is not working:**  
- Ensure the **WeatherStack API key** is correct in the `.env` file.  
- Run `print(os.getenv("WEATHER_API_KEY"))` to debug.  

🔹 **If Streamlit crashes:**  
- Restart the terminal and run `streamlit run app.py` again.  

## 👨‍💻 Credits & Contributors
- Maha Swetha - Developer  
- **Google Gemini AI, Streamlit, WeatherStack** - APIs used  

### 🔥 **Now your project is well-documented and ready to be shared!** 🚀🔥

