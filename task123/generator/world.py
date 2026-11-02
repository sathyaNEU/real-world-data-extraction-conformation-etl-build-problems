"""Architecture 4 world: an owners corporation's apartment risers, the phase each single-phase supply is
wired to (recorded nowhere), the embedded network's July 2026 half-hourly demand and hourly voltage, and the
approved 2027 electrification loads.  Everything is drawn from one fixed seed."""
import numpy as np
from datetime import date, datetime, timedelta

SEED = 30079
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
        r["z_riser"] = float(rng.uniform(0.075, 0.115))
    # wiring styles by riser: the 2004 installer rotated phases on most floors, but some contractors wired
    # pairs of neighbouring apartments to one phase, and the 2015 board replacements re-landed some circuits
    styles = ["rotation", "pairs", "pairs_shift", "rotation_floor", "mixed"]
    apts = []
    lot = 0
    r3 = np.random.default_rng(seed + 9)
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
                three = (r["tower"] in "AC" and fl == TOWERS[r["tower"]] and pos in (1, 6)) or \
                        (pos in (1, 2) and r3.random() < 0.075)
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
            x *= 2.2 if a["floor"] == TOWERS[a["tower"]] else 1.4
        load[i] = np.clip(x * rng.lognormal(0, 0.07, T), 0.02, None)
    # off-peak electric storage hot water on the controlled-load register (E2), 23:00 to 07:00 market time
    rcl = np.random.default_rng(seed + 5)
    cl = np.zeros((n, T))
    has_cl = np.array([rcl.random() < 0.62 for _ in apts])
    night = (hh >= 46) | (hh < 14)
    for i in range(n):
        if has_cl[i]:
            daily = rcl.uniform(3.2, 8.5) * scale[apts[i]["type"]]
            for d in range(JULY_DAYS):
                st = int(rcl.integers(0, 4))
                blk = [(d * 48 + k) % T for k in list(range(46, 48)) + list(range(0, 14))]
                w = rcl.dirichlet(np.ones(len(blk) - st) * 2.0)
                for k, wt in zip(blk[st:], w):
                    cl[i, k] += daily * rcl.uniform(0.9, 1.1) * wt * 2.0
    # approved 2027 additions: owners of the larger apartments apply for chargers more often
    p_ev = {"3B": 0.26, "2B": 0.12, "1B": 0.05}
    ev = np.array([rng.random() < p_ev[a["type"]] for a in apts])
    cook = np.array([rng.random() < 0.38 for a in apts])
    return {"plan": plan, "apts": apts, "load": load, "cl": cl, "has_cl": has_cl, "ev": ev, "cook": cook, "hh": hh, "dow": dow, "rng": rng}

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


# ---------------------------------------------------------------------------------------------------------------
# Identifiers, the five-minute voltage record, meter exchanges, collection gaps, register reads, requests.

def nmi_checksum(nmi):
    """AEMO NMI checksum (the Luhn variant over character codes)."""
    v = 0
    multiply = True
    for ch in reversed(nmi):
        d = ord(ch)
        if multiply:
            d *= 2
        multiply = not multiply
        while d > 0:
            v += d % 10
            d //= 10
    return (10 - (v % 10)) % 10

def identifiers(W, seed=SEED + 11):
    rng = np.random.default_rng(seed)
    apts = W["apts"]
    used = set()
    for a in apts:
        while True:
            body = "VBFF%06d" % int(rng.integers(100000, 999999))
            if body not in used:
                used.add(body)
                break
        a["nmi"] = body + str(nmi_checksum(body))
        a["serial"] = "QL2%07d" % int(rng.integers(1000000, 9999999))
        a["module"] = "CM%06X" % int(rng.integers(0x100000, 0xFFFFFF))
    # 2004 distribution-board labels the meter register still uses
    for a in apts:
        side = "E" if a["pos"] <= 3 else "W"
        a["board_2004"] = "T%s-DB%02d%s" % (a["tower"], a["floor"], side)
    return W

