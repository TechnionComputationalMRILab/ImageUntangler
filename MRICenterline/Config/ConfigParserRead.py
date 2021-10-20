import configparser
import os
from pathlib import Path

import logging
logging.getLogger(__name__)


def initialize():
    config_file = configparser.ConfigParser()
    config_file_path = os.path.join(Path(__file__).resolve().parents[2], 'config.ini')

    try:
        config_file.read(config_file_path)
    except FileNotFoundError:
        raise FileNotFoundError
    else:
        return config_file, config_file_path


def get_config_data(section, key):
    config_file, _ = initialize()
    return config_file[section][key]


def set_config_data(section, key, value):
    config_file, config_file_path = initialize()
    config_file.set(section, key, str(value))

    with open(config_file_path, 'w') as f:
        config_file.write(f)


def set_color_data(section, value):
    config_file, config_file_path = initialize()
    if section == 'display':
        config_file.set('display', 'text-color', '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))
    else:
        config_file.set(section, 'color', '{r}, {g}, {b}'.format(r=int(value[0]), g=int(value[1]), b=int(value[2])))

    with open(config_file_path, 'w') as f:
        config_file.write(f)


def get_color(section):
    config_file, _ = initialize()
    if section == 'display':
        color_str = config_file['display']['text-color']
    elif 'color' not in config_file[section]:
        return 1, 1, 1
    else:
        color_str = config_file[section]['color']
    rgb_str = color_str.split(", ")
    as_list = [int(i) / 255 for i in rgb_str]
    return tuple(as_list)


def get_testing_status(testing):
    config_file, _ = initialize()
    if config_file['testing'][testing]:
        return config_file.getboolean('testing', testing)
    else:
        return False


def get_boolean(section, key):
    config_file, _ = initialize()
    return config_file.getboolean(section, key)
