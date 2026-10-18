"""task165 pack: every file under target/, written from the world and the simulation.

File names follow the systems' own export conventions; the main call reads the AVL exports, the register, the
revision log, the storm log and the two governing documents."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import common as K
import postprocess as PP
import records as R
import world as Wd

BRINE_KG_L = 1.18      # plant brine, kilograms a litre
PREWET_L_T = 40.0      # the tandems' pre-wet rate, litres of brine a tonne of rock salt
F_LEGACY = "avl_legacy_segment_shift_2021-11-01_2023-03-31.csv"
F_PASSES = "telematics_segment_passes_2023-10-01_2026-09-23.parquet"
F_XWALK = "gis_segment_crosswalk_2023.csv"
F_REGISTER = "winter_route_register_2026-09-14.csv"
F_REVLOG = "route_audit_revision_log.csv"
F_STORM = "storm_log_2021-22_to_2025-26.xlsx"
F_FLEET = "fleet_units_2026-09.csv"
F_QRT = "qrt_frequent_network_2026_streets.xlsx"
F_LOADING = "yard_loading_log_2023-11_2026-03.csv"
F_PELLARD = "kettlewood_material_returns_2023-24_to_2025-26.xlsx"
F_DOMES = "salt_dome_register.csv"
F_SCALE = "scale_house_log_2026-08-24_to_2026-09-24.xlsx"
F_DISPATCH1 = "northgrit_dispatch_2026-10_issued_2026-09-14.csv"
F_DISPATCH2 = "northgrit_dispatch_2026-10_issued_2026-09-21.csv"
F_SURVEY = "dome_stock_survey_2026-09.pdf"
F_PLAN = "winter_maintenance_plan_2026-27.pdf"
F_PROC = "road_salt_procurement_procedure_RO-PR-07.pdf"
F_DICT = "data_dictionary.xlsx"
F_MANIFEST = "export_manifest.csv"
F_TIMESHEETS = "yard_timesheets_2025-26.csv"
F_BRINE = "brine_production_log_2023-10_to_2026-09.csv"


def _csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())


# ------------------------------------------------------------------------------------------------------ AVL legacy
def legacy_rows(W, S):
    """Segment-by-shift summaries, local time, kilograms, legacy segment ids (split segments merged)."""
    agg = {}
    for p in S.passes:
        if p["winter"] not in K.LEGACY_WINTERS:
            continue
        for r in p["rows"]:
            t = r["entry"]
            if 7 <= t.hour < 19:
                sd, sh = t.date(), "DAY"
            else:
                sd = t.date() if t.hour >= 19 else t.date() - dt.timedelta(days=1)
                sh = "NIGHT"
            s = W.by_id[r["segment_id"]]
            key = (sd, sh, s["legacy_id"], p["route_code"])
            a = agg.setdefault(key, {"kg": 0.0, "passes": 0, "yard": W.circuits[p["route_code"]]["yard"],
                                     "matl": "SAND/SALT" if s["pool"] == "P3" else "SALT"})
            a["kg"] += r["t"] * 1000.0
            a["passes"] += 1
    rows = []
    for (sd, sh, seg, rc), a in agg.items():
        rows.append((sd.isoformat(), sh, a["yard"], rc, seg, a["passes"], a["matl"], int(round(a["kg"]))))
    rows.sort(key=lambda x: (x[0], 0 if x[1] == "DAY" else 1, x[2], x[3], x[4]))
    return rows


# ------------------------------------------------------------------------------------------------------ telematics
def pass_rows(W, S):
    """One row per spreader pass over one segment: UTC, tonnes, run reference. The M410 controllers report a run's
    total, and the platform writes it on every segment row of the run."""
    rng = np.random.default_rng(W.seed + 20)
    out = []
    runs = 0
    for p in list(S.passes) + list(S.patrols):
        if p["winter"] in K.LEGACY_WINTERS and p.get("day") is None:
            continue
        if p["contract"]:
            continue
        rows = p["rows"]
        if not rows:
            continue
        day = rows[0]["entry"].date()
        unit = p["unit"]
        ctl = W.controller_on(unit, day)
        tandem = W.unit_by_id[unit]["class"] == "TANDEM"
        lpt = PREWET_L_T if tandem else 0.0                         # pre-wet brine, litres a tonne of salt
        i = 0
        while i < len(rows):
            n = int(rng.choice([1, 2, 3], p=[0.45, 0.40, 0.15])) if ctl == "M410" else int(rng.integers(1, 7))
            chunk = rows[i:i + n]
            runs += 1
            ref = "%s-%s-%05d" % (unit, chunk[0]["entry"].strftime("%y%m%d"), runs % 100000)
            tot = sum(r["t"] for r in chunk)
            tot_l = round(tot * lpt, 1)
            for r in chunk:
                s = W.by_id[r["segment_id"]]
                if ctl == "M410":
                    # the older controller reports the run's material as one mass, salt and brine together
                    val, lit = tot + tot_l * BRINE_KG_L / 1000.0, tot_l
                else:
                    val, lit = r["t"], round(round(r["t"], 3) * lpt, 1)
                out.append({"unit_id": unit, "route_code": p["route_code"], "segment_id": r["segment_id"],
                            "entry_utc": K.to_utc(r["entry"]), "exit_utc": K.to_utc(r["exit"]),
                            "material_code": "SS" if s["pool"] == "P3" else "RS",
                            "applied_t": round(val, 3), "prewet_l": float(lit), "run_ref": ref})
            i += n
    out.sort(key=lambda r: (r["entry_utc"], r["unit_id"], r["segment_id"]))
    return out


def write_passes(path, rows):
    tbl = pa.table({
        "unit_id": pa.array([r["unit_id"] for r in rows], pa.string()),
        "route_code": pa.array([r["route_code"] for r in rows], pa.string()),
        "segment_id": pa.array([r["segment_id"] for r in rows], pa.string()),
        "entry_utc": pa.array([r["entry_utc"].replace(tzinfo=K.UTC) for r in rows], pa.timestamp("s", tz="UTC")),
        "exit_utc": pa.array([r["exit_utc"].replace(tzinfo=K.UTC) for r in rows], pa.timestamp("s", tz="UTC")),
        "material_code": pa.array([r["material_code"] for r in rows], pa.string()),
        "applied_t": pa.array([r["applied_t"] for r in rows], pa.float64()),
        "prewet_l": pa.array([r["prewet_l"] for r in rows], pa.float64()),
        "run_ref": pa.array([r["run_ref"] for r in rows], pa.string()),
    })
    pq.write_table(tbl, path, compression="snappy", use_dictionary=True, write_statistics=True,
                   row_group_size=131072)


# ------------------------------------------------------------------------------------------------------ register etc.
FREQ_ROUTES_NEW = ["41", "43", "46", "48", "52", "55", "57", "61", "64"]
FREQ_ROUTES_OLD = ["2", "4", "7", "10", "14", "22"]


def transit_tags(W):
    """Frequent routes on each segment (the register's frequent_transit field)."""
    rng = np.random.default_rng(W.seed + 21)
    tags = {}
    streets_new = sorted({s["street"] for s in W.segments if s["pool"] == "NEW"})
    for i, st in enumerate(streets_new):
        r = FREQ_ROUTES_NEW[i % len(FREQ_ROUTES_NEW)]
        r2 = FREQ_ROUTES_NEW[(i * 7 + 3) % len(FREQ_ROUTES_NEW)] if rng.random() < 0.25 else None
        for s in W.segments:
            if s["street"] == st and s["pool"] == "NEW":
                tags[s["segment_id"]] = r if not r2 or r2 == r else "%s, %s" % tuple(sorted([r, r2], key=int))
    inner = sorted({s["street"] for s in W.segments if s["pool"] == "P1IN"})
    for i, st in enumerate(inner):
        for s in W.segments:
            if s["street"] == st and s["pool"] == "P1IN":
                tags[s["segment_id"]] = FREQ_ROUTES_OLD[i % len(FREQ_ROUTES_OLD)]
    for s in W.segments:
        if s["pool"] == "MOVE" and s["reason"] == "transit":
            tags[s["segment_id"]] = "14" if s["batch"] == "B" else "22"
    for s in W.segments:
        if s["pool"] == "ART":
            if stable_pick(s["street"], 3) == 0:
                tags[s["segment_id"]] = FREQ_ROUTES_OLD[stable_pick(s["street"] + "r", len(FREQ_ROUTES_OLD))]
    return tags


def stable_pick(key, n):
    return K.stable_int(key) % n


def register_rows(W):
    tags = transit_tags(W)
    rows = []
    for s in sorted(W.segments, key=lambda s: s["segment_id"]):
        yard, rc = s["yard"], s["route_code"]
        if rc in W.realigned:
            yard = "KLV"
            rc = W.realigned_codes[rc]
        op = "CONTRACT" if rc in W.contract_circuits else "CITY"
        prio = {"ART": 1, "P1IN": 1, "MOVE": 1, "NEW": 1, "P2": 2, "P3": 3}[s["pool"]]
        audit = dt.date(2026, 8, 28) if s["pool"] == "NEW" else dt.date(2026, 6, 15) - dt.timedelta(
            days=K.stable_int(s["segment_id"]) % 120)
        rows.append((s["segment_id"], s["street"], s["from_street"], s["to_street"], yard, rc, s["func_class"], prio,
                     s["lanes"], "%.2f" % s["centreline_km"], "%.2f" % s["lane_km"], tags.get(s["segment_id"], ""), op,
                     audit.isoformat()))
    return rows


REASONS = {
    "hill": {"A": "Council motion 2022-31, Garrow Hill and Ridge escarpment streets",
             "C": "Council motion 2024-19, winter service petitions, Ward 6"},
    "school": {"A": "School bus route review 2022-23 (QDSB transportation)",
               "C": "School bus route review 2024-25 (QDSB transportation)",
               "D": "School bus route review 2025-26 (QDSB transportation)"},
    "hospital": {"B": "Access to Quellbrook General, east entrance",
                 "C": "Ambulance access review (Paramedic Services)"},
    "transit": {"B": "QRT Route 14 to 15-minute service", "D": "QRT Route 22 to 15-minute service"},
}
AUDIT_USERS = ["rta02", "rta05", "rta07", "rta11"]


def _weekday(d, step):
    while d.weekday() >= 5:
        d += dt.timedelta(days=step)
    return d


def _sittings(key, n, eff):
    """The entry dates of one change of n segments effective eff: the audit keys a change in sittings of 40 to 90
    segments, the first two to six weeks ahead, the next a few working days apart, and finishes one change in four
    in the week after it took effect. Each sitting is one user's."""
    size = 40 + K.stable_int(key, "size") % 51
    k = max(1, -(-n // size))
    day = eff - dt.timedelta(days=14 + K.stable_int(key, "lead") % 29)
    out = []
    for i in range(k):
        out.append(_weekday(day, -1))
        day = out[-1] + dt.timedelta(days=1 + K.stable_int(key, "gap", i) % 5)
    if k > 1 and K.stable_int(key, "late") % 4 == 0:
        out[-1] = _weekday(eff + dt.timedelta(days=2 + K.stable_int(key, "after") % 6), 1)
    users = [AUDIT_USERS[K.stable_int(key, "user", i) % 4] for i in range(k)]
    per = -(-n // k)
    return [(out[i // per], users[i // per]) for i in range(n)]


def revision_rows(W):
    rng = np.random.default_rng(W.seed + 22)
    changes = {}          # (effective date, reason) -> [(segment, rows)]
    for s in W.segments:
        if s["pool"] == "MOVE":
            d, txt = K.MOVE_DATES[s["batch"]], REASONS[s["reason"]][s["batch"]]
        elif s["pool"] == "NEW":
            d, txt = K.REDESIGN, "QRT frequent network redesign, launch 30 August 2026"
        else:
            continue
        changes.setdefault((d, txt), []).append((s, [("PRIORITY", "2", "1"),
                                                     ("ROUTE", s["route_code_p2"], s["route_code_p1"])]))
    for rc in W.contract_circuits:
        txt = "Arterial winter maintenance contract RW-2023-07 (Kettlewood Road Services)"
        for sid in W.circuits[rc]["segments"]:
            changes.setdefault((dt.date(2023, 11, 1), txt), []).append((W.by_id[sid], [("OPERATOR", "CITY", "CONTRACT")]))
    for rc in W.realigned:
        txt = "Yard boundary realignment, Mapleford to Kelvin Road"
        for sid in W.circuits[rc]["segments"]:
            changes.setdefault((K.REALIGN, txt), []).append((W.by_id[sid], [("YARD", "MPF", "KLV"),
                                                                             ("ROUTE", rc, W.realigned_codes[rc])]))
    rows = []
    for (d, txt), segs in sorted(changes.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        segs = sorted(segs, key=lambda x: (x[0]["street"], x[0]["segment_id"]))
        for (s, fields), (ent, user) in zip(segs, _sittings(txt, len(segs), d)):
            for field, old, new in fields:
                rows.append((min(ent, dt.date(2026, 9, 14)), d, s["segment_id"], field, old, new, txt, user))
    # older housekeeping entries, keyed one at a time: new subdivision collectors taken into Priority 2
    p2 = [s for s in W.segments if s["pool"] == "P2"]
    for s in [p2[i] for i in rng.choice(len(p2), 30, replace=False)]:
        d = dt.date(2020, 10, 15) + dt.timedelta(days=int(rng.integers(0, 400)))
        ent = _weekday(d - dt.timedelta(days=int(K.stable_int(s["segment_id"], "lag") % 52) - 9), -1)
        rows.append((ent, d, s["segment_id"], "PRIORITY", "3", "2", "Assumed from developer, subdivision collector",
                     AUDIT_USERS[K.stable_int(s["segment_id"], "user") % 4]))
    # change numbers run in the order the entries were keyed
    rows.sort(key=lambda r: (r[0], r[1], r[6], r[2], r[3]))
    return [("RA-%05d" % (10421 + i), d.isoformat(), sid, field, old, new, txt, user, ent.isoformat())
            for i, (ent, d, sid, field, old, new, txt, user) in enumerate(rows)]


def crosswalk_rows(W):
    rows = []
    for sp in sorted(W.splits, key=lambda x: x["old"]):
        for nid, sh in zip(sp["new"], sp["share"]):
            rows.append((sp["old"], nid, "%.4f" % sh, "SPLIT", "2023-08-21"))
    # every other legacy id carried over unchanged
    for s in sorted(W.segments, key=lambda s: s["segment_id"]):
        if s["legacy_id"] == s["segment_id"]:
            rows.append((s["segment_id"], s["segment_id"], "1.0000", "SAME", "2023-08-21"))
    rows.sort()
    return rows


def fleet_rows(W):
    rows = []
    for u in sorted(W.units, key=lambda u: u["unit_id"]):
        if u["home_circuit"] in W.contract_circuits:
            continue
        yard = u["yard"]
        hc = u["home_circuit"]
        if hc in W.realigned:
            yard, hc = "KLV", W.realigned_codes[hc]
        year = 2009 + K.stable_int(u["unit_id"]) % 13 if u["controller"] == "M410" else 2014 + K.stable_int(u["unit_id"]) % 11
        rows.append((u["unit_id"], yard, u["class"], hc, year, "M720" if u["retrofit"] else u["controller"],
                     u["retrofit"].isoformat() if u["retrofit"] else ""))
    return rows
