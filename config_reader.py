import logging
from datetime import datetime
import os


class ConfigReader:
    '''
    A class for reading and validating configuration parameters from a config.ini file.

    Attributes:
        parameters (dict): A dictionary to store the configuration parameters.
    '''

    def __init__(self):
        self.parameters = {}

    def read_config_file(self):
        '''
        Read the config.ini file and populate the parameters dictionary.
        '''
        try:
            with open('config.ini', 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = map(str.strip, line.split('='))
                        self.parameters[key] = value

        except FileNotFoundError:
            logging.error(f"Configuration file config.ini not found.")

        except Exception as e:
            logging.error(f"Error reading configuration file: {str(e)}.")

        else:
            if self.check_parameters():
                logging.info('Parameters config.ini are correct')
            else:
                logging.error("Configuration issue detected in config.ini.")
                
    def check_parameters(self):
        '''
        Check the validity of parameters.
        '''
        # Check the presence of at least one client email
        if not self.parameters.get('api_key'):
            self.parameters.clear()
            logging.error("API_Key missing")
            return False
        
        if self.parameters['reopen_last_session'] not in ('True', 'False'):
            self.parameters.clear()
            logging.error("Reopen last session must be a boolean")
            return False
        
        return True

            
