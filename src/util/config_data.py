import os, json


def get_icon_file_path() -> str:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file_path = script_dir + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'config/icon.jpeg'
    return os.path.abspath(config_file_path)


def get_config_file_path() -> str:
    # return absolute path of config file
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file_path = script_dir + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'config/config.json'
    return os.path.abspath(config_file_path)


def get_config_data() -> dict:
    # return JSON data for read-only operations
    config_file = open(get_config_file_path(), 'r')
    json_data = json.load(config_file)
    config_file.close()
    return json_data


def write_config_file(json_data: dict):
    config_file = open(get_config_file_path(), 'w')
    json.dump(json_data, config_file)
    config_file.close()


def update_config_value(value_name: str, value: str):
    # updates value_name if legitimate
    json_data = get_config_data()
    try:
        json_data[value_name] = value
    except KeyError:
        return -1
    write_config_file(json_data)


def get_config_value(value_name: str) -> str:
    # returns config value for value name
    json_data = get_config_data()
    try:
        return json_data[value_name]
    except KeyError:
        return -1
