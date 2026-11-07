"""task490 independent verifier: reads only target.zip (its own parsers, no generator module) and recomputes
the call and every graded figure in figures.json."""
import csv
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
Z = zipfile.ZipFile(os.path.join(TASK, "target.zip"))
FIGS = json.load(open(os.path.join(HERE, "figures.json")))
BAD = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        BAD.append(label)


def member(suffix):
    names = [n for n in Z.namelist() if n.endswith(suffix)]
    assert len(names) == 1, suffix
    return Z.read(names[0])


def rows(suffix):
    return list(csv.DictReader(io.StringIO(member(suffix).decode("utf-8"))))


def xlsx(suffix):
    from openpyxl import load_workbook
    return load_workbook(io.BytesIO(member(suffix)), read_only=True, data_only=True)


def pdf_text(suffix):
    from pypdf import PdfReader
    return " ".join(p.extract_text() for p in PdfReader(io.BytesIO(member(suffix))).pages).replace("\n", " ")


def uk_local(u):
    # BST 2026: 29 March 01:00 UTC to 25 October 01:00 UTC
    return u + timedelta(hours=1) if datetime(2026, 3, 29, 1) <= u < datetime(2026, 10, 25, 1) else u


# --------------------------------------------------------------------------------------------- lockage
sites = json.loads(member("counter_sites_2026.json"))
site_lock = {s["site_code"]: (s["asset"], s["lock_name"]) for s in sites["sites"]}
prog = pdf_text("backpumping_programme_2027-28.pdf")
ok("programme paper read back: the siting sentence", "drew the most water from the summit pound by filling their "
   "chambers" in prog)
wb = xlsx("lock_register_2026.xlsx")
lockful = {}
pound = {}
for r in wb["Chamber survey 2025"].iter_rows(values_only=True):
    if r and isinstance(r[0], str) and "/L" in r[0]:
        lockful[r[0]] = float(r[7])
        pound[r[0]] = r[3]
summit_locks = {}
for a, (asset, name) in site_lock.items():
    summit_locks.setdefault(pound[asset].replace(" summit", ""), []).append(asset)
ok("summit locks: two per summit pound, all six in the paper's table",
   all(len(v) == 2 for v in summit_locks.values()) and all(site_lock[s][1] in prog for s in site_lock))
