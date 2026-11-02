"""Architecture 4 world: an owners corporation's apartment risers, the phase each single-phase supply is
wired to (recorded nowhere), the embedded network's July 2026 half-hourly demand and hourly voltage, and the
approved 2027 electrification loads.  Everything is drawn from one fixed seed."""
import numpy as np
from datetime import date, datetime, timedelta

SEED = 1230411
VNOM = 230.0
LIMIT_SHARE = 0.80          # the standard's share of a rising main's per-phase rating
EV_KW = 3.7                 # the standard's evening after-diversity demand of an approved charger
COOK_KW = 1.4               # the standard's evening after-diversity demand of a cooktop conversion
JULY_DAYS = 31
PEAK_WEEK = [date(2026, 7, 13) + timedelta(days=d) for d in range(5)]      # Monday 13 to Friday 17 July
PQ_START_UTC = datetime(2026, 7, 12, 0, 0)                                  # the PQ export runs 12 to 20 July UTC
PQ_HOURS = 192

TOWERS = {"A": 25, "B": 23, "C": 25}       # top floor; apartments start on floor 2, six to a floor
UNIT_TYPE = {1: "3B", 2: "3B", 3: "2B", 4: "2B", 5: "1B", 6: "1B"}

def riser_plan():
    """Each riser serves a run of floors in one tower.  Labels are the 2019 ones; the 2004 labels used by the
    meter register are kept beside them."""
    plan = []
    for tw, top in TOWERS.items():
        floors = list(range(2, top + 1))
        k = 0
        n_r = 6
        sizes = [4] * n_r
        if tw == "B":
            sizes = [4, 4, 4, 4, 3, 3]
        for i, s in enumerate(sizes):
            fl = floors[k:k + s]
            k += s
            plan.append({"riser": f"{tw}{i + 1}", "tower": tw, "floors": fl})
    return plan

