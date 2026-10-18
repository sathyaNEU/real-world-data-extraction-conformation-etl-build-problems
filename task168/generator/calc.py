"""Every figure the build grades, and every rung and rival, computed from the shipped files in target/.

This is the generator's own reading of the pack (csv, sqlite3 and openpyxl); verify.py recomputes the graded
figures on a separate code path with pandas.
"""
import csv
import datetime as dt
import os
import sqlite3
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np

ROME = ZoneInfo("Europe/Rome")
UTC = ZoneInfo("UTC")
NINE = ["CTA", "PMO", "NAP", "BRI", "BDS", "SUF", "REG", "CAG", "TPS"]
S25 = (dt.date(2025, 3, 30), dt.date(2025, 10, 25))


def read_rm(target):
    path = os.path.join(target, "rm_booking_build_s25.csv")
    with open(path, encoding="utf-8") as f:
        r = csv.reader(f)
        head = next(r)
        dcp_cols = [h for h in head if h.startswith("bkd_d")]
        dcps = [int(h[5:]) for h in dcp_cols]
        ix = {h: k for k, h in enumerate(head)}
        rows = []
        for row in r:
            rows.append({
                "flt": int(row[ix["flight_no"]]), "dep": dt.date.fromisoformat(row[ix["dep_date"]]),
                "std": row[ix["std_local"]], "orig": row[ix["orig"]], "dest": row[ix["dest"]],
                "equip": row[ix["equip"]], "cap": int(row[ix["cap"]]), "so": row[ix["sold_out_utc"]],
                "bkd": np.array([int(row[ix[c]]) for c in dcp_cols]),
            })
    return dcps, rows


