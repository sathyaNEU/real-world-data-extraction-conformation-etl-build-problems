"""Independent verifier: reads only the shipped bundle (target/) and the goldens' figures, on its own code path (no
import of the generator's modules), and recomputes the call, the saving and both asks.

    python3 task153/generator/verify.py [target] [golden]"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from xml.etree import ElementTree as ET_
from zoneinfo import ZoneInfo

CHI, NYC, Z = ZoneInfo("America/Chicago"), ZoneInfo("America/New_York"), dt.timezone.utc
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def xlsx_rows(path, sheet_name):
    """A worksheet's rows as lists of raw strings, read straight from the package (no workbook library)."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET_.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        wb = ET_.fromstring(z.read("xl/workbook.xml"))
        names = [s.get("name") for s in wb.find("m:sheets", NS)]
        k = names.index(sheet_name) + 1
        root = ET_.fromstring(z.read("xl/worksheets/sheet%d.xml" % k))
    out = []
    for row in root.iter("{%s}row" % NS["m"]):
        vals = {}
        for c in row.findall("m:c", NS):
            ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
            col = 0
            for ch in ref:
                col = col * 26 + ord(ch) - 64
            v = c.find("m:v", NS)
            if v is None:
                continue
            vals[col] = shared[int(v.text)] if c.get("t") == "s" else v.text
        out.append([vals.get(i) for i in range(1, max(vals) + 1)] if vals else [])
    return out


def excel_date(x):
    return dt.date(1899, 12, 30) + dt.timedelta(days=int(float(x)))


def unit_no(name):
    m = re.match(r"^(?:D|KSC-|HSS )(\d{4})(?: |$)", name)
    return int(m.group(1)) if m else None


def holidays():
    return {dt.date(2026, 5, 25), dt.date(2026, 7, 3), dt.date(2026, 9, 7)}


def wdays(a, b):
    return sum(1 for i in range((b - a).days + 1) if (a + dt.timedelta(days=i)).weekday() < 5 and
               (a + dt.timedelta(days=i)) not in holidays())


