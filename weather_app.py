import requests
import json
import tkinter as tk
from tkinter import Frame, scrolledtext, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from datetime import datetime

class WeatherApp:
    '''
        A weather application using Tkinter for GUI and OpenWeatherMap API for weather data.
    '''
    def __init__(self, root, parameaters):
        self.api_key = parameaters.parameters['api_key']
        self.auto_open_var = tk.BooleanVar(value=parameaters.parameters['reopen_last_session'])
        self.root = root
        root.title("Tkinter App")
        root.geometry("1750x585")
        root.maxsize("1920","1080")
        root.config(bg="#0077cc")

        # Create top frame
        self.top_frame = Frame(self.root, bg='#66aacc', height=50)
        self.top_frame.grid(row=0, column=0, columnspan=10, sticky='ew', padx=10, pady=10)
        # Entry 
        self.call = tk.Button(self.top_frame, text="Get Weather", command=self.call_functions, height=3, width=10)
        self.clear = tk.Button(self.top_frame, text="Clear All", command=self.clear_all, height=3, width=10)
        self.back = tk.Button(self.top_frame, text="Go Back", command=self.go_back, height=3, width=10)        
        self.forward = tk.Button(self.top_frame, text="Go Forward", command=self.go_forward, height=3, width=10)
        self.city = tk.Label(self.top_frame, text="Enter a city", font=('TkDefaultFont', 18))
        self.location_entry = tk.Entry(self.top_frame, font=('TkDefaultFont', 14), width = 10)        
        self.label_long = tk.Label(self.top_frame, text="Enter a longitude", font=('TkDefaultFont', 18))
        self.longitude = tk.Entry(self.top_frame, font=('TkDefaultFont', 14), width = 10)        
        self.label_lati = tk.Label(self.top_frame, text="Enter a latitude", font=('TkDefaultFont', 18))
        self.latitude = tk.Entry(self.top_frame, font=('TkDefaultFont', 14), width = 10)        
        self.cities = tk.Label(self.top_frame, text="Cities: ", font=('TkDefaultFont', 18))
     

        # Use the grid manager to arrange buttons
        self.call.grid(row=0, column=0, padx=10, pady=10)
        self.clear.grid(row=0, column=1, padx=10, pady=10)
        self.back.grid(row=0, column=2, padx=10, pady=10)
        self.forward.grid(row=0, column=3, padx=10, pady=10)
        self.city.grid(row=0, column=4, padx=10, pady=10)
        self.location_entry.grid(row=0, column=5, padx=10, pady=10)
        self.label_long.grid(row=0, column=6, padx=10, pady=10)
        self.longitude.grid(row=0, column=7, padx=10, pady=10)
        self.label_lati.grid(row=0, column=8, padx=10, pady=10)
        self.latitude.grid(row=0, column=9, padx=10, pady=10)
        self.cities.grid(row=0, column=10, padx=10, pady=10)

        self.history = {}
        if self.auto_open_var.get():
            self.read_last_session()

        self.current_dict = len(self.history) if self.history else 0
        self.update_button_state()

        # Create a menu bar
        self.menu_bar = tk.Menu(root)

        # Create a "File" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_to_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Create a "Settings" menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Open Settings", command=self.open_settings)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        # Configure the root window to use the menu bar
        root.config(menu=self.menu_bar)

