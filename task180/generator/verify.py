"""Independent verifier for task180. Reads only the shipped bytes (../target/ and ../golden/) and imports
nothing from the generator. The limit tables, intervals and constants are read out of the shipped
standard itself. Exit 1 on any disagreement with the golden deliverables.
"""
import csv
import datetime as dt
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pyarrow.parquet as pq
from docx import Document
from pypdf import PdfReader

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
T = os.path.join(BASE, "target")
GD = os.path.join(BASE, "golden")
NZ = ZoneInfo("Pacific/Auckland")
GAS7 = ["H2", "CH4", "C2H6", "C2H4", "C2H2", "CO", "CO2"]
LABEL = {"Hydrogen H2": "H2", "Methane CH4": "CH4", "Ethane C2H6": "C2H6", "Ethylene C2H4": "C2H4",
         "Acetylene C2H2": "C2H2", "Carbon monoxide CO": "CO", "Carbon dioxide CO2": "CO2"}
BAD = []


def f(prefix):
    return os.path.join(T, next(x for x in sorted(os.listdir(T)) if x.startswith(prefix)))


def expect(name, got, want):
    ok = got == want
    if not ok:
        BAD.append(name)
    print(("OK   " if ok else "DIFF ") + name + ("" if ok else f"   got {got!r} want {want!r}"))


# ---------------------------------------------------------------------------------------------
# the standard
def read_standard():
    text = "\n".join(p.extract_text() for p in PdfReader(f("ES-DGA-02")).pages)
    lines = [x.strip() for x in text.split("\n") if x.strip()]

    def table(title):
        i = next(k for k, x in enumerate(lines) if x.startswith(title))
        out = {}
        k = i
        while len(out) < 7:
            k += 1
            if lines[k] in LABEL:
                n = 6 if title != "Table A3" else 2
                vals = [float(v.replace(",", "")) for v in lines[k + 1:k + 1 + n]]
                out[LABEL[lines[k]]] = vals
        return out
    a1, a2, a3 = table("Table A1"), table("Table A2"), table("Table A3")
    gap = int(re.search(r"taken (\d+) days or more before", text.replace("\n", " ")).group(1))
    o2n2 = float(re.search(r"sealed where\s+O2/N2 is ([\d.]+) or less", text.replace("\n", " ")).group(1))
    m = re.search(r"10\s*\^?\s*\(?\s*([\d.]+)\s*-\s*(\d+)\s*/\s*\(T \+ 273\)", text.replace("\n", " "))
    c1, c2 = (float(m.group(1)), float(m.group(2))) if m else (None, None)
    return a1, a2, a3, gap, o2n2, c1, c2, text


A1, A2, A3, GAP, O2N2, WS1, WS2, STD = read_standard()
if WS1 is None:   # superscript layout: take the constants from the formula line
    nums = re.findall(r"\(([\d.]+) - (\d+)/\(T \+ 273\)\)", STD.replace("\n", " "))
    WS1, WS2 = float(nums[0][0]), float(nums[0][1])
INOIL_OPS, INOIL_YEARS = 60000, 7
m = re.search(r"In-oil arcing diverter\s+([\d,]+)\s+(\d+)", STD)
if m:
    INOIL_OPS, INOIL_YEARS = int(m.group(1).replace(",", "")), int(m.group(2))
print(f"standard: base gap {GAP} days, sealed O2/N2 <= {O2N2}, Ws constants {WS1} {WS2}, in-oil interval "
      f"{INOIL_OPS} ops / {INOIL_YEARS} years")


def col(cls, band):
    return (0 if cls == "SL" else 3) + ["<10", "10-30", ">30"].index(band)


# ---------------------------------------------------------------------------------------------
# register, results, counters, log
wb = openpyxl.load_workbook(f("asset_register"), read_only=True, data_only=True)
rr = list(wb["Transformers"].iter_rows(values_only=True))
REG = {r[0]: dict(zip(rr[0], r)) for r in rr[1:] if r[0]}

issues = {}
with open(f("dga_main_tank_results")) as fh:
    for r in csv.DictReader(fh):
        k = r["sample_id"]
        if k not in issues or int(r["issue"]) > int(issues[k]["issue"]):
            issues[k] = r
UNIT = {}
for r in issues.values():
    r["t"] = dt.datetime.strptime(r["sampled"], "%Y-%m-%d %H:%M")
    UNIT.setdefault(r["transformer_id"], []).append(r)
for k in UNIT:
    UNIT[k].sort(key=lambda r: r["t"])


def val(s):
    return float(s[1:]) / 2 if s.startswith("<") else float(s)


cdays, cvals = {}, {}
with open(f("scada_tap_counters")) as fh:
    for r in csv.DictReader(fh):
        cdays.setdefault(r["transformer_id"], []).append(dt.date.fromisoformat(r["date"]))
        cvals.setdefault(r["transformer_id"], []).append(int(r["tap_ops_counter"]))

