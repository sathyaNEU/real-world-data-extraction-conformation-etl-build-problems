"""task286 generator checks: the clean truth, the ladder, every semantic fork row, the three rules (R1 to R3c),
mess neutrality, the asks' devices, the realism sweep and the input gates. Exit 1 on any failure."""
import csv
import json
import os
import re
import sys
import zipfile
from collections import Counter
from datetime import date, timedelta

import numpy as np

import world as W
import records as R
import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


homes, parents, entries, oas = R.build_all()
A = W.AREA_CODES
NM = W.AREA_NAME
ORR, ELL, KIT, TAR = "SW01", "SW03", "SW04", "TV04"
OBS = {h.i: G.observed_daily(h) for h in homes}
WIN = {h.i: OBS[h.i][W.W0:W.W1 + 1].reshape(W.NWEEKS, 7) for h in homes}


def tally(pred):
    c = {a: 0 for a in A}
    for h in homes:
        if pred(h):
            c[h.area] += 1
    return c


def winner(c):
    s = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
    return s[0][0], s[0][1] / max(1, s[1][1]), [k for k, _ in s]


def golden_counts(margin=G.USE_MARGIN):
    return tally(lambda h: int(((WIN[h.i].max(1) - WIN[h.i].min(1)) <= margin).sum()) >= 26)


def void_counts(v):
    return tally(lambda h: int((WIN[h.i].sum(1) < v).sum()) >= 26)


figs = json.load(open(os.path.join(HERE, "figures.json")))
gold = golden_counts()
truth = tally(lambda h: h.empty_weeks >= 26)

# ------------------------------------------------------------------------------------------------- truth
check("T1 golden reading equals the clean truth in every area", gold == truth, str({NM[a]: gold[a] for a in A}))
check("T2 figures.json carries the golden counts",
      all(figs["areas"][NM[a]]["left_empty"] == gold[a] for a in A) and figs["call"] == NM[ORR])
wa, wm, order = winner(gold)
check("T3 golden names Orrimouth by 1.2x or more", wa == ORR and wm >= 1.2, "%s x%.3f" % (NM[wa], wm))
check("T4 runner-up Ellingsea and the gap", order[1] == ELL and figs["gap"] == gold[ORR] - gold[ELL],
      "gap %d" % figs["gap"])
check("T5 no two areas share a count of homes left empty", len(set(gold.values())) == len(A))
# separation on the shipped series: every week clearly used or clearly not
mx_empty, mn_use = 0, 10 ** 9
for h in homes:
    tw = W.window_weeks_true(h)
    rg = WIN[h.i].max(1) - WIN[h.i].min(1)
    if (~tw).any():
        mx_empty = max(mx_empty, int(rg[~tw].max()))
    if tw.any():
        mn_use = min(mn_use, int(rg[tw].min()))
check("T6 an empty week's daily totals vary by 30 litres or less", mx_empty <= 30, str(mx_empty))
check("T7 a week of use varies by 80 litres or more", mn_use >= 80, str(mn_use))

# ------------------------------------------------------------------------------- the standing family (SF)
same = all(golden_counts(m) == gold for m in range(30, 80, 5))
check("SF11 every margin from 30 to 75 litres files the same count in every area", same)
fl = tally(lambda h: int((WIN[h.i].max(1) <= WIN[h.i].min() + 50).sum()) >= 26)
fl2 = all(tally(lambda h, m=m: int((WIN[h.i].max(1) <= WIN[h.i].min() + m).sum()) >= 26) == gold
          for m in (35, 50, 65, 85))
check("SF11 a floor read (each home's lowest day plus 35 to 85 litres) files the same counts", fl == gold and fl2)


def bands(c_pred):
    out = {a: [0, 0, 0] for a in A}
    for h in homes:
        e = c_pred(h)
        if e >= 26:
            out[h.area][0 if e <= 38 else (1 if e <= 51 else 2)] += 1
    return out


b_gold = bands(lambda h: int(((WIN[h.i].max(1) - WIN[h.i].min(1)) <= 50).sum()))
b_alt = bands(lambda h: int(((WIN[h.i].max(1) - WIN[h.i].min(1)) <= 70).sum()))
check("SF11 the week bands (26 to 38, 39 to 51, 52) agree across the margins", b_gold == b_alt and all(
    b_gold[a] == [figs["areas"][NM[a]]["w26_38"], figs["areas"][NM[a]]["w39_51"], figs["areas"][NM[a]]["w52"]]
    for a in A))
