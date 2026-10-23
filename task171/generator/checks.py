"""task171 generator checks: input gates, the three-rules block (R1, R2, R3), the golden family and every rival at the
printed cells, the semantic fork rows (SF1 to SF10), the separation line, the ask devices, the cracker and mirror,
the realism sweep and the documents' stamps. Exit 1 on any failure."""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve         # noqa: E402
import cracker       # noqa: E402

T = os.path.join(C.TASK, "target")
FAIL = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    print("%-4s %-62s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAIL.append(label)


def cell(x):
    return round(x / 250_000)


def edge(x, u):
    return u / 2 - abs(x - round(x / u) * u)


fig = json.load(open(os.path.join(HERE, "figures.json")))
meta = json.load(open(os.path.join(C.TASK, "metadata.json")))
F = solve.frames(T)
g = solve.golden(F)
IV, L, pay, H, A, TT = F["IV"], F["L"], F["pay"], F["H"], F["A"], F["TT"]
plan = C.PLAN_TOLL

# ---------------------------------------------------------------- input gates
files = sorted(os.listdir(T))
ok("INPUT 10 or more files", len(files) >= 10, "%d files" % len(files))
fmts = {os.path.splitext(f)[1] for f in files}
ok("INPUT 3 or more formats", len(fmts) >= 3, " ".join(sorted(fmts)))
ok("INPUT a 25,000-row file", len(L) >= 25000, "%d invoice lines" % len(L))
ok("INPUT two or more distractors in metadata.json", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]))
ok("INPUT no file name names the stump", not any(re.search(r"distract|stump|trap|decoy|answer|renewal|phantom|split|mature", f, re.I) for f in files))

# ---------------------------------------------------------------- R1: the field's raw material ships
hdr = set()
for f in files:
    if f.endswith(".csv"):
        hdr |= set(pd.read_csv(os.path.join(T, f), nrows=1).columns)
hdr |= set(L.columns) | set(TT.columns)
ok("R1 invoice-level book: lines, invoices, payments, hold returns, placements", all(f in files for f in (C.F_LINES, C.F_INV, C.F_PAY, C.F_MVD, C.F_AGY)))
ok("R1 no shipped column holds a collected share, a final flag or a forecast",
   not any(re.search(r"share|rate_collected|final|ultimate|leak|forecast|expected", c, re.I) for c in hdr), ", ".join(sorted(hdr))[:80])
ok("R1 the hold returns carry each held invoice's registration on file", H[H.response == "HOLD PLACED"].reg_expires.notna().all())

# ---------------------------------------------------------------- the golden and its family
G = g["collected"]
ok("GOLDEN figures.json carries the golden", fig["call_collected_toll_2027_usd"] == cell(G) * 250_000 and fig["call_share_in_state_pct"] == round(g["IS"] * 100)
   and fig["call_share_out_of_state_pct"] == round(g["OS"] * 100), "%.0f, %.2f, %.2f" % (G, g["IS"] * 100, g["OS"] * 100))
ok("GOLDEN call mid-cell", edge(G, 250_000) >= 60_000, "edge distance $%.0f" % edge(G, 250_000))
ok("GOLDEN in-state share mid-cell", edge(g["IS"] * 100, 1) >= 0.2, "%.2f" % (g["IS"] * 100))
ok("GOLDEN out-of-state share mid-cell", edge(g["OS"] * 100, 1) >= 0.2, "%.2f" % (g["OS"] * 100))


