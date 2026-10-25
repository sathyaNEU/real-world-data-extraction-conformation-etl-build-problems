"""The slurry contractors' spring jobs: Countrywide Slurry Services works every region and, in its busy weeks, passes
jobs to the local contractor (Vale Agri in six regions, Basin Agri in the other six), invoicing the farmer at
the service the farmer ordered and at its own two-thousand-gallon load, dated when the local docket reaches it, with
the local docket's number in its reference field. Pig slurry and digestate jobs ride in the exports beside them."""
import datetime as dt
from collections import defaultdict

import world as W

D = dt.date
GAL = 0.00454609                      # cubic metres in an imperial gallon
ARDVALE_REGIONS = ("Northern Vale", "Eastern Vale", "Midland Basin", "Inner Basin", "Lake Uplands", "Western Seaboard")
NORTHMOOR_REGIONS = ("Southern Vale", "Coastal Vale", "Lower Basin", "Middle Uplands", "Eastern Uplands", "Atlantic Coast")
# slurry a head a day while housed, cubic metres
SLURRY = {"dairy_cow": 0.053, "suckler_cow": 0.038, "over24": 0.033, "m12_24": 0.027, "calf": 0.012}
ORDER_LESS = {"D": 0.46, "B": 0.31, "G": 0.21, "W": 0.24}
ARDVALE_TANKERS = [("T1", 2000, "SPLASH PLATE"), ("T2", 2500, "SPLASH PLATE"), ("T3", 2500, "TRAILING SHOE"),
                   ("T4", 3000, "TRAILING SHOE"), ("T5", 2000, "DRIBBLE BAR"), ("T6", 3000, "SPLASH PLATE")]
KB_SERVICES = [("SS-SP", "Cattle slurry, splash plate", "1000 GAL", 13.50),
               ("SS-TS", "Cattle slurry, trailing shoe", "1000 GAL", 17.00),
               ("SS-TH", "Cattle slurry, trailing hose", "1000 GAL", 16.00),
               ("SS-UMB", "Cattle slurry, umbilical system, dribble bar", "1000 GAL", 19.50),
               ("SS-INJ", "Cattle slurry, shallow injection", "1000 GAL", 21.00),
               ("PS-SP", "Pig slurry, splash plate", "1000 GAL", 13.50),
               ("DS-TS", "Digestate, trailing shoe", "1000 GAL", 17.00),
               ("AG-HR", "Tank agitation", "HR", 65.00)]
KB_RATE = {c: p for c, _, _, p in KB_SERVICES}
LESS_KB = {"SS-TS", "SS-TH", "SS-UMB", "SS-INJ"}
LESS_AV = {"TRAILING SHOE", "DRIBBLE BAR"}
VAT = 0.135


def housed_slurry(w, IV):
    """each farm herd's slurry from the cattle it housed between 1 November 2025 and mid-May"""
    A = w.A
    out = defaultdict(float)
    for a, iv in IV.items():
        for h, s, e in iv:
            hd = w.herds[h]
            if hd["type"] not in ("dairy", "suckler", "finisher", "rearer"):
                continue
            r = hd["region"]
            for s2, e2 in W.splits(A, a, s, e):
                end = min(e2, W.di(D(2026, 5, 15)))
                if end <= s2:
                    continue
                n = W.CUMH[r][end] - W.CUMH[r][s2]
                out[h] += n * SLURRY[W.category(A, a, s2)]
    return out


