"""The identity layer of the clean truth: herd numbers, districts and the 2024 regions, animal tags and registration
dates, farms with a second herd number, the June census by farm, and each herd's farmed land parcel by parcel."""
import datetime as dt
from collections import defaultdict

import numpy as np

import world as W

D = dt.date
HTYPE = {"dairy": "Farm", "suckler": "Farm", "finisher": "Farm", "rearer": "Farm", "letland": "Farm",
         "mart": "Mart", "dealer": "Dealer", "factory": "Slaughter plant", "knackery": "Knackery",
         "export": "Export assembly centre"}
NSO_CATS = ["dairy_cows", "other_cows", "bulls", "male_2yr_plus", "female_2yr_plus", "male_1_2yr", "female_1_2yr",
            "male_calves", "female_calves"]


def check_digit(s):
    return str(sum((i + 1) * int(c) for i, c in enumerate(s)) % 10)


def assign(w, rng):
    herds = w.herds
    # districts: ten to each region by its pre-2024 code; three of Coastal Vale's moved to Southern Vale in 2024
    for h in herds:
        r = h["region"]
        h["district"] = W.RCODE[r] + "%02d" % (1 + int(rng.integers(0, 10)))
        h["region_pre2024"] = r
        h["letter"] = W.RLETTER[r]
    rath = [h for h in herds if h["region"] == "Southern Vale" and h["type"] in ("dairy", "suckler", "rearer")]
    moved = [rath[i] for i in rng.choice(len(rath), 4, replace=False)]
    for k, h in enumerate(moved):
        h["district"] = W.MOVED_DISTRICTS[k % 3]
        h["region_pre2024"] = "Coastal Vale"
        h["letter"] = W.RLETTER["Coastal Vale"]
    # herd numbers: the issuing region's letter and seven digits, unique
    used = set()
    for h in herds:
        while True:
            hi = 9 if h["type"] in ("mart", "dealer", "factory", "knackery", "export") else int(rng.integers(1, 8))
            num = "%s%d%06d" % (h["letter"], hi, int(rng.integers(0, 1000000)))
            if num not in used:
                used.add(num)
                h["herd_no"] = num
                break
    # farm numbers for farm herds; a few suckler and dairy farms keep a second herd number on an out-farm
    fn = set()
    for h in herds:
        if HTYPE[h["type"]] == "Farm":
            while True:
                f = "%07d" % int(rng.integers(1000, 999999))
                if f not in fn:
                    fn.add(f)
                    h["farm_no"] = f
                    break
        else:
            h["farm_no"] = ""
    return moved


def second_herds(w, rng):
    """about one farm in eighteen keeps a second herd number on an out-farm in its own district, holding part of its
    resident stock all year"""
    A = w.A
    moved_any = set(m["a"] for m in w.moves)
    by_herd = defaultdict(list)
    for a in range(len(A["sex"])):
        by_herd[A["herd0"][a]].append(a)
    dams = set(A["dam"][a] for a in range(len(A["sex"])) if A["dam"][a] is not None)
    new = []
    for h in list(w.herds):
        if h["type"] in ("suckler", "dairy") and rng.random() < 0.055:
            nh = dict(h)
            nh["id"] = len(w.herds)
            while True:
                num = "%s%d%06d" % (h["letter"], int(rng.integers(1, 8)), int(rng.integers(0, 1000000)))
                if all(num != x.get("herd_no") for x in w.herds):
                    break
            nh["herd_no"] = num
            nh["out_farm_of"] = h["id"]
            w.herds.append(nh)
            new.append(nh)
            stay = [a for a in by_herd[h["id"]] if a not in moved_any and A["dam"][a] is None and A["exit"][a] is None
                    and a not in dams]
            for a in stay:
                if rng.random() < 0.35:
                    A["herd0"][a] = nh["id"]
    return new


def reissued(w, rng):
    """herd numbers of holdings that ceased before 2018 reissued to current farms: the herd register keeps both"""
    old = []
    farms = [h for h in w.herds if HTYPE[h["type"]] == "Farm" and "out_farm_of" not in h]
    for k in rng.choice(len(farms), 9, replace=False):
        h = farms[k]
        y0 = int(rng.integers(1996, 2009))
        y1 = int(rng.integers(y0 + 4, 2017))
        other = W.REG[int(rng.integers(0, len(W.REG)))]
        old.append(dict(herd_no=h["herd_no"], type="Farm", region=other, region_pre2024=other,
                        district=W.RCODE[other] + "%02d" % (1 + int(rng.integers(0, 10))), farm_no="",
                        valid_from=D(y0, int(rng.integers(1, 13)), 1), valid_to=D(y1, int(rng.integers(1, 13)), 1)))
        h["valid_from"] = D(int(rng.integers(y1 + 1, 2024)), int(rng.integers(1, 13)), 1)
    return old