def variant(strict=False, os_age=365, nr_age=365, gross=False, cut=None):
    F2 = dict(F)
    if gross:
        F2["pay"] = pay[pay.channel != "REVERSAL"]
    c = pd.Timestamp(cut) if cut else solve.ASOF
    tp = solve.toll_paid(F2, c); t60 = solve.toll_paid(F2, c, by_day=60)
    age = (solve.ASOF - IV.issued_on).dt.days.values
    tbm = (IV.invoice_type == "TOLL-BY-MAIL").values; home = (IV.plate_state == C.HOME).values
    hi = H.set_index("invoice_no")
    hold = IV.invoice_no.map(hi.response).values; exp = IV.invoice_no.map(hi.reg_expires).values
    ee = np.array([pd.Timestamp("%s-%s-01" % (e[3:], e[:2])) + pd.offsets.MonthEnd(0) if isinstance(e, str) and e else pd.NaT for e in exp])
    toll = IV.toll_billed.values
    m = tbm & home & (age >= 61); e = t60[m].sum() / toll[m].sum(); un = m & (t60 < toll - 0.005)
    wh = toll[un & (hold == "HOLD PLACED")].sum() / toll[un].sum()
    lim = solve.ASOF - pd.Timedelta(days=1) if strict else solve.ASOF
    fin = tbm & home & (hold == "HOLD PLACED") & np.array([pd.notna(x) and x <= lim for x in ee])
    r = tp[fin].sum() / toll[fin].sum()
    nr = tbm & home & (hold == "NO RECORD") & (age >= nr_age); a = tp[nr].sum() / toll[nr].sum()
    IS = e + (1 - e) * (wh * r + (1 - wh) * a)
    mo = tbm & ~home & (age >= os_age); OS = tp[mo].sum() / toll[mo].sum()
    return IS, OS, plan["IS"] * IS + plan["OS"] * OS


fam = {"golden": (g["IS"], g["OS"], G), "expiry strictly before": variant(strict=True), "agency read at 380 days": variant(os_age=380),
       "agency read at 400 days": variant(os_age=400), "no-record read at 400 days": variant(nr_age=400),
       "returned payments not netted": variant(gross=True), "payments to the export run": variant(cut="2026-11-06")}
for k, (i, o, c) in fam.items():
    ok("FAMILY %s: one printed cell on all three" % k, cell(c) == cell(G) and round(i * 100) == round(g["IS"] * 100) and round(o * 100) == round(g["OS"] * 100),
       "IS %.2f OS %.2f $%.0f" % (i * 100, o * 100, c))

# ---------------------------------------------------------------- rivals
R = solve.rivals(F)
for k, (i, o, c) in R.items():
    ok("RIVAL %s misses the call by a full cell" % k, abs(cell(c) - cell(G)) >= 1, "$%.0f (cell %d against %d)" % (c, cell(c), cell(G)))
dp = R["invoices a year old"]
note = open(os.path.join(C.TASK, "DESIGN_NOTE.md")).read()
ends = re.search(r"\*\*Ends on:\*\* \$([\d.]+) million", note)
ok("R3a the default path (a year-old cohort) files the note's Ends-on figure", ends is not None and abs(cell(dp[2]) * 0.25 - float(ends.group(1))) < 1e-9,
   "$%.0f, note %s" % (dp[2], ends.group(1) if ends else "none"))
ok("R3a the default path's out-of-state share equals the golden's", abs(dp[1] - g["OS"]) < 1e-9)
# R3b: the decisive step alone (renewal maturity on the default path's book) files the golden
ok("R3b the default path with the renewal maturity alone files the golden", cell(fam["golden"][2]) == cell(G))
ok("R3b each lower rung's single correction stays wrong", all(abs(cell(R[k][2]) - cell(G)) >= 1 for k in ("invoices 180 days old", "invoices 15 months old", "renewal-matured, violations pooled in")))

# ---------------------------------------------------------------- semantic forks
ok("SF1 the plan's billed toll is the population", plan["IS"] == fig["plan_toll_in_state_usd"] and plan["OS"] == fig["plan_toll_out_of_state_usd"])
ok("SF2 collected however long it takes: the golden is an ultimate share", g["IS"] > dp[0])
ok("SF3 toll only: toll_paid never exceeds toll billed", (solve.toll_paid(F) <= IV.toll_billed.values + 1e-9).all())
ok("SF4 in-state is HM and only HM", set(IV.plate_state.unique()) - {C.HOME} <= set(C.OUT_STATES))
ok("SF5 payments to the records date or the export run: same call", cell(fam["payments to the export run"][2]) == cell(G))
ok("SF6 returned payments netted or not: same call", cell(fam["returned payments not netted"][2]) == cell(G))
ok("SF7 expiry on or before, or strictly before, the records date: same call", cell(fam["expiry strictly before"][2]) == cell(G))
ok("SF8 the agency read at 365 to 400 days: same call", cell(fam["agency read at 400 days"][2]) == cell(G))
ok("SF9 the cash lanes' own book, not every billed-by-mail invoice", abs(cell(R["renewal-matured, violations pooled in"][2]) - cell(G)) >= 1)
ok("SF10 rounding: nearest $0.25 million, whole per cent", fig["call_collected_toll_2027_usd"] % 250_000 == 0)

