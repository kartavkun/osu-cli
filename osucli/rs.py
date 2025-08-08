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

    # playmode = user.playmode
    recent_score = api.user_scores(user_id, "recent", include_fails=True, limit=1, offset=0)

    if not recent_score:
        print("No recent scores found.")
        return

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
