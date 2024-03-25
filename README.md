# WeatherApp

WeatherApp is a simple weather application developed in Python using the Tkinter library for the graphical user interface and OpenWeatherMap API for fetching weather data. It allows users to retrieve current weather information, forecasts, and air pollution details for a specified city or geographical coordinates.

## Features

1. Access real-time weather details, encompassing temperature, description, wind speed, humidity, and comprehensive data at your fingertips.
2. Effortlessly explore weather forecasts for multiple upcoming days by seamlessly navigating through the forecast section via intuitive buttons.
3. Stay informed about air quality with in-depth pollution information, featuring the Air Quality Index (AQI) and concentrations of various pollutants.
4. Experience a user-friendly Graphical User Interface (GUI) designed for ease of use, offering smooth navigation through a searchable history log. Input the name of a city or precise coordinates (longitude and latitude) to retrieve accurate and up-to-date weather information.

## Application Structure

- **main.py**: Main entry point of the application.
- **weather_app.py**: Contains the WeatherApp class with the Tkinter GUI and weather-related functions.
- **config_reader.py**: Reads and validates configuration parameters from the `config.ini` file.
- **config.ini**: Contains a parameter editable from the application.
- **.env**: Reserved for storing your private API key.
- **.gitignore**: Specifies files and directories that should be ignored by Git, such as sensitive or generated files, notably the .env file.

## Requirements

- Python 3.6 or higher
- Required Python packages can be installed using `pip install -r requirements.txt`

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Eclipse91/WeatherApp.git
   ```

2. Navigate to the project directory:

   ```bash
   cd WeatherApp
   ```

3. It might be necessary to install Tkinter separately on Linux and macOS systems:

   - **Linux Debian Distribution:**
   
     ```bash
     sudo apt-get install python3-tk 
     ```

   - **Linux Fedora Distribution:**
   
     ```bash
     sudo dnf install python3-tkinter
     ```

   - **MacOS:**
   
     ```bash
     brew install python-tk
     ```

4. Install the required dependencies (creating a virtual environment is strongly recommended before this step):

   ```bash
   pip install -r requirements.txt
   ```

5. Add the API key to the .env file under the API_KEY section, follow the steps outlined in the [Configuration](#configuration) section to obtain a valid API key
   
6. Run the application:

   ```bash
   python3 main.py
   ```

## Configuration

Ensure to set up your OpenWeatherMap API key in the `.env` file:
- **Sign In or Sign Up**: Start by signing in or creating a new account at OpenWeatherMap (https://home.openweathermap.org/users/sign_up).
- **Obtain Your API Key**: Once logged in, navigate to API Keys to find your unique API key (https://home.openweathermap.org/api_keys).
- **Configure API Key in .env**: Open the .env file and set API_KEY = your_API_Key without using quotation marks.
- **Activation Time**: Please note that the API key activation process may take a couple of hours, as indicated by OpenWeatherMap.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

## Notes

Feel free to contribute or report issues!
This README provides a clearer structure, concise information, and instructions for setting up and running the WeatherApp. Adjust the content as needed for your project.

## Acknowledgements

- [OpenWeatherMap API](https://openweathermap.org/api)
