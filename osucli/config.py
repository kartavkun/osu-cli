import os
import json

CONFIG_PATH = os.path.expanduser("~/.config/osu-cli/config.json")

def first_run_setup():
    print("Welcome to osufetch first run setup!")
    print("To get your OAuth tokens, please visit:")
    print("https://osu.ppy.sh/home/account/edit\n")

    client_id = input("Enter your osu! OAuth Client ID: ").strip()
    client_secret = input("Enter your osu! OAuth Client Secret: ").strip()

    while True:
        user_id = input("Enter your osu! User ID (number): ").strip()
        if user_id.isdigit():
            break
        print("Invalid user ID, it must be a number.")

    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "user_id": user_id
    }

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Configuration saved to {CONFIG_PATH}\n")
    return config

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return first_run_setup()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
