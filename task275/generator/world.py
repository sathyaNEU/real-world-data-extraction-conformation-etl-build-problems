"""The world before any file is written: the producer organisation's member vessels, their 2025 trips, each haul's
catch split into what is marketable, what is a quota species below its minimum size (BMS) and what may be returned
lawfully, the observer scheme's draws, and what each trip landed.

Under the discard ban a vessel lands its BMS when an observer is aboard and fishes less on the inshore grounds; on a
trip nobody observes it throws the BMS back, except the few vessels that land it every trip. Catch per hour on a
ground does not depend on whether an observer is aboard."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# per segment: vessels, trips a vessel a year, trip days, hauls a day, haul hours, marketable kg an hour,
# marketable mix, legal discard fraction of catch and its mix, BMS fraction of quota catch offshore, nursery
# multiplier, ground weights (WC11..WC15), observed trips' cut on the inshore grounds, share of vessels that land BMS
# on every trip, observer draw probability
SPEC = {
    "TR1": dict(nv=(11, 14), trips=(34, 44), days=(3, 6), hpd=(4, 5), hh=(3.2, 0.5), rate=170,
                mix={"HAD": .25, "WHG": .15, "COD": .10, "HKE": .15, "MON": .10, "MEG": .08, "PLE": .07, "LEM": .05,
                     "POK": .05}, legal=.035, lmix={"DAB": .4, "GUR": .35, "SYC": .25}, bms=.110, nmult=2.0,
                gw=(.40, .25, .35, .0, .0), avoid=.45, comply=.05, draw=.085),
    "TR2": dict(nv=(14, 17), trips=(95, 125), days=(1, 2), hpd=(3, 4), hh=(3.0, 0.5), rate=95,
                mix={"HAD": .25, "WHG": .25, "COD": .10, "PLE": .15, "LEM": .10, "MON": .10, "SOL": .05},
                legal=.037, lmix={"DAB": .5, "GUR": .3, "SYC": .2}, bms=.075, nmult=2.5,
                gw=(.25, .35, .22, .0, .18), avoid=.40, comply=.05, draw=.085),
    "NEP": dict(nv=(13, 16), trips=(105, 135), days=(1, 2), hpd=(3, 4), hh=(4.2, 0.6), rate=42,
                mix={"NEP": .70, "WHG": .10, "HAD": .08, "MON": .07, "COD": .05}, legal=.110,
                lmix={"NEP": .55, "DAB": .25, "GUR": .2}, bms=.025, nmult=2.0,
                gw=(.0, .25, .45, .0, .30), avoid=.30, comply=.05, draw=.085),
    "BT": dict(nv=(11, 13), trips=(55, 66), days=(2, 4), hpd=(8, 10), hh=(1.8, 0.3), rate=75,
               mix={"PLE": .35, "SOL": .30, "MON": .12, "LEM": .10, "MEG": .08, "COD": .05}, legal=.025,
               lmix={"DAB": .6, "GUR": .25, "SYC": .15}, bms=.010, nmult=14.0,
               gw=(.0, .30, .0, .35, .35), avoid=.75, comply=.00, draw=.110),
    "SN": dict(nv=(9, 11), trips=(120, 145), days=(1, 1), hpd=(4, 6), hh=(2.4, 0.4), rate=120,
               mix={"PLE": .30, "HAD": .30, "COD": .15, "WHG": .15, "LEM": .10}, legal=.030,
               lmix={"DAB": .6, "GUR": .4}, bms=.045, nmult=2.0,
               gw=(.35, .45, .0, .20, .0), avoid=.30, comply=.05, draw=.085),
    "GN": dict(nv=(15, 18), trips=(120, 150), days=(1, 1), hpd=(1, 1), hh=(8.0, 1.2), rate=26,
               mix={"HKE": .40, "POL": .20, "SOL": .15, "COD": .10, "LIN": .15}, legal=.043,
               lmix={"SYC": .6, "GUR": .4}, bms=.065, nmult=1.3,
               gw=(.25, .40, .0, .17, .18), avoid=.10, comply=.60, draw=.085),
    "LL": dict(nv=(9, 11), trips=(100, 130), days=(1, 1), hpd=(1, 1), hh=(10.0, 1.5), rate=22,
               mix={"HKE": .35, "LIN": .30, "POL": .20, "COD": .15}, legal=.025,
               lmix={"SYC": .8, "GUR": .2}, bms=.025, nmult=1.2,
               gw=(.35, .35, .30, .0, .0), avoid=.10, comply=.10, draw=.085),
    "POT": dict(nv=(16, 19), trips=(150, 185), days=(1, 1), hpd=(1, 1), hh=(7.0, 1.0), rate=30,
                mix={"CRE": .60, "LBE": .15, "WHE": .25}, legal=.060, lmix={"CRE": .7, "LBE": .3}, bms=.0,
                nmult=1.0, gw=(.0, .35, .0, .35, .30), avoid=.0, comply=.0, draw=.085),
}
NURSERY_IDX = (3, 4)
AVAIL = 0.80          # a drawn trip gets an observer when one is free
SAMPLE_HAUL = 0.75    # kept for the seed's random stream only
START = dt.date(K.YEAR, 1, 1)


def season_weight(d):
    """more fishing days in spring and summer, fewer in the winter gales"""
    m = d.month
    return {1: .55, 2: .6, 3: .85, 4: 1.0, 5: 1.1, 6: 1.15, 7: 1.15, 8: 1.1, 9: 1.0, 10: .9, 11: .7, 12: .5}[m]


def vessels(r):
    out = []
    num = 100
    for s, _, gear, lc, towed in K.SEGMENTS:
        p = SPEC[s]
        nv = int(r.integers(p["nv"][0], p["nv"][1] + 1))
        comply = r.random(nv) < p["comply"]
        for i in range(nv):
            num += int(r.integers(1, 9))
            port = K.PORTS[int(r.integers(0, len(K.PORTS)))]
            length = {"TR1": r.uniform(18.2, 26), "TR2": r.uniform(12.1, 17.8), "NEP": r.uniform(12.5, 19),
                      "BT": r.uniform(14, 24), "SN": r.uniform(14, 22), "GN": r.uniform(10.2, 14.8),
                      "LL": r.uniform(10.5, 15.5), "POT": r.uniform(10.1, 13.9)}[s]
            out.append(dict(seg=s, idx=len(out), port=port, length=round(length, 2), comply=bool(comply[i]),
                            num=num, trips_target=int(r.integers(p["trips"][0], p["trips"][1] + 1))))
    return out


def trips_of(r, v):
    """a vessel's trips through the year: departure days drawn against the season, no overlap"""
    p = SPEC[v["seg"]]
    days = np.array([START + dt.timedelta(days=i) for i in range(365)])
    w = np.array([season_weight(d) for d in days])
    w = w / w.sum()
    n = v["trips_target"]
    out = []
    taken = np.zeros(365 + 10, dtype=bool)
    tries = 0
    while len(out) < n and tries < n * 30:
        tries += 1
        d0 = int(r.choice(365, p=w))
        dur = int(r.integers(p["days"][0], p["days"][1] + 1))
        if d0 + dur > 365 or taken[max(0, d0 - 1):d0 + dur + 1].any():
            continue
        taken[d0:d0 + dur] = True
        out.append((d0, dur))
    out.sort()
    return out


