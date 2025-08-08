import os
import json

CONFIG_PATH = os.path.expanduser("~/.config/osu-cli/config.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
