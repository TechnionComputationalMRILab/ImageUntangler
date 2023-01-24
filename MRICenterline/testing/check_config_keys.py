from pathlib import Path
import configparser

print(Path(__file__).parents[2])

cfg = configparser.ConfigParser()
# cfg.read()