"""verify.py: an independent recomputation from the shipped bundle alone, on its own code path (csv and zipfile
readers, its own grid transformation fitted to the survey monuments, pypdf for the documents). Nothing is imported
from the generator.

    python3 verify.py            exit 0 when every figure the write-up states recomputes
"""
import csv
import datetime as dt
import io
import json
import math
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ZIP = os.path.join(TASK, "target.zip")
OZ = 31.1034768
OUT = []


def ok(name, cond, detail=""):
    OUT.append((name, bool(cond), detail))


def r(v, u):
    return int(round(v / u)) * u


def bundle():
    z = zipfile.ZipFile(ZIP)
    return {n.split("/", 1)[1]: z.read(n) for n in z.namelist()}


def rows(b, name):
    text = b[name].decode("utf-8")
    lines = [l for l in text.splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def fit_similarity(b):
    """Least-squares similarity transform UTM -> mine grid from the control monuments (not the stated parameters)."""
    txt = b["kelvanna_mine_grid_control.txt"].decode("utf-8")
    pts = [tuple(map(float, m.groups())) for m in
           re.finditer(r"KCM-\d+\s+([\d.]+)\s+([\d.]+)\s+[\d.]+\s+([\d.]+)\s+([\d.]+)", txt)]
    X = np.array([[p[2], p[3]] for p in pts])
    Y = np.array([[p[0], p[1]] for p in pts])
    mx, my = X.mean(0), Y.mean(0)
    A = X - mx
    B = Y - my
    a = (A[:, 0] * B[:, 0] + A[:, 1] * B[:, 1]).sum() / (A ** 2).sum()
    c = (A[:, 0] * B[:, 1] - A[:, 1] * B[:, 0]).sum() / (A ** 2).sum()

    def f(e, n):
        de, dn = np.asarray(e) - mx[0], np.asarray(n) - mx[1]
        return my[0] + a * de - c * dn, my[1] + c * de + a * dn
    return f, len(pts)


def gc_blocks(b, f):
    acc = {}
    for d in rows(b, "gc_assays_lims_export_20261105.csv"):
        if d["SAMPLE_TYPE"] not in ("BH", "BLASTHOLE"):
            continue
        v = d["AU_PPB"]
        g = float(d["AU_GRAV_GPT"]) if v.startswith(">") else (float(v[1:]) / 2000.0 if v.startswith("<") else float(v) / 1000.0)
        x, y = f(float(d["EASTING_UTM17"]), float(d["NORTHING_UTM17"]))
        i, j = int((x - 10000.0) // 10), int((y - 20000.0) // 10)
        k = (1295 - int(d["BENCH"])) // 5
        key = i * 10000 + j * 100 + k
        s = acc.setdefault(key, [0.0, 0])
        s[0] += g
        s[1] += 1
    return {k: v[0] / v[1] for k, v in acc.items()}


def model(b):
    return {int(d["IJK"]): (float(d["AU_OK"]), float(d["DENSITY"]) * 500.0) for d in rows(b, "kl_mz_resource_model_2026R.csv")}


def plan(b):
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(b["kelvanna_mine_plan_2027_v3.xlsx"]), read_only=True, data_only=True)
    it = wb["Schedule"].iter_rows(values_only=True)
    hdr = next(it)
    ix = {h: n for n, h in enumerate(hdr)}
    return [(int(rw[ix["IJK"]]), float(rw[ix["AU_OK"]]), float(rw[ix["TONNES"]])) for rw in it]


def lognormal_budget(pairs, sched, cut=0.90):
    from scipy.stats import norm
    lr = np.log(np.array([g / m for m, g, t in pairs]))
    s = lr.std()
    au, tt = 0.0, 0.0
    for _, m, t in sched:
        au += t * m * norm.cdf((math.log(m / cut) + s * s / 2) / s)
        tt += t * norm.cdf((math.log(m / cut) - s * s / 2) / s)
    return au / OZ, tt


def refactor(pairs, sched, cut=0.90):
    gc_oz = sum(t * g for m, g, t in pairs if g >= cut)
    md_oz = sum(t * m for m, g, t in pairs if m >= cut)
    plan_oz = sum(t * m for _, m, t in sched if m >= cut)
    return plan_oz * gc_oz / md_oz / OZ


def dst(y):
    a = dt.datetime(y, 3, 8)
    while a.weekday() != 6:
        a += dt.timedelta(days=1)
    c = dt.datetime(y, 11, 1)
    while c.weekday() != 6:
        c += dt.timedelta(days=1)
    return a.replace(hour=2), c.replace(hour=2)


def to_local(u):
    a, c = dst(u.year)
    loc = u - dt.timedelta(hours=5)
    return u - dt.timedelta(hours=4) if a <= loc < c else loc


def stockpile(b):
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(b["haul_fleet_register_2026-10.xlsx"]), read_only=True, data_only=True)
    units = []
    for sh in ("Fleet", "Disposals"):
        it = wb[sh].iter_rows(values_only=True)
        hdr = next(it)
        for rw in it:
            d = dict(zip(hdr, rw))
            if str(d["UNIT"]).startswith("T-"):
                ins = d["IN_SERVICE"].date() if hasattr(d["IN_SERVICE"], "date") else d["IN_SERVICE"]
                out = d.get("DISPOSED")
                out = out.date() if hasattr(out, "date") else dt.date(2100, 1, 1)
                units.append((d["UNIT"], float(d["NOMINAL_PAYLOAD_T"]), ins, out))
    hauls = []
    for d in rows(b, "dispatch_loads_to_lgsp_2023-2026.csv"):
        u = dt.datetime.strptime(d["TIME_UTC"], "%Y-%m-%dT%H:%M:%SZ")
        hauls.append((d["TRUCK"], u, d["SOURCE"], float(d["SOURCE_AU_GPT"])))
    hauls.sort()
    kept, last = [], {}
    for truck, u, src, g in hauls:
        p = last.get(truck)
        last[truck] = (u, src)
        if p and p[1] == src and (u - p[0]).total_seconds() < 600:
            continue
        kept.append((truck, to_local(u), g))
    inv = [d for d in rows(b, "stockpile_inventory_2022-12-31.csv") if d["STOCKPILE"].startswith("LGSP")][0]
    t0 = float(inv["TONNES"].replace(",", ""))
    a0 = t0 * float(inv["AU_GPT"])
    out = []
    for end in (dt.datetime(2024, 1, 1), dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1)):
        t, a = t0, a0
        for truck, loc, g in kept:
            if loc < end:
                pay = [p for no, p, i, o in units if no == truck and i <= loc.date() < o][0]
                t += pay
                a += pay * g
        out.append((t, a / OZ))
    return out


