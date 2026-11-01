"""The 2025-26 spinal waiting list: referrals, the triage service's routing, treatment, the board's
mutual-aid moves, and what each system records about them (truth before any export is cut)."""
import datetime as dt
import numpy as np
import pandas as pd
from common import PROVIDERS, NHS_KEYS, RENAME, ODS, DISTRICTS, CATCH, INDEX_STENOSIS, INDEX_DISC, SNAPSHOT
from world import stream, hexid, GP, provider_at

D = dt.timedelta
REF_FROM = dt.date(2023, 9, 4)
SNAPS = [dt.date(2026, 1, 31), dt.date(2026, 2, 28), dt.date(2026, 3, 31)]
RECEIVERS = [41206, 41274, 41309, 41402]
MEDIAN = {40117: 41.0, 40152: 35.0, 40188: 45.0}


def ods_for(key, day):
    return ODS[provider_at(key, day)]


def wait_weeks(p, r):
    if p["kind"] == "NHS":
        wk = np.exp(np.log(MEDIAN[p["key"]]) + 0.42 * r.normal())
    elif r.random() < 0.16:
        wk = np.exp(np.log(52.0) + 0.24 * r.normal())
    else:
        wk = np.exp(np.log(19.0 + 3.0 * p["sev"]) + 0.42 * r.normal())
    return float(min(wk, 108.0))


