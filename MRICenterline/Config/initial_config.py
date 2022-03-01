import os
import shutil
import configparser
import logging.config
from pathlib import Path

from MRICenterline.utils.log import LOGGING_CONFIG


class Config:
    """
    creates the log folder if not found and sets up the logging config dict
    handles initial set-up of the configuration file, creates it if not found
    """
    def __init__(self):
        # logging
        Path("./logs").mkdir(parents=True, exist_ok=True)
        logging.config.dictConfig(LOGGING_CONFIG)

        # set up config
        config_file_path = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')
        config_file = configparser.ConfigParser()

        if Path(config_file_path).is_file():
            config_file.read(config_file_path)
            self.is_first_run = False
        else:
            logging.debug("Config file not found, creating from default...")
            shutil.copy(Path(str(Path(__file__).parent) + r'\default_config.ini'), config_file_path)
            self.is_first_run = True


def delete_config_file():
    """
    for use with the initial config box if the user X'ed out of the config box
    """
    config_file_path = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')
    os.remove(config_file_path)
