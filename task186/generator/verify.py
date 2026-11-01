"""Independent verifier for task186: reads only the shipped bundle (target/ and golden/), never the generator's
world or analysis.py, and recomputes the call and every graded figure on its own code path.

    python3 task186/generator/verify.py        # exit 0 when everything agrees
"""
import base64
import csv
import datetime as dt
import json
import os
import re
import sys
import zlib
from collections import defaultdict
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
SYD = ZoneInfo("Australia/Sydney")
OK = []


def say(label, ok, detail=""):
    OK.append(ok)
    print("%s  %s  %s" % ("OK  " if ok else "FAIL", label, detail))


def rows(name):
    with open(os.path.join(TGT, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheet(name, title, header0):
    wb = load_workbook(os.path.join(TGT, name), read_only=True, data_only=True)
    data = list(wb[title].iter_rows(values_only=True))
    for i, r in enumerate(data):
        if r and r[0] == header0:
            hdr = [h for h in r if h is not None]
            return [dict(zip(hdr, x)) for x in data[i + 1:] if x and x[0] is not None]
    raise SystemExit("no header in %s" % name)


def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.rstrip().endswith(b"~>"):
                raw = base64.a85decode(raw.rstrip()[:-2], adobe=False)
            raw = zlib.decompress(raw)
        except Exception:
            continue
        out += [s.decode("latin-1") for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", raw, re.S)]
    return " ".join(out)


def main():
    files = sorted(os.listdir(TGT))
    say("bundle holds twelve files in four formats", len(files) == 12 and
        {f.rsplit(".", 1)[1] for f in files} == {"csv", "xlsx", "pdf", "json"}, str(len(files)))
    std = pdf_strings(os.path.join(TGT, "SCS-04_screening_officer_competency_standard_rev6.pdf"))
    say("PDF read back: the standard's detection term", "Detection performance" in std, "%d chars" % len(std))
    say("PDF read back: the standard's currency clause", "at least 20 hours" in std, "currency")
    cfg = json.load(open(os.path.join(TGT, "tip_projection_settings.json")))
    say("JSON read back", len(cfg["lanes"]) == 7, cfg["library_release"])

    # ------------------------------------------------------------------ the call
    login = {r["login"]: r["staff_no"] for r in rows("ct_operator_logins.csv")}
    obj = {str(r["image_no"]).zfill(6): r["object_code"] for r in sheet("tip_library_catalogue_r1.xlsx", "Images", "image_no")}
    reg = sheet("screening_officer_register.xlsx", "Officers", "staff_no")
    current = {r["staff_no"] for r in reg if r["endorsement_30_nov_2026"] == "Current"}
    seen_rows = set()
    events = []
    for r in rows("tip_events_20250701_20261130.csv"):
        key = tuple(r.values())
        if key in seen_rows:
            continue
        seen_rows.add(key)
        t = dt.datetime.strptime(r["event_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        events.append((login[r["operator_login"]], t, obj[r["image_no"].zfill(6)], r["result"] == "HIT"))
    events.sort()
    w0, w1 = dt.date(2025, 12, 1), dt.date(2026, 11, 30)
    tally = defaultdict(lambda: [0, 0, 0, 0])
    shown = defaultdict(set)
    for s, t, o, hit in events:
        d = t.astimezone(SYD).date()
        first = o not in shown[s]
        shown[s].add(o)
        if w0 <= d <= w1:
            v = tally[s]
            v[0] += 1
            v[1] += hit
            if first:
                v[2] += 1
                v[3] += hit
    off = sorted(s for s in current if tally[s][3] / tally[s][2] < 0.80)
    raw = sorted(s for s in current if tally[s][1] / tally[s][0] < 0.80)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    say("call: the officers coming off recompute", off == sorted(x["staff_no"] for x in fig["call_off"]),
        "%d officers" % len(off))
    say("call: each one's detection performance recomputes to one decimal",
        all(abs(100 * tally[x["staff_no"]][3] / tally[x["staff_no"]][2] - x["detection_pct"]) < 0.051
            for x in fig["call_off"]), "first showings")
    say("call: the raw hit rate route files a different list", raw != off and set(raw) < set(off), str(raw))
    gl = list(csv.DictReader(open(os.path.join(GOLD, "recertification_2027.csv"), encoding="utf-8")))
    say("golden list: every endorsed officer once", sorted(r["staff_no"] for r in gl) == sorted(current), str(len(gl)))
    say("golden list: the officers marked off are the recomputed ones",
        sorted(r["staff_no"] for r in gl if r["xray_duty_from_1_jan_2027"].startswith("Off")) == off, "verdicts")

    # ------------------------------------------------------------------ ask A, minute by minute
    pay = {r["payroll_no"]: r["staff_no"] for r in reg}
    absent = {(pay[r["payroll_no"]], r["leave_date"]) for r in rows("hr_leave_taken_20251201_20261130.csv")
              if r["leave_type"] == "Personal leave"}
    lanes = defaultdict(list)
    for r in rows("lane_roster_20251201_20261130.csv"):
        if (r["staff_no"], r["roster_date"]) in absent:
            continue
        hh, mm = map(int, r["start"].split(":"))
        h2, m2 = map(int, r["finish"].split(":"))
        lanes[(r["roster_date"], r["lane"])].append((r["staff_no"], hh * 60 + mm, h2 * 60 + m2))
    xr = defaultdict(float)
    for (d, ln), team in lanes.items():
        for minute in range(min(x[1] for x in team), max(x[2] for x in team)):
            on = [x[0] for x in team if x[1] <= minute < x[2]]
            for s in on:
                xr[(s, d[:7])] += 1.0 / len(on) / 60.0
    months = ["2025-12"] + ["2026-%02d" % m for m in range(1, 12)]
    counts = []
    for mo in months:
        y, m = int(mo[:4]), int(mo[5:])
        first = dt.date(y, m, 1)
        last = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
        n = 0
        for r in reg:
            e = r["xray_endorsed"].date() if hasattr(r["xray_endorsed"], "date") else r["xray_endorsed"]
            lf = r["left"].date() if r["left"] is not None and hasattr(r["left"], "date") else r["left"]
            if e <= first and (lf is None or lf >= last) and xr.get((r["staff_no"], mo), 0.0) < 20.0:
                n += 1
        counts.append(n)
    say("ask A: every month's count recomputes", counts == [fig["ask_a"][mo] for mo in months], str(counts))

    # ------------------------------------------------------------------ ask B, units placed by exhaustive search
    roster_hours = defaultdict(set)
    first_start = {}
    for r in rows("lane_roster_20251201_20261130.csv"):
        a = int(r["start"][:2]) * 60 + int(r["start"][3:])
        b = int(r["finish"][:2]) * 60 + int(r["finish"][3:])
        k = (r["roster_date"], r["lane"])
        roster_hours[k] |= set(range(a // 60, (b - 1) // 60 + 1))
        first_start[k] = min(first_start.get(k, 99), a // 60)
    unit_reg = {r["unit_serial"]: (r["location"], r["commissioned"]) for r in rows("ct_unit_register.csv")}
    unit_hours = defaultdict(dict)
    for r in rows("ct_unit_bag_counts_hourly_utc.csv"):
        t = dt.datetime.strptime(r["hour_start_utc"], "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc).astimezone(SYD)
        unit_hours[(t.date().isoformat(), r["unit_serial"])][t.hour] = int(r["bags_imaged"])
    by_day = defaultdict(list)
    for (d, u) in unit_hours:
        by_day[d].append(u)
    bags = defaultdict(int)
    quarters = [("Q1", "2025-12-01", "2026-02-28"), ("Q2", "2026-03-01", "2026-05-31"),
                ("Q3", "2026-06-01", "2026-08-31"), ("Q4", "2026-09-01", "2026-11-30")]

    def score(d, u, ln):
        hrs = set(unit_hours[(d, u)])
        lanehrs = roster_hours[(d, ln)]
        if not hrs <= (lanehrs | set(range(first_start[(d, ln)]))):
            return None
        sc = len(hrs & lanehrs) / float(len(hrs | lanehrs))
        loc, com = unit_reg.get(u, ("", "9999"))
        return sc + (0.5 if loc == ln and com <= d else 0.0)
    for d, units in by_day.items():
        if not ("2025-12-01" <= d <= "2026-11-30"):
            continue
        open_l = [ln for ln in ("D1", "D2", "D3", "D4", "D5", "I1", "I2") if (d, ln) in roster_hours]
        cand = {ln: [(score(d, u, ln), u) for u in units if score(d, u, ln) is not None] for ln in open_l}
        best = [None, -1.0]

        def search(i, used, acc, tot):
            if i == len(open_l):
                if tot > best[1]:
                    best[0], best[1] = dict(acc), tot
                return
            ln = open_l[i]
            for sc, u in cand[ln]:
                if u not in used:
                    acc[ln] = u
                    search(i + 1, used | {u}, acc, tot + sc)
                    del acc[ln]
        search(0, frozenset(), {}, 0.0)
        q = next(x[0] for x in quarters if x[1] <= d <= x[2])
        for ln, u in (best[0] or {}).items():
            bags[(ln, q)] += sum(v for h, v in unit_hours[(d, u)].items() if h in roster_hours[(d, ln)])
    okb = all(int(round(bags[(ln, q)] / 1000.0)) * 1000 == fig["ask_b"]["%s %s" % (ln, q)]
              for ln in ("D1", "D2", "D3", "D4", "D5", "I1", "I2") for q, _, _ in quarters)
    worst = max(abs(bags[(ln, q)] - fig["ask_b_raw"]["%s %s" % (ln, q)]) for ln in ("D1", "D2", "D3", "D4", "D5", "I1", "I2")
                for q, _, _ in quarters)
    say("ask B: every lane-quarter count recomputes from an exhaustive placement of units", okb and worst == 0, "max diff %d" % worst)

    gp = pdf_strings(os.path.join(GOLD, "screening_year_review_2026.pdf"))
    say("golden PDF read back: the call is stated", "come off X-ray duty" in gp, "%d chars" % len(gp))
    print("verify: %d of %d agree" % (sum(OK), len(OK)))
    sys.exit(0 if all(OK) else 1)


if __name__ == "__main__":
    main()