# Files Manager
    def open_file(self):
        # Ask user for a file name to open
        file_name = filedialog.askopenfilename(defaultextension=".json", 
                                                  filetypes=[("JSON Files", "*.json")])
        self.open_file_name(file_name)
    
    def open_file_name(self, file_name):
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    loaded_dict = json.load(file)
                    self.history = loaded_dict

                self.current_dict = len(self.history)
                self.cities.config(text="Cities: " + str(self.current_dict))
                self.update_button_state()
                # If contains something load the last visited
                if self.history:
                    self.location_entry.insert(0, list(self.history.values())[-1]['City'])
                    self.longitude.insert(0, list(self.history.values())[-1]['Lon'])
                    self.latitude.insert(0, list(self.history.values())[-1]['Lat'])
                    self.run_functions(0)

                self.save_to_file_name('last_session.json')
            except:
                messagebox.showinfo("Error", 'File last_session.json missing')

    def save_to_file(self):
        # Ask user for a file name to save the dictionary
        file_name = filedialog.asksaveasfilename(defaultextension=".json", 
                                                    filetypes=[("JSON Files", "*.json")])

        if file_name:
            # Write the dictionary to the file in JSON format
            self.save_to_file_name(file_name)

    def save_to_file_name(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.history, file)
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        # Checkbox for automatically reopening the last session
        auto_open_checkbox = tk.Checkbutton(settings_window, 
                                            text="Automatically reopen last session", 
                                            variable=self.auto_open_var,
                                            command=self.save_changes)
        auto_open_checkbox.grid(row=0, column=0, padx=20, pady=20)

    def save_changes(self):
        # Access the value of the checkbox variable
        auto_open_value = self.auto_open_var.get()

        # Read the existing configuration from the file
        with open("config.ini", 'r') as config_file:
            lines = config_file.readlines()

        # Update the 'reopen_last_session' parameter
        for i, line in enumerate(lines):
            if line.startswith("reopen_last_session"):
                lines[i] = f"reopen_last_session = {auto_open_value}\n"

        # Save the changes back to the file
        with open("config.ini", 'w') as config_file:
            config_file.writelines(lines)

    def read_last_session(self):
        file_name = 'last_session.json'        
        self.open_file_name(file_name)
            
