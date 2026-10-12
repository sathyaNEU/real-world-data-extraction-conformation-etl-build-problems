"""The valley's wind at the Harlow Falls station (5-minute records, Pacific standard time), the town's
households, and the season's odor: each source's episodes when its odor reaches the town, and the residents'
complaints, which come when they are home to notice."""
import datetime as dt
import math

import numpy as np

import core

SEED = 121
P = dict(
    linger=[0.05, 0.06, 0.08, 0.11, 0.15, 0.17, 0.18, 0.17, 0.14],   # SW lingering into the evening, by month
    storm=[0.22, 0.20, 0.16, 0.10, 0.03, 0.01, 0.0, 0.0, 0.03],       # synoptic southerly days
    north=[0.03, 0.04, 0.05, 0.04, 0.02, 0.01, 0.01, 0.01, 0.03],     # dry north wind days
    p_nslope=0.52, p_ecanyon=0.56, p_calm=0.30,
    # episodes: per qualifying occasion
    compost=0.95, compost_pre=0.06, landfill=0.13, wwtp=0.11, render=0.22, mush=0.26,
    # complaint intensity per affected household-hour (scaled by home hours)
    q_compost=0.00024, q_compost_calm=0.00060, q_landfill=0.000047, q_wwtp=0.0, q_render=0.0016, q_mush=0.0002,
    freq_nights=[0.40, 0.36, 0.32, 0.28], bg_rate=1.4,
    freq_hours=[23, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6],
    mod_nights=[0.080, 0.065, 0.050, 0.040, 0.035, 0.030, 0.022, 0.015],
    mod_hours=[20, 21, 21, 22, 22, 23, 23, 0, 1, 6, 7],
)
HOME = np.array([0.30, 0.20, 0.12, 0.08, 0.07, 0.12, 0.45, 0.75, 0.55, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.15, 0.70, 0.95, 1.00, 0.95, 0.75, 0.48])          # by local clock hour: nobody notices 9 to 16


def rng_for(*keys):
    return np.random.default_rng([SEED] + [abs(hash_str(k)) % (2 ** 31) for k in keys])


def hash_str(s):
    h = 2166136261
    for ch in str(s).encode():
        h = ((h ^ ch) * 16777619) % (2 ** 32)
    return h


# ----------------------------------------------------------------------------------------------------------------
# households

STREETS_LONG = ["Mill St", "Kestrel Ave", "Oak Ave", "Valley Rd", "Main St", "Sycamore St", "Bidwell Ave",
                "Foothill Blvd", "Creekside Dr", "Granite Way"]
STREETS_CROSS = ["1st St", "2nd St", "3rd St", "4th St", "5th St", "6th St", "7th St", "8th St", "9th St",
                 "10th St", "Pine St", "Cedar St", "Walnut St", "Alder St", "Laurel St", "Madrone St", "Hazel St",
                 "Dogwood Ln", "Ponderosa Dr", "Manzanita Ct", "Buttercup Ln", "Quail Run", "Ridgeview Dr",
                 "Lassen St", "Shasta St", "Feather Dr", "Butte St", "Tehama Ct"]


def households():
    """About 6,800 service addresses on the valley floor plus apartment complexes; x, y in km from the station."""
    rng = rng_for("households")
    ax = (math.sin(math.radians(core.VALLEY_AXIS)), math.cos(math.radians(core.VALLEY_AXIS)))
    px = (math.cos(math.radians(core.VALLEY_AXIS)), -math.sin(math.radians(core.VALLEY_AXIS)))
    out = []
    seen = set()
    n = 0
    while len(out) < 6800:
        t = rng.uniform(-2.7, 2.5)
        w = rng.normal(0.0, 0.42)
        if abs(w) > 0.95:
            continue
        x, y = t * ax[0] + w * px[0], t * ax[1] + w * px[1]
        street = STREETS_LONG[int(rng.integers(len(STREETS_LONG)))] if rng.random() < 0.45 else \
            STREETS_CROSS[int(rng.integers(len(STREETS_CROSS)))]
        num = int(100 + 20 * int(rng.integers(1, 90)) + int(rng.integers(0, 19)))
        key = (num, street)
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(hid=len(out), num=num, street=street, unit=None, x=x, y=y, apt=None))
    # apartment complexes: one parcel point, many units
    for name, num, street, t, w, units in (("Creekside Apartments", 1450, "Creekside Dr", -1.55, -0.35, 48),
                                           ("Mill Street Lofts", 812, "Mill St", 0.25, 0.10, 24),
                                           ("Granite Way Commons", 2216, "Granite Way", 1.35, 0.30, 32)):
        x, y = t * ax[0] + w * px[0], t * ax[1] + w * px[1]
        for u in range(1, units + 1):
            out.append(dict(hid=len(out), num=num, street=street, unit=str(u), x=x, y=y, apt=name))
    for h in out:
        h["lat"], h["lon"] = core.to_latlon(h["x"], h["y"])
        h["bear"] = {k: core.bearing_deg(h["lat"], h["lon"], core.FAC[k]["lat"], core.FAC[k]["lon"]) for k in core.FKEYS}
        h["dist"] = {k: math.hypot(h["x"] - core.FAC[k]["xy"][0], h["y"] - core.FAC[k]["xy"][1]) for k in core.FKEYS}
        h["t"] = h["x"] * ax[0] + h["y"] * ax[1]
    return out


