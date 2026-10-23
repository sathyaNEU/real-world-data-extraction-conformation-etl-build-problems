"""Readers for the shipped files: everything the analysis computes is read back from the pack, never from the world."""
from __future__ import annotations

import csv
import datetime as dt
import os
import re

import common as K


def path(target, key):
    return os.path.join(target, K.FILES[key])


def rows(target, key):
    with open(path(target, key), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def norm_pln(s):
    """port letters and number as the register writes them: letters, one space, number"""
    m = re.match(r"^\s*([A-Za-z]+)[\s\-]*0*(\d+)\s*$", s)
    return "%s %d" % (m.group(1).upper(), int(m.group(2))) if m else s.strip().upper()


def parse(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def register(target):
    return {r["vessel_pln"]: r for r in rows(target, "register")}


def trip_records(target, match_hours=12.0, local=True, raise_hauls=True):
    """one record a logbook trip, with its declared landings and, for an observed trip, the observer's weighings
    raised from the hauls sampled to the trip's hours fished"""
    reg = register(target)
    T = {}
    for r in rows(target, "trips"):
        dep = parse(r["departure_utc"])
        T[r["trip_id"]] = dict(trip=r["trip_id"], pln=r["vessel_pln"], seg=reg[r["vessel_pln"]]["segment"],
                               ground=r["po_ground"], hours=float(r["fishing_hours"]), nhauls=int(r["hauls"]),
                               dep_local=K.to_local(dep) if local else dep, observed=False,
                               self_dis=float(r["discards_declared_kg"] or 0), land_mk=0.0, land_bms=0.0)
    for r in rows(target, "landings"):
        t = T[r["trip_id"]]
        w = float(r["live_weight_kg"])
        if r["mcrs_status"] == "BMS":
            t["land_bms"] += w
        else:
            t["land_mk"] += w
    obs = {}
    for r in rows(target, "hauls"):
        o = obs.setdefault(r["observer_trip_ref"], dict(RET=0.0, BMS=0.0, DIS=0.0, hours={}))
        o[r["fraction"]] += float(r["weight_kg"])
        o["hours"][r["haul_no"]] = (parse(r["hauled_local"]) - parse(r["shot_local"])).total_seconds() / 3600
    by_vessel = {}
    for t in T.values():
        by_vessel.setdefault(t["pln"], []).append(t)
    unmatched = []
    for r in rows(target, "deploy"):
        if r["outcome"] != "Observed":
            continue
        pln = norm_pln(r["vessel_pln"])
        when = parse(r["notified_departure"])
        cands = [t for t in by_vessel.get(pln, [])
                 if abs((t["dep_local"] - when).total_seconds()) <= match_hours * 3600]
        if not cands:
            unmatched.append(r["deployment_ref"])
            continue
        t = min(cands, key=lambda t: abs((t["dep_local"] - when).total_seconds()))
        o = obs[r["observer_trip_ref"]]
        hs = sum(o["hours"].values())
        f = t["hours"] / hs if raise_hauls else 1.0
        t.update(observed=True, obs_ref=r["observer_trip_ref"], obs_mk=o["RET"] * f, obs_bms=o["BMS"] * f,
                 obs_dis=o["DIS"] * f, obs_hours_s=hs, obs_unw_s=o["BMS"] + o["DIS"], obs_mk_s=o["RET"])
    out = []
    for t in sorted(T.values(), key=lambda t: t["trip"]):
        t["half"] = 1 if t["dep_local"].month <= 6 else 2
        out.append(t)
    return out, unmatched


def sales(target):
    return rows(target, "sales")


def vms(target):
    return rows(target, "vms")


def transponders(target):
    return rows(target, "transponders")


def ports(target):
    return rows(target, "ports")