def five_minute_voltage(W, seed=SEED + 21):
    """Five-minute voltages for July at every child meter.  The half-hourly physics (supply, building, riser and
    service drops) is held over each half-hour; the distributor's night tap moves and short swells ride on top."""
    rng = np.random.default_rng(seed)
    plan, apts, load = W["plan"], W["apts"], W["load"]
    T = load.shape[1]
    hh = W["hh"]
    vsup = 250.3 + 2.1 * np.cos(2 * np.pi * (hh - 8) / 48) + np.cumsum(rng.normal(0, 0.03, T))
    vsup -= (vsup.mean() - 250.3)
    # network swells, five-minute resolution, building wide
    T5 = T * 6
    swell = np.zeros(T5)
    for d in range(JULY_DAYS):
        for _ in range(int(rng.integers(0, 3))):
            st = d * 288 + int(rng.integers(0, 84))          # midnight to 07:00 local
            du = int(rng.integers(3, 16))
            swell[st:st + du] += rng.uniform(2.6, 5.0)
        if rng.random() < 0.25:
            st = d * 288 + int(rng.integers(120, 200))
            du = int(rng.integers(2, 7))
            swell[st:st + du] += rng.uniform(1.5, 3.5)
    rix = {r["riser"]: r for r in plan}
    cur = {}
    bph = np.zeros((3, T))
    for r in plan:
        I = np.zeros((3, T))
        for i, a in enumerate(apts):
            if a["riser"] != r["riser"]:
                continue
            amps = (load[i] + W["cl"][i]) * 1000 / VNOM
            if a["three_phase"]:
                I += amps / 3
            else:
                I[a["phase"]] += amps
        cur[r["riser"]] = I
        bph += I
    vb = np.array([vsup - 0.0011 * bph[p] for p in range(3)])
    V5 = np.zeros((len(apts), T5), dtype=np.float32)
    zu_all = []
    for i, a in enumerate(apts):
        r = rix[a["riser"]]
        I = cur[a["riser"]]
        zu = rng.uniform(0.02, 0.09) + 0.004 * (a["floor"] - r["floors"][0])
        zu_all.append(zu)
        own = (load[i] + W["cl"][i]) * 1000 / VNOM
        if a["three_phase"]:
            elems = np.array([vb[p] - r["z_riser"] * I[p] - zu * own / 3 for p in range(3)])
            base = elems.mean(0)
            W.setdefault("V5_3ph", {})[i] = elems
        else:
            p = a["phase"]
            base = vb[p] - r["z_riser"] * I[p] - zu * own
        x = np.repeat(base, 6) + swell
        ar = np.zeros(T5)
        e = rng.normal(0, 0.10, T5)
        for k in range(1, T5):
            ar[k] = 0.6 * ar[k - 1] + e[k]
        lift = 0.6 * (1 - 0.004 * (a["floor"] - 2))
        V5[i] = (x + ar + lift).astype(np.float32)
        if a["three_phase"]:
            el = W["V5_3ph"][i]
            W["V5_3ph"][i] = np.array([(np.repeat(el[p], 6) + swell + ar + lift + rng.normal(0, 0.05, T5)) for p in range(3)], dtype=np.float32)
    W["V5"] = V5
    return W