# ----------------------------------------------------------------------------------------------------------------
# wind: hourly regimes by day, then 5-minute records

def day_plan(d, rng):
    """Hour-by-hour regime for one day, PST clock hours 0 to 23."""
    m = d.month - 1
    reg = [None] * 24
    r = rng.random()
    if r < P["storm"][m]:
        kind = "storm"
    elif r < P["storm"][m] + P["north"][m]:
        kind = "north"
    else:
        kind = "valley"
    linger = kind == "valley" and rng.random() < P["linger"][m]
    t_m = 9 + int(rng.random() < 0.55)                 # up-valley from 9 or 10
    t_e = (20 + int(rng.integers(0, 3))) if linger else (17 + int(rng.integers(0, 3)))
    for h in range(24):
        if kind == "storm":
            reg[h] = "storm"
        elif kind == "north":
            reg[h] = "north"
        elif t_m <= h < t_e:
            reg[h] = "sw_day" if h < 18 else "sw_eve"
        elif h == t_e:
            reg[h] = "transition"
        else:
            reg[h] = "drain"
    if kind == "valley":
        night = [h for h in list(range(t_e + 1, 24)) + list(range(0, t_m))]
        night = [h for h in night if (d, h) not in FORCED]
        # sub-regimes inside the night drainage
        if rng.random() < P["p_nslope"]:
            s = int(rng.choice([22, 23, 0, 1]))
            for k in range(int(rng.integers(2, 5))):
                hh = (s + k) % 24
                if reg[hh] == "drain":
                    reg[hh] = "nslope"
        if rng.random() < P["p_ecanyon"]:
            s = int(rng.choice([0, 1, 2, 3]))
            for k in range(int(rng.integers(2, 6))):
                hh = (s + k) % 24
                if reg[hh] == "drain":
                    reg[hh] = "ecanyon"
        if rng.random() < P["p_calm"]:
            s = int(rng.choice(night))
            for k in range(int(rng.integers(1, 4))):
                hh = (s + k) % 24
                if reg[hh] in ("drain", "transition"):
                    reg[hh] = "calm"
        if rng.random() < 0.20:
            hh = int(rng.choice([18, 19, 20, 21, 22]))
            if reg[hh] in ("transition", "drain"):
                reg[hh] = "south"
    for (dd, hh) in FORCED:
        if dd == d:
            reg[hh] = "drain" if kind == "valley" else reg[hh]
    return dict(kind=kind, linger=linger, t_m=t_m, t_e=t_e, reg=reg)


# the 23:00 standard-time hours that open each local month of the season: one class (a usable, non-calm wind),
# so months counted on the station's clock and on local time hold the same hours
FORCED = {(dt.date(2026, 4, 30), 23), (dt.date(2026, 5, 31), 23), (dt.date(2026, 6, 30), 23),
          (dt.date(2026, 7, 31), 23), (dt.date(2026, 8, 31), 23), (dt.date(2026, 9, 30), 23)}