ev = {}
for r in rows("lock_counter_movements_2026.csv"):
    asset = site_lock[r["site_code"]][0]
    s = r["detected_at"]
    t = uk_local(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")) if s.endswith("Z") else datetime.strptime(s, "%d/%m/%Y %H:%M:%S")
    if r["class"] not in ("BOAT", "VESSEL"):
        continue
    ev.setdefault(asset, []).append([t, "up" if r["direction"] in ("UP", "A>B") else "down", r["index_read"],
                                     int(r["record_no"])])
for a in ev:
    ev[a].sort(key=lambda x: (x[0], x[3]))
    out, last = [], {}
    for x in ev[a]:
        k = (x[2], x[1])
        if x[2] and k in last and (x[0] - last[k]).total_seconds() <= 60:
            continue
        last[k] = x[0]
        out.append(x)
    ev[a] = out
kw = xlsx("tilsey_lock_keepers_log_2026.xlsx")
keep = []
for ws in kw.worksheets:
    started = False
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Day":
            started = True
            continue
        if started and r and r[0]:
            keep.append([datetime.strptime("%s %s" % (r[0], r[1]), "%d/%m/%y %H:%M"),
                         "up" if r[5] == "U" else "down", r[4] or "", r[2]])
top = [k for k in keep if k[3] == "Top"]
es = ev["TC/L08"]
big = max(((y[0] - x[0]).total_seconds(), x[0], y[0]) for x, y in zip(es, es[1:]))
g0, g1 = big[1], big[2]
ok("Tilsey Top camera outage found in the record", g0.date().isoformat() == "2026-08-03" and g1.date().isoformat() ==
   "2026-08-23", "%s to %s" % (g0, g1))
cand = [x for x in es if g0 - timedelta(hours=2) <= x[0] <= g1 + timedelta(hours=2)]
taken = []
used = set()
for k in top:
    if not (g0 - timedelta(hours=1) <= k[0] <= g1 + timedelta(hours=1)):
        continue
    hit = None
    for i, x in enumerate(cand):
        if i not in used and k[2] and x[2] == k[2] and x[1] == k[1] and abs((x[0] - k[0]).total_seconds()) <= 1500:
            hit = i
            break
    if hit is None and g0 - timedelta(minutes=30) <= k[0] <= g1:
        taken.append([k[0], k[1], k[2], 0])
    elif hit is not None:
        used.add(hit)
ev["TC/L08"] = sorted(es + taken, key=lambda x: (x[0], x[3]))
ok("keepers' entries taken in for the outage", len(taken) == FIGS["keepers_entries_taken"], str(len(taken)))
notices = rows("navigation_notices_2026.csv")
reopen = {}
for n in notices:
    if "left empty" in n["summary"] and n["notice_type"] == "Stoppage" and "Steward" in n["location"]:
        reopen["HN/L32"] = datetime.strptime(n["ends"], "%Y-%m-%d %H:%M")
ok("Steward's Lock reopening read from the notices", reopen.get("HN/L32") == datetime(2026, 5, 29, 17, 0))
lock_ml = {}
for a, es in ev.items():
    cyc = []
    for x in es:
        if cyc and cyc[-1][1] == x[1] and (x[0] - cyc[-1][2]).total_seconds() <= 180:
            cyc[-1][2] = x[0]
            continue
        cyc.append([x[0], x[1], x[0]])
    state, fills, prev = "empty", 0, None
    for c in cyc:
        if a in reopen and prev is not None and prev < reopen[a] <= c[0]:
            state = "empty"
        if c[1] == "up":
            fills += 1
            state = "full"
        else:
            if state == "empty":
                fills += 1
            state = "empty"
        prev = c[0]
    lock_ml[a] = fills * lockful[a] / 1000.0
    ok("lock %s: fillings and water" % a, fills == FIGS["locks"][a]["fills"] and
       round(lock_ml[a], 1) == FIGS["locks"][a]["ml"], "%d, %.1f Ml" % (fills, lock_ml[a]))
    up = sum(1 for x in es if x[1] == "up")
    ok("lock %s: boats up and down" % a, up == FIGS["locks"][a]["up"] and len(es) - up == FIGS["locks"][a]["down"])
summ = {s: sum(lock_ml[a] for a in v) for s, v in summit_locks.items()}
best = sorted(summ, key=lambda s: -summ[s])
ok("the call", best[0] == FIGS["call"] and best[1] == FIGS["runner_up"], str({k: round(v, 1) for k, v in summ.items()}))
ok("summit lockage figures", all(round(summ[s], 1) == FIGS["lockage_ml"][s] for s in summ))

# ------------------------------------------------------------------------------------------- reservoirs
reg = pdf_text("reservoir_register_extract_2025.pdf")
ok("register read back: weir formula and plates", "1.84 (b - 0.2h)" in reg and "0.60" in reg and "0.75" in reg)
crest_h = float(re.search(r"Harnock arm 0\.50 (\d+\.\d+)", reg).group(1))
crest_t = float(re.search(r"Tilsey arm 0\.35 (\d+\.\d+)", reg).group(1))
plate_t = datetime(2026, 6, 16, 10, 30) if "From 10:30 UTC on 16 June 2026" in reg else None
ok("register: Fox Bridge crests and the plate change", plate_t is not None and abs(crest_t - crest_h - 0.06) < 1e-9)


def q(b, h):
    return 1.84 * (b - 0.2 * h) * h ** 1.5 if h > 0 else 0.0


tot = harn = tils = 0.0
for r in rows("coldmere_outlet_15min_2026.csv"):
    t = datetime.strptime(r["period_end_utc"], "%Y-%m-%dT%H:%M:%SZ")
    if not (datetime(2026, 3, 31, 23) < t <= datetime(2026, 11, 1)):
        continue
    flow = q(0.75 if t <= plate_t else 0.60, float(r["head_mm_mean"]) / 1000.0)
    lo, hi = 0.0, 2.0
    for _ in range(80):
        H = (lo + hi) / 2
        if q(0.50, H) + q(0.35, H - (crest_t - crest_h)) < flow:
            lo = H
        else:
            hi = H
    a_, b_ = q(0.50, lo), q(0.35, lo - (crest_t - crest_h))
    if a_ + b_ > 0:
        harn += flow * a_ / (a_ + b_) * 900
        tils += flow * b_ / (a_ + b_) * 900
    tot += flow * 900
ret_wb = xlsx("reservoir_returns_2026.xlsx")
rel = {"Coldmere Reservoir": tot / 1000}
for ws in ret_wb.worksheets:
    name, segs, rate, on = None, [], 0.0, False
    for r in ws.iter_rows(values_only=True):
        if r and r[0] == "Site":
            name = r[1]
        elif r and r[0] == "Date":
            on = True
        elif on and r and r[0]:
            d = datetime.strptime(r[0], "%d/%m/%Y")
            start = d + timedelta(hours=9) - timedelta(days=1)
            t0 = start
            for part in [p.strip() for p in (r[5] or "").split(";") if p.strip()]:
                m = re.match(r"(\d\d):(\d\d) valve (?:opened to [\d.]+ turns \(([\d.]+) Ml/d\)|shut)", part)
                tt = d + timedelta(hours=int(m.group(1)), minutes=int(m.group(2)))
                if tt > d + timedelta(hours=9):
                    tt -= timedelta(days=1)
                segs.append((t0, tt, rate))
                t0, rate = tt, float(m.group(3)) if m.group(3) else 0.0
            segs.append((t0, start + timedelta(days=1), rate))
            rate = float(r[3] or 0)
    a, b = datetime(2026, 4, 1), datetime(2026, 11, 1)
    rel[name] = sum(rt * max(0.0, (min(e, b) - max(s, a)).total_seconds()) / 86400 for s, e, rt in segs)
recv = {"Kelsby": rel["Lower Kelsby Reservoir"], "Harnock": harn / 1000, "Tilsey": rel["Tilsey Reservoir"] + tils / 1000}
ok("reservoir releases", all(round(rel[k], 1) == FIGS["reservoir_release_ml"][k] for k in rel),
   str({k: round(v, 1) for k, v in rel.items()}))
ok("summit received", all(round(recv[k], 1) == FIGS["summit_received_ml"][k] for k in recv),
   str({k: round(v, 1) for k, v in recv.items()}))

# ------------------------------------------------------------------------------------------- abstraction
lw = xlsx("abstraction_licences_2026.xlsx")
lic = [r for r in lw.worksheets[0].iter_rows(values_only=True) if r and isinstance(r[0], str) and re.match(r"[KHT]A/\d+", r[0])]
reads = {}
for r in rows("abstraction_meter_readings_2026.csv"):
    reads.setdefault(r["point_ref"], []).append((datetime.strptime(r["read_date"], "%d/%m/%Y"), r["meter_serial"],
                                                 int(r["reading_m3"])))
wo = {r["asset"]: r["completion_note"] for r in rows("works_orders_2026.csv") if r["completion_note"].startswith("Meter SN")}
take = {}
for r in lic:
    ref, point, digits = r[0], r[3], int(r[7])
    rs = sorted(reads[point])
    mod = 10 ** digits
    if point in wo:
        m = re.search(r"SN (\S+) removed, final reading (\d+)\. New meter SN (\S+) fitted and sealed, reading (\d+)", wo[point])
        seq1 = [v for _, s, v in rs if s == m.group(1)] + [int(m.group(2))]
        seq2 = [int(m.group(4))] + [v for _, s, v in rs if s == m.group(3)]
        seqs = [seq1, seq2]
    else:
        seqs = [[v for _, _, v in rs]]
    take[ref] = sum((y - x) % mod for sq in seqs for x, y in zip(sq, sq[1:]))
ok("abstraction by licence", all(take[k] == FIGS["abstraction_m3"][k] for k in take), str(take))

# ------------------------------------------------------------------------------------ the pack's own gates
names = [n for n in Z.namelist()]
ok("pack: 14 files under target/, no describing file", len(names) == 14 and not any(
    re.search(r"readme|dictionar|manifest|notes", n, re.I) for n in names))
print("%d checks, %d failed" % (N[0], len(BAD)))
sys.exit(1 if BAD else 0)