def exchanges_and_gaps(W, seed=SEED + 31):
    """Meter exchanges in the first ten days of July, two concentrator outages late in the month, and the
    distributor-substituted (estimated) days the embedded network operator fills itself."""
    rng = np.random.default_rng(seed)
    apts = W["apts"]
    n = len(apts)
    ex = []
    pick = rng.choice(n, size=21, replace=False)
    for i in sorted(pick):
        day = int(rng.integers(2, 11))                     # 2 to 10 July
        hhx = int(rng.integers(18, 30))                    # 09:00 to 14:30
        newser = "QL3%07d" % int(rng.integers(1000000, 9999999))
        ex.append({"i": int(i), "day": day, "hh": hhx, "old_serial": apts[i]["serial"], "new_serial": newser})
        apts[i]["old_serial"] = apts[i]["serial"]
        apts[i]["serial"] = newser
        apts[i]["exchange"] = (day, hhx)
    W["exchanges"] = ex
    # concentrator outages: whole floors lose collection from 21 July to the month's end at the extract
    gaps = []
    zones = [("B", 9, 12), ("C", 18, 21), ("A", 14, 16)]
    for tw, f0, f1 in zones:
        start = int(rng.integers(20, 24))
        for i, a in enumerate(apts):
            if a["tower"] == tw and f0 <= a["floor"] <= f1:
                gaps.append((i, start))
    W["gaps"] = gaps
    # estimated (substituted) days: never inside 13 to 17 July
    est = []
    for i in range(n):
        if rng.random() < 0.10:
            for d in rng.choice([x for x in range(1, 32) if x not in (13, 14, 15, 16, 17)], size=int(rng.integers(2, 4)), replace=False):
                est.append((i, int(d)))
    W["estimated"] = est
    return W

def register_reads(W, seed=SEED + 41):
    rng = np.random.default_rng(seed)
    apts, load = W["apts"], W["load"]
    for i, a in enumerate(apts):
        if W["has_cl"][i]:
            x2 = W["cl"][i] * 0.5
            if "exchange" in a:
                d, h = a["exchange"]
                cut = (d - 1) * 48 + h
                o0 = float(rng.uniform(900, 21000))
                a["reads_e2"] = {"old_jul": round(o0, 2), "old_final": round(o0 + x2[:cut].sum(), 2),
                                 "new_initial": 0.0, "new_aug": round(x2[cut:].sum(), 2)}
            else:
                r0 = float(rng.uniform(900, 24000))
                a["reads_e2"] = {"jul": round(r0, 2), "aug": round(r0 + x2.sum(), 2)}
            a["july_kwh_e2_true"] = float(x2.sum())
    gapset = {i for i, _ in W["gaps"]}
    estset = {i for i, _ in W["estimated"]}
    rq = np.random.default_rng(seed + 3)
    for i, a in enumerate(apts):
        a["aug_estimated"] = bool(i not in gapset and i not in estset and "exchange" not in a and rq.random() < 0.10)
    for i, a in enumerate(apts):
        kwh_half = load[i] * 0.5
        if "exchange" in a:
            d, h = a["exchange"]
            cut = (d - 1) * 48 + h
            old0 = float(rng.uniform(4000, 61000))
            old_final = old0 + kwh_half[:cut].sum()
            new0 = round(float(rng.uniform(0.2, 1.4)), 2)
            new1 = new0 + kwh_half[cut:].sum()
            a["reads"] = {"old_jul": round(old0, 2), "old_final": round(old_final, 2),
                          "new_initial": new0, "new_aug": round(new1, 2)}
        else:
            r0 = float(rng.uniform(3000, 72000))
            a["reads"] = {"jul": round(r0, 2), "aug": round(r0 + kwh_half.sum(), 2)}
            if a["aug_estimated"]:
                # the head-end could not reach the meter at midnight on 1 August and estimated the read from the
                # meter's average daily use over the previous quarter
                a["reads"]["aug"] = round(r0 + kwh_half.sum() * rq.uniform(0.82, 1.18), 2)
                if "reads_e2" in a:
                    e2 = a["reads_e2"]
                    e2["aug"] = round(e2["jul"] + (e2["aug"] - e2["jul"]) * rq.uniform(0.85, 1.15), 2)
        a["july_kwh_true"] = float(kwh_half.sum()) + a.get("july_kwh_e2_true", 0.0)
    return W

CARPARK = {"B1": 96, "B2": 142, "B3": 150}

