import os
import sys
import configparser

CONFIG_FILE = "config.ini"

if not os.path.isfile(CONFIG_FILE):
    print("Please create the 'config.ini' first!")
    sys.exit(1)

class Config(object):
    def load(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config