wb = openpyxl.load_workbook(f("maintenance_log"), read_only=True, data_only=True)
lr = list(wb.worksheets[0].iter_rows(values_only=True))
LOG = [dict(zip(lr[0], r)) for r in lr[1:] if r[0]]
LAST, REPLACED, READING = {}, {}, {}
for e in LOG:
    if not str(e["work_type"]).startswith("OLTC"):
        continue
    d = e["completed"].date() if isinstance(e["completed"], dt.datetime) else e["completed"]
    a = e["asset"]
    if a not in LAST or d > LAST[a]:
        LAST[a] = d
    txt = e["description"].lower()
    if ("new counter" in txt or "counter replaced" in txt or "replaced the operations counter" in txt) \
            and "not replaced" not in txt:
        REPLACED.setdefault(a, set()).add(d)
    m = re.search(r"op counter ([\d,]+), not replaced", txt)
    if m:
        READING[(a, d)] = int(m.group(1).replace(",", ""))


def ops_window(tid, d1, d2):
    days, v = cdays[tid], cvals[tid]
    i, j = days.index(d1), days.index(d2)
    n = 0
    for k in range(i, j):
        step = v[k + 1] - v[k]
        if step < 0:
            step = v[k + 1] if days[k] in REPLACED.get(tid, set()) else step + 100000
        n += step
    return n


# ---------------------------------------------------------------------------------------------
# coding
def band(tid):
    y = max(REG[tid]["year_manufactured"], REG[tid]["rewound"] or 0)
    age = UNIT[tid][-1]["t"].year - y
    return "<10" if age < 10 else ("10-30" if age <= 30 else ">30")


def code(tid, drop=()):
    s = UNIT[tid]
    lat = s[-1]
    cls = "SL" if float(lat["O2"]) / float(lat["N2"]) <= O2N2 else "FB"
    base = [r for r in s[:-1] if (lat["t"].date() - r["t"].date()).days >= GAP][-1]
    days = (lat["t"].date() - base["t"].date()).days
    c, best = 1, (-1.0, None)
    for g in GAS7:
        if g in drop:
            continue
        inc = (val(lat[g]) - val(base[g])) * 365 / days
        lim = A3[g][0 if cls == "SL" else 1]
        lvl = val(lat[g])
        hi95 = lvl > A2[g][col(cls, band(tid))]
        hi90 = lvl > A1[g][col(cls, band(tid))]
        rate = inc > lim
        if hi95 and rate:
            c = 3
        elif (hi90 or rate) and c < 3:
            c = max(c, 2)
        ratio = max(inc, 0.0) / lim
        if ratio > best[0]:
            best = (ratio, g)
    return c, best[0], best[1], (cls, base, days)


# attribution: acetylene rising, an in-oil arcing tap changer, increments tracking the operations from
# the first detectable result, and acetylene that brings no hydrogen of its own: the twelve-month C2H2
# rise against the hydrogen rise over and above the pace hydrogen already had in the year before the
# first acetylene, 3 or more
ATTR = []
for tid in sorted(UNIT):
    s = UNIT[tid]
    c, sev, gas, (cls, base, days) = code(tid)
    lat = s[-1]
    inc_c2h2 = (val(lat["C2H2"]) - val(base["C2H2"])) * 365 / days
    inc_h2 = (val(lat["H2"]) - val(base["H2"])) * 365 / days
    if inc_c2h2 <= A3["C2H2"][0 if cls == "SL" else 1]:
        continue
    first = next(k for k, r in enumerate(s) if not r["C2H2"].startswith("<"))
    seg = s[first:]
    incs = [val(b["C2H2"]) - val(a["C2H2"]) for a, b in zip(seg[:-1], seg[1:])]
    ops = [ops_window(tid, a["t"].date(), b["t"].date()) for a, b in zip(seg[:-1], seg[1:])]
    r = float(np.corrcoef(incs, ops)[0, 1])
    ratio = inc_c2h2 / inc_h2 if inc_h2 > 0 else float("inf")
    t1 = s[first]["t"]
    before = [x for x in s[:first] if (t1 - x["t"]).days <= 366]
    pace = 0.0
    if len(before) >= 3:
        yrs = np.array([(x["t"] - before[0]["t"]).days / 365.25 for x in before])
        h = np.array([val(x["H2"]) for x in before])
        pace = max(float(np.polyfit(yrs, h, 1)[0]), 0.0)
    own = inc_h2 - pace
    own_ratio = inc_c2h2 / own if own > 0 else float("inf")
    inoil = REG[tid]["oltc_type"] == "In-oil arcing"
    print(f"  {tid}: in-oil {inoil}, r {r:.3f}, C2H2/H2 {ratio:.2f}, hydrogen pace before {pace:.1f}/yr, "
          f"own ratio {own_ratio:.2f}")
    if inoil and r >= 0.9 and own_ratio >= 3:
        ATTR.append(tid)
CODED = {tid: code(tid, ("C2H2",) if tid in ATTR else ()) for tid in UNIT}
NAIVE = {tid: code(tid) for tid in UNIT}
c3 = sorted([t for t in CODED if CODED[t][0] == 3], key=lambda t: -CODED[t][1])
SLATE = c3[:3]
n3 = sorted([t for t in NAIVE if NAIVE[t][0] == 3], key=lambda t: -NAIVE[t][1])
print("attributed to the tap changer:", ATTR)
print("naive slate:", n3[:3], [round(NAIVE[t][1], 2) for t in n3[:3]])
print("slate:", SLATE, [round(CODED[t][1], 2) for t in SLATE])

