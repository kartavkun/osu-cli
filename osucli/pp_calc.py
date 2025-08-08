import rosu_pp_py as rosu
from osucli.download_map import download_map
from osucli.rs import recent_score_data

def pp_calc():
    score_data = recent_score_data()

    acc = score_data["acc"]
    misses = score_data["misses"]
    max_combo = score_data["max_combo"]
    mods = score_data["mods"]

    diff_path = download_map()
# either `path`, `bytes`, or `content` must be specified when parsing a map
    map = rosu.Beatmap(path = diff_path)

# Whereas osu! simply times out on malicious maps, rosu-pp does not. To
# prevent potential performance/memory issues, it is recommended to check
# beforehand whether a map is too suspicious for further calculation.
    if map.is_suspicious():
        exit()

    perf = rosu.Performance(
        # various kwargs available
        accuracy = acc,
        lazer = False, # defaults to True if not specified
        misses = misses,
        combo = max_combo,
        mods = { 'acronym': f'{mods}' },
        # If only accuracy is given but no specific hitresults, it is recommended
        # to generate hitresults via `HitResultPriority.Fastest`. Otherwise,
        # finding the best hitresults can be very slow.
        hitresult_priority=rosu.HitResultPriority.Fastest,
    )

# Each kwarg can also be specified afterwards through setters
    # perf.set_accuracy(acc) # override previously specified accuracy
    # perf.set_mods(0)    # HDDT
    # perf.set_clock_rate(1.4)

# Second argument of map attributes specifies whether mods still need to be accounted for
# `True`: mods already considered; `False`: value should still be adjusted
    # perf.set_ar(10.5, True)
    # perf.set_od(5, False)

# Calculate for the map
    attrs = perf.calculate(map)

# Note that calculating via map will have to calculate difficulty attributes
# internally which is fairly expensive. To speed it up, you can also pass in
# previously calculated attributes, but be sure they were calculated for the
# same difficulty settings like mods, clock rate, custom map attributes, ...

    perf.set_accuracy(100)
    perf.set_misses(None)
    perf.set_combo(None)

# Calculate a new set of attributes by re-using previous attributes instead of the map
    max_attrs = perf.calculate(attrs)

    print(f'PP: {attrs.pp}/{max_attrs.pp} | Stars: {max_attrs.difficulty.stars}')

if __name__ == "__main__":
    pp_calc()