def simulate(seed):
    r = np.random.default_rng(seed)
    V = vessels(r)
    T = []
    for v in V:
        p = SPEC[v["seg"]]
        gw = np.array(p["gw"], dtype=float)
        rate_v = p["rate"] * r.lognormal(0, 0.12)
        for d0, dur in trips_of(r, v):
            drawn = r.random() < p["draw"]
            observed = drawn and (r.random() < AVAIL)
            w = gw.copy()
            if observed:
                w[list(NURSERY_IDX)] *= (1 - p["avoid"])
            w = w / w.sum()
            g = int(r.choice(5, p=w))
            nh = int(sum(r.integers(p["hpd"][0], p["hpd"][1] + 1) for _ in range(dur)))
            hh = np.clip(r.normal(p["hh"][0], p["hh"][1], nh), 0.6, None)
            nursery = g in NURSERY_IDX
            gfac = 0.8 if nursery else 1.0
            hauls = []
            for h in hh:
                mk = rate_v * gfac * h * r.lognormal(0, 0.28)
                quota_mk = sum(f for sp, f in p["mix"].items() if K.SPECIES[sp][1]) * mk
                bf = p["bms"] * (p["nmult"] if nursery else 1.0)
                bms = quota_mk * bf / max(1e-9, (1 - bf)) * r.lognormal(0, 0.3)
                legal = (mk + bms) * p["legal"] / (1 - p["legal"]) * r.lognormal(0, 0.3)
                hauls.append(dict(hours=float(h), mk=float(mk), bms=float(bms), legal=float(legal)))
            dep = dt.datetime.combine(START + dt.timedelta(days=d0), dt.time(0)) + \
                dt.timedelta(hours=float(r.uniform(2.5, 6.0)))
            ret = dep + dt.timedelta(hours=24 * (dur - 1) + float(r.uniform(9, 15)))
            B = sum(h["bms"] for h in hauls)
            if observed or v["comply"]:
                landed_bms = B
            else:
                landed_bms = B * (r.uniform(0.0, 0.06) if r.random() < 0.25 else 0.0)
            if observed:
                # the scheme's observers sample every haul; the draw stays so the seed keeps the world it chose
                samp = r.random(len(hauls)) < SAMPLE_HAUL
                if not samp.any():
                    samp[int(r.integers(0, len(hauls)))] = True
                for h in hauls:
                    h["sampled"] = True
            T.append(dict(id=len(T), v=v["idx"], seg=v["seg"], ground=g, dep=dep, ret=ret, dur=dur,
                          drawn=drawn, observed=observed, hauls=hauls,
                          hours=sum(h["hours"] for h in hauls), mk=sum(h["mk"] for h in hauls), bms=B,
                          legal=sum(h["legal"] for h in hauls), landed_bms=landed_bms))
    lawful_by_ground_and_season(T, seed)
    return dict(V=V, T=T, seed=seed)


