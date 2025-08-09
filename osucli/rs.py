from ossapi import Ossapi
from osucli.config import load_config
from colorama import Fore, Style

def recent_score_data():
    config = load_config()
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    user_id = config["user_id"]
    
    api = Ossapi(client_id, client_secret)

    if not str(user_id).isdigit():
        user = api.user(user_id)
        user_id = user.id
    else:
        user = api.user(user_id)

    recent_score = api.user_scores(user_id, "recent", include_fails=True, limit=1, offset=0)

    if not recent_score:
        print("No recent scores found.")
        return None

    score = recent_score[0]

    # Score info
    pp = score.pp if score.pp is not None else None
    acc = score.accuracy
    rank = score.rank.value if score.passed else "F"
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
    beatmap_id = score.beatmapset.id
    beatmap_mapper = score.beatmapset.creator

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

    return {
        "pp": pp,
        "acc": acc,
        "misses": misses,
        "max_combo": max_combo,
        "beatmap_title": beatmap_title,
        "beatmap_artist": beatmap_artist,
        "beatmap_diff_name": beatmap_diff_name,
        "beatmap_diff_rate": beatmap_diff_rate,
        "beatmap_url": beatmap_url,
        "beatmap_id": beatmap_id,
        "beatmap_mapper": beatmap_mapper,
        "beatmap_od": beatmap_od,
        "beatmap_ar": beatmap_ar,
        "beatmap_cs": beatmap_cs,
        "beatmap_hp": beatmap_hp,
        "beatmap_bpm": beatmap_bpm,
        "beatmap_length": beatmap_length,
        "country": country,
        "username": username,
        "player_pp": player_pp,
        "global_rank": global_rank,
        "country_rank": country_rank,
        "mods": mods,
        "rank": rank,
        "total_score": total_score,
    }

def print_score_data():
    from osucli.pp_calc import pp_calc
    pp_stat = pp_calc()
    score_data = recent_score_data()
    if not score_data:
        return

    pp = score_data["pp"]
    acc = score_data["acc"]
    misses = score_data["misses"]
    max_combo = score_data["max_combo"]

    beatmap_title = score_data["beatmap_title"]
    beatmap_artist = score_data["beatmap_artist"]
    beatmap_diff_name = score_data["beatmap_diff_name"]
    beatmap_diff_rate = score_data["beatmap_diff_rate"]
    beatmap_url = score_data["beatmap_url"]

    beatmap_od = score_data["beatmap_od"]
    beatmap_ar = score_data["beatmap_ar"]
    beatmap_cs = score_data["beatmap_cs"]
    beatmap_hp = score_data["beatmap_hp"]
    beatmap_bpm = score_data["beatmap_bpm"]
    beatmap_length = score_data["beatmap_length"]

    country = score_data["country"]
    username = score_data["username"]
    player_pp = score_data["player_pp"]
    mods = score_data["mods"]
    global_rank = score_data["global_rank"]
    country_rank = score_data["country_rank"]
    rank = score_data["rank"]
    total_score = score_data["total_score"]

    if pp_stat:
        pp = pp_stat.get("pp", "N/A")
        pp_SS = pp_stat.get("pp_SS", "N/A")
    else:
        pp = "N/A"
        pp_SS = "N/A"

    # if pp is None:
    #     pp = 0

    print(f" > {country} {username}: {player_pp}pp (#{global_rank} {country}{country_rank})")
    print(f" > {beatmap_artist} - {beatmap_title} [{beatmap_diff_name}] [{beatmap_diff_rate}★] | {beatmap_url}")
    print(f" > {rank} | {mods} | {total_score} | {acc * 100:.2f}%")
    print(f" > {pp}pp/{pp_SS}pp | {max_combo}x | {misses}❌")
    print(f" > {beatmap_length} | CS: {beatmap_cs} AR: {beatmap_ar} OD: {beatmap_od} HP: {beatmap_hp} | BPM: {beatmap_bpm}")
    print()
