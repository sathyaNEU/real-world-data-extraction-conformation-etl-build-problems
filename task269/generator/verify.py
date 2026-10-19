"""An independent recomputation of every graded figure from the shipped files alone (it imports nothing from the
generator but the file names): the excess wait per corridor boarding of every route, the four routes and the first
below them, the pilot's shifts and cost by route; then the goldens are read back and compared.

    python3 task269/generator/verify.py"""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import FILES   # noqa: E402

TASK = os.path.dirname(HERE)
PEAKS = {"AM": (420, 540), "PM": (930, 1080)}


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mins(stamp):
    t = dt.datetime.fromisoformat(stamp)
    return t.hour * 60 + t.minute + t.second / 60


def hmsm(x):
    h, m, s = (int(v) for v in x.split(":"))
    return h * 60 + m + s / 60


def wait(times):
    h = np.diff(np.sort(np.asarray(times, float)))
    return float((h ** 2).sum() / (2 * h.sum())) if len(h) else float("nan")


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def excess_wait(t):
    p = lambda k: os.path.join(t, FILES[k])
    moved = {r["new_stop_number"]: r["stop_number"] for r in rows(p("stops_log")) if r["new_stop_number"]}
    wb = openpyxl.load_workbook(p("corridors"), read_only=True)
    cor = defaultdict(list)
    for r in list(wb["Corridor stops"].iter_rows(values_only=True))[1:]:
        cor[(str(r[0]), r[2])].append((r[3], str(r[4]), r[6] == "Yes"))
    tp_of = {}
    for key, lst in cor.items():
        cur = None
        for _, s, tp in sorted(lst):
            if tp:
                cur = s
            tp_of[(key, s)] = cur
    # the stops each outbound headsign serves, and each trip's direction
    serve = defaultdict(set)
    tdir = {}
    for name in ("gtfs1", "gtfs2"):
        z = zipfile.ZipFile(p(name))
        trips = {r["trip_id"]: r for r in csv.DictReader(io.TextIOWrapper(z.open("trips.txt"), encoding="utf-8"))}
        for tid, r in trips.items():
            tdir[tid] = ("Outbound" if r["direction_id"] == "0" else "Inbound", r["route_id"], r["trip_headsign"])
        for r in csv.DictReader(io.TextIOWrapper(z.open("stop_times.txt"), encoding="utf-8")):
            d, rt, sign = tdir[r["trip_id"]]
            if d == "Outbound":
                serve[(rt, moved.get(r["stop_id"], r["stop_id"]))].add(sign)
    signs = defaultdict(set)
    for (rt, s), v in serve.items():
        signs[rt] |= v
    # departures: the revised release, the later of a doubled record; scheduled times from the vendor's column
    dep = {}
    for r in rows(p("avl_rev")):
        k = (r["service_date"], r["trip_id"], moved.get(r["timing_point"], r["timing_point"]))
        m = mins(r["departure_time"])
        if k not in dep or m > dep[k][0]:
            dep[k] = (m, hmsm(r["scheduled_time"]), r["route"], r["direction"], r["destination"])
    cells = defaultdict(lambda: ([], []))
    for (day, tid, stop), (m, s, rt, d, dest) in dep.items():
        for pk, (a, b) in PEAKS.items():
            for st in ("ALL", dest):
                if st == dest and (d == "Inbound" or len(signs[rt]) < 2):
                    continue
                c = cells[(day, rt, d, stop, pk, st)]
                if a <= m < b:
                    c[0].append(m)
                if a <= s < b:
                    c[1].append(s)
    ew = {k: wait(v[0]) - wait(v[1]) for k, v in cells.items()}
    tot, n = defaultdict(float), defaultdict(int)
    pend = defaultdict(list)
    for r in rows(p("journeys")):
        d, rt, _ = tdir[r["trip_id"]]
        board = moved.get(r["tag_on_stop"], r["tag_on_stop"])
        if (( rt, d), board) not in tp_of:
            continue
        m = mins(r["tag_on_time"])
        pk = next((k for k, (a, b) in PEAKS.items() if a <= m < b), None)
        if pk is None:
            continue
        tp = tp_of[((rt, d), board)]
        day = r["tag_on_time"][:10]
        if d == "Outbound" and len(signs[rt]) == 2:
            if not r["tag_off_stop"]:
                pend[(day, rt, d, tp, pk)].append(None)
                continue
            sv = serve.get((rt, moved.get(r["tag_off_stop"], r["tag_off_stop"])), set())
            st = "ALL" if len(sv) == 2 else next(iter(sv))
        else:
            st = "ALL"
        pend[(day, rt, d, tp, pk)].append(ew[(day, rt, d, tp, pk, st)])
    for (day, rt, d, tp, pk), vals in pend.items():
        known = [v for v in vals if v is not None]
        fill = float(np.mean(known)) if known else 0.0
        tot[rt] += sum(known) + fill * (len(vals) - len(known))
        n[rt] += len(vals)
    return {rt: tot[rt] / n[rt] for rt in tot}


