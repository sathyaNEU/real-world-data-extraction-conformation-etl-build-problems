"""The inspection program's licensed stations: where each sits, when its licence began and ended, and the licence
numbers the Department gave again to a new station after the one holding it closed."""
import datetime as dt
from functools import lru_cache

import numpy as np

import world as W

N_STATIONS = {"Wexmoor": 12, "Halvering": 7, "Linnmere": 7, "Elkhollow": 5, "Dunmarsh": 5, "Quarrybrook": 4,
              "Marlbank": 4, "Larkhaven": 3, "Copperleaf": 3, "Thorncastle": 3, "Sallowford": 3, "Kinnard": 2}
# a station that closed, and the county of the station its number went to next
REISSUED = [("Dunmarsh", "Larkhaven", dt.date(2024, 6, 28), dt.date(2024, 10, 7)),
            ("Kinnard", "Thorncastle", dt.date(2024, 9, 13), dt.date(2025, 1, 21)),
            ("Copperleaf", "Sallowford", dt.date(2024, 4, 30), dt.date(2024, 8, 19)),
            ("Quarrybrook", "Marlbank", dt.date(2025, 2, 14), dt.date(2025, 5, 5)),
            ("Halvering", "Elkhollow", dt.date(2024, 11, 22), dt.date(2025, 3, 10)),
            ("Linnmere", "Wexmoor", dt.date(2025, 3, 31), dt.date(2025, 7, 14))]
# counties whose residents also use each other's stations (shared commuting corridors)
NEIGHBOURS = {"Wexmoor": ["Linnmere", "Halvering", "Quarrybrook"], "Linnmere": ["Wexmoor", "Elkhollow", "Marlbank"],
              "Halvering": ["Wexmoor", "Dunmarsh", "Quarrybrook"],
              "Elkhollow": ["Linnmere", "Copperleaf", "Marlbank", "Halvering"],
              "Dunmarsh": ["Halvering", "Larkhaven", "Kinnard"], "Quarrybrook": ["Wexmoor", "Halvering", "Sallowford"],
              "Marlbank": ["Linnmere", "Elkhollow", "Thorncastle", "Quarrybrook"], "Larkhaven": ["Dunmarsh", "Kinnard", "Thorncastle"],
              "Copperleaf": ["Elkhollow", "Sallowford"], "Thorncastle": ["Marlbank", "Larkhaven", "Kinnard"],
              "Sallowford": ["Quarrybrook", "Copperleaf"], "Kinnard": ["Dunmarsh", "Larkhaven"]}
FIRST = ["Broadway", "Precision", "Main Street", "Hilltop", "Valley", "Northside", "Southgate", "Lakeside", "Express",
         "Pioneer", "Summit", "Gateway", "Riverbend", "Crossroads", "Parkway", "Redline", "Liberty", "Heritage",
         "Brightway", "Cornerstone", "Interstate", "Frontier", "Keystone", "Midtown", "Westside", "Eastgate"]
LAST = ["Auto Care", "Emissions Center", "Lube & Tune", "Service Center", "Automotive", "Tire & Auto",
        "Car Care", "Garage", "Motors Service", "Inspection Station", "Auto Repair"]
STREETS = ["Main St", "Oak Ave", "Commerce Dr", "Industrial Pkwy", "Route 9", "Mill Rd", "Center St", "Elm St",
           "Highway 41", "Market St", "Depot Rd", "Lincoln Ave", "Fairground Rd", "Station Rd", "Church St"]


class Register:
    def __init__(self, stations):
        self.s = stations

    def open_in(self, county, d):
        return [x for x in self.s if x["county"] == county and x["start"] <= d and (x["end"] is None or d <= x["end"])]

    def pick(self, rng, county, d):
        c = county
        if rng.random() < 0.16:
            nb = NEIGHBOURS[county]
            c = nb[int(rng.integers(0, len(nb)))]
        cand = self.open_in(c, d) or self.open_in(county, d)
        w = np.array([x["size"] for x in cand], float)
        x = cand[int(rng.choice(len(cand), p=w / w.sum()))]
        return x["no"], int(rng.integers(1, x["lanes"] + 1))


@lru_cache(maxsize=None)
def register():
    rng = np.random.default_rng(W.SEED + 501)
    nums = rng.permutation(np.arange(1012, 4980))[:80]
    k = 0
    out = []
    used = set()
    for name in W.NAMES:
        towns = W.TOWNS[name]
        for i in range(N_STATIONS[name]):
            while True:
                nm = "%s %s" % (FIRST[int(rng.integers(0, len(FIRST)))], LAST[int(rng.integers(0, len(LAST)))])
                if nm not in used:
                    used.add(nm)
                    break
            start = dt.date(2023, 11, 1) + dt.timedelta(days=int(rng.integers(0, 55)))
            out.append(dict(no=int(nums[k]), name=nm, county=name, town=towns[i % len(towns)],
                            street="%d %s" % (int(rng.integers(100, 9900)), STREETS[int(rng.integers(0, len(STREETS)))]),
                            start=start, end=None, lanes=int(rng.integers(1, 4)), size=float(rng.uniform(0.6, 1.6)),
                            gen=0))
            k += 1
    # stations that closed during the cycle; the Department gave each number again to a new licensee elsewhere
    for (old_c, new_c, closed, reissued) in REISSUED:
        cands = [x for x in out if x["county"] == old_c and x["end"] is None and x["gen"] == 0]
        x = cands[int(rng.integers(0, len(cands)))]
        x["end"] = closed
        while True:
            nm = "%s %s" % (FIRST[int(rng.integers(0, len(FIRST)))], LAST[int(rng.integers(0, len(LAST)))])
            if nm not in used:
                used.add(nm)
                break
        towns = W.TOWNS[new_c]
        out.append(dict(no=x["no"], name=nm, county=new_c, town=towns[int(rng.integers(0, len(towns)))],
                        street="%d %s" % (int(rng.integers(100, 9900)), STREETS[int(rng.integers(0, len(STREETS)))]),
                        start=reissued, end=None, lanes=int(rng.integers(1, 3)), size=float(rng.uniform(0.7, 1.4)), gen=1))
    return Register(out)