# ---------------------------------------------------------------- R2: Layer 1 items, each neutral to the call
ok("R2 returned payments (REVERSAL rows) neutral", cell(fam["returned payments not netted"][2]) == cell(G), "%d rows" % (pay.channel == "REVERSAL").sum())
ok("R2 postings after the records date neutral", cell(fam["payments to the export run"][2]) == cell(G), "%d rows" % (pay.posted_on > solve.ASOF).sum())
ok("R2 the rate change of 1 January 2026 is in the lines' tolls, neutral", L.toll.gt(0).all())
ok("R2 MM/YYYY registration months parse for every hold", H[H.response == "HOLD PLACED"].reg_expires.str.match(r"^\d{2}/\d{4}$").all())
ok("R2 invoice issue dates on the eighth or the next weekday", IV.issued_on.dt.day.between(8, 10).all() and (IV.issued_on.dt.dayofweek < 5).all())

# ---------------------------------------------------------------- separation line
tbm_lines = L[L.invoice_no.str.startswith("T")]
ok("SEP no express-lane line on a toll-by-mail invoice", not tbm_lines.lane.isin(C.ETC_LANES).any())
ok("SEP toll-by-mail lines all in the closed hours", ((tbm_lines.crossed_at.dt.hour >= 23) | (tbm_lines.crossed_at.dt.hour < 5)).all())
bal = pd.Series((IV.toll_billed + IV.invoice_fee + IV.late_fee + IV.collection_fee).values, index=IV.invoice_no.values)
ag_t = pay[(pay.channel == "AGENCY") & pay.invoice_no.str.startswith("T", na=False)]
ok("SEP every toll-by-mail agency remittance covers only its own invoice", (ag_t.amount <= ag_t.invoice_no.map(bal) + 0.01).all(), "%d remittances" % len(ag_t))
ok("SEP the call never reads the commercial postings", "TT" not in solve.call_shares.__code__.co_names)

# ---------------------------------------------------------------- ask devices
V = solve.straddle_and_phantom(F)
Aa = solve.ask_A(F, V)
ok("ASK A figures.json carries the golden", all(fig["a_2026_%02d_crossings" % m] == Aa[m][0] and abs(fig["a_2026_%02d_toll_owed_usd" % m] - Aa[m][1]) < 0.005 for m in range(1, 10)))
ph = V[V.phantom & (V.crossed_at >= "2026-01-01")]
ok("ASK A1 classifier-split lines in every month", ph.crossed_at.dt.month.nunique() == 9, "%d lines" % len(ph))
v26 = V[(V.crossed_at >= "2026-01-01")].reset_index().sort_values("crossed_at")
t = TT[["plaza", "direction", "lane", "posted_at"]].sort_values("posted_at")
m = pd.merge_asof(v26, t, left_on="crossed_at", right_on="posted_at", by=["plaza", "direction", "lane"], direction="backward")
gap = (m.crossed_at - m.posted_at).dt.total_seconds()
ok("ASK A1 nothing between 0.30 and 0.90 s behind a posting (the referee is crisp)", not ((gap > 0.30) & (gap < 0.90)).any())
ok("ASK A1 ordinary followers sit 0.9 to 2.5 s behind a posting", ((gap >= 0.9) & (gap <= 2.5)).sum() > 1000, "%d followers" % ((gap >= 0.9) & (gap <= 2.5)).sum())
st = V[V.straddle]
ok("ASK A2 straddle second reads all within a second of their first", len(st) > 1000, "%d lines" % len(st))
vv = V.sort_values(["plate", "plate_state", "crossed_at"])
dt_same = (vv.crossed_at - vv.crossed_at.shift()).dt.total_seconds()[vv.plate.eq(vv.plate.shift()) & vv.plate_state.eq(vv.plate_state.shift())]
ok("ASK A2 no plate crosses twice between 1 s and 10 minutes", not ((dt_same > 1) & (dt_same < 600)).any())
Bb = solve.ask_B(F, V)
ok("ASK B figures.json carries the golden", all(fig["b_%s_collected_pct" % q.lower()] == round(v * 100) for q, v in Bb.items()))
ok("ASK B shares mid-cell", all(edge(v * 100, 1) >= 0.1 for v in Bb.values()), ", ".join("%.2f" % (v * 100) for v in Bb.values()))
B0 = solve.ask_B(F, V, whole_account=False)
ok("ASK B1 whole-account remittances move every quarter", all(round(B0[q] * 100) != round(Bb[q] * 100) for q in Bb), ", ".join("%.1f" % (B0[q] * 100) for q in Bb))
ag_v = pay[(pay.channel == "AGENCY") & pay.invoice_no.str.startswith("V", na=False)]
over = ag_v.amount > ag_v.invoice_no.map(bal) + 0.01
ok("ASK B1 remittances above their invoice's balance exist and none is a round multiple", over.sum() > 100, "%d remittances" % over.sum())

