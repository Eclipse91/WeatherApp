import os
import logging
import tkinter as tk
from weather_app import WeatherApp
from config_reader import ConfigReader
from dotenv import dotenv_values


def main():
    # Configure and initialize the logger
    logging.basicConfig(filename='weather_app_logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Program started')

    # Check the existence of the .env file
    if os.path.exists('.env'):
        # Get the api_key
        api_key = dotenv_values('.env')['API_KEY']

        # Read configuration parameters from config.ini
        parameters = ConfigReader()
        parameters.read_config_file()
    else:
        logging.error('.env file missing')
    
    # Launch the application if configuration parameters are valid
    if parameters.parameters:
        # Create the Tkinter root window and start the WeatherApp
        root = tk.Tk()
        app = WeatherApp(root, parameters, api_key)
        root.mainloop()
    else:
        # Display a message if there are configuration issues
        print('Configuration issues detected in config.ini or .env file. See weather_app_logger.log for details.')

    logging.info('Program Ended')

if __name__ == '__main__':
    main()
