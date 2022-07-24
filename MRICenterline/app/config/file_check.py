import shutil
import os
import logging.config
from pathlib import Path

from MRICenterline.app.config.log import LOGGING_CONFIG
from MRICenterline.app.database.setup import db_init


def file_checks() -> None:
    """
    - creates the log folder if not found and sets up the logging config dict
    - sets up the database if it doesn't exist
    """
    home_path = Path(__file__).resolve().parents[3]
    # logging
    Path("./logs").mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)

    # config
    config_file_path = os.path.join(Path(__file__).resolve().parents[3], 'config.ini')

    if Path(config_file_path).is_file():
        logging.info(f"Using configuration file: {config_file_path}")
    else:
        logging.info("Config file not found, creating from default...")

        shutil.copy(os.path.join(home_path, "default_config.ini"), config_file_path)

    # set up database
    db_file_path = os.path.join(home_path, 'metadata.db')
    if Path(db_file_path).is_file():
        logging.info(f"Using database file: {db_file_path}")
    else:
        logging.info("Database not found, initializing...")
        db_init(db_file_path)


def delete_config_file() -> None:
    """
    for use with the initial config box if the user X'ed out of the config box
    """
    os.remove(os.path.join(Path(__file__).resolve().parents[3], 'config.ini'))


def reset_config_to_defaults() -> None:
    home_path = Path(__file__).resolve().parents[3]

    # delete existing config file
    delete_config_file()

    # copy the default config file to the directory
    config_file_path = os.path.join(home_path, 'config.ini')
    shutil.copy(os.path.join(home_path, 'default_config.ini'), config_file_path)
