"""Cut the task308 pack from the world: trips, dispatch, the audit, the station feeds, the account register, the
Harbour charging sessions, the workshop jobs, the documents and the distractors."""
import csv
import datetime as dt
import json
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

import docs
import params as P
import postprocess
import records as R
import world as Wd

F = P.FILES
PACK = list(F)
DISTRACTORS = ("opendata", "quote")
CONTEXT = ("board",)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def lt(t, sep=" "):
    return R.loc(t).strftime("%Y-%m-%d" + sep + "%H:%M:%S")


def ut(t):
    return R.utc(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def fare(dur, typ, fs):
    if fs:
        return 0.0
    return P.UNLOCK + (P.PER_MIN_EBIKE if typ == "ebike" else P.PER_MIN_CLASSIC) * math.ceil(dur / 60)


def bike_old(b):
    return ("E-%04d" % int(b[1:])) if isinstance(b, str) else "B-%05d" % b


def bike_new(b):
    return (500000 + int(b[1:])) if isinstance(b, str) else 100000 + b


def bike_tag(b):
    return ("EB%04d" % int(b[1:])) if isinstance(b, str) else "BK%05d" % b


def build(target):
    os.makedirs(target, exist_ok=True)
    path = {k: os.path.join(target, v) for k, v in F.items()}
    W = Wd.world()
    st = R.stations(W)
    sid = {x["k"]: x["station_id"] for x in st}
    rs = np.random.default_rng([P.SEED_DOCS, 2])
    # ------------------------------------------------------------------ stations
    upd = int(dt.datetime(2026, 11, 1, 6, 0, tzinfo=P.TZ).timestamp())
    regions = {a: str(i + 1) for i, a in enumerate(P.NETWORKS)}
    with open(path["stations"], "w", encoding="utf-8") as fh:
        json.dump({"last_updated": upd, "ttl": 300, "version": "2.3",
                   "data": {"stations": [{"station_id": x["station_id"], "name": x["name"], "short_name": x["code"],
                                          "lat": x["lat"], "lon": x["lon"], "region_id": regions[x["network"]],
                                          "capacity": x["capacity"]}
                                         for x in sorted(st, key=lambda x: x["station_id"])]}}, fh, indent=1)
        fh.write("\n")
    with open(path["regions"], "w", encoding="utf-8") as fh:
        json.dump({"last_updated": upd, "ttl": 86400, "version": "2.3",
                   "data": {"regions": [{"region_id": regions[a], "name": P.NETWORKS[a][0]} for a in P.NETWORKS]}},
                  fh, indent=1)
        fh.write("\n")
    # ------------------------------------------------------------------ riders and accounts
    persons, accounts, rereg, house = R.people(W, W.rides)
    acc_of = {}
    for acc in accounts:
        for j in acc["rides"]:
            acc_of[j] = acc
    # ------------------------------------------------------------------ trips
    order = sorted(range(len(W.rides)), key=lambda j: (W.rides[j][0], W.rides[j][2], str(W.rides[j][5])))
    tid = int(41203117)
    rid = int(rs.integers(2100000, 2200000))
    halves = {"q1": [], "q2": [], "q3": [], "q4": []}
    for j in order:
        t0, t1, k0, k1, typ, b, fs = W.rides[j]
        q = (R.loc(t0).month - 1) // 3 + 1
        dur = t1 - t0
        f = fare(dur, typ, fs)
        acc = acc_of[j]
        if q <= 2:
            tid += int(rs.integers(1, 4))
            halves["q%d" % q].append([str(tid), lt(t0), lt(t1), st[k0]["name"], st[k1]["name"], bike_old(b),
                                      "electric" if typ == "ebike" else "classic", acc["legacy"],
                                      "Member" if acc["plan"] == "annual" else "Casual", dur, "%.2f" % f])
        else:
            rid += int(rs.integers(1, 3))
            halves["q%d" % q].append(["R%d" % rid, lt(t0, "T"), lt(t1, "T"),
                                      st[k0]["code"], st[k1]["code"], bike_new(b),
                                      "EBIKE" if typ == "ebike" else "CLASSIC", acc["id"], acc["plan"], dur,
                                      int(round(f * 100))])
    old_h = ["trip_id", "start_time", "end_time", "start_station", "end_station", "bike_no", "bike_type", "account_no",
             "member_type", "duration_sec", "fare_usd"]
    new_h = ["ride_id", "started_at", "ended_at", "start_station_code", "end_station_code", "vehicle_id",
             "vehicle_type", "account_id", "plan", "duration_s", "fare_cents"]
    for q in ("q1", "q2"):
        _csv(path[q], old_h, halves[q])
    for q in ("q3", "q4"):
        _csv(path[q], new_h, halves[q])
    # ------------------------------------------------------------------ dispatch
    mv = sorted(W.moves, key=lambda m: (m[0], m[1], m[2]))
    rows = []
    for i, (t, f_, to, n, cls) in enumerate(mv, 1):
        k = f_ if f_ >= 0 else to
        net = W.area[k]
        h = R.loc(t).hour
        crew = ("E-crew %s" % net) if cls == "ebike" else (("Night %s" % net) if h < 4 else ("Van %s" % net))
        rows.append(["D25-%06d" % i, ut(t), sid[f_] if f_ >= 0 else "DEPOT", sid[to] if to >= 0 else "DEPOT", n,
                     "e-bike" if cls == "ebike" else "classic", crew])
    _csv(path["moves"], ["move_id", "completed_utc", "from_station", "to_station", "qty", "bike_class", "van"], rows)
    # ------------------------------------------------------------------ the 03:00 audit
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("audit")
    ws.append(["audit_date", "station_id", "classic_docked", "ebikes_docked"])
    for d, k, c, e in sorted(W.counts, key=lambda x: (x[0], sid[x[1]])):
        ws.append([dt.date(P.YEAR, 1, 1) + dt.timedelta(days=int(d)), sid[k], int(c), int(e)])
    wb.properties.creator = "Fleet audit"
    wb.save(path["audit"])
    postprocess.scrub(path["audit"], P.ORG, "2026-01-02")
    postprocess.finish_office(path["audit"], "2026-01-02T09:14:00Z", "2026-01-02T09:14:00Z", P.ORG)
    # ------------------------------------------------------------------ the account register
    ra = np.random.default_rng([P.SEED_PEOPLE, 3])
    rows = []
    for acc in accounts:
        last = max((W.rides[j][1] for j in acc["rides"]), default=None)
        status, closed = "active", ""
        if acc["plan"] == "payg" and last is not None and R.loc(last).month < 10 and ra.random() < 0.25:
            status, closed = "closed", lt(last + int(ra.integers(3600, 60 * 86400)))
        elif acc["pid"] is None and ra.random() < 0.3:
            status, closed = "closed", (acc["created"] + dt.timedelta(days=int(ra.integers(30, 600)))).strftime("%Y-%m-%d %H:%M:%S")
            if closed > "2025-12-31":
                status, closed = "active", ""
        home = P.AREA_NAME[acc["home"]]
        if acc["legacy"] and ra.random() < 0.18:
            home = [home.lower(), home.upper(), home + " "][int(ra.integers(0, 3))]
        rows.append([acc["id"], acc["legacy"], acc["created"].strftime("%Y-%m-%d %H:%M:%S"), acc["plan"], home,
                     acc["card"], status, closed])
    _csv(path["accounts"], ["account_id", "legacy_account_no", "created_at", "plan", "home_area", "card_fingerprint",
                            "status", "closed_at"], rows)
    # ------------------------------------------------------------------ charging
    ses, swap = R.charging(W, st)
    _csv(path["charging"], ["session_id", "station_code", "point", "vehicle_tag", "plug_in_utc", "plug_out_utc",
                            "meter_start_wh", "meter_stop_wh", "energy_kwh"],
         [[s["sid"], st[s["k"]]["code"], s["p"], bike_tag(s["e"]), ut(s["t0"]), ut(s["t1"]), s["ms"], s["me"],
           "%.3f" % ((s["me"] - s["ms"]) / 1000.0)] for s in sorted(ses, key=lambda s: s["sid"])])
    # ------------------------------------------------------------------ the workshop
    jobs = R.workshop(W)
    _csv(path["workshop"], ["job_no", "asset_tag", "asset_class", "opened_utc", "closed_utc", "fault_code", "fault",
                            "outcome", "bay", "technician"],
         [[j["job"], bike_tag(j["bike"]), "E-bike" if j["typ"] == "ebike" else "Classic", ut(j["open"]),
           ut(j["close"]), j["code"], R.FAULT_TEXT[j["code"]],
           "Scrapped" if j["outcome"] == "scrapped" else "Returned to service", j["bay"], j["tech"]] for j in jobs])
    # ------------------------------------------------------------------ the City's open data (a distractor)
    od = {}
    for t0, t1, k0, k1, typ, b, fs in W.rides:
        if fs:
            continue
        key = (P.NETWORKS[W.area[k0]][0], R.loc(t0).strftime("%Y-%m"))
        od[key] = od.get(key, 0) + 1
    _csv(path["opendata"], ["area", "month", "trips"],
         [[a, m, n if n >= 10000 else "suppressed"] for (a, m), n in sorted(od.items(), key=lambda x: (x[0][1], x[0][0]))])
    # ------------------------------------------------------------------ documents
    docs.board(path["board"])
    postprocess.scrub(path["board"], "Microsoft Word 2019", "2026-11-05T16:40:00")
    docs.pilot(path["pilot"], st)
    postprocess.scrub(path["pilot"], "Microsoft Word 2019", "2026-11-03T10:05:00")
    docs.fares(path["fares"])
    postprocess.scrub(path["fares"], "Microsoft Word 2019", "2024-02-12T13:30:00")
    docs.quote(path["quote"])
    postprocess.scrub(path["quote"], "Microsoft Word 2019", "2026-10-02T09:00:00")
    docs.dictionary(path["dictionary"])
    postprocess.scrub(path["dictionary"], P.ORG, "2026-11-04")
    postprocess.finish_office(path["dictionary"], "2025-07-08T14:20:00Z", "2026-11-04T11:02:00Z", P.ORG,
                              person="Data team")
    return {"W": W, "st": st, "persons": persons, "accounts": accounts, "rereg": rereg, "house": house,
            "sessions": ses, "swap": swap, "jobs": jobs}


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    out = build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target"))
    print("built in", round(time.time() - t, 1), "s")
