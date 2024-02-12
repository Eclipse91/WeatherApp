# WeatherApp

## Overview

WeatherApp is a simple weather application developed in Python using the Tkinter library for the graphical user interface and OpenWeatherMap API for fetching weather data. It allows users to retrieve current weather information, forecasts, and air pollution details for a specified city or geographical coordinates.

## Features

- Current weather details including temperature, description, wind speed, humidity, and more.
- Weather forecasts for multiple days.
- Air pollution information, including Air Quality Index (AQI) and pollutant concentrations.
- User-friendly GUI with options to navigate through the search history.

## Requirements

- Python 3.6 or higher
- Required Python packages can be installed using `pip install -r requirements.txt`

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/WeatherApp.git
   ```

2. Navigate to the project directory:

   ```bash
   cd WeatherApp
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Explore Configuration Below Update the config.ini adding the api_key
   


6. Run the application:

   ```bash
   python main.py
   ```

## Configuration

Ensure to set up your OpenWeatherMap API key in the `config.ini` file:
- **Sign In or Sign Up**: Start by signing in or creating a new account at OpenWeatherMap (https://home.openweathermap.org/users/sign_up).
- **Obtain Your API Key**: Once logged in, navigate to API Keys to find your unique API key (https://home.openweathermap.org/api_keys).
- **Configure API Key in config.ini**: Open the config.ini file and set api_key = your_API_Key without using quotation marks.
- **Activation Time**: Please note that the API key activation process may take a couple of hours, as indicated by OpenWeatherMap.

## Application Structure

- **weather_app.py**: Contains the WeatherApp class with the Tkinter GUI and weather-related functions.
- **config_reader.py**: Reads and validates configuration parameters from the `config.ini` file.
- **main.py**: Main entry point of the application.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

## Acknowledgements

- [OpenWeatherMap API](https://openweathermap.org/api)

## Notes

Feel free to contribute or report issues!
This README provides a clearer structure, concise information, and instructions for setting up and running the WeatherApp. Adjust the content as needed for your project.