# Util
    def empty_frame(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

    def clear_all(self):
        self.location_entry.delete(0, tk.END)
        self.longitude.delete(0, tk.END)
        self.latitude.delete(0, tk.END)

    def error_message(self):
        message = (
            f"Error fetching data. The issue is likely related to one of the following reasons:\n"
            f"1. Incorrect API Key: {self.api_key}\n"
            f"2. Incorrect City Name"
        )

        messagebox.showinfo("Error", message)

    def add_history(self):
        if self.history:
            if list(self.history.values())[-1]['City'] != self.location_entry.get() or list(self.history.values())[-1]['Lon'] != self.longitude.get() or list(self.history.values())[-1]['Lat'] != self.latitude.get():
                self.add_voice_to_history()
        else:
            self.add_voice_to_history()
            
    def add_voice_to_history(self):
        self.history[str(len(self.history) + 1)] = {'City': self.location_entry.get(), 
                                                'Lon': float(self.longitude.get()) if self.longitude.get() else '',
                                                'Lat': float(self.latitude.get()) if self.latitude.get() else ''
                                                }
        self.current_dict = len(self.history)
        self.cities.config(text="Cities: " + str(self.current_dict))
        self.update_button_state()
        self.save_to_file_name('last_session.json')


    def go_back(self):
        self.clear_all()

        self.location_entry.insert(0, self.history[str(self.current_dict - 1)]['City'])
        self.longitude.insert(0, self.history[str(self.current_dict - 1)]['Lon'])
        self.latitude.insert(0, self.history[str(self.current_dict - 1)]['Lat'])
        self.current_dict -= 1
        self.cities.config(text="Cities: " + str(self.current_dict))

        self.update_button_state()
        self.run_functions(0)

    def go_forward(self):
        self.clear_all()

        self.location_entry.insert(0, self.history[str(self.current_dict + 1)]['City'])
        self.longitude.insert(0, self.history[str(self.current_dict + 1)]['Lon'])
        self.latitude.insert(0, self.history[str(self.current_dict + 1)]['Lat'])
        self.current_dict += 1
        self.cities.config(text="Cities: " + str(self.current_dict))

        self.update_button_state()
        self.run_functions(0)

    def update_button_state(self):
        # Check the value of your parameter
        if self.current_dict <= 1:
            # Disable the button if the parameter is 0
            self.back.config(state=tk.DISABLED)
        else:
            self.back.config(state=tk.NORMAL)

        if self.current_dict == len(self.history):
            # Disable the button if the parameter is 0
            self.forward.config(state=tk.DISABLED)
        else:
            # Enable the button if the parameter is not 0
            self.forward.config(state=tk.NORMAL)

# Weather Functions        
    def call_functions(self):
        if self.location_entry.get():
            self.run_functions(1)
        elif self.latitude.get() and self.longitude.get():
            if -90 <= float(self.latitude.get()) <= 90 and -180 <= float(self.longitude.get()) <= 180:
                self.run_functions(1)
            else:
                messagebox.showinfo("Popup", "Insert a name of a city or a latitude between -90 and 90 and a longitude between -180 and 180")
        else:
            messagebox.showinfo("Popup", "Insert a name of a city or a latitude between -90 and 90 and a longitude between -180 and 180")

    def run_functions(self, historicize):
        self.create_frames()
        self.empty_frame()
        
        if self.get_weather():
            self.get_weather_forecast()
            self.get_air_pollution()
            if historicize:
                self.add_history()
            self.clear_all()
        else:
            self.left_frame.destroy()
            self.right_frame.destroy()
            self.error_message()

    def create_frames(self):
        try:
            self.left_frame.destroy()
            self.right_frame.destroy()
        except:
            pass            
        # Create left frame
        self.left_frame = Frame(self.root, bg='#99ccdd')
        self.left_frame.grid(row=1, column=0, columnspan=1, rowspan=3, sticky='ew', padx=10, pady=10)
        # Create right frame
        self.right_frame = Frame(self.root, bg='#cceeff')
        self.right_frame.grid(row=1, column=1, columnspan=1, rowspan=3, sticky='ew', padx=8, pady=10)

        # Labels
        self.forecast = tk.Label(self.left_frame, text="Forecast", height=5, width=10,)#, command=self.get_weather_forecast, height=3, width=10)
        self.weather = tk.Label(self.left_frame, text="Weather", height=7, width=10)#, command=self.get_weather, height=6, width=10)
        self.air = tk.Label(self.left_frame, text="Air", height=8, width=10)#, command=self.get_air_pollution, height=8, width=10)
        self.forecast.grid(row=1, column=0, padx=10, pady=10)
        self.weather.grid(row=2, column=0, padx=10, pady=10)
        self.air.grid(row=3, column=0, padx=10, pady=10)

# Weather
    def get_weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        if self.location_entry.get():
            # https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
            params = {
                "q": self.location_entry.get(),
                "appid": self.api_key,
                "units": "metric"  # You can change this to "imperial" for Fahrenheit
            }
        else:
            # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
            params = {
                "lon": self.longitude.get(),
                "lat": self.latitude.get(),
                "appid": self.api_key,
                "units": "metric"
            }
        
        if self.weather_request(base_url, params):
            return True
        else:
            return False


    def weather_request(self, base_url, params):
        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            # Assign entry fields and update history
            self.clear_all()
            self.location_entry.insert(0, data['name'])
            self.longitude.insert(0, data['coord']['lon'])
            self.latitude.insert(0, data['coord']['lat'])

            # Assign weather values
            name = data['name']
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            dt = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
            country = "" if name == "" or name == "Globe" else data['sys']['country']
            feels_like = data['main']['feels_like']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            deg = data['wind']['deg']
            deg = self.degrees_to_direction(data['wind']['deg'])
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
            icon_code = data['weather'][0]['icon']
            name = name if len(name) < 19 else f'\n{name}'
            # Manage position
            state_label = tk.Label(self.right_frame, text=f"City: {name}\nCountry: {country}\n Longitude: {data['coord']['lon']}\n Latitude: {data['coord']['lat']}\nDate: {dt.strftime('%d-%m-%Y')}\nTime: {dt.strftime('%H:%M:%S')}" if name else f"Ocean or Sea\nLongitude: {data['coord']['lon']}\nLatitude: {data['coord']['lat']}\nDate: {dt.strftime('%Y-%m-%d')}\nTime: {dt.strftime('%H:%M:%S')}", font=('Courier', 12))
            state_label.grid(row=2, column=3, sticky='nsew', padx=10, pady=10)

            weather_label = tk.Label(self.right_frame, text=f"Weather:\n{weather_description}", font=('Courier', 14))
            weather_label.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

            temperature_label = tk.Label(self.right_frame, text=f"Temperature: {temperature}°C\nFeels like: {feels_like}°C\nMax: {temp_max}°C\nMin: {temp_min}°C\nPressure: {pressure} mbar\nHumidity: {humidity}%", font=('Courier', 12))
            temperature_label.grid(row=2, column=4, sticky='nsew', padx=10, pady=10)

            wind_label = tk.Label(self.right_frame, text=f"Wind: {wind} m/s\nDirection: {deg}", font=('Courier', 12))
            wind_label.grid(row=2, column=5, sticky='nsew', padx=10, pady=10)

            sun_label = tk.Label(self.right_frame, text=f"Sunrise: {sunrise}\nSunset: {sunset}", font=('Courier', 12))
            sun_label.grid(row=2, column=6, sticky='nsew', padx=10, pady=10)

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
            icon_image = Image.open(requests.get(icon_url, stream=True).raw)
            icon_image = icon_image.resize((130, 130), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)

            icon_label = tk.Label(self.right_frame, image=icon_photo)
            icon_label.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')
            icon_label.image = icon_photo

            return True

        except:
            return False

    def degrees_to_direction(self, degrees):
        if 0 <= degrees < 22.5 or degrees >= 337.5:
            return "North"
        elif 22.5 <= degrees < 67.5:
            return "Northeast"
        elif 67.5 <= degrees < 112.5:
            return "East"
        elif 112.5 <= degrees < 157.5:
            return "Southeast"
        elif 157.5 <= degrees < 202.5:
            return "South"
        elif 202.5 <= degrees < 247.5:
            return "Southwest"
        elif 247.5 <= degrees < 292.5:
            return "West"
        elif 292.5 <= degrees < 337.5:
            return "Northwest"
        else:
            return "Invalid degrees"
        
# Air
    def get_air_pollution(self):
        # http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={API key}
        base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            "lon": self.longitude.get(),
            "lat": self.latitude.get(),
            "appid": self.api_key,
            "units": "metric"  # You can change this to "imperial" for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            # Air
            aqi = tk.Label(self.right_frame, text="", font=('Courier', 14))
            aqi.grid(row=3, column=1, pady=10, padx=10, sticky='nsew')
            
            molecule = tk.Label(self.right_frame, text="", font=('Courier', 12))
            molecule.grid(row=3, column=2, pady=10, padx=10, sticky='nsew')

            quality = tk.Label(self.right_frame, text="", font=('Courier', 12))
            quality.grid(row=3, column=3, pady=10, padx=10, sticky='nsew')        

            aqi_data = data['list'][0]['main']['aqi']
            co_data = data['list'][0]['components']['co']
            no_data = data['list'][0]['components']['no']
            no2_data = data['list'][0]['components']['no2']
            so2_data = data['list'][0]['components']['so2']
            pm25_data = data['list'][0]['components']['pm2_5']
            pm10_data = data['list'][0]['components']['pm10']
            nh3_data = data['list'][0]['components']['nh3']

            quality_dict = {1: 'Good', 2: 'Fair', 3: 'Moderate', 4: 'Poor', 5: 'Very Poor'}

            aqi.config(text=f"Air Quality:\n{quality_dict[aqi_data]}")
            molecule.config(text=f"Molecule\nCO: {co_data} μg/m3\nNO2: {no2_data} μg/m3\nSO2: {so2_data} μg/m3\nPM2_5: {pm25_data} μg/m3\nPM10: {pm10_data} μg/m3\nNO: {no_data} μg/m3\nNH3: {nh3_data} μg/m3")
            quality.config(text=f"Quality\n{quality_dict[self.get_category_range('CO', co_data)]}\n{quality_dict[self.get_category_range('NO2', no2_data)]}\n{quality_dict[self.get_category_range('SO2', so2_data)]}\n{quality_dict[self.get_category_range('PM25', pm25_data)]}\n{quality_dict[self.get_category_range('PM10', pm10_data)]}\nmin 0.1 - max 200\nmin 0.1 - max 100")
        except:
            messagebox.showinfo("Error", f"Error fetching data. The issue is likely due to an incorrect API Key: {self.api_key}")

    def get_category_range(self, molecule, value):
        """Helper function to get the AQI category range for a specific molecule."""
        if molecule == 'SO2':
            ranges = [(0, 20), (20, 80), (80, 250), (250, 350), (350, float('inf'))]
        elif molecule == 'NO2':
            ranges = [(0, 20), (20, 80), (80, 250), (250, 350), (350, float('inf'))]
        elif molecule == 'PM10':
            ranges = [(0, 40), (40, 70), (70, 150), (150, 200), (200, float('inf'))]
        elif molecule == 'PM25':
            ranges = [(0, 20), (20, 50), (50, 100), (100, 200), (200, float('inf'))]
        elif molecule == 'O3':
            ranges = [(0, 10), (10, 25), (25, 50), (50, 75), (75, float('inf'))]
        elif molecule == 'CO':
            ranges = [(0, 60), (60, 100), (100, 140), (140, 180), (180, float('inf'))]
        else:
            # if molecule == 'NH3':
            #     ranges = [(0.1, 200)]
            # elif molecule == 'NO':
            #     ranges = [(0.1, 100)]
            return None
        
        for i, (low, high) in enumerate(ranges, start=1):
            if low <= value < high:
                return i

        return len(ranges) + 1


# Forecast
    def get_weather_forecast(self):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"

        if self.location_entry.get():
            #api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}
            params = {
                "q": self.location_entry.get(),
                "appid": self.api_key,
                "units": "metric"
            }
        elif self.latitude.get() and self.longitude.get():    
            # api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
            params = {
                "lon": self.longitude.get(),
                "lat": self.latitude.get(),
                "appid": self.api_key,
                "units": "metric"
            }

        self.forecast_request(base_url, params)

    def forecast_request(self, base_url, params):
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            timezone = data['city']['timezone']
            grouped_data = self.group_data_by_day(data['list'], timezone)
            self.create_buttons(grouped_data, timezone)

        except:
            self.error_message()

    def create_buttons(self, grouped_data, timezone):
        buttons_per_line = 8
        for index, (day, day_data) in enumerate(grouped_data.items()):
            row, col = divmod(index, buttons_per_line)
            button_text = f"          {day} ({len(day_data['entries'])} forecasts)          " if len(day_data['entries']) > 1 else f"          {day} ({len(day_data['entries'])} forecast)          "
            button = tk.Button(self.right_frame, text=button_text, pady=10, command=lambda day=day: self.display_day_data(day, grouped_data, timezone))

            # Add an image to each button
            image_url = f"http://openweathermap.org/img/w/{day_data['icon_url']}.png"
            image = Image.open(requests.get(image_url, stream=True).raw)
            image = image.resize((50, 50), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            button.config(image=photo, compound=tk.TOP)
            button.image = photo

            button.grid(row=row+1, column=col+1)

    def display_day_data(self, day, grouped_data, timezone):
        day_entries = grouped_data[day]['entries']

        entry_window = tk.Toplevel(self.right_frame)
        entry_window.title(f"Weather Entries for {day}")

        text_area = scrolledtext.ScrolledText(entry_window, wrap=tk.WORD, width=60, height=20)
        for entry in day_entries:
            text_area.insert(tk.END, self.format_entry_data(entry, timezone))
        text_area.pack(expand=True, fill='both')

    def format_entry_data(self, entry, timezone):
        formatted_data = f"Date/Time: {datetime.utcfromtimestamp(entry['dt'] + timezone).strftime('%d-%m-%Y %H:%M:%S')}\n"
        formatted_data += f"Temperature: {entry['main']['temp']}°C\n"
        formatted_data += f"Description: {entry['weather'][0]['description']}\n"
        formatted_data += f"Wind Speed: {entry['wind']['speed']} m/s\n"
        formatted_data += f"Humidity: {entry['main']['humidity']}%\n"
        formatted_data += f"-------------------------\n"

        return formatted_data

    def group_data_by_day(self, data, timezone):
        grouped_data = {}
        for entry in data:
            dt = datetime.utcfromtimestamp(entry['dt'] + timezone).strftime('%d-%m-%Y')
            if dt not in grouped_data:
                grouped_data[dt] = {'entries': [], 'icon_url': entry['weather'][0]['icon']}
            grouped_data[dt]['entries'].append(entry)
        return grouped_data
