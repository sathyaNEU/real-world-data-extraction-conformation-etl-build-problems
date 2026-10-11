"""Independent verifier for task180: reads only ../target/, shares no code with golden.py.

Daily consumption is rebuilt by differencing reads on one serial, spreading any gap evenly over its
days and bridging meter exchanges with the exchange reads; weeks are summed from days.
"""
import csv
import datetime as dt
import math
import os
import sys
from collections import defaultdict

import numpy as np
import openpyxl
import pyarrow.parquet as pq

T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "target")
EXPECT = {"referrals": {"INV": 19, "NRN": 14, "FRS": 11, "ELG": 35, "SPY": 16, "LOC": 8, "CAI": 54, "SKY": 17},
          "history": {"INV": (64, 26, 40.6), "NRN": (38, 22, 57.9), "FRS": (30, 14, 46.7), "ELG": (71, 37, 52.1),
                      "SPY": (33, 15, 45.5), "LOC": (22, 15, 68.2), "CAI": (41, 17, 41.5), "SKY": (29, 13, 44.8)},
          "capacity": {"INV": 690, "NRN": 552, "FRS": 552, "ELG": 690, "SPY": 552, "LOC": 414, "CAI": 552, "SKY": 414}}


def f(prefix):
    return os.path.join(T, next(x for x in os.listdir(T) if x.startswith(prefix)))


def sheet_rows(path, name):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[name]
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, r in enumerate(rows) if r and r[0] in ("mpan_core", "account_ref", "appeal_ref",
                                                                 "officer", "date", "related_mpan_core"))
    hdr = rows[hi]
    return [dict(zip(hdr, r)) for r in rows[hi + 1:] if r and r[0] is not None]


