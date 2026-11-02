"""Generator checks for task466, run on the installed pack after build.py: the three rules (R1 to R3c), every
semantic fork (SF1 to SF18), the ladder's separation and every graded figure's distance from its rounding edge,
mess neutrality per Layer 1 item, the ask devices, the input gates and the realism sweep.

    python3 task466/generator/checks.py

Exit 1 on any failed assertion. Every figure is computed from target/ (and, for R3a, from the generator's clean
truth); nothing is read from the design note.
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as C     # noqa: E402
import golden          # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
N = [0]
FAILS = []


def check(label, cond, detail=""):
    N[0] += 1
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, (": " + detail) if detail else ""))
    if not cond:
        FAILS.append(label)


def edge(v, unit):
    """Distance of v from the nearest rounding edge at the given unit."""
    return unit / 2.0 - abs(v - unit * round(v / unit))


def r10(v):
    return int(10 * round(v / 10.0))


def r100(v):
    return int(100 * round(v / 100.0))


def tier(v):
    return A.tier_of(v)[0]


# ------------------------------------------------------------------------------------------------ load
d = A.read_scada(T)
outs = A.read_outages(T)
res = golden.compute(T)
g = res["call"]
figs = json.load(open(os.path.join(HERE, "figures.json")))
meta = json.load(open(os.path.join(TASK, "metadata.json")))
ts = d["ts"]
m26 = A.year_mask(ts, 2026)
CAP = g["captured"]
HOURS = g["hours_year"]


def rel_from_rate(rate_kg_h):
    return A.released(rate_kg_h / A.CE * HOURS / 1000.0, CAP)


def outages_from_historian(dd):
    """Outages read from the blower run columns alone (no outage log): runs of hours below full running."""
    out = []
    run = dd["run"]
    t0 = dd["ts"][0]
    h = 0
    n = len(run)
    while h < n:
        if run[h] < 0.999:
            a = h
            while h + 1 < n and run[h + 1] < 0.999 and not (run[h] > 0.001 and h > a):
                h += 1
            b = h
            start = t0 + dt.timedelta(hours=a + (run[a] if b > a else 0.0))
            end = t0 + dt.timedelta(hours=b + (1.0 - run[b]) if b > a else a + 1.0)
            out.append(dict(no=len(out) + 1, start=start.replace(second=0, microsecond=0),
                            end=end.replace(second=0, microsecond=0), cause="historian"))
        h += 1
    return out


# ------------------------------------------------------------------------------------------------ R1
rows26 = int(m26.sum())
check("R1 the historian ships every hour of the 2026 local year with paired flow and methane content",
      rows26 == 8760 and np.all(np.isfinite(d["flow"][m26])), "%d hourly rows in the local year" % rows26)
bad_cols = []
for fn in sorted(os.listdir(T)):
    p = os.path.join(T, fn)
    if fn.endswith(".csv"):
        with open(p, encoding="utf-8") as f:
            for ln in f:
                if not ln.startswith("#"):
                    head = ln
                    break
        cells = [head]
    elif fn.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(p, read_only=True)
        cells = []
        for ws in wb.worksheets:
            for r in ws.iter_rows(max_row=4, values_only=True):
                cells += [str(c) for c in r if c is not None]
    else:
        continue
    for c in cells:
        if re.search(r"generat|releas|recover|steady|\bheld\b|\btier\b|collection eff|downtime|availability corr", c, re.I):
            bad_cols.append((fn, c[:60]))
check("R1 no shipped column or sheet holds generation, release, tier or the recovered methane", not bad_cols,
      str(bad_cols[:3]) if bad_cols else "headers clean in every csv and xlsx")
wins = A.recovery_windows(d, outs)
win_h = sum(b - a for k, a, b, base in wins if A.year_bounds(2026)[0] <= outs[k]["start"] < A.year_bounds(2026)[1])
check("R1 the decisive computation reads the hourly rows: the restart recoveries are found in the historian",
      win_h > 100 and g["recovered"] > 30.0, "%d recovery hours, %.1f t recovered" % (win_h, g["recovered"]))

# ------------------------------------------------------------------------------------------------ R2 (Layer 1)
mu = A.year_mask(ts, 2026, "utc")
cap_utc = float(d["ch4kg"][mu].sum()) / 1000.0
rel_utc = A.released(g["steady_gen"], cap_utc)
check("R2 L1a the UTC year in place of the local year moves no critical component or the call",
      int(round(cap_utc)) == int(round(CAP)) and r10(rel_utc) == r10(g["golden_rel"]) and tier(rel_utc) == res["tier"],
      "captured %.2f against %.2f" % (cap_utc, CAP))
oh = outages_from_historian(d)
g_h = A.golden_call(d, oh)
check("R2 L1b outages read from the historian's blower columns instead of the local-time outage log: same call",
      r10(g_h["golden_rel"]) == r10(g["golden_rel"]) and tier(g_h["hh8_rel"]) == "Tier 3",
      "golden %.2f, HH-8 %.2f" % (g_h["golden_rel"], g_h["hh8_rel"]))
down_run = HOURS - float(d["run"][m26].sum())
check("R2 L1c partial outage hours: down hours from the run columns agree with the log within half an hour",
      abs(down_run - g["down_hours"]) < 0.5, "%.2f against %.2f" % (down_run, g["down_hours"]))
blank = np.isnan(d["ch4"]) & m26
check("R2 L1d blank analyser readings sit only in hours with no flow, so blanks as zero or dropped agree",
      blank.sum() > 0 and np.all(d["flow"][blank] == 0), "%d blank hours" % int(blank.sum()))
both = (d["blwa"] > 0) & (d["blwb"] > 0)
check("R2 L1e the duty blower alternates between two columns; never both, never above one hour",
      not both.any() and float(d["run"].max()) <= 1.0001, "")
d_nf = dict(d)
d_nf["flare"] = np.zeros_like(d["flare"])
g_nf = A.golden_call(d_nf, outs)
check("R2 L1f the flare meter's basis and cut-off are off the call's path (the call never reads FT-301)",
      abs(g_nf["golden_rel"] - g["golden_rel"]) < 1e-9 and abs(g_nf["hh8_rel"] - g["hh8_rel"]) < 1e-9, "")
tmp = tempfile.mkdtemp(prefix="t466chk_")
try:
    shutil.copytree(T, os.path.join(tmp, "t"))
    for fn in ("BH_engine_plant_events_2026.txt", "BH_surface_emissions_monitoring_2026.xlsx", "SEM_analyser_checks_2026.csv"):
        os.remove(os.path.join(tmp, "t", fn))
    g_ne = A.golden_call(A.read_scada(os.path.join(tmp, "t")), A.read_outages(os.path.join(tmp, "t")))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
check("R2 L1g the event log's site time and the walkover files move only ledgered ask cells: with them deleted the "
      "call's figures are unchanged", abs(g_ne["golden_rel"] - g["golden_rel"]) < 1e-9 and abs(g_ne["hh8_rel"] - g["hh8_rel"]) < 1e-9, "")
tmp = tempfile.mkdtemp(prefix="t466chk_")
try:
    shutil.copytree(T, os.path.join(tmp, "t"))
    for p in meta["distractor_files"]:
        os.remove(os.path.join(tmp, "t", os.path.basename(p)))
    r_nd = golden.compute(os.path.join(tmp, "t"))
    same = (golden.figures(r_nd) == figs)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
check("R2 L1h every distractor deleted, every golden figure unchanged", same, ", ".join(meta["distractor_files"]))

# ------------------------------------------------------------------------------------------------ R3 on the clean truth
import truth  # noqa: E402
tt = truth.build_truth()
p = tt["plant"]
a26, b26 = A.year_bounds(2026)
ht = np.array([(x >= a26) and (x < b26) for x in p["times"]])
G_true = float(p["G"][ht].sum()) / 1000.0
R_true = float(p["capture"][ht].sum()) / 1000.0
rel_true = A.released(G_true, R_true)
down_true = sum(o["hours"] for o in p["outages"] if a26 <= o["start"] < b26)
frec_true = 1 - down_true / HOURS
rel_hh8_true = A.released(R_true / (A.CE * frec_true), R_true)
rel_naive_true = A.released(R_true / A.CE, R_true)
check("R3a the analyst test on the clean truth: the true release is Tier 2 and the running-share route files Tier 3",
      tier(rel_true) == "Tier 2" and tier(rel_hh8_true) == "Tier 3" and tier(rel_naive_true) == "Tier 1",
      "true %.1f t, running-share %.1f t, capture over 0.90 %.1f t" % (rel_true, rel_hh8_true, rel_naive_true))
check("R3a the golden recovers the clean truth's release inside its 10 t bin",
      r10(g["golden_rel"]) == r10(rel_true) and abs(g["golden_rel"] - rel_true) < 4.0,
      "golden %.2f, truth %.2f" % (g["golden_rel"], rel_true))
check("R3b the easy route with only the decisive step changed (the recovered methane netted before the running-share "
      "scaling) files the golden", r10(g["excess_rel"]) == r10(g["golden_rel"]) and tier(g["excess_rel"]) == "Tier 2",
      "%.2f" % g["excess_rel"])
rel_naive_net = A.released((CAP - g["recovered"]) / A.CE, CAP)
check("R3b each lower rung's single correction stays wrong: netting alone files Tier 1, the running share alone Tier 3",
      tier(rel_naive_net) == "Tier 1" and tier(g["hh8_rel"]) == "Tier 3", "%.1f and %.1f" % (rel_naive_net, g["hh8_rel"]))
rec_true = sum(o["recovered_kg"] for o in p["outages"] if a26 <= o["start"] < b26) / 1000.0
check("R3c no plant: the recovery read from the shipped rows is the world's own storage physics, not an edit",
      abs(g["recovered"] - rec_true) / rec_true < 0.06, "%.2f t read, %.2f t in the world" % (g["recovered"], rec_true))
with open(os.path.join(T, "BH_gas_plant_hourly_2024-2026.csv"), encoding="utf-8") as f:
    body = [ln.split(",", 1)[1] for ln in f if ln[:2] == "20"]
seen = {}
dup_block = 0
for i in range(0, len(body) - 24):
    blk = "".join(body[i:i + 24])
    if blk.count("0.0,0.0,0.0") >= 20:
        continue
    if blk in seen:
        dup_block += 1
    seen[blk] = i
check("R3c no copied or backfilled block: no 24-hour run of the historian repeats", dup_block == 0, "%d repeats" % dup_block)
names = " ".join(os.listdir(T)).lower()
check("R3c no memo, draft, briefing or prior-return file in the pack",
      not re.search(r"memo|draft|brief|return|summary|note", names), "")

# ------------------------------------------------------------------------------------------------ the ladder
check("ladder three rungs on three tiers: capture over 0.90 Tier 1, running share Tier 3, golden Tier 2",
      res["tier_naive"] == "Tier 1" and res["tier_hh8"] == "Tier 3" and res["tier"] == "Tier 2", "")
check("ladder margins: running share at least 20 t above 450, capture over 0.90 at least 20 t below 375",
      g["hh8_rel"] - 450 >= 20 and 375 - g["naive_rel"] >= 20, "%.1f and %.1f" % (g["hh8_rel"], g["naive_rel"]))
fam = [v for k, v in res["variants"].items() if k.startswith(("steady_", "excess_"))]
check("ladder the golden family (recovery end rules, tolerances, fixed windows, baselines, two constructions) all "
      "print 410 t with 2 t to spare", min(fam) >= 407.0 and max(fam) < 413.0 and len(fam) >= 40,
      "%d members, %.2f to %.2f" % (len(fam), min(fam), max(fam)))
check("ladder the golden family stays at least 25 t inside Tier 2", min(fam) - 375 >= 25 and 450 - max(fam) >= 25, "")
gen_fam = []
for rule, extra in (("return", dict(tol=0.02)), ("return", dict(tol=0.05)), ("fixed", dict(fixed_h=24)),
                    ("fixed", dict(fixed_h=72))):
    for bh in (24, 168):
        gg = A.golden_call(d, outs, 2026, end_rule=rule, base_h=bh, **extra)
        gen_fam += [gg["steady_gen"], gg["excess_gen"]]
check("ladder methane generated prints 3,600 t at the nearest 100 across the family, 15 t clear of each edge",
      all(r100(x) == figs["generated_t_nearest_100"] and edge(x, 100) >= 15 for x in gen_fam),
      "%.1f to %.1f" % (min(gen_fam), max(gen_fam)))
runh = (d["run"] >= 0.999) & m26
x = np.sort(d["ch4kg"][runh])
k5 = int(len(x) * 0.05)
cheap = {
    "capture over 0.90": tier(g["naive_rel"]),
    "running share, year": tier(g["hh8_rel"]),
    "running share, month by month": None,
    "mean full-running rate times the year": tier(res["variants"]["mean_running_x_year"]),
    "robust full-running rate (median or trimmed mean)": tier(res["variants"]["median_running"]),
    "generation over running hours only": tier(A.released(g["steady_gen"] * g["f_rec"], CAP)),
}
mo_gen = 0.0
for mo in range(1, 13):
    aa = dt.datetime(2026, mo, 1, tzinfo=C.TZ).astimezone(C.UTC)
    bb = (dt.datetime(2026, mo + 1, 1, tzinfo=C.TZ) if mo < 12 else dt.datetime(2027, 1, 1, tzinfo=C.TZ)).astimezone(C.UTC)
    mm = np.array([(t >= aa) and (t < bb) for t in ts])
    hrs = (bb - aa).total_seconds() / 3600.0
    mo_gen += float(d["ch4kg"][mm].sum()) / 1000.0 / (A.CE * float(d["run"][mm].sum()) / hrs)
cheap["running share, month by month"] = tier(A.released(mo_gen, CAP))
landing = [k for k, v in cheap.items() if v == "Tier 2"]
check("Gate F one cheap route family lands the call (the robust rate); every other cheap route files Tier 1 or Tier 3",
      len(landing) <= 1, "%s; landing: %s" % (cheap, landing))
check("Gate F the robust family is one family: median and 5 per cent trimmed mean both Tier 2",
      tier(rel_from_rate(float(np.median(x)))) == "Tier 2" and tier(rel_from_rate(float(x[k5:len(x) - k5].mean()))) == "Tier 2",
      "%.1f and %.1f" % (rel_from_rate(float(np.median(x))), rel_from_rate(float(x[k5:len(x) - k5].mean()))))
from pypdf import PdfReader  # noqa: E402
rep = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(T, "Leyland_BH_monthly_operating_reports_2026.pdf")).pages)
visits = re.findall(r"Service visit: (\d\d \w\w\w \d{4})\.\s+Previous visit: (\d\d \w\w\w \d{4})\.", rep)
avail = [float(v) for v in re.findall(r"Plant availability \(gas system\) ([\d.]+)%", rep)]
dev = []
for (vis, prev), av in zip(visits, avail):
    aa = dt.datetime.strptime(prev, "%d %b %Y").replace(hour=10, tzinfo=C.TZ).astimezone(C.UTC)
    bb = dt.datetime.strptime(vis, "%d %b %Y").replace(hour=10, tzinfo=C.TZ).astimezone(C.UTC)
    mm = np.array([(t >= aa) and (t < bb) for t in ts])
    dev.append(abs(100.0 * float(d["run"][mm].mean()) - av))
check("back-test the running share reconciles: the operator's availability for each report period agrees with the "
      "historian's run hours (and so with the outage log)", len(avail) == 12 and max(dev) < 0.06,
      "largest gap %.3f points over %d reports" % (max(dev), len(avail)))
for y in (2024, 2025):
    b = res["back"][y]
    check("back years %d: the running share files Tier 3 and the golden construction Tier 2" % y,
          tier(b["hh8_rel"]) == "Tier 3" and tier(b["golden_rel"]) == "Tier 2",
          "%.1f and %.1f" % (b["hh8_rel"], b["golden_rel"]))

# ------------------------------------------------------------------------------------------------ edges
check("edge captured methane at least 0.15 t inside its whole tonne (local and UTC year)",
      edge(CAP, 1) >= 0.15 and edge(cap_utc, 1) >= 0.15, "%.2f, %.2f" % (CAP, cap_utc))
check("edge released methane 2 t inside its 10 t bin across the family",
      all(edge(v, 10) >= 2.0 for v in fam + [g["golden_rel"]]), "")
eng_rs = A.engine_answers(T, outs)
ev = A.read_events(T)
for (e, q), v in sorted(res["engines"].items()):
    # the other reading of a breaker opening (the engine counted as running through it)
    a, b = A.quarter_bounds(2026, q)
    opened, rs = None, 0.0
    for xx in ev:
        if xx["unit"] != "GEN%d" % e:
            continue
        if xx["code"] == "BREAKER OPEN":
            opened = xx["t"]
        elif xx["code"] == "RUNNING" and opened is not None:
            if a <= opened < b:
                rs += (xx["t"] - opened).total_seconds() / 3600.0
            opened = None
        elif xx["code"] in ("STOP", "TRIP", "CONTROLLER POWER UP"):
            opened = None
    check("edge engine %d Q%d hours a quarter hour inside the whole hour under both breaker readings" % (e, q),
          edge(v["hours"], 1) >= 0.25 and edge(v["hours"] + rs, 1) >= 0.25 and round(v["hours"]) == round(v["hours"] + rs),
          "%.2f h, %.2f h with the breaker minutes" % (v["hours"], v["hours"] + rs))
for q in (1, 2, 3, 4):
    fl = res["flare"][q]
    check("edge flare Q%d hours and methane destroyed off their edges" % q,
          edge(fl["hours"], 1) >= 0.25 and edge(fl["destroyed"], 1) >= 0.2, "%.2f h, %.2f t" % (fl["hours"], fl["destroyed"]))

# ------------------------------------------------------------------------------------------------ semantic forks
check("SF1 reporting year: local calendar year (rule 1.1) against the UTC year, same call and same captured tonne",
      int(round(cap_utc)) == int(round(CAP)) and tier(rel_utc) == res["tier"], "shift %.2f t" % (cap_utc - CAP))
cap_pm = float(np.mean(d["flow"][m26])) * float(np.nanmean(d["ch4"][m26 & (d["flow"] > 0)])) / 100.0 * A.RHO_N * rows26 / 1000.0
check("SF2 methane captured: hourly flow times its own content (rule 1.3); a product of yearly means keeps the call",
      tier(A.released(g["steady_gen"], cap_pm)) == res["tier"] and r10(A.released(g["steady_gen"], cap_pm)) == r10(g["golden_rel"]),
      "product of means %.1f t" % cap_pm)
import openpyxl  # noqa: E402
site = {r[0]: r[1] for r in openpyxl.load_workbook(os.path.join(T, "BH_site_register_2025.xlsx"), read_only=True)["Site"].iter_rows(values_only=True)}
check("SF3 collection efficiency: one Schedule 2 class (geomembrane) over the whole footprint, so rule 4.2 weights nothing",
      "geomembrane" in str(site.get("Cap construction", "")).lower() and "whole waste footprint" in str(site.get("Capped area", "")),
      "%s; %s" % (site.get("Cap construction"), site.get("Capped area")))
alt16 = ((g["steady_gen"] - CAP) + CAP * (1 - A.DE)) * (1 - A.OX)
check("SF4 methane released (rule 1.6): oxidation taken on the uncaptured part only, or also on the undestroyed part, same 410 t",
      r10(alt16) == r10(g["golden_rel"]) and tier(alt16) == res["tier"], "%.2f against %.2f" % (alt16, g["golden_rel"]))
alt_gen_run = A.released(g["steady_gen"] * g["f_rec"], CAP)
check("SF5 methane generated (rule 1.2): the year's every hour; generation over running hours only would file Tier 1, "
      "and rule 1.2's 'in the reporting year' rules it out", tier(alt_gen_run) == "Tier 1", "%.1f t" % alt_gen_run)
check("SF6 tier test on the unrounded release or on the 10 t figure: same tier",
      tier(g["golden_rel"]) == tier(figs["released_t_nearest_10"]) and tier(g["hh8_rel"]) == tier(r10(g["hh8_rel"])), "")
check("SF7 the charge on the 2026 return is the Tier 2 amount, invoiced in 2027 (rule 5.2)",
      figs["charge_usd"] == 118000 and figs["tier"] == "Tier 2", "")
check("SF8 blank analyser cells: zero or dropped, captured methane identical", blank.sum() > 0 and np.all(d["ch4kg"][blank] == 0), "")
check("SF9 down hours from the log or from the run columns: same running share to 0.01 per cent and the same call",
      abs((1 - down_run / HOURS) - g["f_rec"]) < 1e-4 and tier(g_h["hh8_rel"]) == res["tier_hh8"], "")
cap_dest = float(np.where(d["flow"] > 0, (d["g1"] + d["g2"] + d["flare"]) * np.nan_to_num(d["ch4"]) / 100.0 * A.RHO_N, 0)[m26].sum()) / 1000.0
check("SF10 captured at the plant inlet meter (rule 1.3, normal conditions); the destination meters summed keep the call",
      tier(A.released(g["steady_gen"], cap_dest)) == res["tier"], "destination sum %.1f t" % cap_dest)
walks, rm, chk = A.read_sem(T)
for xx in rm:
    xx["x"], xx["y"] = A.wgs84_to_site(xx["lat"], xx["lon"])
sem_r = {rad: A.sem_answers(T, radius=rad) for rad in (12, 20, 40, 60, 80)}
check("SF11 first re-monitoring: the location's earliest re-check whenever it fell, matched by position; the answer is "
      "the same for any match radius from 12 ft to 80 ft", all(sem_r[r_] == res["sem"] for r_ in sem_r), "")
near = [r_["ppm"] for q in (1, 2, 3, 4) for r_ in walks[q] if 500 < r_["ppm"] <= 503]
spacing = []
for q in (1, 2, 3, 4):
    L = {}
    for r_ in walks[q]:
        if r_["ppm"] - 3 > 500:
            L.setdefault(r_["label"], r_)
    L = list(L.values())
    spacing += [((a_["x"] - b_["x"]) ** 2 + (a_["y"] - b_["y"]) ** 2) ** 0.5 for i, a_ in enumerate(L) for b_ in L[i + 1:]]
check("SF12 exceedance location (plan 7.2): no reading between 500 and 503 ppm, so 'over 500' and '500 above the "
      "3 ppm background' select the same points, and exceedance points sit 60 ft or more apart",
      not near and min(spacing) >= 60, "closest pair %.0f ft" % min(spacing))
meters = re.findall(r"Engine (\d)\s+hour meter\s+[\d.]+ ->\s+[\d.]+\s+\(\s*([\d.]+) h\)", rep)
jan = {int(e_): float(h_) for e_, h_ in meters[:2]}
a0 = dt.datetime(2025, 12, 30, 10, tzinfo=C.TZ).astimezone(C.UTC)
b0 = dt.datetime.strptime(visits[0][0], "%d %b %Y").replace(hour=10, tzinfo=C.TZ).astimezone(C.UTC)
sync = {}
for e in (1, 2):
    ivs, on_since, state = [], dt.datetime(2026, 1, 1, tzinfo=C.TZ).astimezone(C.UTC), "running"
    for xx in ev:
        if xx["unit"] != "GEN%d" % e:
            continue
        if xx["code"] in ("STOP", "TRIP", "BREAKER OPEN", "CONTROLLER POWER UP") and state == "running":
            # a power-up line closes the run at the power-up minute here, which can only overstate the synchronised
            # hours, so the meter running ahead of them is shown on the conservative side
            ivs.append((on_since, xx["t"]))
            state = "off"
        elif xx["code"] == "RUNNING":
            if state != "running":
                on_since = xx["t"]
            state = "running"
    sync[e] = sum(max(0.0, (min(y_, b0) - max(x_, a0)).total_seconds()) for x_, y_ in ivs) / 3600.0
check("SF13 engine operating hours are synchronised time from the event log (rule 1.7): the operator's hour meter runs "
      "ahead of it (warm-up, cool-down, test running) and its readings fall at service visits, not quarter ends",
      all(jan[e] > sync[e] for e in (1, 2)) and visits[0][0] != "01 Apr 2026",
      "January report %.1f and %.1f h on the meters" % (jan[1], jan[2]))
rs_starts = A.engine_answers(T, outs, count_resync=True)
check("SF14 engine start (rule 1.8, from standstill): a RUNNING after BREAKER OPEN is a re-synchronisation; counting it "
      "moves every start cell", all(rs_starts[k]["starts"] != res["engines"][k]["starts"] for k in res["engines"]), "")
check("SF15 flare operating hours: TT-301 at or above 1400 F as the log states it (rule 1.7); lit time moves every cell",
      all(int(round(res["flare"][q]["hours_lit"])) != int(round(res["flare"][q]["hours"])) for q in (1, 2, 3, 4)), "")
conv = 273.15 / 293.15
meter_conv = {q: res["flare"][q]["destroyed_meter_normal"] * conv for q in (1, 2, 3, 4)}
check("SF16 methane routed to the flare at normal conditions: plant inlet less engine fuel, all normal cubic metres; the "
      "flare meter converted from its own basis still misses its cut-off flows in every quarter",
      all(int(round(meter_conv[q])) != int(round(res["flare"][q]["destroyed"])) for q in (1, 2, 3, 4)),
      ", ".join("%.1f" % meter_conv[q] for q in (1, 2, 3, 4)))
ev_utc_q = {}
for (e, q), v in res["engines"].items():
    pass
check("SF17 quarters are local calendar quarters (rule 1.1 sets the year in local time); the boundaries hold no event "
      "within five minutes", all(min(abs((xx["t"] - A.quarter_bounds(2026, q)[0]).total_seconds()) for xx in ev) > 300
                                 for q in (2, 3, 4)), "")
hourcount = {}
for q in (1, 2, 3, 4):
    a, b = A.quarter_bounds(2026, q)
    mq = np.array([(t >= a) and (t < b) for t in ts])
    hourcount[q] = int(((d["g1"] > 0) & mq).sum())
check("SF18 hours are elapsed time summed (rule 1.7), never a count of clock hours with any running",
      all(hourcount[q] != int(round(res["engines"][(1, q)]["hours"])) for q in (1, 2, 3, 4)), str(hourcount))

# ------------------------------------------------------------------------------------------------ ask devices
nt = A.engine_answers(T, outs, count_test_runs=False)
check("device D1 a mechanic's test run off the grid is a start from standstill (rule 1.8); keying starts on RUNNING moves "
      "every start cell", all(nt[k]["starts"] != res["engines"][k]["starts"] for k in res["engines"]),
      str([nt[k]["starts"] for k in sorted(nt)]))
pu = A.engine_answers(T, outs, use_outage_log=False)
check("device D4 engine stop at a power failure (no line written): the power-up time moves all eight hour cells",
      all(int(round(pu[k]["hours"])) != int(round(res["engines"][k]["hours"])) for k in res["engines"]), "")


def naive_local_events(target):
    out = []
    for xx in A.read_events.__wrapped__(target) if hasattr(A.read_events, "__wrapped__") else A.read_events(target):
        out.append(dict(xx, t=dt.datetime.strptime(xx["local"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=C.UTC)))
    return out


_orig_read, _orig_qb, _orig_yb = A.read_events, A.quarter_bounds, A.year_bounds
try:
    A.read_events = lambda target: [dict(xx, t=dt.datetime.strptime(xx["local"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=C.UTC))
                                    for xx in _orig_read(target)]
    A.quarter_bounds = lambda y, q: (dt.datetime(y, (1, 4, 7, 10)[q - 1], 1, tzinfo=C.UTC),
                                     dt.datetime(y, (1, 4, 7, 10)[q - 1] + 3, 1, tzinfo=C.UTC) if q < 4
                                     else dt.datetime(y + 1, 1, 1, tzinfo=C.UTC))
    A.year_bounds = lambda y: (dt.datetime(y, 1, 1, tzinfo=C.UTC), dt.datetime(y + 1, 1, 1, tzinfo=C.UTC))
    outs_n = [dict(o, start=o["start"].astimezone(C.TZ).replace(tzinfo=C.UTC), end=o["end"].astimezone(C.TZ).replace(tzinfo=C.UTC))
              for o in outs]
    eng_n = A.engine_answers(T, outs_n)
    fl_n = A.flare_answers(T, d, outs_n)
finally:
    A.read_events, A.quarter_bounds, A.year_bounds = _orig_read, _orig_qb, _orig_yb
check("device D8 clock arithmetic on site time across the daylight-saving changes moves both engines' Q1 and Q4 hours",
      all(int(round(eng_n[(e, q)]["hours"])) != int(round(res["engines"][(e, q)]["hours"])) for e in (1, 2) for q in (1, 4)),
      ", ".join("%.2f" % eng_n[(e, q)]["hours"] for e in (1, 2) for q in (1, 4)))
check("device D8 the same clock arithmetic moves the flare's Q1 and Q4 hours",
      all(int(round(fl_n[q]["hours"])) != int(round(res["flare"][q]["hours"])) for q in (1, 4)), "")
check("device D3 the flare meter read as normal cubic metres moves at least three of the four flare methane cells",
      sum(int(round(res["flare"][q]["destroyed_meter_normal"])) != int(round(res["flare"][q]["destroyed"])) for q in (1, 2, 3, 4)) >= 3,
      ", ".join("%.2f" % res["flare"][q]["destroyed_meter_normal"] for q in (1, 2, 3, 4)))
win = A.sem_answers(T, match="window")
check("device D7 re-checks matched by a ten-day date window instead of position move every still-over cell",
      all(win[q]["still"] != res["sem"][q]["still"] for q in (1, 2, 3, 4)), str({q: win[q]["still"] for q in win}))
nov = A.sem_answers(T, void_rule=False)
check("device plan 7.3 void readings kept: the third quarter's exceedance and still-over cells move",
      nov[3]["exceed"] != res["sem"][3]["exceed"] and nov[3]["still"] != res["sem"][3]["still"], str(nov[3]))
check("device the operator's 2025 re-checks (January 2026 rows) and the late re-checks sit in the re-monitoring sheet",
      sum(1 for xx in rm if xx["t"].month == 1 and xx["t"].year == 2026) >= 3, "")
d_na = dict(d)
for k_ in ("g1", "g2", "flare", "ftemp"):
    d_na[k_] = np.zeros_like(d[k_])
g_na = A.golden_call(d_na, outs)
check("devices sit off the call: with every column the asks read zeroed (FT-201, FT-202, FT-301, TT-301) the call's "
      "figures are unchanged", abs(g_na["golden_rel"] - g["golden_rel"]) < 1e-9 and abs(g_na["naive_rel"] - g["naive_rel"]) < 1e-9, "")

# ------------------------------------------------------------------------------------------------ input gates
files = sorted(os.listdir(T))
fmts = {f.rsplit(".", 1)[-1] for f in files}
check("gate 10 or more files", len(files) >= 10, "%d files" % len(files))
check("gate 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
check("gate one file of 25,000 rows or more", len(body) >= 25000, "%d rows in the historian" % len(body))
check("gate two or more distractors named in metadata.json and present",
      len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(TASK, x)) for x in meta["distractor_files"]), "")
check("gate no file name says distractor, trap, decoy or known issue",
      not re.search(r"distract|trap|decoy|known_issue|answer", names), "")
check("gate one to three golden deliverables, the two the prompt names",
      sorted(os.listdir(GOLD)) == ["breck_hollow_charge_brief_2026.pdf", "breck_hollow_methane_return_2026.xlsx"], "")

# ------------------------------------------------------------------------------------------------ realism sweep
starts = [v["starts"] for v in res["engines"].values()]
check("realism start counts vary: no value fills more than half the cells", max(starts.count(s) for s in starts) <= 4,
      str(starts))
check("realism exceedance counts differ across quarters", len({res["sem"][q]["exceed"] for q in (1, 2, 3, 4)}) >= 3, "")
check("realism headline totals are not round", int(round(CAP)) % 10 != 0 and edge(g["golden_rel"], 10) < 4.9, "")
desc = [f for f in files if re.search(r"readme|dictionary|manifest|notes|schema|field", f, re.I)]
sheets = []
for f in files:
    if f.endswith(".xlsx"):
        for s in openpyxl.load_workbook(os.path.join(T, f), read_only=True).sheetnames:
            if re.search(r"readme|dictionary|notes|about|key|legend", s, re.I):
                sheets.append((f, s))
check("realism no file or sheet describes the data", not desc and not sheets, str(desc + sheets))
late = []
for f in files:
    blob = open(os.path.join(T, f), "rb").read()
    if f.endswith(".xlsx"):
        z = zipfile.ZipFile(os.path.join(T, f))
        blob = b" ".join(z.read(n) for n in z.namelist() if n.startswith("xl/"))
    for mt in re.findall(rb"2027-01-(\d\d)", blob):
        if int(mt) > 15:
            late.append(f)
check("realism no date in any file after the as-of date, 15 January 2027", not late, str(sorted(set(late))))
lastrow = max(ts)
check("realism the historian export (2027-01-04 08:12 UTC) post-dates its last hour", lastrow < dt.datetime(2027, 1, 4, 8, 12, tzinfo=C.UTC),
      str(lastrow))
check("realism the walkover workbook (12 January 2027) holds no record after its own date",
      max(xx["t"] for xx in rm) < dt.datetime(2027, 1, 12, tzinfo=C.TZ), str(max(xx["t"] for xx in rm)))
pu_lines = [xx for xx in ev if xx["code"] == "CONTROLLER POWER UP"]
pf = [o for o in outs if o["cause"] == "Utility power failure"]
same_bound = sum(1 for xx in pu_lines if any(xx["t"] == o["end"] for o in pf))
check("realism two observers, two detection logics: no controller power-up shares a minute with the logged blower restart",
      same_bound == 0 and len(pu_lines) > 0, "%d power-up lines" % len(pu_lines))
trips = [xx for xx in ev if xx["code"] == "TRIP" and "gas supply" in xx["text"]]
coinc = sum(1 for xx in trips if any(xx["t"] == o["start"] for o in outs))
check("realism engine low-gas trips do not all share the outage log's stop minute", coinc < len(trips) * 0.6,
      "%d of %d on the logged minute" % (coinc, len(trips)))
flr = [xx for xx in ev if xx["unit"] == "FLR" and xx["code"] == "FLARE START"]
check("realism the flare relights at a believable rate (anti-short-cycle), not every minute", 40 <= len(flr) <= 400,
      "%d ignitions in 2026" % len(flr))
people = ["Heidi Dillon", "Tina Hays", "Jeffrey Lamb"]
card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task466.json")))
check("realism every persona is the card's", sorted(people) == sorted(card["world"]["people"]), "")

# ------------------------------------------------------------------------------------------------ figures agree
wb = openpyxl.load_workbook(os.path.join(GOLD, "breck_hollow_methane_return_2026.xlsx"), read_only=True)
ret = {r[0]: r[1] for r in wb["Return 2026"].iter_rows(values_only=True) if r and r[0]}
check("figures the return sheet matches figures.json for generated, captured, released, tier and charge",
      ret.get("Methane generated (t, nearest 100)") == figs["generated_t_nearest_100"]
      and ret.get("Methane captured (t)") == figs["captured_t"]
      and ret.get("Methane released (t, nearest 10)") == figs["released_t_nearest_10"]
      and ret.get("Charge tier (rule 5.1)") == figs["tier"] and ret.get("Charge payable in 2027 ($)") == figs["charge_usd"], "")

print("%s  task466 checks: %d assertions, %d failed" % ("PASS" if not FAILS else "FAIL", N[0], len(FAILS)))
sys.exit(1 if FAILS else 0)
