import requests


def get_weather(location="Chennai"):
    api_key = "449a7c3b616bbac19889d1e7606b9df2"  # Replace with your actual API key
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={location}"

    response = requests.get(url).json()
    
    if "current" in response:
        temp = response["current"]["temperature"]
        condition = response["current"]["weather_descriptions"][0]
        feels_like = response["current"]["feelslike"]
        humidity = response["current"]["humidity"]
        
        return f"🌡️ Temperature: {temp}°C\n☁️ Condition: {condition}\n🥵 Feels Like: {feels_like}°C\n💧 Humidity: {humidity}%"
    else:
        return f"⚠️ Error: {response.get('error', {}).get('info', 'Could not fetch weather data.')}"

# Example Usage
print(get_weather("Chennai"))