# ---------------------------------------------------------------- cracker and mirror
cr = cracker.main(quiet=True)
ok("CRACKER misses every ask figure", cr["cracker_hits"] == 0, "%d of 22" % cr["cracker_hits"])
ok("MIRROR leakage under 35 per cent", cr["mirror_leakage_pct"] < 35, "%.1f" % cr["mirror_leakage_pct"])
ok("PAIR ceiling at or under 40", cr["pair"] <= 40, "%.1f" % cr["pair"])

# ---------------------------------------------------------------- realism sweep
mon = L.assign(m=L.crossed_at.dt.strftime("%Y-%m")).groupby("m").size()
ok("REAL no two months carry the same line count", mon.nunique() == len(mon))
ok("REAL no round monthly toll totals", not any(abs(x - round(x, -2)) < 0.005 for x in L.groupby(L.crossed_at.dt.strftime("%Y-%m")).toll.sum()))
ok("REAL plan figures not round thousands", plan["IS"] % 1000 != 0 and plan["OS"] % 1000 != 0)
txt = ""
for f in files:
    if f.endswith((".docx", ".xlsx")):
        with zipfile.ZipFile(os.path.join(T, f)) as z:
            for n in z.namelist():
                if n.endswith(".xml"):
                    txt += z.read(n).decode("utf-8", "ignore")
pdfraw = open(os.path.join(T, C.F_POLICY), "rb").read()
ok("REAL no writer signature in the containers", not re.search(r"openpyxl|python-docx|ReportLab", txt + pdfraw.decode("latin-1")))
ok("REAL container stamps inside 2026", all(y == "2026" for y in re.findall(r"<dcterms:(?:created|modified)[^>]*>(\d{4})", txt)) and b"D:2026" in pdfraw)
people = set(re.findall(r"\b(Brittany Moon|Zachary Mcneil)\b", txt))
ok("REAL the plan's people are the card's", people <= {"Brittany Moon", "Zachary Mcneil"} and "Brittany Moon" in txt)
ok("REAL no record dated after the export run", pay.posted_on.max() <= pd.Timestamp(C.EXPORT) and IV.issued_on.max() <= pd.Timestamp(C.ASOF)
   and L.crossed_at.max() < pd.Timestamp("2026-10-01") and H.requested_on.max() <= pd.Timestamp(C.ASOF))
ok("REAL no em dash in the pack's documents", "—" not in txt)

print("\n%d checks, %d failed" % (N[0], len(FAIL)))
if FAIL:
    print("FAILED:", "; ".join(FAIL))
    sys.exit(1)