def lawful_by_ground_and_season(T, seed):
    """the lawful discards (dab, gurnard, dogfish and the rest) follow each ground's fauna and the season rather than a
    fixed share of the catch: a factor for each of a segment's grounds, at least 1.35 apart from lowest to highest,
    and a seasonal swing, scaled so the segment's year total is the one the haul draws gave; its own random stream,
    so every other draw of the world is untouched"""
    q = np.random.default_rng(seed + 104729)
    for s in K.SEG:
        gl = np.clip(q.lognormal(0, 0.28, 5), 0.55, 1.8)
        used = [i for i, x in enumerate(SPEC[s]["gw"]) if x > 0]
        lg = np.log(gl[used]) - np.log(gl[used]).mean()
        if lg.max() - lg.min() < math.log(1.35):
            lg *= math.log(1.35) / max(lg.max() - lg.min(), 1e-9)
        gl[used] = np.exp(lg)
        ph = float(q.uniform(0, 12))
        amp = 0.25 * float(q.uniform(0.6, 1.0))
        mine = [t for t in T if t["seg"] == s]
        before = sum(h["legal"] for t in mine for h in t["hauls"])
        for t in mine:
            sf = 1 + amp * math.sin(2 * math.pi * (t["dep"].month - ph) / 12)
            for h in t["hauls"]:
                h["legal"] *= gl[t["ground"]] * sf
        after = sum(h["legal"] for t in mine for h in t["hauls"])
        for t in mine:
            for h in t["hauls"]:
                h["legal"] *= before / after
            t["legal"] = sum(h["legal"] for h in t["hauls"])


def analysis_trips(w):
    """the trip records the analysis reads, as the pack will carry them: every trip's ground, hours, hauls and
    declared landings; on observed trips the observer's sampled hauls raised to the trip"""
    out = []
    for t in w["T"]:
        rec = dict(seg=t["seg"], ground=K.GR[t["ground"]], hours=t["hours"], nhauls=len(t["hauls"]),
                   observed=t["observed"], land_mk=t["mk"], land_bms=t["landed_bms"],
                   half=1 if t["dep"].month <= 6 else 2)
        if t["observed"]:
            S = [h for h in t["hauls"] if h["sampled"]]
            f = len(t["hauls"]) / len(S)
            rec.update(obs_mk=f * sum(h["mk"] for h in S), obs_bms=f * sum(h["bms"] for h in S),
                       obs_dis=f * sum(h["legal"] for h in S), obs_hours_s=sum(h["hours"] for h in S),
                       obs_unw_s=sum(h["bms"] + h["legal"] for h in S), obs_mk_s=sum(h["mk"] for h in S))
        out.append(rec)
    return out


def truth(w):
    """each segment's 2025 discard share of catch in the world"""
    out = {}
    for s in K.SEG:
        T = [t for t in w["T"] if t["seg"] == s]
        catch = sum(t["mk"] + t["bms"] + t["legal"] for t in T)
        disc = sum(t["legal"] + t["bms"] - t["landed_bms"] for t in T)
        out[s] = 100 * disc / catch
    return out
