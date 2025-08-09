import os
import re
import requests
import zipfile
from osucli.rs import recent_score_data

def download_map():
    score_data = recent_score_data()
    if not score_data:
        print("Нет данных по недавнему скоору, скачивание карты невозможно.")
        return None

    beatmap_id = score_data["beatmap_id"]
    beatmap_mapper = score_data["beatmap_mapper"]
    beatmap_artist = score_data["beatmap_artist"]
    beatmap_title = score_data["beatmap_title"]
    beatmap_diff_name = score_data["beatmap_diff_name"]

    cache_dir = os.path.expanduser("~/.cache/osu-cli")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    url = f"https://api.nerinyan.moe/d/{beatmap_id}"
    headers = {
        "Accept": "application/x-osu-beatmap-archive"
    }

    output_path = os.path.join(cache_dir, f"{beatmap_id}.zip")
    extract_dir = os.path.join(cache_dir, str(beatmap_id))

    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка загрузки карты {beatmap_id}: {e}")
        return None

    # print(f"Файл сохранён в {output_path}")

    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    def clean_filename(s):
        return re.sub(r'[\\/*?:"<>|]', '', s)

    beatmap_artist = clean_filename(beatmap_artist)
    beatmap_title = clean_filename(beatmap_title)
    beatmap_mapper = clean_filename(beatmap_mapper)
    beatmap_diff_name = clean_filename(beatmap_diff_name)

    diff_path = os.path.join(
        extract_dir,
        f"{beatmap_artist} - {beatmap_title} ({beatmap_mapper}) [{beatmap_diff_name}].osu"
    )

    # print(f"Карта сохранена в {diff_path}")

    return diff_path


if __name__ == "__main__":
    download_map()