# ---------------------------------------------------------------------------------------------
# ask A
END = max(cdays["LST-T1"])
ASKA = {}
for tid in sorted(REG):
    if REG[tid]["oltc_type"] != "In-oil arcing":
        continue
    d0 = LAST[tid]
    if d0 < cdays[tid][0]:
        n = (cvals[tid][0] - READING[(tid, d0)]) % 100000 + ops_window(tid, cdays[tid][0], END)
    else:
        n = ops_window(tid, d0, END)
    seven = dt.date(d0.year + INOIL_YEARS, d0.month, d0.day)
    ASKA[tid] = (d0, n, n > INOIL_OPS or END > seven)

# ask B
pt = pq.read_table(f("scada_top_oil"), columns=["transformer_id", "timestamp", "top_oil_c"])
ids = np.array(pt.column("transformer_id").to_pylist())
ts = pt.column("timestamp").to_numpy().astype("datetime64[s]")
top = pt.column("top_oil_c").to_numpy()
ASKB = {}
for tid in sorted(UNIT):
    r = UNIT[tid][-1]
    if r["oil_temp_c"]:
        temp = float(r["oil_temp_c"])
    else:
        hour = r["t"].replace(minute=0)
        u = hour.replace(tzinfo=NZ).astimezone(dt.timezone.utc).replace(tzinfo=None)
        idx = np.nonzero((ids == tid) & (ts == np.datetime64(u, "s")))[0]
        temp = float(top[idx[0]])
    ws = 10 ** (WS1 - WS2 / (temp + 273))
    ASKB[tid] = (float(r["moisture_ppm"]) / ws * 100, r["t"])

# ---------------------------------------------------------------------------------------------
# against the golden deliverables
with open(os.path.join(GD, "dga_fleet_review.csv")) as fh:
    gold = {r["transformer_id"]: r for r in csv.DictReader(fh)}
expect("fleet review has 44 rows", len(gold), 44)
for tid in sorted(UNIT):
    g = gold[tid]
    expect(f"{tid} code", g["condition_code"], str(NAIVE[tid][0]))
    expect(f"{tid} severity", g["severity_score"], f"{NAIVE[tid][1]:.2f}")
    expect(f"{tid} on slate", g["on_slate"], "yes" if tid in SLATE else "no")
    expect(f"{tid} ops since service", g["oltc_operations_since_service"], str(ASKA[tid][1]) if tid in ASKA else "")
    expect(f"{tid} relative saturation", g["relative_saturation_pct"], f"{ASKB[tid][0]:.1f}")

doc = Document(os.path.join(GD, "inspection_slate_2027-28.docx"))
tabs = [[[c.text for c in row.cells] for row in t.rows] for t in doc.tables]
sl = next(t for t in tabs if t[0][0] == "Order")
expect("board paper slate", [r[1] for r in sl[1:]], SLATE)
expect("board paper codes", [r[4] for r in sl[1:]], [str(CODED[t][0]) for t in SLATE])
expect("board paper severities", [r[5] for r in sl[1:]], [f"{CODED[t][1]:.2f}" for t in SLATE])
expect("board paper gases", [r[6].lower() for r in sl[1:]],
       [{"C2H2": "acetylene", "C2H4": "ethylene", "CH4": "methane", "C2H6": "ethane", "H2": "hydrogen",
         "CO": "carbon monoxide", "CO2": "carbon dioxide"}[CODED[t][2]] for t in SLATE])
tc = next(t for t in tabs if t[0][0] == "Transformer" and "Operations since" in t[0])
expect("tap-changer table covers every in-oil tap changer", sorted(r[0] for r in tc[1:]), sorted(ASKA))
for r in tc[1:]:
    expect(f"tap-changer table {r[0]} operations", r[3].replace(",", ""), str(ASKA[r[0]][1]))
    expect(f"tap-changer table {r[0]} past interval", r[4], "Yes" if ASKA[r[0]][2] else "No")
    expect(f"tap-changer table {r[0]} last service", r[2], f"{ASKA[r[0]][0].day} {ASKA[r[0]][0]:%b %Y}")
wt = next(t for t in tabs if t[0][-1].startswith("Relative saturation"))
wet = sorted([t for t in ASKB if ASKB[t][0] > 30], key=lambda t: -ASKB[t][0])
expect("wet-transformer table", [r[0] for r in wt[1:]], wet)
for r in wt[1:]:
    expect(f"wet-transformer table {r[0]}", r[3], f"{ASKB[r[0]][0]:.1f}")

print(f"\n{'VERIFY OK' if not BAD else 'VERIFY FAILED'}: slate {SLATE}, {len(ASKA)} tap changers, "
      f"{len(wet)} wet transformers, {len(BAD)} differences")
sys.exit(1 if BAD else 0)
