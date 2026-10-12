"""Simulate each centre's Thornacre pick faces from a burn-in to 06:00 on 7 December 2026.

Per face and trading day: picks (Poisson at the face's velocity), silent record errors that persist to the
next count, loud errors that surface the same day as a short pick, a negative balance or an empty-face
report and draw an exception count that night, false triggers (an overflowed replenishment, an empty face
reported in error), the routine cycle for the face's class with roll-over slips, and every count posting
the confirmed quantity as the record. Keeps the private truth (each face's state at the stand-down), which
never ships.
"""
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np

import world as W

KIND_ROUTINE, KIND_LOUD, KIND_FALSE = 0, 1, 2
FILES = {
    "counts": "THN_pickface_count_history_20260601_20261207.csv",
    "locations": "wms_location_master_THN_eff.csv",
    "centres": "corderoy_thornacre_centre_register.csv",
}


def simulate_centre(c):
    rng = np.random.default_rng(c["seed"])
    n = c["n"]
    cls = rng.choice(np.array(["A", "B", "C"]), size=n, p=c["mix"])
    L = np.array([W.CYCLE[k] for k in cls])
    clsv = np.array([c["cls_vel"][k] for k in cls])
    v = (np.array([W.VMEAN[k] for k in cls]) * c["vel"] * clsv
         * rng.lognormal(-0.5 * c["vsd"] ** 2, c["vsd"], n))
    v = np.maximum(np.round(v, 1), 0.1)          # the velocity the slotting review recorded, as shipped
    phase = rng.integers(0, L)
    # out-of-scope faces: on quality hold at the stand-down (counting suspended), or released mid-window
    u = rng.random(n)
    held = u < W.HELD_SHARE
    released = (u >= W.HELD_SHARE) & (u < W.HELD_SHARE + W.RELEASED_SHARE)
    hold_day = np.where(held, rng.integers(W.F - 14, W.F - 2, n), 10 ** 6)
    release_day = np.where(released, rng.integers(35, W.F - 20, n), 10 ** 6)
    s, l, fa = c["silent"] / 1e4, c["loud"] / 1e4, c["false"] / 1e4
    wrong = np.zeros(n, bool)
    next_due = (phase - W.BURN).astype(int)
    slip_left = np.full(n, -1)
    logs = []
    for day in range(-W.BURN, W.F):
        active = (day < hold_day) & (day < release_day)
        tx = np.where(active, rng.poisson(v), 0)
        wrong |= rng.binomial(tx, s) > 0
        loud = rng.binomial(tx, l) > 0
        false = (rng.binomial(tx, fa) > 0) & ~loud
        exc = loud | false
        due = (next_due <= day) & active
        start_slip = due & (slip_left < 0) & (rng.random(n) < c["slip"])
        slip_left[start_slip] = rng.integers(1, 7, start_slip.sum())
        counting_slip = due & (slip_left > 0) & ~start_slip
        slip_left[counting_slip] -= 1
        routine = due & ((slip_left < 0) | (slip_left == 0)) & ~start_slip
        if day >= 0:
            ix = np.where(exc)[0]
            logs.append((ix, np.full(len(ix), day), np.where(loud[ix], KIND_LOUD, KIND_FALSE),
                         ~(wrong[ix] | loud[ix]), wrong[ix] & ~loud[ix]))
            ix = np.where(routine & ~exc)[0]
            logs.append((ix, np.full(len(ix), day), np.full(len(ix), KIND_ROUTINE), ~wrong[ix],
                         np.zeros(len(ix), bool)))
        counted = exc | routine
        wrong[counted] = False
        cleared = routine | (exc & due)
        k = np.floor((day - (phase - W.BURN)) / L) + 1
        next_due = np.where(cleared, (phase - W.BURN + k * L).astype(int), next_due)
        slip_left[cleared] = -1
    loc = np.concatenate([x[0] for x in logs])
    order = np.lexsort((np.concatenate([x[1] for x in logs]), loc))
    log = dict(face=loc[order], day=np.concatenate([x[1] for x in logs])[order],
               kind=np.concatenate([x[2] for x in logs])[order], hit=np.concatenate([x[3] for x in logs])[order],
               silent_at_exc=np.concatenate([x[4] for x in logs])[order])
    faces = dict(cls=cls, v=v, L=L, held=held, released=released, hold_day=hold_day, release_day=release_day,
                 truth_wrong=wrong.copy())
    return faces, log