def car_spaces(W, seed=SEED + 51):
    """Accessory car spaces, the 2025 re-marking of the second basement and the charger requests."""
    rng = np.random.default_rng(seed)
    apts = W["apts"]
    spaces = []
    for lvl, nmax in CARPARK.items():
        for k in range(1, nmax + 1):
            spaces.append("%s-%03d" % (lvl, k))
    order = rng.permutation(len(spaces))
    spaces = [spaces[k] for k in order]
    s = 0
    for a in apts:
        ncs = 2 if a["type"] == "3B" and rng.random() < 0.55 else (1 if a["type"] != "1B" or rng.random() < 0.6 else 0)
        a["spaces"] = spaces[s:s + ncs]
        s += ncs
    # the March 2025 re-marking renumbered B2 and B3 (EV bays laid out along the north walls)
    remark = {}
    for lvl in ("B2", "B3"):
        bl = sorted([sp for sp in spaces if sp.startswith(lvl + "-")])
        newnums = rng.permutation(np.arange(1, len(bl) + 1))
        remark.update({old: "%s-%03d" % (lvl, int(nn)) for old, nn in zip(bl, newnums)})
    # the register and the lot schedule carry the new B2 numbers
    for a in apts:
        a["spaces"] = [remark.get(sp, sp) for sp in a["spaces"]]
    W["remark"] = remark                       # old -> new
    W["remark_inv"] = {v: k for k, v in remark.items()}
    return W

def requests(W, seed=SEED + 61):
    """Owners' charger requests since the 2024 by-law.  The approved set is the works schedule's chargers;
    other requests were declined, lapsed or are pending; some were re-lodged after a lapse or decline."""
    rng = np.random.default_rng(seed)
    apts = W["apts"]
    ev = W["ev"]
    apps = []
    reqs = []
    nonres = set()
    for i, a in enumerate(apts):
        if not a["spaces"]:
            continue
        if ev[i]:
            outcome = "approved"
        elif rng.random() < 0.13:
            outcome = str(rng.choice(["declined", "lapsed", "pending"], p=[0.35, 0.35, 0.30]))
        else:
            continue
        sp = a["spaces"][0]
        investor = rng.random() < 0.16
        if investor:
            nonres.add(i)
        reqs.append({"i": i, "space": sp, "outcome": outcome, "investor": investor})
    # re-lodgements: some approved or pending requests went in first before the 2025 re-marking and lapsed
    for q in reqs:
        q["relodged"] = bool(rng.random() < 0.30 and q["outcome"] in ("approved", "pending", "declined"))
    W["requests"] = reqs
    W["nonres"] = nonres
    return W

def tune_july_edges(W):
    """The controlled-load hot water is a free quantity of the world: where a riser's July use would sit within
    0.4 kWh of a rounding edge at two decimals of a MWh, one off-peak apartment's heater runs a little longer,
    moving the riser to the middle of its bin.  The register is zero in the call's evening window."""
    apts = W["apts"]
    for r in W["plan"]:
        idx = [i for i, a in enumerate(apts) if a["riser"] == r["riser"]]
        tot = sum((W["load"][i].sum() + W["cl"][i].sum()) * 0.5 for i in idx) / 1000.0
        e = 0.005 - abs(tot - round(tot, 2))
        if e >= 0.0004:
            continue
        cand = [i for i in idx if W["has_cl"][i]]
        if not cand:
            continue
        i = cand[0]
        lo = np.floor(tot * 100) / 100
        target = lo + 0.0025 if tot - lo < 0.005 else lo + 0.0075
        need = (target - tot) * 1000.0
        cur = W["cl"][i].sum() * 0.5
        W["cl"][i] = W["cl"][i] * (1 + need / cur)
    return W


def build_all(seed=SEED):
    W = build(seed)
    W = tune_july_edges(W)
    W = identifiers(W)
    W = five_minute_voltage(W)
    W = exchanges_and_gaps(W)
    W = register_reads(W)
    W = car_spaces(W)
    W = requests(W)
    return W
