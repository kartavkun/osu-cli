from ossapi import Ossapi
from osucli.config import load_config
from osucli.ascii_arts import get_ascii_art
import httpx
from colorama import Fore, Style

def fetch_user_data(user_id_or_name=None):
    config = load_config()
    user_id_or_name = user_id_or_name or config.get("user_id")

    client_id = config["client_id"]
    client_secret = config["client_secret"]

    api = Ossapi(client_id, client_secret)

    user_id = user_id_or_name  # ВАЖНО: присваиваем user_id

    if not str(user_id).isdigit():
        user = api.user(user_id)
        user_id = user.id
    else:
        user = api.user(user_id)
    playmode = user.playmode

    url = f"https://osuworld.octo.moe/api/users/{user_id}?mode={playmode}"
    with httpx.Client(http2=True) as client:
        response = client.get(url)
        data = response.json()

    def load_regions():
        url = "https://osuworld.octo.moe/locales/en/regions.json"
        try:
            with httpx.Client(http2=True, timeout=10) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Warning: Failed to fetch regions mapping: {e}")
            return {}

    regions = load_regions()

    region_id = data.get("region_id")

    state = "-"
    if region_id:
        region_id_str = str(region_id)
        country_code = region_id_str.split("-")[0]

        if country_code in regions:
            country_regions = regions[country_code]
            state = country_regions.get(region_id_str, "-")
        else:
            state = regions.get(region_id_str, "-")
    else:
        state = "—"

    grades = user.statistics.grade_counts

    ascii_art = get_ascii_art().get(playmode, "(no ascii art)")

    ascii_lines = ascii_art.strip("\n").split("\n")
    info_lines = [
        f"{Fore.CYAN}Username:{Style.RESET_ALL}       {Fore.WHITE}{user.username}{Style.RESET_ALL}",
        f"{Fore.CYAN}Also known as:{Style.RESET_ALL}  {Fore.WHITE}{', '.join(user.previous_usernames) if user.previous_usernames else '-'}{Style.RESET_ALL}",
        f"{Fore.CYAN}Country:{Style.RESET_ALL}        {Fore.WHITE}{user.country.code} | {user.country.name}{Style.RESET_ALL}",
        f"{Fore.CYAN}State:{Style.RESET_ALL}          {Fore.WHITE}{state}{Style.RESET_ALL}",
        f"{Fore.CYAN}Playmode:{Style.RESET_ALL}       {Fore.WHITE}{playmode}{Style.RESET_ALL}",
        f"{Fore.CYAN}Team:{Style.RESET_ALL}           {Fore.WHITE}{f'{user.team.short_name} | {user.team.name}' if user.team else '-'}{Style.RESET_ALL}",
        f"{Fore.CYAN}PP:{Style.RESET_ALL}             {Fore.WHITE}{round(user.statistics.pp)}{Style.RESET_ALL}",
        f"{Fore.CYAN}Accuracy:{Style.RESET_ALL}       {Fore.WHITE}{round(user.statistics.hit_accuracy, 2)}%{Style.RESET_ALL}",
        f"{Fore.CYAN}Global Rank:{Style.RESET_ALL}    {Fore.WHITE}#{user.statistics.global_rank}{Style.RESET_ALL}",
        f"{Fore.CYAN}Country Rank:{Style.RESET_ALL}   {Fore.WHITE}#{user.statistics.country_rank}{Style.RESET_ALL}",
        f"{Fore.CYAN}State Rank:{Style.RESET_ALL}     {Fore.WHITE}#{data.get('placement', '-')}{Style.RESET_ALL}",
        f"{Fore.CYAN}Play Count:{Style.RESET_ALL}     {Fore.WHITE}{user.statistics.play_count}{Style.RESET_ALL}",
        f"{Fore.CYAN}Max Combo:{Style.RESET_ALL}      {Fore.WHITE}{user.statistics.maximum_combo}{Style.RESET_ALL}",
        f"{Fore.CYAN}Grades:{Style.RESET_ALL}         {Fore.WHITE}SS: {grades.ss} | SSH: {grades.ssh} | S: {grades.s} | SH: {grades.sh} | A: {grades.a}{Style.RESET_ALL}",
        f"{Fore.CYAN}Supporter:{Style.RESET_ALL}      {Fore.WHITE}{'Yes' if user.is_supporter else 'No'}{Style.RESET_ALL}",
        f"{Fore.CYAN}Joined:{Style.RESET_ALL}         {Fore.WHITE}{user.join_date.date()}{Style.RESET_ALL}",
    ]

    if playmode == "mania":
        info_lines[6] = f"{Fore.CYAN}PP:{Style.RESET_ALL}             {Fore.WHITE}{round(user.statistics.pp)} (4K: {round(user.statistics.variants[0].pp)}, 7K: {round(user.statistics.variants[1].pp)}){Style.RESET_ALL}"
        info_lines[8] = f"{Fore.CYAN}Global Rank:{Style.RESET_ALL}    {Fore.WHITE}#{user.statistics.global_rank} (4K: #{user.statistics.variants[0].global_rank}, 7K: #{user.statistics.variants[1].global_rank}){Style.RESET_ALL}"
        info_lines[9] = f"{Fore.CYAN}Country Rank:{Style.RESET_ALL}   {Fore.WHITE}#{user.statistics.country_rank} (4K: #{user.statistics.variants[0].country_rank}, 7K: #{user.statistics.variants[1].country_rank}){Style.RESET_ALL}"

    max_lines = max(len(ascii_lines), len(info_lines))
    for i in range(max_lines):
        art_line = ascii_lines[i] if i < len(ascii_lines) else " " * 40
        info_line = info_lines[i] if i < len(info_lines) else ""
        print(f"{Fore.YELLOW}{art_line:<40}{Style.RESET_ALL}  {info_line}")

    print()