def make_waits():
    paths = []
    pid = 0
    for p in PROVIDERS:
        r = stream(p["key"], 9700)
        rate = p["vol"][2] * 1.15 / 52.0
        wk = REF_FROM
        while wk <= SNAPSHOT:
            for _ in range(int(r.poisson(rate))):
                pid += 1
                receipt = wk + D(days=int(r.integers(0, 5)))
                if receipt > SNAPSHOT:
                    continue
                u = r.random()
                route = "MSK triage" if u < 0.62 else ("GP" if u < 0.92 else "Consultant")
                if route == "MSK triage":
                    routed = receipt - D(days=int(r.integers(1, 7)))
                    tri = routed - D(days=int(r.integers(21, 85)))
                    clock = tri
                else:
                    routed = tri = None
                    clock = receipt
                wks = wait_weeks(p, r)
                treat = clock + D(days=int(round(wks * 7)))
                if treat <= receipt:
                    treat = receipt + D(days=int(r.integers(7, 30)))
                v = r.random()
                other = None
                if v < 0.06:
                    other = ("Validated off (no longer requires treatment)", receipt + D(days=int(r.integers(28, 300))))
                elif v < 0.08:
                    other = ("Patient declined treatment", receipt + D(days=int(r.integers(28, 300))))
                elif v < 0.084:
                    other = ("Patient died", receipt + D(days=int(r.integers(28, 300))))
                if other is not None and other[1] >= treat:
                    other = None
                if p["kind"] == "NHS" and r.random() < 0.7:
                    dist = CATCH[p["key"]][int(r.integers(0, len(CATCH[p["key"]])))]
                else:
                    dist = DISTRICTS[int(r.integers(0, len(DISTRICTS)))]
                paths.append(dict(path=pid, prov=p["key"], kind=p["kind"], receipt=receipt, route=route, routed=routed,
                                  tri=tri, clock=clock, treat=treat, other=other, district=dist,
                                  gp=GP[dist][int(r.integers(0, len(GP[dist])))],
                                  yob=int(2025 - np.clip(r.normal(57, 13), 20, 90)), sex=1 + int(r.random() < 0.53),
                                  pseudo=hexid(r, 10), token=hexid(r, 12),
                                  proc=(INDEX_STENOSIS + INDEX_DISC)[int(r.integers(0, 7))],
                                  prio=["P2", "P3", "P4"][int(r.choice(3, p=[0.1, 0.35, 0.55]))],
                                  origin=None, moved=None))
            wk += D(days=7)
    P = {x["path"]: x for x in paths}

    def end_of(x):
        e = x["treat"]
        if x["other"] is not None:
            e = min(e, x["other"][1])
        if x["moved"] is not None:
            e = min(e, x["moved"][0])
        return e

    # the board's mutual-aid moves: each Monday the two longest recorded waits at each trust go to an
    # independent site in rotation, which treats them within a few weeks
    rm = stream(9800)
    day = dt.date(2025, 11, 3)
    rot = 0
    while day <= dt.date(2026, 3, 30):
        for k in NHS_KEYS:
            cand = [x for x in paths if x["prov"] == k and x["moved"] is None and x["receipt"] <= day
                    and end_of(x) > day]
            cand.sort(key=lambda x: (x["receipt"], x["path"]))
            for x in cand[:2]:
                dest = RECEIVERS[rot % 4]
                rot += 1
                pid += 1
                lag = int(rm.integers(3, 26))
                x["moved"] = (day, dest, day + D(days=lag))
                treat = day + D(days=int(rm.integers(21, 99)))
                y = dict(x)
                y.update(path=pid, prov=dest, kind="IS", receipt=day, route="Transfer", routed=None, tri=None,
                         clock=x["clock"], treat=treat, other=None, origin=x["path"], moved=None)
                paths.append(y)
                P[pid] = y
        day += D(days=7)

    # the triage service's surgical routings, with identities settled before any system writes a row
    sur = pd.DataFrame([dict(token=x["token"], yob=x["yob"], sex=x["sex"], district=x["district"], gp=x["gp"],
                             received=x["tri"], outcome="Surgical opinion - spinal",
                             routed_to=ods_for(x["prov"], x["routed"]), routed_on=x["routed"], path=x["path"])
                        for x in paths if x["route"] == "MSK triage" and x["tri"] >= dt.date(2023, 6, 1)])
    sur = settle_keys(sur, paths)
    # what each provider's list holds at each month end, and the removals it recorded
    rows, rem = [], []
    rs = stream(9900)
    for x in paths:
        rec_clock = x["receipt"]
        end_eff = x["treat"]
        reason, dest, rec_on = "Treated (admitted)", "", x["treat"]
        if x["other"] is not None and x["other"][1] < end_eff:
            end_eff = x["other"][1]
            reason, rec_on = x["other"][0], x["other"][1]
        if x["moved"] is not None and x["moved"][0] < end_eff:
            end_eff = x["moved"][0]
            reason, dest, rec_on = "Transferred to another provider", ods_for(x["moved"][1], x["moved"][0]), x["moved"][2]
        x["end_eff"], x["reason"], x["dest"], x["rec_on"] = end_eff, reason, dest, rec_on
        if dt.date(2025, 11, 1) <= end_eff <= dt.date(2026, 4, 30):
            rem.append(dict(path=x["path"], prov=provider_at(x["prov"], end_eff), pseudo=x["pseudo"], route=x["route"],
                            receipt=x["receipt"], clock_rec=rec_clock, removal=end_eff, reason=reason, dest=dest,
                            rec_on=rec_on))
        for s in SNAPS:
            if x["receipt"] <= s < rec_on:
                blank = (x["route"] in ("GP", "Consultant") and (s - x["receipt"]).days <= 20 and rs.random() < 0.5)
                tci = x["treat"] if (x["treat"] > s and (x["treat"] - s).days <= 42 and reason == "Treated (admitted)") else None
                rows.append(dict(snap=s, prov=provider_at(x["prov"], s), path=x["path"], pseudo="" if blank else x["pseudo"],
                                 yob=x["yob"], sex=x["sex"], district=x["district"], gp=x["gp"], route=x["route"],
                                 receipt=x["receipt"], clock_rec=rec_clock, weeks=(s - rec_clock).days // 7,
                                 proc=x["proc"], prio=x["prio"], tci=tci))
    ptl = pd.DataFrame(rows)
    removals = pd.DataFrame(rem)

    rt = stream(9950)
    n_non = int(0.9 * len(sur))
    outs = ["Physiotherapy", "Physiotherapy", "Pain management", "Discharged to GP"]
    tri = []
    for _ in range(n_non):
        dist = DISTRICTS[int(rt.integers(0, len(DISTRICTS)))]
        rec = dt.date(2023, 6, 1) + D(days=int(rt.integers(0, (SNAPSHOT - dt.date(2023, 6, 1)).days)))
        tri.append(dict(token=hexid(rt, 12), yob=int(2025 - np.clip(rt.normal(52, 15), 18, 92)), sex=1 + int(rt.random() < 0.55),
                        district=dist, gp=GP[dist][int(rt.integers(0, len(GP[dist])))], received=rec,
                        outcome=outs[int(rt.integers(0, 4))], routed_to="", routed_on=rec + D(days=int(rt.integers(14, 70))),
                        path=-1))
    triage = pd.concat([sur, pd.DataFrame(tri)], ignore_index=True)
    run = dt.date(2026, 4, 14)
    pending = triage.routed_on > run
    assert not (pending & (triage.outcome == "Surgical opinion - spinal")).any()
    triage.loc[pending, "outcome"] = "Awaiting triage"
    triage.loc[pending, "routed_on"] = None
    paths_df = pd.DataFrame(paths)
    return dict(paths=paths_df, ptl=ptl, removals=removals, triage=triage)


def settle_keys(triage, paths):
    """A surgical routing is placed on a provider's list by birth year, sex, district, practice and the routing
    date; where two routings to one site would share that key within 12 days, the later patient's practice is the
    district's next one (both files carry the patient's practice, so they stay consistent)."""
    P = {x["path"]: x for x in paths}
    sur = triage[triage.outcome == "Surgical opinion - spinal"].sort_values(["routed_on", "path"])
    seen = {}
    for i, r in sur.iterrows():
        key = (r.yob, r.sex, r.district, r.routed_to)
        gp = r.gp
        prac = GP[r.district]
        for _ in range(len(prac)):
            hits = [d for d in seen.get(key + (gp,), []) if abs((d - r.routed_on).days) <= 12]
            if not hits:
                break
            gp = prac[(prac.index(gp) + 1) % len(prac)]
        seen.setdefault(key + (gp,), []).append(r.routed_on)
        if gp != r.gp:
            triage.at[i, "gp"] = gp
            x = P[r.path]
            x["gp"] = gp
            for y in paths:
                if y.get("origin") == x["path"]:
                    y["gp"] = gp
    return triage