REGIME = {  # mean direction, direction spread (5-minute), speed range
    "sw_day": (227.0, 11.0, (2.4, 5.2)), "sw_eve": (233.0, 13.0, (0.9, 2.6)), "transition": (None, 60.0, (0.05, 0.40)),
    "drain": (41.0, 12.0, (0.8, 2.4)), "nslope": (352.0, 12.0, (0.6, 1.5)), "ecanyon": (112.0, 13.0, (0.6, 1.7)),
    "calm": (None, 70.0, (0.05, 0.42)), "storm": (196.0, 18.0, (3.0, 8.5)), "north": (2.0, 14.0, (3.5, 8.0)),
    "south": (171.0, 12.0, (0.7, 1.6)),
}


def five_minute(d, plan, rng):
    """288 records for one day: (minute_of_day, speed, direction, sigma)."""
    out = []
    for h in range(24):
        name = plan["reg"][h]
        mean, spread, (s0, s1) = REGIME[name]
        if mean is None:
            mean = float(rng.uniform(0, 360))
        base_dir = mean + rng.normal(0, 6.0)
        base_sp = rng.uniform(s0, s1)
        for k in range(12):
            if name in ("calm", "transition"):
                dr = (base_dir + rng.normal(0, spread)) % 360
                sp = max(0.0, base_sp * rng.uniform(0.3, 1.5))
            else:
                dr = (base_dir + rng.normal(0, spread * 0.55)) % 360
                sp = max(0.1, base_sp * rng.lognormal(0, 0.18))
            sig = float(np.clip(spread * rng.uniform(0.6, 1.4), 3.0, 75.0))
            out.append((h * 60 + 5 * k, sp, dr, sig))
    return out


def vector_hour(recs):
    if not recs:
        return None
    u = sum(-s * math.sin(math.radians(d)) for _, s, d, _ in recs) / len(recs)
    v = sum(-s * math.cos(math.radians(d)) for _, s, d, _ in recs) / len(recs)
    sp = math.hypot(u, v)
    dr = (math.degrees(math.atan2(-u, -v)) + 360.0) % 360.0
    return sp, dr


def build_wind():
    plans, recs = {}, {}
    for d in core.DAYS:
        rng = rng_for("wind", d.isoformat())
        plans[d] = day_plan(d, rng)
        recs[d] = five_minute(d, plans[d], rng)
    return plans, recs


# ----------------------------------------------------------------------------------------------------------------
# odor episodes and complaints (truth; local clock for people, PST for the wind)

def pst_hour_of_local(d, h_local):
    t = dt.datetime(d.year, d.month, d.day, h_local)
    p = core.local_to_pst(t)
    return p.date(), p.hour