# SF1 homes are the gazetteer's dwellings; parent shells carry no meter and no count
check("SF1 parent shells have no water property, so only dwellings are counted",
      all(p["uprn"] not in {h.uprn for h in homes} for p in parents))
# SF2 the 52 weeks, not the extract's 57: the window changes the counts and ToR 4.1 fixes it
ext = tally(lambda h: int(((OBS[h.i][:399 - 399 % 7].reshape(-1, 7).max(1) -
                            OBS[h.i][:399 - 399 % 7].reshape(-1, 7).min(1)) <= 50).sum()) >= 26)
check("SF2 counting over the whole extract moves the counts (ruled out by ToR 4.1), the call holds",
      ext != gold and winner(ext)[0] == ORR)
# SF2b weeks Sunday to Saturday instead of Monday to Sunday: the call holds
sun = tally(lambda h: int(((OBS[h.i][W.W0 - 1:W.W1].reshape(52, 7).max(1) -
                            OBS[h.i][W.W0 - 1:W.W1].reshape(52, 7).min(1)) <= 50).sum()) >= 26)
check("SF6 weeks read one day earlier (the hour BST moves a UTC day) still name Orrimouth", winner(sun)[0] == ORR)
# SF3 a week of use is any day with anybody in; a reading needing most days in use is ruled out by ToR 4.3
maj = tally(lambda h: int((h.present[W.W0:W.W1 + 1].reshape(52, 7).sum(1) < 4).sum()) >= 26)
check("SF3 'lived in on most days' would count more homes (ToR 4.3 rules it out)", maj != gold)
# SF4 a share of homes instead of a count: same call
share = {a: gold[a] / figs["areas"][NM[a]]["homes"] for a in A}
check("SF4 the share of each area's homes names the same area", max(share, key=share.get) == ORR,
      "%.4f vs %.4f" % (share[ORR], sorted(share.values())[-2]))
# SF5 more than 26 weeks instead of at least 26: same call
gt = tally(lambda h: h.empty_weeks > 26)
check("SF5 more than 26 weeks names the same area", winner(gt)[0] == ORR)
# SF7 exchange days: keeping one of the two rows leaves every count where it was
one_row = {}
for h in homes:
    x = OBS[h.i].copy()
    if h.exchange:
        x[h.exchange[0]] = h.exchange[1]
    one_row[h.i] = x[W.W0:W.W1 + 1].reshape(52, 7)
c_one = tally(lambda h: int(((one_row[h.i].max(1) - one_row[h.i].min(1)) <= 50).sum()) >= 26)
check("SF7 an exchange day read from one meter only moves no count", c_one == gold)
# SF8 estimated days left out: no count moves
def no_est(h):
    x = OBS[h.i][W.W0:W.W1 + 1].reshape(52, 7).astype(float)
    t = h.rtype[W.W0:W.W1 + 1].reshape(52, 7)
    n = 0
    for w in range(52):
        a = x[w][t[w] == "ACTUAL"]
        n += int(len(a) == 0 or a.max() - a.min() <= 50)
    return n >= 26
check("SF8 leaving out estimated days moves no count", tally(no_est) == gold)
# SF9 properties the water company left unmatched: dropping them moves no count
c_drop = tally(lambda h: h.match != "UNMATCHED" and h.empty_weeks >= 26)
check("SF9 dropping the unmatched properties moves no count", c_drop == gold,
      "%d unmatched" % sum(1 for h in homes if h.match == "UNMATCHED"))
check("SF9 every postcode lies in one community area", all(len({h.area for h in homes if h.postcode == pc}) == 1
                                                           for pc in {h.postcode for h in homes}))
# SF10 holiday lets and second homes are homes (ToR 4.2): leaving the rated lets out moves counts, not the call
no_lets = tally(lambda h: h.empty_weeks >= 26 and not (h.typ == W.LET and getattr(h, "rated", False)))
check("SF10 leaving business-rated lets out moves counts (ruled out by ToR 4.2) but not the call",
      no_lets != gold and winner(no_lets)[0] == ORR)
check("SF12 no tie for first place", order[0] != order[1] and gold[order[0]] > gold[order[1]])

# --------------------------------------------------------------------------- the enumerated easy family
easy = {}
for v in (1, 50, 100, 200, 300, 500, 700, 1000, 1400):
    easy["void week under %d L" % v] = void_counts(v)
for x in (1, 30, 60, 100, 150):
    easy["no day over %d L" % x] = tally(lambda h, x=x: int((WIN[h.i].max(1) <= x).sum()) >= 26)
for t in (1, 5, 10, 20, 30):
    easy["year under %d m3" % t] = tally(lambda h, t=t: WIN[h.i].sum() / 1000.0 < t)
