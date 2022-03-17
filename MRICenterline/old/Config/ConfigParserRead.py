import sqlite3
import configparser
import os
from pathlib import Path

from MRICenterline.Config.MetadataDatabaseSetup import sql_strings

import logging
logging.getLogger(__name__)


class ConfigParser:
    def __init__(self):
        self.config_file = configparser.ConfigParser()
        self.config_file_path = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')

        try:
            self.config_file.read(self.config_file_path)
        except FileNotFoundError:
            raise FileNotFoundError

    def get_config_data(self, section, key):
        return self.config_file[section][key]

    def set_config_data(self, section, key, value):
        try:
            self.config_file.set(section, key, str(value))
        except Exception as e:
            print(e)

        with open(self.config_file_path, 'w') as f:
            self.config_file.write(f)

    def set_color_data(self, section, value):
        if section == 'display':
            self.config_file.set('display', 'text-color', '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))
        else:
            self.config_file.set(section, 'color', '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))

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
            'raw_data': self.get_config_data("folders", "default-folder"),
            'raw': self.get_config_data("folders", "default-folder"),
            'script': self.get_config_data('folders', 'image-untangler-folder'),
            'log': os.path.join(self.get_config_data('folders', 'image-untangler-folder'), 'logs'),
        }

        if folder_key in list(folders.keys()):
            if append:
                return os.path.join(folders[folder_key], *append)
            else:
                return folders[folder_key]
        else:
            raise KeyError(f"{folder_key} does not exist in the get_folder list")

    def get_db(self):
        metadata_db = self.get_folder("script", "metadata.db")
        if Path(metadata_db).is_file():
            return metadata_db
        else:
            # initialize the metadata db if it does not exist
            con = sqlite3.connect(metadata_db)

            with con:
                for table_name, query in sql_strings.items():
                    logging.debug(f"Create table {table_name}")
                    con.execute(query)

            con.close()
            return metadata_db


if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.get_db()
