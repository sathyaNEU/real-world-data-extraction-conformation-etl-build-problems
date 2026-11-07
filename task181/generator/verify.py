"""Independent verifier: reads target.zip only (never the generator's modules), recomputes the referred set and every
ask figure, and compares them with figures.json and the golden CSV.

    python3 task181/generator/verify.py
"""
import bisect
import csv
import datetime as dt
import io
import json
import math
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ZIP = os.path.join(TASK, "target.zip")
FAIL = []


def ok(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "   " + str(detail)))
    if not cond:
        FAIL.append(label)


def rows(z, name):
    return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8"))))


def upper(mu):
    p = math.exp(-mu)
    cum, c = p, 0
    while cum < 0.975:
        c += 1
        p *= mu / c
        cum += p
    return c


def local(u):
    """UTC to Melbourne wall clock: AEDT from the first Sunday of October 02:00 to the first Sunday of April 03:00."""
    def fs(y, m):
        d = dt.date(y, m, 1)
        return d + dt.timedelta(days=(6 - d.weekday()) % 7)
    for h in (10, 11):
        t = u + dt.timedelta(hours=h)
        end = dt.datetime.combine(fs(t.year, 4), dt.time(3))
        start = dt.datetime.combine(fs(t.year, 10), dt.time(2))
        if (10 if end <= t < start else 11) == h:
            return t
    return u + dt.timedelta(hours=10)