easy["week under a tenth of the home's median week"] = tally(
    lambda h: int((WIN[h.i].sum(1) < 0.1 * np.median(WIN[h.i].sum(1))).sum()) >= 26)
asof = W.ASOF
easy["council tax: unoccupied, exempt or second home"] = tally(
    lambda h: R.state_on(h, asof)[0] in (W.UNF, W.FUR, W.EXEMPT, W.SECOND))
easy["council tax: unoccupied or exempt"] = tally(lambda h: R.state_on(h, asof)[0] in (W.UNF, W.FUR, W.EXEMPT))
easy["council tax: long-term empty or second home"] = tally(lambda h: R.lte_on(h) or R.second_on(h))
cen = {a: 0 for a in A}
for o in oas:
    cen[o["bestfit"]] += o["nur"]
easy["census 2021 no usual residents"] = cen
easy["void week under 300 L or council tax no resident"] = tally(
    lambda h: int((WIN[h.i].sum(1) < 300).sum()) >= 26 or R.state_on(h, asof)[0] in (W.UNF, W.FUR, W.EXEMPT,
                                                                                         W.SECOND))
landing = [k for k, c in easy.items() if winner(c)[0] == ORR]
check("R3a no easy route names Orrimouth (%d routes priced)" % len(easy), not landing, ", ".join(landing))
v300 = easy["void week under 300 L"]
check("R3a the default path (void weeks under 300 litres) names Ellingsea by 1.15x or more",
      winner(v300)[0] == ELL and winner(v300)[1] >= 1.15, "x%.3f" % winner(v300)[1])
check("R3a every void threshold up to 1,000 litres names Ellingsea",
      all(winner(easy["void week under %d L" % v])[0] == ELL for v in (1, 50, 100, 200, 300, 500, 700, 1000)))
# R3b the decisive step alone: the default path with only the week reading changed files the golden
check("R3b swapping only the void read for the steady-flow split files Orrimouth", golden_counts()[ORR] == gold[ORR]
      and winner(golden_counts())[0] == ORR)
# ladder positions and margins
r0 = easy["council tax: unoccupied, exempt or second home"]
w0, m0, o0 = winner(r0)
check("C1 rung 0 (council tax) names Kittlesea by 1.15x, Orrimouth 4th or 5th",
      w0 == KIT and m0 >= 1.15 and o0.index(ORR) in (3, 4), "x%.3f, Orrimouth %d" % (m0, o0.index(ORR) + 1))
w1, m1, o1 = winner(cen)
check("C2 rung 1 (census 2021) names Tarnhithe by 1.15x, Orrimouth not first or second",
      w1 == TAR and m1 >= 1.15 and o1.index(ORR) >= 2, "x%.3f" % m1)
w2, m2, o2 = winner(v300)
check("C3 rung 2 (void read) names Ellingsea, Orrimouth not first or second", w2 == ELL and o2.index(ORR) >= 2,
      "Orrimouth %d" % (o2.index(ORR) + 1))
check("C4 each rung names a different area", len({w0, w1, w2, wa}) == 4)
dom = (gold[ORR] - gold[ELL]) >= 0.2 * (v300[ELL] - v300[ORR])
check("C5 dominance: the decisive step's edge clears 1.2 times the decoy's carried advantage",
      (gold[ORR] - v300[ORR]) - (gold[ELL] - v300[ELL]) >= 1.2 * (v300[ELL] - v300[ORR]),
      "%d vs %.1f" % ((gold[ORR] - v300[ORR]) - (gold[ELL] - v300[ELL]), 1.2 * (v300[ELL] - v300[ORR])))
# the back-test: on homes the council tax records show unoccupied, the void read agrees
decl = [h for h in homes if R.state_on(h, asof)[0] in (W.UNF, W.FUR, W.EXEMPT)]
agree = sum(1 for h in decl if (int((WIN[h.i].sum(1) < 300).sum()) >= 26) == (h.empty_weeks >= 26)) / len(decl)
check("C6 back-test: the void read agrees with the truth on nine in ten homes the councils show unoccupied",
      agree >= 0.9, "%.3f of %d" % (agree, len(decl)))
# shock: Orrimouth does not top any simple per-area statistic the pack offers
stats = {"homes": {a: figs["areas"][NM[a]]["homes"] for a in A},
         "mean litres a day": {a: np.mean([WIN[h.i].mean() for h in homes if h.area == a]) for a in A},
         "homes with every day zero": tally(lambda h: int(WIN[h.i].max()) == 0),
         "lets on the list": R.ndr_homes_on(entries),
         "long-term empty (CTB)": tally(lambda h: R.lte_on(h))}