def build(seed=SEED):
    rng = np.random.default_rng(seed)
    plan = riser_plan()
    # rising main ratings per phase (A); a few lighter mains on the low risers that also feed the podium
    rating_choices = [160, 200, 250, 315]
    for r in plan:
        r["rating_a"] = int(rng.choice(rating_choices, p=[0.10, 0.40, 0.35, 0.15]))
        r["z_riser"] = float(rng.uniform(0.045, 0.085))
    # wiring styles by riser: the 2004 installer rotated phases on most floors, but some contractors wired
    # pairs of neighbouring apartments to one phase, and the 2015 board replacements re-landed some circuits
    styles = ["rotation", "pairs", "pairs_shift", "rotation_floor", "mixed"]
    apts = []
    lot = 0
    for r in plan:
        style = rng.choice(styles, p=[0.30, 0.25, 0.15, 0.15, 0.15])
        r["style"] = str(style)
        shift = int(rng.integers(0, 3))
        for fl in r["floors"]:
            for pos in range(1, 7):
                lot += 1
                k = pos - 1
                if style == "rotation":
                    ph = (k + shift) % 3
                elif style == "pairs":
                    ph = (k // 2 + shift) % 3
                elif style == "pairs_shift":
                    ph = (k // 2 + shift + fl) % 3
                elif style == "rotation_floor":
                    ph = (k + shift + fl) % 3
                else:
                    ph = ((k // 2) if fl % 2 == 0 else k) % 3
                    ph = (ph + shift) % 3
                if rng.random() < 0.08:
                    ph = int(rng.integers(0, 3))
                three = (r["tower"] in "AC" and fl == TOWERS[r["tower"]] and pos in (1, 6))
                apts.append({"lot": lot, "apt": f"{r['tower']}-{fl:02d}{pos:02d}", "riser": r["riser"],
                             "tower": r["tower"], "floor": fl, "pos": pos, "type": UNIT_TYPE[pos],
                             "phase": -1 if three else ph, "three_phase": bool(three)})
    n = len(apts)
    T = JULY_DAYS * 48
    hh = np.arange(T) % 48
    dow = np.array([(date(2026, 7, 1) + timedelta(days=int(d))).weekday() for d in np.arange(T) // 48])
    scale = {"3B": 1.35, "2B": 1.0, "1B": 0.72}
    load = np.zeros((n, T))
    ev_now = rng.random(n) < 0.05
    for i, a in enumerate(apts):
        s = scale[a["type"]] * rng.uniform(0.8, 1.25)
        x = np.full(T, rng.uniform(0.10, 0.30) * s)
        occ_evening = rng.uniform(0.6, 0.95)
        for d in range(JULY_DAYS):
            o = d * 48
            if rng.random() < occ_evening:          # heating block, evening
                st = o + int(rng.integers(33, 37)); du = int(rng.integers(5, 11))
                x[st:st + du] += rng.uniform(0.8, 1.9) * s
            if rng.random() < 0.75:                 # cooking
                st = o + int(rng.integers(34, 39)); du = int(rng.integers(1, 3))
                x[st:st + du] += rng.uniform(1.0, 2.4) * s
            if rng.random() < 0.65:                 # morning
                st = o + int(rng.integers(12, 17)); du = int(rng.integers(1, 3))
                x[st:st + du] += rng.uniform(0.4, 1.3) * s
            if rng.random() < 0.35:                 # an appliance at some other hour
                st = o + int(rng.integers(0, 46)); du = int(rng.integers(1, 3))
                x[st:st + du] += rng.uniform(0.5, 1.8)
            if ev_now[i] and rng.random() < 0.45:   # an EV already charging off a power point
                st = o + int(rng.integers(36, 44)); du = int(rng.integers(4, 9))
                x[st:st + du] += 2.3
        if a["three_phase"]:
            x *= 2.2
        load[i] = np.clip(x * rng.lognormal(0, 0.07, T), 0.02, None)
    # approved 2027 additions: owners of the larger apartments apply for chargers more often
    p_ev = {"3B": 0.26, "2B": 0.12, "1B": 0.05}
    ev = np.array([rng.random() < p_ev[a["type"]] for a in apts])
    cook = np.array([rng.random() < 0.38 for a in apts])
    return {"plan": plan, "apts": apts, "load": load, "ev": ev, "cook": cook, "hh": hh, "dow": dow, "rng": rng}

def voltages(W, seed=SEED + 7):
    """Half-hourly voltage at every child meter, then the hourly averages the PQ export carries."""
    rng = np.random.default_rng(seed)
    plan, apts, load = W["plan"], W["apts"], W["load"]
    T = load.shape[1]
    hh = W["hh"]
    vsup = 249.2 + 2.2 * np.cos(2 * np.pi * (hh - 8) / 48) + np.cumsum(rng.normal(0, 0.03, T))
    vsup -= (vsup.mean() - 249.2)
    rix = {r["riser"]: r for r in plan}
    # phase currents per riser and building
    cur = {}
    bph = np.zeros((3, T))
    for r in plan:
        idx = [i for i, a in enumerate(apts) if a["riser"] == r["riser"]]
        I = np.zeros((3, T))
        for i in idx:
            a = apts[i]
            amps = load[i] * 1000 / VNOM
            if a["three_phase"]:
                I += amps / 3
            else:
                I[a["phase"]] += amps
        cur[r["riser"]] = I
        bph += I
    vb = np.array([vsup - 0.0011 * bph[p] for p in range(3)])
    V = np.zeros((len(apts), T))
    for i, a in enumerate(apts):
        r = rix[a["riser"]]
        I = cur[a["riser"]]
        zu = rng.uniform(0.02, 0.09) + 0.004 * (a["floor"] - r["floors"][0])
        own = load[i] * 1000 / VNOM
        if a["three_phase"]:
            vr = np.mean([vb[p] - r["z_riser"] * I[p] for p in range(3)], axis=0)
            V[i] = vr - zu * own / 3 + rng.normal(0, 0.08, T)
        else:
            p = a["phase"]
            V[i] = vb[p] - r["z_riser"] * I[p] - zu * own + rng.normal(0, 0.08, T)
    return V