def simulate():
    return {c["name"]: simulate_centre(c) for c in W.CENTRES}


def truth(sim):
    """Private: the share of in-scope faces a full count at 06:00 on 7 December would find correct."""
    out = {}
    for name, (faces, _) in sim.items():
        ins = ~faces["held"] & ~faces["released"]
        out[name] = 100.0 * (1 - faces["truth_wrong"][ins].mean())
    return out


# ---------------------------------------------------------------------------------------------------------
# The main-path files: the location master, the pick-face count history and the centre register.
# ---------------------------------------------------------------------------------------------------------
LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def to_utc(day, minutes_after_midnight):
    """A local wall-clock time on the calendar date after trading day `day` (the count night), as UTC text."""
    d = W.day_date(day) + dt.timedelta(days=1)
    local = dt.datetime(d.year, d.month, d.day, tzinfo=LONDON) + dt.timedelta(minutes=int(minutes_after_midnight))
    return local.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def to_utc_day(day, minutes_from_six):
    """A local time inside trading day `day` (06:00 to 06:00), as UTC text."""
    d = W.day_date(day)
    local = dt.datetime(d.year, d.month, d.day, 6, tzinfo=LONDON) + dt.timedelta(minutes=int(minutes_from_six))
    return local.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


REASON_LOUD = (["SHP", "NEG", "EMP"], [0.52, 0.18, 0.30])
REASON_FALSE = (["OVR", "EMP"], [0.62, 0.38])