def jobs(w, IV, rng):
    slurry = housed_slurry(w, IV)
    herds = w.herds
    lo, hi = W.di(W.WIN0), W.di(W.WIN1)
    busy0, busy1 = W.di(D(2026, 2, 9)), W.di(D(2026, 3, 27))
    av, kb, nm = [], [], []

    def jday(peak):
        while True:
            d = int(rng.normal(peak, 26))
            if lo <= d <= hi + 18:
                return d

    def av_job(herd_no, d, vol, material="CATTLE SLURRY", less=None):
        cands = [t for t in ARDVALE_TANKERS if (t[2] in LESS_AV) == less] if less is not None else ARDVALE_TANKERS
        tk = cands[int(rng.integers(0, len(cands)))]
        loads = max(1, int(round(vol / (tk[1] * GAL))))
        av.append(dict(key=len(av), date=d, herd=herd_no, material=material, tanker=tk[0], gal=tk[1],
                       equipment=tk[2], loads=loads))
        return av[-1]

    def nm_job(herd_no, d, vol, material="Cattle slurry", site=""):
        method = "Trailing shoe" if rng.random() < 0.7 else "Dribble bar"
        nm.append(dict(key=len(nm), date=d, herd=herd_no, site=site, method=method,
                       m3=round(vol * rng.uniform(0.97, 1.03), 1), material=material,
                       operator="D%02d" % int(rng.integers(1, 9))))
        return nm[-1]

    def kb_job(herd_no, d_inv, service, qty, ref, acct, agit=None):
        kb.append(dict(key=len(kb), date=d_inv, acct=acct, herd=herd_no, service=service, qty=qty, ref=ref,
                       agit=agit))
        return kb[-1]

    accts = {}
    for h in herds:
        if h["type"] not in ("dairy", "suckler", "finisher", "rearer") or "out_farm_of" in h:
            continue
        vol_total = slurry.get(h["id"], 0.0) * rng.uniform(0.85, 1.0)
        if vol_total < 40 or rng.random() < 0.38:
            continue                                   # spreads its own slurry
        r = h["region"]
        local = "av" if r in ARDVALE_REGIONS else "nm"
        u = rng.random()
        users = ["kb"] if u < 0.45 else ([local] if u < 0.82 else ["kb", local])
        accts.setdefault(h["id"], "%05d" % int(rng.integers(10000, 99999)))
        p_less = ORDER_LESS[W.RTYPE[r]]
        own_days = []
        twin = len(users) == 2 and rng.random() < 0.6
        for who in users:
            share = vol_total / len(users)
            njobs = max(1, int(round(share / rng.uniform(110, 260))))
            peak = int(rng.normal(W.di(D(2026, 3, 1)), 14))
            for k in range(njobs):
                d = jday(peak)
                if who != "kb" and twin and k == 0 and own_days:
                    d = own_days[int(rng.integers(0, len(own_days)))]     # both contractors on the farm that day
                vol = share / njobs * rng.uniform(0.7, 1.3)
                less = rng.random() < p_less
                if who == "kb":
                    service = str(rng.choice(["SS-TS", "SS-TH", "SS-UMB", "SS-INJ"], p=[0.55, 0.2, 0.15, 0.1])) if less else "SS-SP"
                    if busy0 <= d <= busy1 and rng.random() < 0.32:
                        # passed to the local contractor: its sheet is the job; Countrywide's line bills it
                        if local == "av":
                            j = av_job(h["herd_no"], d, vol, less=(True if less else bool(rng.random() < 0.35)))
                            loads = j["loads"]
                        else:
                            j = nm_job(h["herd_no"], d, vol)
                            loads = max(1, int(-(-j["m3"] // (2000 * GAL))))
                        kb_job(h["herd_no"], d + int(rng.integers(3, 11)), service, 2.0 * loads, (local, j["key"]),
                               accts[h["id"]])
                    else:
                        loads = max(1, int(round(vol / (2000 * GAL))))
                        agit = round(float(rng.uniform(1.0, 3.5)) * 2) / 2 if rng.random() < 0.15 else None
                        kb_job(h["herd_no"], d, service, 2.0 * loads, ("kb", None), accts[h["id"]], agit)
                        if lo <= d <= hi:
                            own_days.append(d)
                elif who == "av":
                    av_job(h["herd_no"], d, vol, less=less)
                else:
                    nm_job(h["herd_no"], d, vol)
    # pig slurry for the pig units (Vale Agri), digestate (Countrywide to farms, Basin Agri at the digester's sites)
    pig_units = ["P%d%06d" % (int(rng.integers(1, 8)), int(rng.integers(0, 1000000))) for _ in range(14)]
    for k in range(60):
        av_job(pig_units[k % len(pig_units)], jday(W.di(D(2026, 3, 5))), rng.uniform(60, 220), material="PIG SLURRY")
    farms = [h for h in herds if h["type"] in ("dairy", "suckler") and "out_farm_of" not in h]
    for k in range(70):
        h = farms[int(rng.integers(0, len(farms)))]
        accts.setdefault(h["id"], "%05d" % int(rng.integers(10000, 99999)))
        kb_job(h["herd_no"], jday(W.di(D(2026, 3, 20))), "DS-TS", 2.0 * int(rng.integers(3, 14)), ("kb", None),
               accts[h["id"]])
    sites = ["AD01", "AD02", "AD03"]
    for k in range(25):
        nm_job("", jday(W.di(D(2026, 3, 10))), rng.uniform(80, 240), material="Digestate", site=sites[k % 3])
    return finalise(dict(av=av, kb=kb, nm=nm, pig_units=pig_units), rng)


def finalise(cj, rng):
    """job and invoice numbers run in date order in each contractor's system; Countrywide's reference field carries its
    own docket number, or the local contractor's job number for a job it passed on"""
    num = {}
    seq = 3104
    for j in sorted(cj["av"], key=lambda j: (j["date"], j["key"])):
        seq += int(rng.integers(1, 4))
        j["job_id"] = "%05d" % seq
        num[("av", j["key"])] = j["job_id"]
    seq = 411
    for j in sorted(cj["nm"], key=lambda j: (j["date"], j["key"])):
        seq += int(rng.integers(1, 3))
        j["job_no"] = "BA26-%04d" % seq
        num[("nm", j["key"])] = j["job_no"]
    inv, dock = 24113, 88104
    for l in sorted(cj["kb"], key=lambda l: (l["date"], l["key"])):
        inv += int(rng.integers(1, 3))
        l["invoice"] = "SI%06d" % inv
        if l["ref"][0] == "kb":
            dock += int(rng.integers(1, 4))
            l["ref"] = "CW%d" % dock
        else:
            l["ref"] = num[l["ref"]]
    return cj


def golden(cj, herd_region):
    """each region's cattle slurry spread on its farms in the window, each job once (Countrywide's lines for a local
    contractor's docket left out, that docket kept), cubic metres, and its low-emission share"""
    lo, hi = W.di(W.WIN0), W.di(W.WIN1)
    vol, less = defaultdict(float), defaultdict(float)
    passed = {l["ref"] for l in cj["kb"] if not l["ref"].startswith("CW")}
    for j in cj["av"]:
        if j["material"] != "CATTLE SLURRY" or not (lo <= j["date"] <= hi) or j["herd"] not in herd_region:
            continue
        v = j["loads"] * j["gal"] * GAL
        r = herd_region[j["herd"]]
        vol[r] += v
        less[r] += v if j["equipment"] in LESS_AV else 0
    for j in cj["nm"]:
        if j["material"] != "Cattle slurry" or not (lo <= j["date"] <= hi) or j["herd"] not in herd_region:
            continue
        r = herd_region[j["herd"]]
        vol[r] += j["m3"]
        less[r] += j["m3"]
    for l in cj["kb"]:
        if l["ref"] in passed or not l["service"].startswith("SS-") or not (lo <= l["date"] <= hi):
            continue
        v = l["qty"] * 1000 * GAL
        r = herd_region[l["herd"]]
        vol[r] += v
        less[r] += v if l["service"] in LESS_KB else 0
    return {r: (vol[r], 100.0 * less[r] / vol[r]) for r in vol}
