import os
import sys
import argparse
from configparser import ConfigParser
from ossapi import Ossapi
from datetime import datetime
from colorama import Fore, Style, init

# === Initialize colorama for cross-platform coloring ===
init(autoreset=True)

# === Config defaults and paths ===
CONFIG_DIR = os.path.expanduser("~/.config/osufetch")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")

def load_or_create_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

    config = ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        # Проверим, что все нужные поля есть
        if ("DEFAULT" not in config or
            not config["DEFAULT"].get("client_id") or
            not config["DEFAULT"].get("client_secret") or
            not config["DEFAULT"].get("user_id")):
            print("Config file is missing required fields. Recreating...")
            os.remove(CONFIG_FILE)
            return load_or_create_config()
        return config
    else:
        print("Welcome to osu-cli first run setup!")
        print("To get your OAuth tokens, please visit:")
        print("https://osu.ppy.sh/home/account/edit\n")
        client_id = input("Enter your osu! OAuth Client ID: ").strip()
        client_secret = input("Enter your osu! OAuth Client Secret: ").strip()
        while True:
            user_id = input("Enter your osu! User ID (number): ").strip()
            if user_id.isdigit():
                break
            print("Invalid user ID, it must be a number.")
        config["DEFAULT"] = {
            "client_id": client_id,
            "client_secret": client_secret,
            "user_id": user_id,
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        print(f"Configuration saved to {CONFIG_FILE}\n")
        return config

def fetch_user_data(api, user_id):
    try:
        user = api.user(user_id)
        return user
    except Exception as e:
        print(f"Error fetching user data: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="osu-cli — terminal tool for osu! info")
    parser.add_argument("id", nargs="?", help="Specify osu! user ID/Name for this run only (does NOT overwrite config)")
    # parser.add_argument("-v", "--version", action="version", version=f"{__version__}")
    args = parser.parse_args()

    config = load_or_create_config()

    client_id = config["DEFAULT"].get("client_id")
    client_secret = config["DEFAULT"].get("client_secret")

    user_id = args.id if args.id else config["DEFAULT"].get("user_id")

    if not user_id:
        print("Error: osu! user ID is missing or invalid.")
        sys.exit(1)

    if not user_id.isdigit() and not user_id.startswith("@"):
        user_id = f"@{user_id}"
    
    api = Ossapi(client_id, client_secret)
    user = fetch_user_data(api, user_id)

    if not user_id.isdigit():
        user_id = user.id

    # playmode = user.playmode
    recent_score = api.user_scores(user_id, "recent", include_fails=True, limit=1, offset=0)
    score = recent_score[0]

    # Score info
    if score.pp == None:
        pp = 0
    else:
        pp = score.pp
    acc = score.accuracy
    if score.passed == True:
        rank = score.rank.value
    else:
        rank = "F"
    mods = "".join([mod.acronym for mod in score.mods])
    misses = score.statistics.miss
    total_score = f"{score.total_score:,}"
    max_combo = score.max_combo

    # Beatmap info
    beatmap_title = score.beatmapset.title
    beatmap_artist = score.beatmapset.artist
    beatmap_diff_name = score.beatmap.version
    beatmap_diff_rate = score.beatmap.difficulty_rating
    beatmap_url = score.beatmap.url

    beatmap_od = score.beatmap.accuracy
    beatmap_ar = score.beatmap.ar
    beatmap_cs = score.beatmap.cs
    beatmap_hp = score.beatmap.drain
    bpm = score.beatmap.bpm
    if bpm is None:
        beatmap_bpm = "N/A"
    elif bpm.is_integer():
        beatmap_bpm = int(bpm)
    else:
        beatmap_bpm = round(bpm, 2)

    def format_length(seconds: int) -> str:
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}:{minutes:02}:{sec:02}"
        else:
            return f"{minutes}:{sec:02}"

    beatmap_length = format_length(score.beatmap.hit_length)

    # Player info
    country = user.country.code
    username = user.username
    player_pp = user.statistics.pp
    global_rank = user.statistics.global_rank
    country_rank = user.statistics.country_rank

    print(f"{country} {username}: {player_pp}pp (#{global_rank} {country}{country_rank})")
    print(f"{beatmap_artist} - {beatmap_title} [{beatmap_diff_name}] [{beatmap_diff_rate}★] | {beatmap_url}")
    print(f"{rank} | {mods} | {total_score} | {acc * 100:.2f}%")
    print(f"{pp}pp | {max_combo}x | {misses}❌")
    print(f"{beatmap_length} |  CS: {beatmap_cs} AR: {beatmap_ar} OD: {beatmap_od} HP: {beatmap_hp} | BPM: {beatmap_bpm}")

    print()

if __name__ == "__main__":
    main()