QUARTERS = [(dt.datetime(2025, 1, 1), dt.datetime(2025, 4, 1)), (dt.datetime(2025, 4, 1), dt.datetime(2025, 7, 1)),
            (dt.datetime(2025, 7, 1), dt.datetime(2025, 10, 1)), (dt.datetime(2025, 10, 1), dt.datetime(2026, 1, 1)),
            (dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1)), (dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1)),
            (dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1))]


def hours(b):
    ev = sorted({(d["TIME_UTC"], d["VALUE"]) for d in rows(b, "dcs_event_export_grinding_2025-2026.csv")
                 if "BM" in d["TAG"] and ("101" in d["TAG"] or "BM01" in d["TAG"])})
    intervals, state, since = [], None, None
    for t, v in ev:
        loc = to_local(dt.datetime.strptime(t, "%Y-%m-%d %H:%M:%S"))
        if state is None or v != state:
            if state == "0":
                intervals.append((since, loc))
            state, since = v, loc
    if state == "0":
        intervals.append((since, dt.datetime(2026, 11, 1)))
    for d in rows(b, "cmms_work_orders_grinding_2025-2026.csv"):
        if d["WO_TYPE"] == "SD":
            intervals.append((dt.datetime.strptime(d["ACTUAL_START"], "%Y-%m-%d %H:%M"),
                              dt.datetime.strptime(d["ACTUAL_FINISH"], "%Y-%m-%d %H:%M")))
    out = []
    for a, c in QUARTERS:
        mins = int((c - a).total_seconds() // 60)
        down = np.zeros(mins, dtype=bool)
        for x, y in intervals:
            lo = max(0, int((x - a).total_seconds() // 60))
            hi = min(mins, int(math.ceil((y - a).total_seconds() / 60)))
            if hi > lo:
                down[lo:hi] = True
        out.append((mins - down.sum()) / 60.0)
    return out


def fine(b):
    bars = {}
    for d in rows(b, "goldroom_bar_register_2025-2026.csv"):
        yy, seq = d["BAR_NO"].split("-")
        bars[(int(seq), d["POUR_DATE"])] = float(d["GROSS_OZT"])
    lines = rows(b, "refinery_outturn_statements_2025-2026.csv")
    lot_bars = {}
    for d in lines:
        seq = int(d["CLIENT_REF"].split()[-1])
        rec = dt.date.fromisoformat(d["RECEIVED_DATE"])
        cands = [k for k in bars if k[0] == seq and 0 <= (rec - dt.date.fromisoformat(k[1])).days <= 60]
        lot_bars.setdefault(d["LOT_NO"], (float(d["LOT_FINE_AU_OZT"]), set()))[1].add(cands[0])
    per_bar = {}
    for lot, (fine_oz, members) in lot_bars.items():
        g = sum(bars[k] for k in members)
        for k in members:
            per_bar[k] = per_bar.get(k, 0.0) + fine_oz * bars[k] / g
    out = []
    for a, c in QUARTERS:
        out.append(sum(v for k, v in per_bar.items() if a.date() <= dt.date.fromisoformat(k[1]) < c.date()))
    return out


def pdf_texts(b, name):
    import pypdf
    rd = pypdf.PdfReader(io.BytesIO(b[name]))
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in rd.pages))


def main():
    b = bundle()
    F = json.load(open(os.path.join(HERE, "figures.json")))
    f, nmon = fit_similarity(b)
    ok("grid: the transformation is fitted to the survey's own monuments", nmon >= 3, nmon)
    gc = gc_blocks(b, f)
    mdl = model(b)
    pairs = [(mdl[k][0], g, mdl[k][1]) for k, g in gc.items() if k in mdl]
    sched = plan(b)
    ok("pairs: every blast-hole block lands in a model block", len(pairs) == F["n_pairs"], (len(pairs), F["n_pairs"]))
    plan_oz = sum(t * m for _, m, t in sched if m >= 0.90) / OZ
    plan_t = sum(t for _, m, t in sched if m >= 0.90)
    ok("plan basis: model gold at 0.90 g/t prints %s oz" % F["plan_oz_100"], r(plan_oz, 100) == F["plan_oz_100"], round(plan_oz))
    ok("plan basis: model ore prints %.2f Mt" % F["plan_mt_2dp"], round(plan_t / 1e6, 2) == F["plan_mt_2dp"], plan_t)
    f05 = sum(t * g for m, g, t in pairs if g >= 0.5) / sum(t * m for m, g, t in pairs if m >= 0.5)
    f09 = sum(t * g for m, g, t in pairs if g >= 0.9) / sum(t * m for m, g, t in pairs if m >= 0.9)
    ok("record: gold factor at 0.50 g/t prints %.2f" % F["f05_2dp"], round(f05, 2) == F["f05_2dp"], f05)
    ok("record: gold factor at 0.90 g/t prints %.1f" % F["f09_1dp"], round(f09, 1) == F["f09_1dp"], f09)
    au, tt = lognormal_budget(pairs, sched)
    ok("budget: the log-normal per-block reading prints %s oz" % format(F["budget_oz"], ","), r(au, 10000) == F["budget_oz"], round(au))
    ok("budget: its ore prints %s t" % format(F["ore_t_100k"], ","), r(tt, 100000) == F["ore_t_100k"], round(tt))
    ra = refactor(pairs, sched)
    ok("budget: the record's re-cut factor on the plan prints the same", r(ra, 10000) == F["budget_oz"], round(ra))
    ok("budget: the reports' 0.50 g/t factor on the plan prints another cell", r(plan_oz * f05, 10000) != F["budget_oz"],
       round(plan_oz * f05))
    st = stockpile(b)
    ok("stockpile: every date recomputes", [(r(t, 1000), r(a, 100)) for t, a in st] == [(x[1], x[2]) for x in F["stock_rows"]],
       [(round(t), round(a)) for t, a in st])
    hs = hours(b)
    ok("ball mill hours: every quarter recomputes", [r(h, 1) for h in hs] == [x[1] for x in F["hours_rows"]], [round(h, 2) for h in hs])
    fg = fine(b)
    ok("fine gold: every quarter recomputes", [r(v, 100) for v in fg] == [x[1] for x in F["fine_rows"]], [round(v) for v in fg])
    memo = pdf_texts(b, "budget_2027_basis_of_ore_and_gold.pdf")
    ok("memo (pypdf): the ore definition is filed", "A block is ore when its grade-control grade is 0.90 g/t or more" in memo)
    ok("memo (pypdf): budget gold is contained gold in calendar 2027", "gold contained in the ore mined in calendar 2027" in memo)
    rep = pdf_texts(b, "monthly_reconciliation_jan2023_oct2026.pdf")
    m_ = re.search(r"Jan 2023-Oct 2026 ((?:[\d.]+ ){14})", rep + " ")
    nums = m_.group(1).split() if m_ else []
    ok("reconciliation (pypdf): the report's summary F1 equals the recomputed factor at 0.50 g/t",
       nums and abs(float(nums[11]) - round(f05, 2)) < 1e-9, nums[:14])
    ok("reconciliation (pypdf): the report is at the 0.50 g/t cut-off", "0.50 g/t cut-off" in rep)
    # the goldens agree with the write-up
    from openpyxl import load_workbook
    gb = load_workbook(os.path.join(TASK, "golden", "kelvanna_2027_budget_gold.xlsx"), data_only=True)
    ws = gb["Budget gold"]
    ok("golden workbook: budget gold and ore match", ws["C5"].value == F["budget_oz"] and ws["B5"].value == F["ore_t_100k"],
       (ws["C5"].value, ws["B5"].value))
    sv = open(os.path.join(TASK, "golden", "lg_stockpile_2023-2026.svg"), encoding="utf-8").read()
    ok("golden chart: every stockpile label is drawn", all(format(x[2], ",") in sv for x in F["stock_rows"]))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    ok("write-up: the call states %s oz" % format(F["budget_oz"], ","), "**Budget %s ounces" % format(F["budget_oz"], ",") in sub)
    fails = [o for o in OUT if not o[1]]
    for n, c, d in OUT:
        print("%s  %s%s" % ("PASS" if c else "FAIL", n, "" if c else "  " + str(d)[:200]))
    print("%d checks, %d FAIL" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
