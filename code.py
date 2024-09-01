import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to get weather data
def get_weather(city):
    api_key = 'dfccd093412c857d9453edc1fb93a1fd'  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    
    if response.status_code == 200:
        main = data["main"]
        weather = data["weather"][0]
        return {
            "city": data["name"],
            "temperature": main["temp"],
            "humidity": main["humidity"],
            "description": weather["description"],
            "icon": weather["icon"]
        }
    else:
        return {"error": "City not found"}

# Function to display weather data in the GUI
def show_weather():
    city = city_entry.get()
    weather_data = get_weather(city)
    
    if "error" in weather_data:
        messagebox.showerror("Error", "City not found")
    else:
        result = f"City: {weather_data['city']}\n"
        result += f"Temperature: {weather_data['temperature']}°C\n"
        result += f"Humidity: {weather_data['humidity']}%\n"
        result += f"Description: {weather_data['description']}"
        
        weather_label.config(text=result)
        
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@4x.png"
        icon_response = requests.get(icon_url, stream=True)
        
        if icon_response.status_code == 200:
            icon_image = Image.open(icon_response.raw)
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
        else:
            icon_label.config(image='')  # Clear the label if image not found

# Set up the GUI
root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter city name (India):") 
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather)
get_weather_button.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

icon_label = tk.Label(root)
icon_label.pack()

root.mainloop()