tops = [k for k, c in stats.items() if max(c, key=c.get) == ORR]
check("C7 Orrimouth tops no simple statistic of the pack", not tops, ", ".join(tops))

# ---------------------------------------------------------------------------------- the three rules (R)
check("R1 the golden reads every home's daily meter rows (row-level, %d rows)" % figs["meter_rows"],
      figs["meter_rows"] >= 25000)
import pyarrow.parquet as pq
cols = pq.read_schema(os.path.join(TARGET, "meter_reads_daily_2025-26.parquet")).names
bad_cols = [c for c in cols if re.search(r"leak|flow|occup|empty|void|use", c, re.I)]
check("R1 no shipped meter column holds the deciding quantity", not bad_cols and cols == [
    "PROPERTY_REF", "METER_SERIAL", "READ_DATE_UTC", "CONSUMPTION_L", "READ_TYPE"], str(cols))
undecl = sum(1 for h in homes if h.empty_weeks >= 26 and R.state_on(h, asof)[0] == W.OCC)
check("R1 the council tax status is not the deciding quantity (it shows homes left empty as occupied)",
      undecl >= 100, str(undecl))
check("R2 exchange days, estimated days and unmatched properties are each neutral (SF7, SF8, SF9)",
      c_one == gold and tally(no_est) == gold and c_drop == gold)
check("R2 the main call reads no council tax, rating list or census row (the golden from meter, match and "
      "gazetteer alone)", gold == truth)
# R3c no plant: no copied series between homes, no repeated block inside a series beyond a home's own steadiness
sig = Counter()
for h in homes:
    x = WIN[h.i]
    if x.max() > 0:
        sig[x.tobytes()] += 1
check("R3c no two homes carry the same 52 weeks of daily totals", max(sig.values()) == 1)
leakers = [h for h in homes if h.leak > 0]
check("R3c steady flows vary from day to day (no constant stream)",
      all(len(set(WIN[h.i][~W.window_weeks_true(h)].ravel().tolist())) > 5 for h in leakers
          if (~W.window_weeks_true(h)).sum() >= 4))

# --------------------------------------------------------------------------------------------- the asks
lte = tally(lambda h: R.lte_on(h))
check("ASK1 the long-term empty counts in figures.json", all(figs["areas"][NM[a]]["lte_ctb"] == lte[a] for a in A))
spells_near = [h.i for h in homes for s, e, st, ex, k in h.ctax_segs
               if st == W.UNF and abs((s - W.SIX_MONTHS_BEFORE).days) <= 3]
check("ASK1 no unfurnished spell starts within three days of 27 March 2026", not spells_near, str(spells_near[:5]))


def lte_reading(h, mode):
    """the cracker merges consecutive unfurnished accounts within each system and, in Teversby, follows a carried
    account's Legacy Account link to that one legacy account and takes its start; the naive reading takes the
    current account's start as each system shows it."""
    st, ex = R.state_on(h, asof)
    if st != W.UNF:
        return False
    segs = sorted(h.ctax_segs, key=lambda x: x[0])
    idx = [k for k, sg in enumerate(segs) if sg[0] <= asof and (sg[1] is None or asof <= sg[1])][0]
    tev = W.AREA_DISTRICT[h.area] == "Teversby"
    if mode == "naive":
        start = max(segs[idx][0], W.GO_LIVE) if tev else segs[idx][0]
    else:
        j = idx
        while j > 0 and segs[j - 1][2] == W.UNF and (segs[j][0] - segs[j - 1][1]).days == 1:
            if tev and segs[j][0] < W.GO_LIVE:
                break
            j -= 1
        start = segs[j][0]
    return start < W.SIX_MONTHS_BEFORE


crack = tally(lambda h: lte_reading(h, "cracker"))
naive = tally(lambda h: lte_reading(h, "naive"))
tev_missed = [a for a in A if W.AREA_DISTRICT[a] == "Teversby" and crack[a] != lte[a]]
check("ASK1 the cracker (Legacy Account link, merges within each system) misses every Teversby figure",
      len(tev_missed) == 4, str({NM[a]: (crack[a], lte[a]) for a in A}))
check("ASK1 the naive reading (current account start) misses every area", all(naive[a] != lte[a] for a in A),
      str({NM[a]: (naive[a], lte[a]) for a in A}))