def build_odor(H, plans, hourly):
    """Complaint seeds: (household, local noticed datetime, cause). `hourly[(date, pst_hour)]` = (speed, dir)."""
    rng = rng_for("odor")
    seeds = []
    by_t = {}
    for h in H:
        by_t.setdefault(round(h["t"] * 4) / 4, []).append(h)
    freq = [H[i] for i in (412, 1903, 3377, 5120)]
    for d in core.DAYS:
        wk = d.weekday()
        for hl in range(24):
            pd_, ph = pst_hour_of_local(d, hl)
            if pd_ not in plans:
                continue
            reg = plans[pd_]["reg"][ph]
            sp, dr = hourly.get((pd_, ph), (None, None))
            home = HOME[hl]
            if home <= 0:
                continue
            # compost: lingering SW evenings, then the pooled odor in the calm that follows
            fw = d >= core.CHANGES["compost"][0]
            fw2 = d >= dt.date(2026, 6, 1)
            pc = P["compost"] * (1.0 if fw2 else 0.8) if fw else P["compost_pre"]
            if reg == "sw_eve" and ph >= 19 and wk < 6 and rng_for("cep", d.isoformat()).random() < pc and dr is not None:
                for hh in H:
                    if core.angdiff(dr, hh["bear"]["compost"]) <= 22 and hh["dist"]["compost"] < 6.5:
                        lam = P["q_compost"] * home * (1.6 if fw2 else 1.0) * min(1.0, 3.0 / hh["dist"]["compost"])
                        if rng.random() < lam:
                            seeds.append((hh["hid"], d, hl, "compost"))
            if reg in ("calm", "transition") and ph >= 19 and plans[pd_]["linger"] and fw and wk < 6:
                for hh in H:
                    if hh["dist"]["compost"] < 4.6:
                        lam = P["q_compost_calm"] * home * (1.6 if fw2 else 1.0) * min(1.0, 2.6 / hh["dist"]["compost"])
                        if rng.random() < lam:
                            seeds.append((hh["hid"], d, hl, "compost_calm"))
            # landfill: drainage nights, more after cell 7
            if reg == "drain" and dr is not None:
                pl = P["landfill"] * (1.4 if d >= core.CHANGES["landfill"][0] else 1.0)
                if rng_for("lep", d.isoformat(), ph).random() < pl:
                    for hh in H:
                        if core.angdiff(dr, hh["bear"]["landfill"]) <= 20:
                            if rng.random() < P["q_landfill"] * home * min(1.0, 5.0 / hh["dist"]["landfill"]):
                                seeds.append((hh["hid"], d, hl, "landfill"))
            # treatment plant: southerly evenings and calm hours near the plant, more after the drying beds
            if d >= core.CHANGES["wwtp"][0] or rng.random() < 0.3:
                if reg == "south" and dr is not None and rng_for("wep", d.isoformat(), ph).random() < 0.75:
                    for hh in H:
                        if core.angdiff(dr, hh["bear"]["wwtp"]) <= 22 and hh["dist"]["wwtp"] < 3.0:
                            if rng.random() < P["q_wwtp"] * home:
                                seeds.append((hh["hid"], d, hl, "wwtp"))
                if reg == "calm" and rng_for("wcp", d.isoformat(), ph).random() < P["wwtp"]:
                    for hh in H:
                        if hh["dist"]["wwtp"] < 1.1:
                            if rng.random() < P["q_wwtp"] * home:
                                seeds.append((hh["hid"], d, hl, "wwtp_calm"))
            # rendering: north slope flow nights while the second shift cooks
            if reg == "nslope" and dr is not None and d >= core.CHANGES["render"][0]:
                if rng_for("rep", d.isoformat()).random() < P["render"]:
                    for hh in H:
                        if core.angdiff(dr, hh["bear"]["render"]) <= 20:
                            if rng.random() < P["q_render"] * home:
                                seeds.append((hh["hid"], d, hl, "render"))
            # mushroom substrate: east canyon flow nights after the wharf extension
            if reg == "ecanyon" and dr is not None and d >= core.CHANGES["mush"][0]:
                if rng_for("mep", d.isoformat()).random() < P["mush"]:
                    for hh in H:
                        if core.angdiff(dr, hh["bear"]["mush"]) <= 20:
                            if rng.random() < P["q_mush"] * home:
                                seeds.append((hh["hid"], d, hl, "mush"))
            # background: a resident who smells something, any wind
            if rng.random() < P["bg_rate"] * home / 24.0 * (1.0 if d.month >= 5 else 0.45):
                seeds.append((int(rng.integers(len(H))), d, hl, "background"))
        # four residents who report most nights in the season, whatever the wind
        for i, fh in enumerate(freq):
            if rng.random() < P["freq_nights"][i] * (1.0 if d.month >= 5 else 0.35):
                hl = int(rng.choice(P["freq_hours"]))
                seeds.append((fh["hid"], d, hl, "frequent"))
    # eight residents who report now and then, whatever the wind (their own draws, so nothing above moves)
    pick = rng_for("moderate-households")
    mod = []
    while len(mod) < len(P["mod_nights"]):
        i = int(pick.integers(len(H)))
        if i not in (412, 1903, 3377, 5120) and i not in mod:
            mod.append(i)
    for d in core.DAYS:
        r2 = rng_for("moderate", d.isoformat())
        for i, hid in enumerate(mod):
            if r2.random() < P["mod_nights"][i] * (1.0 if d.month >= 5 else 0.35):
                seeds.append((hid, d, int(r2.choice(P["mod_hours"])), "moderate"))
    # an early riser on Alder Street who called once in July
    seeds.append((1203, dt.date(2026, 7, 14), 5, "background"))
    return seeds, [f["hid"] for f in freq]


def hourly_from_recs(recs):
    out = {}
    for d, rr in recs.items():
        for h in range(24):
            hr = [r for r in rr if r[0] // 60 == h]
            vh = vector_hour(hr)
            if vh:
                out[(d, h)] = vh
    return out


def build():
    H = households()
    plans, recs = build_wind()
    hourly = hourly_from_recs(recs)
    seeds, freq = build_odor(H, plans, hourly)
    return dict(H=H, plans=plans, recs=recs, hourly=hourly, seeds=seeds, freq=freq)
