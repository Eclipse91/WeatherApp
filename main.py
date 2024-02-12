import logging
import tkinter as tk
from weather_app import WeatherApp
from config_reader import ConfigReader

def main():
    # Configure and initialize the logger
    logging.basicConfig(filename='weather_app_logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Program started')

    # Read configuration parameters from config.ini
    parameters = ConfigReader()
    parameters.read_config_file()

    if parameters.parameters:
        # Create the Tkinter root window and start the WeatherApp
        root = tk.Tk()
        app = WeatherApp(root, parameters)
        root.mainloop()
    else:
        # Display a message if there are configuration issues
        print('Configuration issues detected in config.ini. See weather_app_logger.log for details.')
    
    logging.info('Program Ended')

if __name__ == "__main__":
    main()