def birth_herds(w, rng):
    """each animal's herd of birth: its own herd for calves born in the year and home-bred stock; for stock bought in
    before the year, a farm in the regions such stock comes from"""
    A = w.A
    src = defaultdict(list)
    for h in w.herds:
        if h["type"] in ("dairy", "suckler") and "out_farm_of" not in h:
            src[(W.RTYPE[h["region"]], h["type"])].append(h["id"])
    out = []
    sucklers = [h for k, v in src.items() if k[1] == "suckler" for h in v]
    for a in range(len(A["sex"])):
        h0 = w.herds[A["herd0"][a]]
        if A["role"][a] == "bull":
            out.append(int(rng.choice(sucklers)))
        elif A["birth"][a] >= 0 or h0["type"] in ("dairy", "suckler", "letland"):
            out.append(A["herd0"][a])
        elif h0["type"] == "rearer" or A["breed"][a] in ("HO", "FR"):
            out.append(int(rng.choice(src[("D", "dairy")])))
        else:
            t = str(rng.choice(["G", "W", "B"], p=[0.55, 0.25, 0.2]))
            out.append(int(rng.choice(src[(t, "suckler")])))
    return out


def tags(w, rng, bherd):
    A = w.A
    seq = defaultdict(int)
    out = []
    for a in range(len(A["sex"])):
        bh = w.herds[bherd[a]]
        b = W.dd(A["birth"][a])
        key = (bh["letter"], b.year % 100)
        seq[key] += 1
        body = "%02d%06d" % (b.year % 100, seq[key] * 7 + int(rng.integers(0, 7)))
        out.append("%s%s%s" % (bh["letter"], body, check_digit(body)))
        A["reg_lag"][a] = int(rng.integers(1, 28))
    assert len(set(out)) == len(out)
    return out


def census(w, IV):
    """each farm's cattle on 1 June 2026 in the statistics office's categories (the census is the stock the holdings
    hold that morning; marts, dealers and plants are not farms)"""
    A = w.A
    by_farm = defaultdict(lambda: defaultdict(int))
    day = W.CENSUS
    for a, iv in IV.items():
        for h, s, e in iv:
            if s <= day < e:
                hd = w.herds[h]
                if HTYPE[hd["type"]] != "Farm":
                    break
                farm = hd["farm_no"] if "out_farm_of" not in hd else w.herds[hd["out_farm_of"]]["farm_no"]
                c = W.category(A, a, day)
                male = A["sex"][a] == "M"
                if c == "dairy_cow":
                    k = "dairy_cows"
                elif c == "suckler_cow":
                    k = "other_cows"
                elif c == "over24":
                    k = ("bulls" if A["role"][a] == "bull" else "male_2yr_plus") if male else "female_2yr_plus"
                elif c == "m12_24":
                    k = "male_1_2yr" if male else "female_1_2yr"
                else:
                    k = "male_calves" if male else "female_calves"
                by_farm[farm][k] += 1
                break
    return by_farm


def land(w, IV, golden_kg, rng):
    """farmed land parcel by parcel: each region's declared area set so its golden kilograms a hectare sits at its
    design target against the line; commonage shared across herds in Eastern Uplands and Atlantic Coast"""
    farms = [h for h in w.herds if HTYPE[h["type"]] == "Farm"]
    days = defaultdict(float)
    for a, iv in IV.items():
        for h, s, e in iv:
            days[h] += e - s
    parcels = []
    pid = [100000]

    def parcel(herd, area, share, use):
        pid[0] += int(rng.integers(1, 9))
        parcels.append(dict(parcel="P%07d" % pid[0], herd=herd, area=area, share=share, use=use))
        return parcels[-1]["parcel"]

    for r in W.REG:
        target_ha = golden_kg[r] / (W.TARGET[r] * W.LINE * (1 + rng.uniform(-0.006, 0.006)))
        hs = [h for h in farms if h["region"] == r]
        weight = np.array([max(days[h["id"]] / W.NDAY, 3.0) * rng.lognormal(0, 0.35) for h in hs])
        if r in ("Eastern Uplands", "Atlantic Coast"):
            common_ha = target_ha * 0.12
            private_ha = target_ha - common_ha
        else:
            common_ha, private_ha = 0.0, target_ha
        alloc = private_ha * weight / weight.sum()
        for h, ha in zip(hs, alloc):
            n = max(1, int(rng.normal(5, 2)))
            cuts = np.sort(rng.uniform(0, 1, n - 1))
            pieces = np.diff(np.concatenate([[0], cuts, [1]])) * ha
            for p in pieces:
                use = "Grassland" if rng.random() < 0.86 else ("Arable" if rng.random() < 0.7 else "Rough grazing")
                parcel(h["herd_no"], round(float(p), 2), 100.0, use)
        if common_ha:
            left = common_ha
            while left > 1:
                size = min(left, float(rng.uniform(25, 90)))
                sharers = [hs[k] for k in rng.choice(len(hs), int(rng.integers(3, 12)), replace=False)]
                sh = rng.dirichlet(np.ones(len(sharers)))
                sh = np.round(sh * 100, 1)
                sh[-1] = round(100 - sh[:-1].sum(), 1)
                pid[0] += int(rng.integers(1, 9))
                code = "C%07d" % pid[0]
                for h, s in zip(sharers, sh):
                    parcels.append(dict(parcel=code, herd=h["herd_no"], area=round(size, 2), share=float(s), use="Commonage"))
                left -= size
    return parcels
