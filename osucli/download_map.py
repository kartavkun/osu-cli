import os
import requests
import zipfile
from osucli.rs import recent_score_data

def download_map():
    score_data = recent_score_data()

    beatmap_id = score_data["beatmap_id"]
    beatmap_mapper = score_data["beatmap_mapper"]
    beatmap_artist = score_data["beatmap_artist"]
    beatmap_title = score_data["beatmap_title"]
    beatmap_diff_name = score_data["beatmap_diff_name"]

    if not os.path.exists(f"/home/kartavkun/.cache/osu-cli"):
        os.makedirs(f"/home/kartavkun/.cache/osu-cli")

    url = f"https://api.nerinyan.moe/d/{beatmap_id}"
    headers = {
        "Accept": "application/x-osu-beatmap-archive"
    }

    output_path = f"/home/kartavkun/.cache/osu-cli/{beatmap_id}.zip"
    directory_to_extract_to = f"/home/kartavkun/.cache/osu-cli/{beatmap_id}/"

    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка загрузки карты {beatmap_id}: {e}")
        return

    print(f"Файл сохранён в {output_path}")

    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

    diff_path = f"{directory_to_extract_to}{beatmap_artist} - {beatmap_title} ({beatmap_mapper}) [{beatmap_diff_name}].osu"

    return diff_path

if __name__ == "__main__":
    download_map()
