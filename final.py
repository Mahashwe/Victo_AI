import streamlit as st
import google.generativeai as genai
import sounddevice as sd
import wave
import tempfile
import speech_recognition as sr
import re
import json  
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import numpy as np
import pyttsx3
import requests

# Load API Key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Missing API_KEY")

# Configure Gemini API here i will have the model configured 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Persistent Storage File a json storage
ALARM_FILE = "alarms.json"

# Load Alarms from JSON - by json loads
def load_alarms():
    if os.path.exists(ALARM_FILE):
        try:
            with open(ALARM_FILE, "r") as f:
                return json.load(f) or []  
        except json.JSONDecodeError:
            return []  
    return []

# Save Alarms to JSON
def save_alarms(alarms):
    with open(ALARM_FILE, "w") as f:
        json.dump(alarms, f)

# Initialize Alarms
if "alarms" not in st.session_state:
    st.session_state.alarms = load_alarms()

# Record Audio
def record_audio(filename="input.wav", duration=5, samplerate=16000):
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())
    return filename

# Convert Speech to Text
def convert_wav_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except (sr.UnknownValueError, sr.RequestError):
        return "Could not understand the audio"

# Extract Alarm Time
def extract_alarm_time(user_text):
    match = re.search(r"(\d{1,2}[:.]?\d{0,2})\s?(AM|PM|am|pm)?", user_text)
    if match:
        time_part, am_pm_part = match.groups()
        user_text = user_text.lower()
        if "morning" in user_text:
            am_pm_part = "AM"
        elif "night" in user_text or "evening" or "afternoon" in user_text:
            am_pm_part = "PM"
        elif not am_pm_part:
            am_pm_part = "AM" if datetime.now().hour < 12 else "PM"
        return f"{time_part} {am_pm_part}"
    return None  

# Extract Alarm Number (Supports "Delete All")
def extract_alarm_number(user_text):
    """Extracts alarm number or detects 'delete all' command."""
    if re.search(r"\bdelete all\b", user_text, re.IGNORECASE):
        return "all"
    match = re.search(r"alarm (\d+)", user_text, re.IGNORECASE)
    return int(match.group(1)) if match else None

#getting the weather using api key
def get_weather(location="Chennai"):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}"
    response = requests.get(url).json()
    
    if "current" in response:
        temp = response["current"]["temperature"]
        condition = response["current"]["weather_descriptions"][0]
        feels_like = response["current"]["feelslike"]
        humidity = response["current"]["humidity"]
        
        return f"Temperature: {temp}°C\n Condition: {condition}\n Feels Like: {feels_like}°C\n Humidity: {humidity}%"
    else:
        return f"Error: {response.get('error', {}).get('info', 'Could not fetch weather data.')}"

# Text-to-Speech the extracted text given to respond as speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# LLM Bedtime & Weather Advice
def llm_advice(alarm_time,weather): #uses gemini ai to give a personalized message
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.today().strftime("%d-%m-%Y")
    weather_now = weather
    #to predict what will be the best bedtime 
    try:
        alarm_dt = datetime.strptime(alarm_time, "%I:%M %p")
        bedtime_dt = alarm_dt - timedelta(hours=8)
        bedtime = bedtime_dt.strftime("%I:%M %p")
    except ValueError:
        return "I can help with scheduling! Let me know your alarm time."

    prompt = f"""
    weather: {weather_now}
    Today's Date: {current_date}
    Current Time: {current_time}
    Alarm Set For: {alarm_time}
    - Recommend a bedtime: **{bedtime}** for 8-hour sleep.
    - Give small tip on their sleep like small sentances and make them feel good like an AI sleep advice
    - no points just use small sentances
    - also analse the weather from {weather} and give short comments to the user
    - just provide advice if needed some scheduling advice like an AI productivity guru
    -But make sure you reply only in small to medium sentances with a polite tone 
    """

    response = model.generate_content(prompt)
    return response.text if response else f"Model is not able to respond right now- LLM error"

# Main Function
def main():
    st.set_page_config(page_title="Victo AI - Smart Assistant", page_icon="⏰")
    st.markdown(
    "<h1 style='text-align: center; background-color: #007BFF; color: white; padding: 10px; border-radius: 10px;'>🕰️ Victo AI - Smart Assistant</h1>", 
    unsafe_allow_html=True #box
)
    st.markdown("<br><br>", unsafe_allow_html=True)  # Adds two empty lines

    st.write("📅 Say your wake time and whether it's morning or night to set an alarm.")
    st.write("Say : 'Hey Victo, Set an Alarm for tomorrow morning at 7' ")
    wake_words = ["hey victo", "hey victopia", "hey viccto", "hey vic"]  # List of wake words

    # Set Alarm Button
    if st.button("🎤 Set Alarm"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            user_text = convert_wav_to_text(record_audio(tmp_file.name)) #sending the audio file to convert it as a text

        user_text_lower = user_text.lower() #we change all to lower case
        detected_wake_word = next((word for word in wake_words if word in user_text_lower), None)

        if not detected_wake_word:
            st.write("⚠️ Wake word not detected. Please say 'Hey Victo' before your command.")
            text_to_speech("Wake word not detected. Please try again.")
            return  # Stop processing if wake word is missing

        user_text = user_text_lower.replace(detected_wake_word, "").strip()  # Remove wake word

        st.write(f"You said: **{user_text}**")
        alarm_time = extract_alarm_time(user_text)

        if alarm_time:
            alarm_name = f"Alarm {len(st.session_state.alarms) + 1}"
            st.session_state.alarms.append((alarm_name, alarm_time))
            save_alarms(st.session_state.alarms)

            st.write(f"✅ {alarm_name} set for: **{alarm_time}**")
            text_to_speech(f"Alarm set for {alarm_time}")

            weather = get_weather() #calling weather function to retrive current weather
            # call LLM
            bedtime_advice = llm_advice(alarm_time,weather)
            st.write("🤖 Victo AI Says:", bedtime_advice)
            text_to_speech(bedtime_advice)
        else:
            st.write("⚠️ No valid alarm time detected. Try again.")
            text_to_speech("Please try again.")

    # Delete Alarm Button
    if st.button("🗑️ Delete Alarm"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            user_text = convert_wav_to_text(record_audio(tmp_file.name))

        st.write(f"You said: **{user_text}**")
        alarm_number = extract_alarm_number(user_text)

        if alarm_number == "all":
            st.session_state.alarms.clear()
            save_alarms(st.session_state.alarms)
            st.write("🗑️ All alarms deleted.")
            text_to_speech("All alarms have been deleted.")
        elif isinstance(alarm_number, int) and 1 <= alarm_number <= len(st.session_state.alarms):
            deleted_alarm = st.session_state.alarms.pop(alarm_number - 1)
            save_alarms(st.session_state.alarms)
            st.write(f"🗑️ Deleted {deleted_alarm[0]}: {deleted_alarm[1]}")
            text_to_speech(f"{deleted_alarm[0]} deleted.")
        else:
            st.write("⚠️ No valid alarm number detected. Try again.")
            text_to_speech("Please try again.")

    # Display Scheduled Alarms
    st.sidebar.subheader("⏰ Scheduled Alarms:")
    if st.session_state.alarms:
        for alarm_name, alarm_time in st.session_state.alarms:
            st.sidebar.write(f"🕒 {alarm_name}: {alarm_time}")
    else:
        st.sidebar.write("No alarms set yet.")



# Run main function
if __name__ == "__main__":
    main()