def read_dcs(target):
    out = {}
    with open(os.path.join(target, "dcs_flight_close_s25.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[(int(row["flight_no"]), row["dep_date"])] = row
    return out


def is_nine(o, d):
    return (o == "LIN" and d in NINE) or (d == "LIN" and o in NINE)


def station(o, d):
    return d if o == "LIN" else o


def x_sellout(r):
    """Days from the sell-out to the end of the local departure date."""
    t = dt.datetime.strptime(r["so"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    nxt = r["dep"] + dt.timedelta(days=1)
    end = dt.datetime(nxt.year, nxt.month, nxt.day, tzinfo=ROME).astimezone(UTC)
    return (end - t).total_seconds() / 86400.0


def curves(rows, key, keep=lambda r: True):
    acc = defaultdict(list)
    for r in rows:
        if r["so"] == "" and keep(r) and r["bkd"][-1] > 0:
            acc[key(r)].append(r["bkd"] / r["bkd"][-1])
    return {k: np.mean(v, axis=0) for k, v in acc.items()}, {k: len(v) for k, v in acc.items()}


def interp(c, dcps, x):
    xs = np.array(dcps, float)[::-1]
    return float(np.interp(x, xs, c[::-1]))


def demand(r, c, dcps, mode="exact"):
    if r["so"] == "":
        return float(r["bkd"][-1])
    x = x_sellout(r)
    if mode == "exact":
        return r["cap"] / interp(c, dcps, x)
    arr = np.array(dcps, float)
    if mode == "lastopen":
        jj = np.nonzero(arr > x)[0][-1]
        return r["bkd"][jj] / c[jj]
    if mode == "firstclosed":
        j = int(np.nonzero(r["bkd"] >= r["cap"])[0][0])
        return r["cap"] / c[j]
    if mode == "datediff":
        t = dt.datetime.strptime(r["so"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(ROME).date()
        return r["cap"] / interp(c, dcps, float((r["dep"] - t).days))
    raise ValueError(mode)


def seats_s26(r):
    """Summer 2026 seats on the same flight 364 days later, from the capacity plan's gauge and effective dates."""
    st = station(r["orig"], r["dest"])
    d26 = r["dep"] + dt.timedelta(days=364)
    if st in ("BDS", "SUF") and d26 < dt.date(2026, 6, 1):
        return 144
    return 232


def noshow_by_leg(rows, dcs):
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        if not is_nine(r["orig"], r["dest"]):
            continue
        d = dcs[(r["flt"], r["dep"].isoformat())]
        acc[(r["orig"], r["dest"])][0] += int(d["pax_booked"])
        acc[(r["orig"], r["dest"])][1] += int(d["pax_flown"])
    return {k: 1 - v[1] / v[0] for k, v in acc.items()}


def forecast(rows, dcs, dcps, curve_for, mode="exact", ns=None, s26=seats_s26, include_infants=False):
    """Additional passengers carried on the nine routes, summer 2026 over summer 2025, and the pieces."""
    ns = ns if ns is not None else noshow_by_leg(rows, dcs)
    base = 0
    fc = 0.0
    inf_share = None
    if include_infants:
        f_ = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["pax_flown"]) for r in rows if is_nine(r["orig"], r["dest"]))
        i_ = sum(int(dcs[(r["flt"], r["dep"].isoformat())]["inf_flown"]) for r in rows if is_nine(r["orig"], r["dest"]))
        inf_share = i_ / f_
    for r in rows:
        if not is_nine(r["orig"], r["dest"]):
            continue
        d = dcs[(r["flt"], r["dep"].isoformat())]
        flown = int(d["pax_flown"])
        D = demand(r, curve_for(r), dcps, mode)
        f = min(D, s26(r)) * (1 - ns[(r["orig"], r["dest"])])
        if include_infants:
            flown = flown + int(d["inf_flown"])
            f = f * (1 + inf_share)
        base += flown
        fc += f
    return fc - base, base, fc


def golden(target):
    dcps, rows = read_rm(target)
    dcs = read_dcs(target)
    c, n = curves(rows, lambda r: r["dep"].month, keep=lambda r: not is_nine(r["orig"], r["dest"]))
    gain, base, fc = forecast(rows, dcs, dcps, lambda r: c[r["dep"].month])
    return {"gain": gain, "base": base, "forecast": fc, "curves": c, "n_curve": n, "dcps": dcps, "rows": rows,
            "dcs": dcs}


# ------------------------------------------------------------------ the ask: turned away because the flight was full
def read_refusals(target):
    with open(os.path.join(target, "booking_engine_refusals_s25.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def turnaways(target, rows=None, mode="golden", refusals=None):
    """Passengers turned away from summer 2025 departures of the nine routes because the flight was full, by
    route direction (orig, dest).

    golden    request logged at or after the departure sold out; a website or app session asking again for the
              same departure is one party; every agency-feed record is one passenger name; every contact-centre
              record is one call
    cracker   the same sell-out test, every repeated (session_ref, flight, date) dropped whatever the channel
    nodedup   the same sell-out test, every record's pax summed
    departure every request for a departure that sold out at some point, repeated keys dropped
    nolight   requests for a higher fare family only (LIGHT read as a fare closure), repeated keys dropped
    naive     every record's pax summed
    """
    if rows is None:
        _, rows = read_rm(target)
    so = {(r["flt"], r["dep"].isoformat()): r["so"] for r in rows}
    out = defaultdict(int)
    seen = set()
    for e in (refusals if refusals is not None else read_refusals(target)):
        o, d = e["orig"], e["dest"]
        if not is_nine(o, d):
            continue
        dep = dt.date.fromisoformat(e["dep_date"])
        if not (S25[0] <= dep <= S25[1]):
            continue
        s = so[(int(e["flight_no"]), e["dep_date"])]
        after = s != "" and e["logged_utc"] >= s
        key = (e["session_ref"], e["flight_no"], e["dep_date"])
        pax = int(e["pax"])
        ch = e["channel"]
        if mode == "naive":
            out[(o, d)] += pax
            continue
        if mode == "nodedup":
            if after:
                out[(o, d)] += pax
            continue
        if mode == "departure":
            keep = s != ""
        elif mode == "nolight":
            keep = e["fare_family"] != "LIGHT"
        else:
            keep = after
        if not keep:
            continue
        if mode == "golden" and ch in ("GDS", "CC"):
            out[(o, d)] += pax
            continue
        if key in seen:
            continue
        seen.add(key)
        out[(o, d)] += pax
    return dict(out)