def main():
    z = zipfile.ZipFile(ZIP)
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    rates = {}
    import re
    from pypdf import PdfReader
    txt = " ".join(p.extract_text() for p in PdfReader(io.BytesIO(z.read("haisc_procedure_rates_2026.pdf"))).pages)
    for m in re.finditer(r"\b(COLO|SB|XLAP|APPY|CHOL|HER)\b\s+[A-Za-z ]+?\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+"
                         r"([\d.]+)", txt):
        rates[m.group(1)] = (int(m.group(2)), [float(m.group(k)) / 100 for k in range(3, 7)])
    ok("rates table read for six categories", len(rates) == 6, sorted(rates))
    wc = {"Clean": 1, "Clean-contaminated": 2, "Contaminated": 3, "Dirty": 4}
    procs = {}
    seen = set()
    for r in rows(z, "theatre_operations_2022_2027.csv"):
        if r["status"] != "Completed" or r["return_to_theatre"] == "Y" or r["procedure_seq"] != "1":
            continue
        if r["surveillance_category"] not in rates:
            continue
        key = (r["ur_number"], r["theatre"], r["knife_to_skin"])
        if key in seen:
            continue
        seen.add(key)
        k = dt.datetime.strptime(r["knife_to_skin"], "%Y-%m-%d %H:%M")
        c = dt.datetime.strptime(r["wound_closure"], "%Y-%m-%d %H:%M")
        cut, rt = rates[r["surveillance_category"]]
        idx = int(int(r["asa_class"]) >= 3) + int(wc[r["wound_class"]] >= 3) + int((c - k).total_seconds() / 60 > cut)
        cons = r["responsible_consultant"].replace("GS-41", "GS-14")
        procs[r["booking_no"]] = dict(ur=r["ur_number"], cat=r["surveillance_category"], knife=k, close=c,
                                      anaes=dt.datetime.strptime(r["anaesthetic_start"], "%Y-%m-%d %H:%M"),
                                      theatre=r["theatre"], cons=cons, exp=rt[min(idx, 3)], implant=r["implant"])
    by_ur = {}
    for b, p in procs.items():
        by_ur.setdefault((p["ur"], p["cat"]), []).append((p["knife"].date(), b))
    latest = {}
    for r in rows(z, "ssi_surveillance_2022_2027.csv"):
        if r["infection_id"] not in latest or int(r["record_version"]) > int(latest[r["infection_id"]]["record_version"]):
            latest[r["infection_id"]] = r
    inf = {}
    for r in latest.values():
        if r["status"] != "Confirmed":
            continue
        b = r["booking_no"] if r["booking_no"] in procs else None
        if b is None:
            od = dt.date.fromisoformat(r["operation_date"])
            near = sorted((d, bb) for d, bb in by_ur.get((r["ur_number"], r["surveillance_category"]), [])
                          if 0 <= (d - od).days <= 3)
            b = near[0][1] if near else None
        if b is None:
            continue
        days = (dt.date.fromisoformat(r["onset_date"]) - procs[b]["knife"].date()).days
        if 0 <= days <= (90 if procs[b]["implant"] == "Y" else 30):
            inf[b] = True
    w0, w1 = dt.date(2027, 4, 1), dt.date(2027, 9, 30)
    win = {b: p for b, p in procs.items() if w0 <= p["knife"].date() <= w1}
    # repair time from the log
    from openpyxl import load_workbook
    ws = load_workbook(io.BytesIO(z.read("cssd_equipment_log_2026_2027.xlsx")), read_only=True)["Log"]
    rep = [dt.datetime.strptime(str(x[4]), "%Y-%m-%d %H:%M") for x in ws.iter_rows(values_only=True)
           if x and x[0] == "S3" and "Vacuum pump" in str(x[3])][0]
    rep_utc = rep - dt.timedelta(hours=10)
    last = {}
    for r in rows(z, "steriliser_cycles_2027.csv"):
        if r["cycle_type"] != "Load" or r["result"] != "Pass":
            continue
        t = dt.datetime.strptime(r["start_utc"], "%Y-%m-%dT%H:%M:%SZ")
        for b in r["items"].split(";"):
            last.setdefault(b, []).append((t, r["steriliser"]))
    for v in last.values():
        v.sort()
    idx = {}
    for b, p in win.items():
        idx.setdefault((p["ur"], p["theatre"]), []).append(b)
    exposed = set()
    for r in rows(z, "instrument_tracking_scans_2027.csv"):
        if not r["station"].startswith("THEATRE"):
            continue
        u = dt.datetime.strptime(r["scan_utc"], "%Y-%m-%dT%H:%M:%SZ")
        lt = local(u)
        for b in idx.get((r["ur_number"], r["station"][8:]), []):
            p = win[b]
            if p["anaes"] - dt.timedelta(hours=1) <= lt <= p["close"] and r["barcode"] in last:
                L = last[r["barcode"]]
                k = bisect.bisect_left([t for t, _ in L], u) - 1
                if k >= 0 and L[k][1] == "S3" and L[k][0] >= rep_utc:
                    exposed.add(b)
    cons = sorted({p["cons"] for p in win.values()})
    refd = []
    for c in cons:
        bs = [b for b, p in win.items() if p["cons"] == c and b not in exposed]
        e = sum(win[b]["exp"] for b in bs)
        o = sum(b in inf for b in bs)
        if o > upper(e):
            refd.append(c)
    ok("the referred set recomputes from the zip: %s" % ", ".join(refd), refd == fig["call"]["referred"], refd)
    ok("the exposed procedures recompute (%d)" % len(exposed), len(exposed) == fig["exposed_procedures"])
    for y in (2022, 2023, 2024):
        for c in cons:
            n = sum(1 for p in procs.values() if p["cons"] == c and p["knife"].year == y)
            i = sum(1 for b, p in procs.items() if p["cons"] == c and p["knife"].year == y and b in inf)
            ok("ask A %s %d procedures %d" % (c, y, n), n == fig["ask_a"]["%s %d" % (c, y)], fig["ask_a"]["%s %d" % (c, y)])
            ok("ask B %s %d infections %d" % (c, y, i), i == fig["ask_b"]["%s %d" % (c, y)], fig["ask_b"]["%s %d" % (c, y)])
    gold = {(r["figure"], r["consultant"], r["year"]): int(r["value"]) for r in
            csv.DictReader(open(os.path.join(TASK, "golden", "ssi_review_figures_2027.csv"), encoding="utf-8"))}
    ok("the golden CSV carries every ask figure", all(gold[("procedures",) + tuple(k.split())] == v
                                                     for k, v in fig["ask_a"].items()) and
       all(gold[("infections",) + tuple(k.split())] == v for k, v in fig["ask_b"].items()))
    print("%d verifier failures" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