def pilot(t):
    p = lambda k: os.path.join(t, FILES[k])
    plan = pdf_text(p("pilot_plan"))
    posts = {m.group(2): (m.group(1), m.group(3).strip()) for m in
             re.finditer(r"\b(\d{1,2}) (HP\d\d) Route \1, (.+?) (?:Monday|Tuesday|Wednesday|Thursday|Friday)", plan)}
    assert len(posts) == 8, posts
    loc = {(rt, place) for rt, place in posts.values()}
    app2emp = {r["roster_app_user"]: r["employee_number"] for r in rows(p("staff"))}
    seen = set()
    month = defaultdict(int)
    for r in rows(p("timesheets")):
        if r["source_system"] == "Payroll":
            if r["post_code"] not in posts:
                continue
            rt = posts[r["post_code"]][0]
            day = dt.datetime.strptime(r["work_date"], "%d/%m/%Y").date()
            key = (r["employee_number"], rt, day, r["shift"])
        else:
            if r["status"] != "Worked" or (r["route"], r["location"]) not in loc:
                continue
            st = dt.datetime.fromisoformat(r["shift_start"])
            key = (app2emp[r["app_user"]], r["route"], st.date(), "AM" if st.hour < 12 else "PM")
        if key not in seen:
            seen.add(key)
            month[(key[1], key[2].month)] += 1
    shifts = defaultdict(int)
    for (rt, m), v in month.items():
        shifts[rt] += v
    led = rows(p("ledger"))
    gone = {r["narration"].split()[-1] for r in led if r["narration"].startswith("Reverse 30 June journal")}
    cost = defaultdict(float)
    for r in led:
        if r["account"] == "6421" and r["cost_centre"] != "NP00" and r["document"] not in gone:
            cost[str(int(r["cost_centre"][2:]))] += float(r["amount"])
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    for r in led:
        if r["account"] == "6422":
            mm = next(i for i, x in enumerate(names, 1) if " %s-26" % x in r["narration"])
            tot = sum(v for (rt, m), v in month.items() if m == mm)
            for (rt, m), v in month.items():
                if m == mm:
                    cost[rt] += float(r["amount"]) * v / tot
    return dict(shifts), dict(cost)


def run(task=TASK):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    ew = excess_wait(t)
    order = sorted(ew, key=lambda r: -ew[r])
    if sorted(int(r) for r in order[:4]) != fig["call"]["routes"]:
        bad.append("the four routes %s" % sorted(order[:4]))
    if int(order[4]) != fig["first_below"]:
        bad.append("the first below %s" % order[4])
    for rt, v in ew.items():
        if round(v, 1) != fig["ewt"][rt]:
            bad.append("route %s excess wait %.3f against %.1f" % (rt, v, fig["ewt"][rt]))
    shifts, cost = pilot(t)
    for rt in fig["ask_a"]:
        if shifts.get(rt) != fig["ask_a"][rt]:
            bad.append("route %s shifts %s against %s" % (rt, shifts.get(rt), fig["ask_a"][rt]))
        if int(round(cost.get(rt, -1))) != fig["ask_b"][rt]:
            bad.append("route %s cost %.2f against %s" % (rt, cost.get(rt, -1), fig["ask_b"][rt]))
    wb = openpyxl.load_workbook(os.path.join(task, "golden", "pellbrook_2027_headway_programme_routes.xlsx"),
                                data_only=True)
    ws = wb["Ranking"]
    got = {str(r[1]): (r[3], r[4]) for r in ws.iter_rows(min_row=5, values_only=True) if r[1] is not None}
    for rt in fig["ewt"]:
        if got[rt][0] != fig["ewt"][rt] or (got[rt][1] == "Yes") != (int(rt) in fig["call"]["routes"]):
            bad.append("golden workbook route %s" % rt)
    pil = {str(r[0]): (r[1], r[2]) for r in wb["Pilot 2026"].iter_rows(min_row=2, values_only=True) if r[0] != "Total"}
    for rt in fig["ask_a"]:
        if pil[rt] != (fig["ask_a"][rt], fig["ask_b"][rt]):
            bad.append("golden workbook pilot route %s" % rt)
    print("verify: %d figures recomputed, %d disagreements" % (8 + 2 + 16 + 24, len(bad)))
    for x in bad:
        print("  DISAGREE", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