def count_rows(c, faces, log, assign, lines, rng):
    """One row per count task, in the order the WMS posted them."""
    code = c["code"]
    n = len(log["face"])
    unit = np.array([lines[assign["line"][f]]["unit"] for f in range(len(faces["cls"]))])
    cap = np.where(unit == "EA", rng.integers(12, 145, len(faces["cls"])), rng.integers(6, 49, len(faces["cls"])))
    face = log["face"]
    kind = log["kind"]
    hit = log["hit"]
    system = np.array([int(rng.integers(1, cap[f] + 1)) for f in face])
    counted = system.copy()
    reason = np.empty(n, dtype=object)
    reason[kind == KIND_ROUTINE] = "CYC"
    li = np.where(kind == KIND_LOUD)[0]
    reason[li] = rng.choice(REASON_LOUD[0], size=len(li), p=REASON_LOUD[1])
    fi = np.where(kind == KIND_FALSE)[0]
    reason[fi] = rng.choice(REASON_FALSE[0], size=len(fi), p=REASON_FALSE[1])
    mag = np.where(rng.random(n) < 0.62, 1, np.where(rng.random(n) < 0.55, 2, rng.integers(3, 13, n)))
    sign = np.where(rng.random(n) < 0.58, -1, 1)
    for i in np.where(~hit)[0]:
        r = reason[i]
        if r == "EMP" and kind[i] == KIND_LOUD:
            counted[i] = 0
        elif r == "NEG" and kind[i] == KIND_LOUD:
            system[i] = -int(rng.integers(1, 7))
            counted[i] = int(rng.integers(0, max(2, cap[face[i]] // 3)))
        elif r == "SHP" and kind[i] == KIND_LOUD:
            counted[i] = max(0, system[i] - mag[i])
            if counted[i] == system[i]:
                counted[i] = system[i] - 1
        else:
            counted[i] = system[i] + sign[i] * mag[i]
            if counted[i] < 0:
                counted[i] = system[i] + mag[i]
    # blind first count: occasionally miscounted, and any difference from the record draws a recount
    first = counted.copy()
    slip = rng.random(n) < 0.022
    first[slip] = counted[slip] + np.where(rng.random(slip.sum()) < 0.5, -1, 1) * rng.integers(1, 4, slip.sum())
    first = np.maximum(first, 0)
    recount = first != system
    counters = ["%s%04d" % (code[:2], x) for x in rng.choice(np.arange(1100, 9800), 31, replace=False)]
    sups = ["%sS%03d" % (code[:2], x) for x in rng.choice(np.arange(100, 990), 7, replace=False)]
    cnt_min = rng.integers(120, 331, n)                  # 02:00 to 05:30 local on the count night
    rows = []
    for i in range(n):
        d = int(log["day"][i])
        f = int(face[i])
        ln = lines[assign["line"][f]]
        if kind[i] == KIND_ROUTINE:
            created = to_utc_day(d, 16 * 60 + int(rng.integers(10, 50)))
        else:
            created = to_utc_day(d, int(rng.integers(30, 17 * 60)))
        counted_at = to_utc(d, int(cnt_min[i]))
        post_min = int(cnt_min[i]) + (int(rng.integers(6, 25)) if recount[i] else int(rng.integers(0, 3)))
        rows.append(dict(
            site=code, location=assign["loc"][f], line_no=ln["line_no"], reason_code=reason[i],
            created_utc=created, counted_utc=counted_at,
            counter_id=counters[int(rng.integers(len(counters)))],
            system_qty=int(system[i]), first_count_qty=int(first[i]),
            recount_qty=int(counted[i]) if recount[i] else "",
            supervisor_id=sups[int(rng.integers(len(sups)))] if recount[i] else "",
            confirmed_qty=int(counted[i]), uom=ln["unit"], variance_qty=int(counted[i] - system[i]),
            result="MATCH" if counted[i] == system[i] else "VARIANCE",
            posted_utc=to_utc(d, min(post_min, 359)), _hit=bool(hit[i]), _face=f, _day=d, _kind=int(kind[i])))
    return rows


def write_main(out, sim, assign, lines):
    rng = np.random.default_rng(W.QTY_SEED)
    allrows = []
    for c in W.CENTRES:
        faces, log = sim[c["name"]]
        rows = count_rows(c, faces, log, assign[c["name"]], lines, rng)
        allrows += rows
    for r in allrows:
        assert r["result"] == ("MATCH" if r["_hit"] else "VARIANCE")
    allrows.sort(key=lambda r: (r["posted_utc"], r["site"], r["location"]))
    seq = {}
    base = {c["code"]: 4100000 + 137000 * i for i, c in enumerate(W.CENTRES)}
    cols = ["count_task", "site", "location", "line_no", "reason_code", "created_utc", "counted_utc", "counter_id",
            "system_qty", "first_count_qty", "recount_qty", "supervisor_id", "confirmed_qty", "uom", "variance_qty",
            "result", "posted_utc"]
    by_created = sorted(range(len(allrows)), key=lambda i: (allrows[i]["created_utc"], allrows[i]["site"], allrows[i]["location"]))
    for i in by_created:
        s = allrows[i]["site"]
        seq[s] = seq.get(s, 0) + 1
        allrows[i]["count_task"] = "%s%07d" % (s, base[s] + seq[s] * 3 + (i % 3))
    path = os.path.join(out, FILES["counts"])
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in allrows:
            w.writerow([r[k] for k in cols])
    return allrows



OTHER_CLIENT = {"HNK": ("HPF", 210), "THU": ("MRV", 160)}   # other clients' pick faces in shared sites


def write_locations(out, sim, assign, lines):
    rng = np.random.default_rng(W.QTY_SEED + 1)
    cols = ["site", "location", "location_type", "zone", "client", "line_no", "slot_class", "pick_velocity",
            "status", "eff_from", "eff_to", "change_reason"]
    rows = []
    for c in W.CENTRES:
        faces, _ = sim[c["name"]]
        a = assign[c["name"]]
        zone = {"Ambient": "AMB", "Chilled": "CHL", "Frozen": "FRZ"}[c["regime"]]
        for f in range(len(faces["cls"])):
            ln = lines[a["line"][f]]
            v = "%.1f" % faces["v"][f]
            eff = W.START - dt.timedelta(days=int(rng.integers(8, 23)))
            if rng.random() < 0.18:
                eff = W.START - dt.timedelta(days=int(rng.integers(40, 700)))
            base = dict(site=c["code"], location=a["loc"][f], location_type="PICK", zone="%s-%s" % (zone, faces["cls"][f]),
                        client="THN", line_no=ln["line_no"], slot_class=faces["cls"][f], pick_velocity=v,
                        status="ACTIVE", eff_from=eff.isoformat(), eff_to="", change_reason="RESLOT")
            if faces["held"][f]:
                hd = W.day_date(int(faces["hold_day"][f]))
                rows.append(dict(base, eff_to=(hd - dt.timedelta(days=1)).isoformat()))
                rows.append(dict(base, status="RECALL" if rng.random() < 0.3 else "HOLD", eff_from=hd.isoformat(),
                                 change_reason="QA"))
            elif faces["released"][f]:
                rd = W.day_date(int(faces["release_day"][f]) )
                rows.append(dict(base, eff_to=rd.isoformat()))
                why = ["MERGE", "DELIST", "RESLOT"][int(rng.choice(3, p=[0.3, 0.45, 0.25]))]
                rows.append(dict(base, client="", line_no="", slot_class="", pick_velocity="", status="EMPTY",
                                 eff_from=(rd + dt.timedelta(days=1)).isoformat(), change_reason=why))
            else:
                rows.append(base)
        # reserve locations above the pick faces, Thornacre stock, some relabelled after re-racking
        n_res = int(len(faces["cls"]) * 0.42)
        aisles = a["aisles"]
        res_codes = ["%02d-%03d-%d" % (x, b, lv) for x in range(11, 11 + aisles) for b in range(1, 56) for lv in (3, 4, 5)]
        pick = rng.choice(len(res_codes), size=n_res, replace=False)
        for j in pick:
            code = res_codes[j]
            li = a["line"][int(rng.integers(len(a["line"])))]
            eff = D2(2025, 3, 3) + dt.timedelta(days=int(rng.integers(0, 420)))
            base = dict(site=c["code"], location=code, location_type="RESV", zone="%s-R" % zone, client="THN",
                        line_no=lines[li]["line_no"], slot_class="", pick_velocity="", status="ACTIVE",
                        eff_from=eff.isoformat(), eff_to="", change_reason="")
            if rng.random() < 0.05:
                old = "R" + code
                ch = W.START + dt.timedelta(days=int(rng.integers(10, 170)))
                rows.append(dict(base, location=old, eff_to=(ch - dt.timedelta(days=1)).isoformat()))
                rows.append(dict(base, eff_from=ch.isoformat(), change_reason="RELABEL"))
            else:
                rows.append(base)
        if c["code"] in OTHER_CLIENT:
            cl, k = OTHER_CLIENT[c["code"]]
            for j in range(k):
                code = "%02d-%03d-%d" % (81 + j // 110, (j // 2) % 55 + 1, 1 + j % 2)
                rows.append(dict(site=c["code"], location=code, location_type="PICK", zone="%s-X" % zone, client=cl,
                                 line_no="", slot_class=["A", "B", "C"][int(rng.integers(3))], pick_velocity="",
                                 status="ACTIVE", eff_from=(W.START - dt.timedelta(days=int(rng.integers(20, 300)))).isoformat(),
                                 eff_to="", change_reason="RESLOT"))
    rows.sort(key=lambda r: (r["site"], r["location"], r["eff_from"]))
    with open(os.path.join(out, FILES["locations"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([r[k] for k in cols])
    return rows


def D2(y, m, d):
    return dt.date(y, m, d)


CENTRE_TOWNS = {"HNK": ("Hinckley", "LE10"), "DAV": ("Daventry", "NN11"), "BEL": ("Bellshill", "ML4"),
                "THU": ("Grays", "RM20"), "MAG": ("Magor", "NP26"), "WAR": ("Warrington", "WA5"),
                "AVO": ("Avonmouth", "BS11"), "DON": ("Doncaster", "DN4")}


def write_centres(out):
    cols = ["site", "centre", "postcode_district", "country", "temperature_regime", "thornacre_depot", "wms_instance",
            "client_since", "shared_site"]
    since = {"HNK": "2014-03-02", "DAV": "2017-09-10", "BEL": "2015-05-17", "THU": "2012-10-07", "MAG": "2019-02-24",
             "WAR": "2016-06-12", "AVO": "2013-08-04", "DON": "2018-11-11"}
    with open(os.path.join(out, FILES["centres"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for c in W.CENTRES:
            w.writerow([c["code"], c["name"], CENTRE_TOWNS[c["code"]][1], c["country"], c["regime"].upper(), c["depot"],
                        "WMS-%s" % ("N" if c["code"] in ("BEL", "WAR", "DON") else "S"), since[c["code"]],
                        "Y" if c["code"] in OTHER_CLIENT else "N"])