def main():
    run = dt.date(2026, 12, 7)
    a0 = run - dt.timedelta(56)
    h0 = a0 - dt.timedelta(728)
    reg = f("supply_point_register")
    sup = sheet_rows(reg, "Supplies")
    prim = {r["mpan_core"]: r for r in sup}
    for r in sheet_rows(reg, "Related metering points"):
        p = prim[r["primary_mpan_core"]]
        sup.append({"mpan_core": r["related_mpan_core"], "uprn": p["uprn"], "rp_patch": p["rp_patch"],
                    "payment_method": p["payment_method"]})
    exch = {r["mpan_core"]: r for r in sheet_rows(reg, "Meter exchanges")}
    stations = {}
    import json
    for p in json.load(open(f("patch_weather_stations")))["patches"]:
        stations[p["rp_patch"]] = p["station"]
    hdd = defaultdict(dict)
    with open(f("station_degree_days")) as fh:
        for r in csv.DictReader(fh):
            hdd[r["station"]][dt.date.fromisoformat(r["date"])] = float(r["hdd_15_5c"])
    excl = set()
    with open(f("change_of_occupier")) as fh:
        for r in csv.DictReader(fh):
            d = dt.datetime.strptime(r["event_date"], "%d/%m/%Y").date()
            if h0 <= d < run:
                excl.add(int(r["uprn"]))
    with open(f("heating_measures")) as fh:
        for r in csv.DictReader(fh):
            d = dt.datetime.strptime(r["commissioned_on"], "%d %b %Y").date()
            if h0 <= d < run and r["measure"] in ("Air source heat pump", "High heat retention storage heaters"):
                excl.add(int(r["uprn"]))
    tbl = pq.read_table(f("smart_daily_reads")).to_pydict()
    by = defaultdict(list)
    for m, s, d, v in zip(tbl["mpan_core"], tbl["meter_serial"], tbl["read_date"], tbl["cumulative_kwh"]):
        by[m].append((d, s, v))
    counts = defaultdict(int)
    nday = (run - h0).days
    for r in sup:
        if r["payment_method"] != "Credit" or int(r["uprn"]) in excl:
            continue
        rd = sorted(by[r["mpan_core"]])
        daily = np.zeros(nday)
        e = exch.get(r["mpan_core"])
        for (d1, s1, v1), (d2, s2, v2) in zip(rd, rd[1:]):
            if d2 <= h0 or d1 >= run:
                continue
            if s1 != s2:
                used = (e["final_read_kwh"] - v1) + (v2 - e["initial_read_kwh"])
            else:
                used = v2 - v1
            n = (d2 - d1).days
            for k in range(n):
                day = d1 + dt.timedelta(k)
                if h0 <= day < run:
                    daily[(day - h0).days] += used / n
        wk = daily.reshape(112, 7).sum(1)
        st = stations[r["rp_patch"]]
        hw = np.array([sum(hdd[st][h0 + dt.timedelta(7 * i + j)] for j in range(7)) for i in range(112)])
        b = np.polyfit(hw[:104], wk[:104], 1)
        exp = np.polyval(b, hw[104:])
        act = wk[104:]
        if 1 - act.sum() / exp.sum() >= 0.30 and (act < exp).all():
            counts[r["rp_patch"]] += 1
    ref = {p: counts.get(p, 0) for p in EXPECT["referrals"]}
    ok = ref == EXPECT["referrals"]
    print("referrals", ref, "OK" if ok else "MISMATCH")

    # history
    patch = {int(r["uprn"]): r["rp_patch"] for r in sup}
    fo = list(csv.DictReader(open(f("fieldops_visits"))))
    rekeyed = {r["legacy_job_no"] for r in fo if r["legacy_job_no"]}
    over = {r["job_reference"] for r in sheet_rows(f("tamper_appeals"), "Register") if r["decision"] == "Overturned"}
    vis = []
    for r in csv.DictReader(open(f("fieldlink_visits"))):
        if r["JobNo"] in rekeyed:
            continue
        d = dt.datetime.strptime(r["VisitDate"], "%d/%m/%Y").date()
        o = r["Outcome"]
        if o == "CONF" and r["JobNo"] in over:
            o = "NFF"
        vis.append((d, int(r["UPRN"]), o))
    for r in fo:
        t = dt.datetime.strptime(r["visit_start_utc"], "%Y-%m-%dT%H:%M:%SZ")
        d = t.date()        # visits run 08:00 to 16:00 local, so the UTC date is the local date
        o = {"DIV-CONFIRMED": "CONF", "NO-FAULT": "NFF", "NO-ACCESS": "NOACC"}[r["outcome"]]
        if o == "CONF" and (r["job_id"] in over or r["legacy_job_no"] in over):
            o = "NFF"
        vis.append((d, int(r["uprn"]), o))
    win = [(dt.date(2023, 10, 1), dt.date(2024, 3, 31)), (dt.date(2024, 10, 1), dt.date(2025, 3, 31)),
           (dt.date(2025, 10, 1), dt.date(2026, 3, 31))]
    hist = {}
    for p in EXPECT["history"]:
        sel = [v for v in vis if patch[v[1]] == p and any(a <= v[0] <= b for a, b in win)]
        acc = sum(1 for v in sel if v[2] != "NOACC")
        conf = sum(1 for v in sel if v[2] == "CONF")
        hist[p] = (acc, conf, round(100 * conf / acc, 1))
    okh = hist == EXPECT["history"]
    print("history", hist, "OK" if okh else "MISMATCH")

    # capacity
    rota = f("rp_field_rota")
    team = sheet_rows(rota, "Team")
    leave = {(r["officer"], r["date"].date()) for r in sheet_rows(rota, "Leave and training") if r["code"] in ("AL", "TRN", "IND")}
    hols = {r["date"].date() for r in sheet_rows(rota, "Bank holidays") if r["calendar"] == "Scotland"}
    days = 0
    d = dt.date(2027, 1, 1)
    while d <= dt.date(2027, 3, 31):
        if d.weekday() < 5 and d not in hols:
            days += sum(1 for t in team if d >= t["field_start"].date() and (t["officer"], d) not in leave)
        d += dt.timedelta(1)
    from docx import Document
    tab = Document(f("FW-3")).tables[0]
    cap = {row.cells[1].text: days * math.floor(450 / (70 + int(row.cells[2].text))) for row in tab.rows[1:]}
    okc = cap == EXPECT["capacity"]
    print("capacity", days, cap, "OK" if okc else "MISMATCH")
    sys.exit(0 if (ok and okh and okc) else 1)


if __name__ == "__main__":
    main()