def golden(target):
    units = {}
    rows = xlsx_rows(os.path.join(target, "fleet_units_2026-08.xlsx"), "Units")
    specs = {r[0]: float(r[2]) for r in xlsx_rows(os.path.join(target, "fleet_units_2026-08.xlsx"), "Model Specs")[1:]}
    for r in rows[1:]:
        units[int(float(r[0]))] = dict(yard=r[2], model=r[5], active=r[8] == "Active", tank=specs[r[5]])
    dev = {}
    with open(os.path.join(target, "telematics_device_assignments.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            dev[r["Device Serial"]] = unit_no(r["Vehicle"])
    who = lambda name, serial: unit_no(name) or dev.get(serial)
    zone = {"Memphis": CHI, "Jackson": CHI, "Nashville": CHI, "Cookeville": CHI, "Knoxville": NYC, "Blountville": NYC}
    days = collections.defaultdict(list)
    with open(os.path.join(target, "vehicle_days_2024-09-01_2026-08-27.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Day"] < "2026-03-01":
                continue
            u = who(r["Vehicle"], r["Device Serial"])
            tz = CHI if r["TZ"] == "CT" else NYC
            d = dt.date.fromisoformat(r["Day"])
            t0 = dt.datetime.combine(d, dt.time.fromisoformat(r["First Ignition"]), tz).astimezone(Z)
            t1 = dt.datetime.combine(d, dt.time.fromisoformat(r["Last Ignition Off"]), tz).astimezone(Z)
            days[u].append((t0, t1, float(r["Fuel Used (gal)"])))
    ev = collections.defaultdict(list)
    with open(os.path.join(target, "geofence_events_2026-03-01_2026-08-27.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            u = who(r["Vehicle"], r["Device Serial"])
            if u in units and r["Geofence"] == "KSC %s Yard" % units[u]["yard"]:
                ev[u].append((dt.datetime.strptime(r["Event Time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=Z), r["Event"]))
    # the reserve: what the 2025 islands put aboard sleepers coming back (fills over three quarters of a 300-gal tank)
    seen, big = set(), []
    with open(os.path.join(target, "fms_island_transactions_2025.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if (r["Site"], r["Txn"]) in seen:
                continue
            seen.add((r["Site"], r["Txn"]))
            u = int(r["Unit"])
            if units[u]["model"] == "T68SL" and float(r["Gallons"]) >= 225:
                big.append(float(r["Gallons"]) / 300.0)
    keep = sum(big) / len(big)
    base0, base1 = dt.date(2026, 6, 29), dt.date(2026, 8, 23)
    k = wdays(dt.date(2026, 9, 14), dt.date(2026, 11, 8)) / wdays(base0, base1)
    draw = collections.defaultdict(float)
    for u, info in units.items():
        if not info["active"]:
            continue
        E = sorted(ev[u])
        stays, start = [], None
        for t, kind in E:
            if kind == "Enter":
                start = t
            else:
                stays.append((start, t))
                start = None
        if start is not None:
            stays.append((start, None))
        D = days[u]
        # driving time of each day outside the yard, to apportion its fuel
        def outside(t0, t1):
            tot = (t1 - t0).total_seconds()
            for (a, b) in stays:
                a_ = a or dt.datetime(1990, 1, 1, tzinfo=Z)
                b_ = b or dt.datetime(2100, 1, 1, tzinfo=Z)
                lo, hi = max(a_, t0), min(b_, t1)
                if hi > lo:
                    tot -= (hi - lo).total_seconds()
            return tot
        drive = [outside(t0, t1) for (t0, t1, f) in D]
        prev_exit = None
        for (a, b) in stays:
            if a is None:
                prev_exit = b
                continue
            if prev_exit is not None:
                fuel = 0.0
                for (t0, t1, f), dv in zip(D, drive):
                    if dv <= 0 or t1 <= prev_exit or t0 >= a:
                        continue
                    lo, hi = max(t0, prev_exit), min(t1, a)
                    fuel += f * outside(lo, hi) / dv
                if base0 <= a.astimezone(zone[info["yard"]]).date() <= base1:
                    draw[info["yard"]] += min(fuel, info["tank"] * keep)
            prev_exit = b
    draw = {y: g * k for y, g in draw.items()}
    loads = {y: int(math.floor(g / 8000.0 + 1e-9)) for y, g in draw.items()}
    return draw, loads, keep


def ask_a(target):
    """Each account's diesel purchases by the local day they were made; duplicate postings and their credits out."""
    out = collections.defaultdict(float)
    with open(os.path.join(target, "riverbend_direct_bill_2024-09_2026-08.csv"), encoding="utf-8") as fh:
        rb = list(csv.DictReader(fh))
    gone = {r["REF_TRAN_ID"] for r in rb if r["REF_TRAN_ID"]}
    for r in rb:
        if r["PROD_CD"] == "01" and not r["REF_TRAN_ID"] and r["TRAN_ID"] not in gone:
            t = dt.datetime.strptime(r["TRAN_DATE_TIME"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=Z).astimezone(CHI)
            out[("West", t.year, t.month)] += float(r["QTY"])
    rows = xlsx_rows(os.path.join(target, "crossroads_transactions_2024-09_2026-08.xlsx"), "Transactions")
    head = rows[0]
    ix = {h: k for k, h in enumerate(head)}
    body = [r + [None] * (len(head) - len(r)) for r in rows[1:]]
    gone = {r[ix["Reverses"]] for r in body if r[ix["Reverses"]]}
    for r in body:
        if r[ix["Product"]] != "Diesel" or r[ix["Reverses"]] or r[ix["Reference"]] in gone:
            continue
        d = excel_date(r[ix["Transaction Date"]])
        if int(r[ix["Transaction Time"]][:2]) >= 22:
            d -= dt.timedelta(days=1)
        out[("Central", d.year, d.month)] += float(r[ix["Quantity"]])
    weeks, recs = set(), []
    with open(os.path.join(target, "smpm_card_activity_2024-09_2026-08.txt"), encoding="utf-8") as fh:
        skip = False
        for ln in fh:
            ln = ln.rstrip("\r\n")
            if ln[0] == "H":
                skip = ln[8:16] in weeks           # the same week received again
                weeks.add(ln[8:16])
            elif ln[0] in "DC" and not skip:
                recs.append(ln)
    gone = {ln[108:121] for ln in recs if ln[0] == "C"}
    for ln in recs:
        if ln[0] != "D" or ln[55:59] != "DSL2" or ln[1:14] in gone:
            continue
        d = dt.datetime.strptime(ln[14:22], "%Y%m%d").date()
        if int(ln[22:24]) >= 22:
            d -= dt.timedelta(days=1)
        out[("East", d.year, d.month)] += int(ln[59:68]) / 1000.0
    return out


def ask_b(target):
    post = {}
    with open(os.path.join(target, "overton_rack_postings_2024-09_2026-08.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            post[(r["Terminal"].upper(), r["Effective Date"])] = float(r["Overton Posted"])
    load = {}
    with open(os.path.join(target, "overton_deliveries_2025.csv"), encoding="utf-8") as fh:
        for r in sorted(csv.DictReader(fh), key=lambda r: dt.datetime.strptime(r["Delivered (CT)"], "%m/%d/%Y %H:%M")):
            if r["Terminal BOL"] not in load:
                load[r["Terminal BOL"]] = r
    credited = set()
    with open(os.path.join(target, "overton_credit_memos_2025.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            credited.add(r["Ref Invoice"])
    out = collections.defaultdict(lambda: [0.0, 0.0])

    def month(r):
        d = dt.datetime.strptime(r["Delivered (CT)"], "%m/%d/%Y %H:%M")
        return (r["Ship To"].split()[1], d.year, d.month)
    for b, r in load.items():
        lifted = dt.datetime.strptime(r["Lifted (CT)"], "%m/%d/%Y %H:%M")
        eff = (lifted + dt.timedelta(hours=6)).date()          # 6 pm Central posts the next day's rack
        out[month(r)][0] += float(r["BOL Net Gal"])
        out[month(r)][1] -= float(r["BOL Net Gal"]) * post[(r["Terminal"], eff.isoformat())]
    with open(os.path.join(target, "overton_invoices_2025.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["Class"] != "TAX" and r["Invoice"] not in credited:
                out[month(load[r["Terminal BOL"]])][1] += float(r["Amount"])
    return out


def main(target, golden_dir):
    F = json.load(open(os.path.join(os.path.dirname(os.path.abspath(target)), "generator", "figures.json")))
    draw, loads, keep = golden(target)
    bad = []
    if loads != F["call"]["loads_by_yard"] or sum(loads.values()) != F["call"]["total_loads"]:
        bad.append("loads %s" % loads)
    for y, g in draw.items():
        if format(int(round(g)), ",") != F["steps"]["draw_gal"][y]:
            bad.append("draw %s %.1f against %s" % (y, g, F["steps"]["draw_gal"][y]))
    charge = {"West": 0.119, "Central": 0.099, "East": 0.127}
    acct = {"Memphis": "West", "Jackson": "West", "Nashville": "Central", "Cookeville": "Central", "Knoxville": "East",
            "Blountville": "East"}
    saving = sum(loads[y] * 8000 * (charge[acct[y]] - 0.019) for y in loads)
    if format(int(round(saving)), ",") != F["call"]["saving_usd"]:
        bad.append("saving %.2f" % saving)
    A = ask_a(target)
    for key, v in F["answers"]["ask_a"].items():
        a, ym = key.split()
        y, m = (int(x) for x in ym.split("-"))
        if format(int(round(A[(a, y, m)])), ",") != v:
            bad.append("ask A %s %.3f against %s" % (key, A[(a, y, m)], v))
    B = ask_b(target)
    for key, v in F["answers"]["ask_b"].items():
        yd, ym = key.split()
        y, m = (int(x) for x in ym.split("-"))
        g, usd = B[(yd, y, m)]
        if format(int(round(g)), ",") != v["net_gal"] or format(int(round(usd)), ",") != v["usd"]:
            bad.append("ask B %s %.1f %.2f against %s" % (key, g, usd, v))
    print("verify: loads %s (%d), reserve %.4f, saving %.0f; ask A %d figures, ask B %d figures; %s" % (
        loads, sum(loads.values()), 1 - keep, saving, len(F["answers"]["ask_a"]), 2 * len(F["answers"]["ask_b"]),
        "all reproduce" if not bad else "MISMATCH: " + "; ".join(bad)))
    if bad:
        raise SystemExit("verify failed")


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, g)
