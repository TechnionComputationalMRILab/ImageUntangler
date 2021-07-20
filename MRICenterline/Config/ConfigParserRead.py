import configparser
import os
from pathlib import Path


def initialize():
    config_file = configparser.ConfigParser()
    config_file_path = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')

    try:
        config_file.read(config_file_path)
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found!")
    return config_file, config_file_path


def get_config_data(section, key):
    config_file, _ = initialize()
    return config_file[section][key]


def set_config_data(section, key, value):
    config_file, config_file_path = initialize()
    config_file[section][key] = value
    with open(config_file_path, 'w') as f:
        config_file.write(f)


def get_color(section):
    config_file, _ = initialize()
    if 'color' not in config_file[section]:
        return 1, 1, 1
    else:
        color_str = config_file[section]['color']
        rgb_str = color_str.split(", ")
        as_list = [int(i)/255 for i in rgb_str]
        return tuple(as_list)


def get_testing_status(testing):
    config_file, _ = initialize()
    if config_file['testing'][testing]:
        return config_file.getboolean('testing', testing)
    else:
        return False