lets = R.ndr_homes_on(entries)
by_entry = {a: 0 for a in A}
with_deleted = {a: 0 for a in A}
for e in entries:
    if e["from"] <= asof and (e["to"] is None or asof <= e["to"]):
        by_entry[e["area"]] += 1
    if e["from"] <= asof:
        with_deleted[e["area"]] += len(e["homes"])
check("ASK2 the holiday-let homes in figures.json",
      all(figs["areas"][NM[a]]["holiday_let_homes"] == lets[a] for a in A))
check("ASK2 counting list entries (a site's cottages as one) misses every area", all(by_entry[a] != lets[a]
                                                                                       for a in A),
      str({NM[a]: (by_entry[a], lets[a]) for a in A}))
check("ASK2 keeping entries deleted before 27 September 2026 misses the areas with a deleted entry",
      sum(1 for a in A if with_deleted[a] != lets[a]) >= 5)
check("ASK separation: deleting every council tax, rating list and census row leaves the call and the main counts",
      gold == truth and figs["call"] == NM[ORR])

# --------------------------------------------------------------------------------------- realism sweep
def steps(vals):
    v = sorted(vals)
    return {b - a for a, b in zip(v, v[1:])}


check("RS1 property references have no constant step", len(steps(int(h.prop_ref) for h in homes)) > 3)
check("RS1 UPRNs have no constant step", len(steps(h.uprn for h in homes)) > 3)
check("RS1 rating list references have no constant step", len(steps(int(e["ba_ref"]) for e in entries)) > 3)
check("RS2 area codes do not run in alphabetical order", [NM[a] for a in A] != sorted(NM[a] for a in A))
check("RS3 no two areas share a long-term empty count or a holiday-let count",
      len(set(lte.values())) == len(A) and len(set(lets.values())) == len(A))
mx_week = max(int(WIN[h.i].sum(1).max()) for h in homes)
check("RS4 the busiest week of any home is plausible (under 35,000 litres)", mx_week < 35000, str(mx_week))
check("RS5 steady flows are those of running cisterns and supply pipes (110 to 950 litres a day)",
      all(110 <= h.leak <= 950 for h in homes if h.leak > 0))

import docs as D
import pdfplumber
for pdf_name in sorted(f for f in os.listdir(TARGET) if f.endswith(".pdf")):
    path = os.path.join(TARGET, pdf_name)
    with pdfplumber.open(path) as pdf:
        n_chars = sum(len(pg.chars) for pg in pdf.pages)
        n_rules = sum(len(pg.lines) + len(pg.rects) for pg in pdf.pages)
    faults = D.layout_faults(path)
    check("RS6 %s: no character crosses a table rule or the right margin (%d glyphs, %d rules read)" % (
        pdf_name, n_chars, n_rules), n_chars > 500 and n_rules > 0 and not faults, str(faults[:4]))

# --------------------------------------------------------------------------------------------- input gates
files = sorted(os.listdir(TARGET))
fmts = {os.path.splitext(f)[1] for f in files}
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("IG1 ten or more files", len(files) >= 10, str(len(files)))
check("IG2 three or more formats", len(fmts) >= 3, str(sorted(fmts)))
check("IG3 one file of 25,000 rows or more", figs["meter_rows"] >= 25000)
check("IG4 two or more distractors declared and shipped", len(meta["distractor_files"]) >= 2 and all(
    os.path.basename(p) in files for p in meta["distractor_files"]))
check("IG5 the wrong-basis distractor is declared with the fact that rules it out",
      meta["wrong_basis_distractor"]["file"].endswith("summary.pdf") and "4.1" in meta["wrong_basis_distractor"][
          "ruled_out_by"])
check("IG6 no file describes the data (readme, dictionary, notes, fields, manifest)",
      not [f for f in files if re.search(r"readme|dictionar|notes|field|manifest|schema|guide", f, re.I)])
from openpyxl import load_workbook
wb = load_workbook(os.path.join(TARGET, "teversby_ctax_extract_2026-10-05.xlsx"), read_only=True)
check("IG6 the council's workbook carries its liabilities sheet only", wb.sheetnames == ["Liabilities"])
check("IG7 no file is named after the decisive step", not [f for f in files if re.search(
    r"leak|steady|flow|void|distractor|trap|empty", f, re.I)])
del_ok = True
for p in meta["distractor_files"]:
    del_ok &= gold == truth           # the golden reads none of them
check("IG8 deleting each distractor leaves the golden and the asks", del_ok)

# ----------------------------------------------------------------------------------------------- report
fails = [r for r in RESULTS if not r[1]]
for label, ok, detail in RESULTS:
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
print("%d assertions, %d failed" % (len(RESULTS), len(fails)))
sys.exit(1 if fails else 0)
