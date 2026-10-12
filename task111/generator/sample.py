"""The twin pair and the quality team's verified sample of first-half missed appointments."""
import copy
import datetime as dt

import numpy as np

from days import misses, run_day
from world import MOVES

D = dt.date

NOTES = {
    "late": ["Van would not start, logged on after a jump start", "Slept in", "Childcare drop-off ran late",
             "Handset would not sync, logged on late", "Medical appointment, not booked as leave",
             "Locked out of van, spare key from depot", "Flat tyre on driveway"],
    "travel": ["Lane closure M74 J3", "Collision on A8 at Newbridge", "Roadworks diversion at Kirkintilloch",
               "Queue at Kingston Bridge", "M8 J15 closure", "Diversion on A92", "Slow traffic M9 Kirkliston"],
    "overrun": ["Diagnosis ran long, PCB fault", "Leak traced under kitchen floor", "Second flue check needed",
                "Seized valve, drained system", "Intermittent fault, extended test"],
    "parts": ["Diverter valve collected at merchant", "PCB not on van, trade counter collection",
              "Pump collected at merchant", "Expansion vessel collected"],
    "access": ["Customer not home until arrival plus 40 min", "Key holder late", "Customer at school run, waited"],
    "other": ["Van breakdown, recovery called"],
}
FAMILY = {"late": "Engineer attendance & punctuality", "travel": "Travel & routing",
          "overrun": "Job duration & standards", "parts": "Parts & van stock", "access": "Customer access",
          "other": "Other", "rest": "Rota & cover"}


def make_twin(W, seed=111):
    """Copy a Q3 rest-forced day's plan and timeline onto a spring day of the same engineer as a genuine late
    log-on, so the two days are identical on every day-app column and differ only in origin."""
    rng = np.random.default_rng([seed, 6])
    recs = {(r["engineer_id"], r["date"]): r for r in W.day_records}
    cands = []
    for r in W.day_records:
        if not r["event"] or r["event"][0] != "rest" or r["date"] < D(2026, 7, 1):
            continue
        if len(r["missed"]) < 2 or any(j["long"] for j in r["jobs"]):
            continue
        if any(j["district"] in MOVES for j in r["jobs"]) or any(j.get("no_access") for j in r["jobs"]):
            continue
        if r["logon"] - 480 > 200 or r["logon"] - 480 < 60:
            continue
        cands.append(r)
    cands.sort(key=lambda r: (r["date"], r["engineer_id"]))
    for r2 in cands:
        eid = r2["engineer_id"]
        spring = [d for d in W.days if D(2026, 4, 13) <= d <= D(2026, 5, 22) and W.roster[eid].get(d) == "D"
                  and recs.get((eid, d)) and not recs[(eid, d)]["missed"]]
        if not spring:
            continue
        d1 = spring[int(rng.integers(len(spring)))]
        r1 = recs[(eid, d1)]
        jobs = copy.deepcopy(r2["jobs"])
        acts = run_day(rng, jobs, d1, r2["logon"], None, True)
        if [a["arr"] for a in acts] != [a["arr"] for a in r2["acts"]]:
            continue
        r1["jobs"] = jobs
        r1["acts"] = acts
        r1["logon"] = r2["logon"]
        r1["event"] = ("late", 0, r2["logon"] - 480)
        r1["missed"] = misses(jobs, acts)
        W.twin = (r1, r2)
        return r1, r2
    raise RuntimeError("no twin")


def verified_sample(W, seed=111):
    rng = np.random.default_rng([seed, 7])
    out = []
    twin_first = None
    if getattr(W, "twin", None):
        r1 = W.twin[0]
        twin_first = [a for a in W.appointments if a["day"] is r1 and a["missed"]][0]
    for m in (1, 2, 3, 4, 5):
        pool = [a for a in W.appointments if a["missed"] and a["date"].year == 2026 and a["date"].month == m]
        pool.sort(key=lambda a: a["appointment_ref"])
        idx = rng.choice(len(pool), 40, replace=False)
        chosen = [pool[i] for i in sorted(idx)]
        if twin_first is not None and twin_first["date"].month == m and twin_first not in chosen:
            chosen[int(rng.integers(len(chosen)))] = twin_first
        for a in chosen:
            r = a["day"]
            kind = r["event"][0]
            assert kind != "rest", "verified sample must be blind to rest-forced log-ons"
            k0 = r["event"][1]
            jobs = r["jobs"]
            # origin record and time
            day_apps = [x for x in W.appointments if x["day"] is r]
            day_apps.sort(key=lambda x: x["k"])
            if kind == "late":
                otime = r["logon"]
                oref = ""
            elif kind in ("travel", "parts", "other"):
                otime = day_apps[k0]["arr"]
                oref = day_apps[k0]["appointment_ref"]
            elif kind == "access":
                otime = day_apps[k0]["start"]
                oref = day_apps[k0]["appointment_ref"]
            else:
                otime = day_apps[k0]["dep"]
                oref = day_apps[k0]["appointment_ref"]
            if a is twin_first:
                note = "Van would not start, logged on after a jump start"
            else:
                note = NOTES[kind][int(rng.integers(len(NOTES[kind])))]
            out.append({"a": a, "kind": kind, "family": FAMILY[kind], "origin_time": otime, "origin_ref": oref,
                        "note": note, "month": m})
    W.verified = out
    return out
