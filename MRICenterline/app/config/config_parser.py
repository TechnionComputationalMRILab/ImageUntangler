import configparser
import os
from pathlib import Path

from MRICenterline.app.config.file_check import file_checks

import logging
logging.getLogger(__name__)


def singleton(cls):
    """ https://peps.python.org/pep-0318/ """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class ConfigParser:
    def __init__(self):
        file_checks()

        self._home_path = Path(__file__).resolve().parents[3]
        self.config_file = configparser.ConfigParser()
        self.config_file_path = os.path.join(self._home_path, 'config.ini')

        self.config_file.read(self.config_file_path)
        self.reset_script_folder()

    def reset_script_folder(self):
        if self.get_config_data('folders', 'script-folder') == "none":
            self.set_config_data('folders', 'script-folder', self._home_path)

    def get_config_data(self, section, key):
        return self.config_file[section][key]

    def set_config_data(self, section, key, value):
        self.config_file[section][key] = str(value)

        with open(self.config_file_path, 'w') as f:
            self.config_file.write(f)

    def set_color_data(self, section, value):
        if section == 'display':
            self.config_file.set('display',
                                 'text-color',
                                 '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))
        else:
            self.config_file.set(section,
                                 'color',
                                 '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))

        with open(self.config_file_path, 'w') as f:
            self.config_file.write(f)

    def get_color(self, section):
        if section == 'display':
            color_str = self.config_file['display']['text-color']
        elif 'color' not in self.config_file[section]:
            return 1, 1, 1
        else:
            color_str = self.config_file[section]['color']
        rgb_str = color_str.split(", ")
        as_list = [int(i) / 255 for i in rgb_str]
        return tuple(as_list)

    def get_testing_status(self, testing):
        if self.config_file['testing'][testing]:
            return self.config_file.getboolean('testing', testing)
        else:
            return False

    def get_boolean(self, section, key):
        return self.config_file.getboolean(section, key)

    def get_folder(self, folder_key, *append):
        folders = {
            'raw_data': self.get_config_data("folders", "data-folder"),
            'raw': self.get_config_data("folders", "data-folder"),
            'script': self.get_config_data('folders', 'script-folder'),
            'log': os.path.join(self.get_config_data('folders', 'script-folder'), 'logs'),
        }

        if folder_key in list(folders.keys()):
            if append:
                return os.path.join(folders[folder_key], *append)
            else:
                return folders[folder_key]
        else:
            raise KeyError(f"{folder_key} does not exist in the get_folder list")

    def get_db(self):
        return self.get_folder("script", "metadata.db")
