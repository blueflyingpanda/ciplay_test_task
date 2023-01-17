from pathlib import Path
from configparser import ConfigParser


CONF_NAME = 'rest.ini'
conf = ConfigParser()
conf.read(Path() / CONF_NAME)
