import rosu_pp_py as rosu
from osucli.download_map import download_map

MODS_DICT = {
    "NF": 1,          # NoFail
    "EZ": 2,          # Easy
    "TD": 4,          # TouchDevice
    "HD": 8,          # Hidden
    "HR": 16,         # HardRock
    "SD": 32,         # SuddenDeath
    "DT": 64,         # DoubleTime
    "RX": 128,        # Relax
    "HT": 256,        # HalfTime
    "NC": 512,        # Nightcore (DT + NC = 576)
    "FL": 1024,       # Flashlight
    "AO": 2048,       # Autoplay
    "SO": 4096,       # SpunOut
    "AP": 8192,       # Relax2 (Autopilot)
    "PF": 16384,      # Perfect (SD + PF = 16416)
    "K4": 32768,      # Key4
    "K5": 65536,      # Key5
    "K6": 131072,     # Key6
    "K7": 262144,     # Key7
    "K8": 524288,     # Key8
    "FI": 1048576,    # FadeIn
    "RD": 2097152,    # Random
    "CN": 4194304,    # Cinema
    "TP": 8388608,    # Target
    "K9": 16777216,   # Key9
    "KC": 33554432,   # KeyCoop
    "K1": 67108864,   # Key1
    "K3": 134217728,  # Key3
    "K2": 268435456,  # Key2
    "V2": 536870912,  # ScoreV2
    "MR": 1073741824, # Mirror
    "CL": 0,          # Laser flag — не влияет на число модов
}

def mods_str_to_int(mods_str: str) -> int:
    mods_str = mods_str.upper()
    mods_int = 0
    i = 0
    while i < len(mods_str):
        mod_code = mods_str[i:i+2]
        if mod_code in MODS_DICT:
            mods_int |= MODS_DICT[mod_code]
            i += 2
        else:
            i += 1
    return mods_int

def pp_calc():
    from osucli.rs import recent_score_data  # локальный импорт чтобы избежать цикла
    score_data = recent_score_data()
    if not score_data:
        print("Нет данных для расчёта PP")
        return {"pp": 0, "pp_SS": 0}

    diff_path = download_map()
    if not diff_path:
        print("Не удалось скачать карту для расчёта PP")
        return {"pp": 0, "pp_SS": 0}

    mods_str = score_data["mods"]
    mods_int = mods_str_to_int(mods_str)

    # Анализируем карту
    beatmap = rosu.Beatmap(path=diff_path)

    # Параметры из последнего скора
    max_combo = score_data["max_combo"]
    misses = score_data["misses"]
    acc = score_data["acc"]

    # Вычисляем PP с учётом модов и точности
    # PP для последнего скора
    perf = rosu.Performance(
        mods=mods_int,
        combo=max_combo,
        misses=misses,
        accuracy=acc
    )
    attrs = perf.calculate(beatmap)
    pp_value = round(attrs.pp, 2)

    # PP для SS (максимального) на этой карте с теми же модами
    perf.set_accuracy(100)
    perf.set_misses(None)
    perf.set_combo(None)

    max_attrs = perf.calculate(beatmap)
    ss_pp_value = round(max_attrs.pp, 2)

    # print(f'PP: {pp_value}/{ss_pp_value}')

    return {"pp": pp_value, "pp_SS": ss_pp_value}

if __name__ == "__main__":
    pp_calc()
