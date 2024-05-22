from requests import get
from time import sleep
import tkinter as tk
import config


def get_weather(city):
    api_key = config.api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    for i in range(10):  # try 10 times
        response = get(base_url, params=params)
        data = response.json()

        if data.get('cod') == 429:  # 429 is the HTTP status code for Too Many Requests
            print("Rate limit exceeded. Waiting for 60 seconds before retrying...")
            sleep(60)  # wait for 60 seconds before retrying
        elif (data.get('cod') != 200):
            print(f"Error: {data['message']}")
            return None
        else:
            return data

def display_weather(data):
    main = data['main']
    weather = data['weather'][0]
    print(f"City: {data['name']}")
    print(f"Weather: {weather['description']}")
    print(f"Temperature: {main['temp']}°C")
    print(f"Humidity: {main['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")

def update_label():
    city = city_entry.get()
    weather_data = get_weather(city)
    if (weather_data != None):
        city_label.config(text=f"City: {weather_data['name']}")
        weather_label.config(text=f"Weather: {weather_data['weather'][0]['description']}")
        temp_label.config(text=f"Temperature: {weather_data['main']['temp']}°C")
        humidity_label.config(text=f"Humidity: {weather_data['main']['humidity']}%")
        wind_label.config(text=f"Wind Speed: {weather_data['wind']['speed']} m/s")

        icon = weather_data['weather'][0]['icon']
    else:
        city_label.config(text="City: N/A")
        weather_label.config(text="Weather: N/A")
        temp_label.config(text="Temperature: N/A")
        humidity_label.config(text="Humidity: N/A")
        wind_label.config(text="Wind Speed: N/A")
        
        icon = ""

    if (icon in icon_code):
        icon_path = f"icons/{icon_code[icon]}"
        icon_img = tk.PhotoImage(file=icon_path)
        weather_icon_label.config(image=icon_img)
        weather_icon_label.image = icon_img


if __name__ == "__main__":
    w, h = 480, 640
    buffer_size = 10
    input_box_height = 80
    text_height = 20
    box_height = h / 4

    icon_code = {
        "01d": "sun.png",
        "01n": "sun.png",
        "02d": "fewClouds.png",
        "02n": "fewClouds.png",
        "03d": "clouds.png",
        "03n": "clouds.png",
        "04d": "brokenClouds.png",
        "04n": "brokenClouds.png",
        "09d": "showerRain.png",
        "09n": "showerRain.png",
        "10d": "rain.png",
        "10n": "rain.png",
        "11d": "storm.png",
        "11n": "storm.png",
        "13d": "snowy.png",
        "13n": "snowy.png",
        "50d": "fog.png",
        "50n": "fog.png"
    }

    root = tk.Tk()
    root.geometry(f"{w}x{h}")  # Width x Height
    root.configure(bg="#202020")  # Background color

    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    city_entry = tk.Entry(canvas, width=30)

    submit_button = tk.Button(canvas, text="Submit", command=update_label)

    city_label = tk.Label(canvas, text="City: N/A", bg="#202020", fg="white")
    weather_label = tk.Label(canvas, text="Weather: N/A", bg="#202020", fg="white")
    temp_label = tk.Label(canvas, text="Temperature: N/A", bg="#202020", fg="white")
    humidity_label = tk.Label(canvas, text="Humidity: N/A", bg="#202020", fg="white")
    wind_label = tk.Label(canvas, text="Wind Speed: N/A", bg="#202020", fg="white")

    # Add widgets to canvas
    canvas.create_window(w / 2, 30, window=city_entry)
    canvas.create_window(w * 7 / 8, 30, window=submit_button)

    canvas.create_window(w / 4, input_box_height + box_height - buffer_size - text_height, window=weather_label)
    canvas.create_window(w * 3 / 4, input_box_height + box_height - buffer_size - text_height, window=temp_label)
    canvas.create_window(w / 4, input_box_height + (box_height * 2) - buffer_size - text_height, window=humidity_label)
    canvas.create_window(w * 3 / 4, input_box_height + (box_height * 2) - buffer_size - text_height, window=wind_label)
    canvas.create_window(w / 4, 540, window=city_label)

    # Add icons for weather
    bc_img = tk.PhotoImage(file="icons/brokenClouds.png")
    cl_img = tk.PhotoImage(file="icons/clouds.png")
    fc_img = tk.PhotoImage(file="icons/fewClouds.png")
    fo_img = tk.PhotoImage(file="icons/fog.png")
    ra_img = tk.PhotoImage(file="icons/rain.png")
    sr_img = tk.PhotoImage(file="icons/showerRain.png")
    sn_img = tk.PhotoImage(file="icons/snowy.png")
    st_img = tk.PhotoImage(file="icons/storm.png")
    su_img = tk.PhotoImage(file="icons/sun.png")

    # Add images for weather
    weather_icon_label = tk.Label(canvas, image="")
    canvas.create_window(buffer_size, input_box_height + buffer_size, window=weather_icon_label)

    # Add icon scale for temperature

    # Add icon scale for humidity

    # Add icon scale for wind speed

    # Add city town country logos based on city population? 

    # Create rectangles around each label
    canvas.create_rectangle(buffer_size, input_box_height + buffer_size, (w / 2) - buffer_size, input_box_height + box_height - buffer_size, outline="blue")
    canvas.create_rectangle((w / 2) + buffer_size, input_box_height + buffer_size, w - buffer_size, input_box_height + box_height - buffer_size, outline="blue")
    canvas.create_rectangle(buffer_size, input_box_height + box_height + buffer_size, (w / 2) - buffer_size, input_box_height + (box_height * 2) - buffer_size, outline="blue")
    canvas.create_rectangle((w / 2) + buffer_size, input_box_height + box_height + buffer_size, w - buffer_size, input_box_height + (box_height * 2) - buffer_size, outline="blue")


    root.mainloop()

    
