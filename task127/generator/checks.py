"""task127 architecture 4: the generator's assertions, run on the built target/ and world's clean truth.
Every SF row of the design note's fork table is asserted by its id; R1 to R3c are the client's three rules."""
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
fails = []
n = 0


def check(label, ok, detail=""):
    global n
    n += 1
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        fails.append(label)


def rnd(x, u):
    return int(math.floor(x / u + 0.5)) * u


def edge(x, u):
    return u / 2 - abs(x - rnd(x, u))


w = W.build()
lines = {c["cid"]: c["line"] for c in w.watch.values()}
name = {c["cid"]: c["name"].replace(" Limited", "") for c in w.watch.values()}
key = {c["key"]: c["cid"] for c in w.watch.values()}
P = GD.Pack(T, lines)
p1, k1, n1, pairs = P.p1(0.30)
p0, k0, n0 = P.p0(0.30)
up = p1 - p0
own = {c: P.own(c) for c in lines}
val = P.values(up)
gold, gtot, runner, rtot = P.best_set(val)
GOLD = set(gold)


def setof(vals):
    return set(P.best_set(vals)[0])


# ---- input gates -------------------------------------------------------------------------------------------
files = sorted(os.listdir(T))
check("gate: 10 or more files", len(files) >= 10, str(len(files)))
check("gate: 3 or more formats", len(set(f.rsplit(".", 1)[-1] for f in files)) >= 3, str(sorted(set(f.rsplit(".", 1)[-1] for f in files))))
with open(os.path.join(T, "business_account_transactions_2021-2026.csv")) as fh:
    nrows = sum(1 for _ in fh) - 1
check("gate: a file of 25,000 or more rows", nrows >= 25_000, str(nrows))
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("gate: two or more distractors named in metadata", len(meta["distractor_files"]) >= 2 and
      all(d in files for d in meta["distractor_files"]))
check("gate: no file describes the data", not any(re.search(r"readme|dictionary|notes|manifest|schema|guide", f, re.I) for f in files))
check("gate: no distractor word in a file name", not any("distract" in f.lower() for f in files))

# ---- R1: the field's raw material ships ------------------------------------------------------------------
with open(os.path.join(T, "business_account_transactions_2021-2026.csv")) as fh:
    hdr = next(csv.reader(fh))
check("R1 ledger at transaction grain with counterparties", "other_party_account" in hdr and "posting_date" in hdr)
allhdr = set()
for f in files:
    if f.endswith(".csv"):
        with open(os.path.join(T, f)) as fh:
            allhdr |= set(next(csv.reader(fh)))
check("R1 no shipped column holds dependence, share or uplift",
      not any(re.search(r"depend|share|uplift|contag|main_payer|payee", h, re.I) for h in allhdr), str(sorted(allhdr))[:80])
check("R1 the golden reads the payments: Matai's dependants found in the ledger", len(P.dependents(key["MAT"])) == 8)

# ---- R3a / R3b: the analyst test and the decisive step alone ---------------------------------------------
TB = setof(own)
check("R3a default path (own twelve-month expected write-off) files Kinloch and Ridgeway",
      TB == {key["KIN"], key["RID"]}, str(sorted(name[c] for c in TB)))
check("R3a default path is not the golden", TB != GOLD)
check("R3b the decisive step alone files the golden: Kinloch and Matai", GOLD == {key["KIN"], key["MAT"]})
life = {c: P.own(c, "pd_lifetime") for c in lines}
check("R3b rung R2 (lifetime PD) stays on Kinloch and Ridgeway", setof(life) == TB)
r3 = {c: own[c] + sum(P.pd(s) * P.lgd_ead(s) for s in P.dependents(c)) for c in lines}
check("R3b rung R3 (payees' own expected loss added) stays on Kinloch and Ridgeway", setof(r3) == TB)
check("R3b rung R4a (an assumed uplift of 0.25) stays on Kinloch and Ridgeway", setof(P.values(0.25)) == TB)
# pooled uplift over every on-us payee of a defaulting payer, whatever its share
pk = pn = 0
U = P.borrower_universe()
for a, eps in P.episodes.items():
    for s, _ in eps:
        if not (GD.D(2022, 1, 1) <= s <= GD.D(2025, 12, 31)):
            continue
        for p in U:
            if p == a or a not in P.payers_of[p] or P.in_default(p, s):
                continue
            if P.share(p, a, GD.add_months(GD.D(s.year, s.month, 1), -12), GD.D(s.year, s.month, 1)) <= 0:
                continue
            pn += 1
            pk += any(s < t <= GD.add_months(s, 12) for t in P.starts(p))
pooled = pk / pn
vb = {c: own[c] + P.pd(c) * max(0.0, pooled - p0) * sum(P.lgd_ead(s) for s in P.dependents(c, T=0.0001)) for c in lines}
check("R3b rung R4b (pooled uplift over every payee of a defaulting payer) stays on Kinloch and Ridgeway",
      setof(vb) == TB, "pooled %.4f over %d payees" % (pooled, pn))

# ---- the fork table ---------------------------------------------------------------------------------------
check("SF1 the book's write-off, not the supported borrower's own, decides: the two sets differ", TB != GOLD)
check("SF2 lifetime PD read: the golden set is unchanged", setof(P.values(up, pdcol="pd_lifetime")) == GOLD)
drawn = {}
for r in P.run26:
    drawn.setdefault(r["customer_no"], []).append(r)
def own_drawn(c):
    return sum(float(r["pd_12m"]) * float(r["lgd"]) * float(r["drawn_nzd"]) for r in drawn[c])
vd = {c: own_drawn(c) + (val[c] - own[c]) for c in lines}
check("SF3 drawn balance in place of EAD: the golden set is unchanged", setof(vd) == GOLD)
check("SF4 whole packages: the golden set's lines fit the envelope", sum(lines[c] for c in GOLD) <= W.ENVELOPE,
      str(sum(lines[c] for c in GOLD)))
check("SF5 the watch list holds eight borrowers, all on the 2026 run", all(c in P.borrowers26() for c in lines) and len(lines) == 8)
half = {c: own[c] / 2 + (val[c] - own[c]) / 2 for c in lines}
check("SF6 a supported borrower's PD halved, not removed: the golden set is unchanged", setof(half) == GOLD)
raw_deps = all(P.dependents(c, raw=True) == P.dependents(c) for c in lines)
check("SF7 receipts with own-account transfers and lending kept: the same dependants", raw_deps)
gap = []
for p in P.borrowers26():
    for a in P.payers_of[p]:
        sh = P.share(p, a, GD.D(2026, 1, 1), GD.D(2027, 1, 1))
        if 0.20 < sh < 0.40:
            gap.append((p, a, round(sh, 3)))
check("SF7 no 2026 payee between 20 and 40 per cent of receipts from one payer", not gap, str(gap[:3]))
check("SF7 thresholds 0.20 to 0.45 give the same dependants", all(
    P.dependents(c, T=t) == P.dependents(c) for c in lines for t in (0.2, 0.25, 0.35, 0.4, 0.45)))
check("SF8 follow-up windows of 9, 15 and 18 months give the same rate", all(P.p1(0.30, window=m)[:3] == (p1, k1, n1)
                                                                           for m in (9, 15, 18)))
check("SF8 thresholds 0.10 to 0.45 give the same treated and control counts",
      all(P.p1(t)[:3] == (p1, k1, n1) and P.p0(t) == (p0, k0, n0) for t in (0.1, 0.2, 0.4, 0.45)))
gt_bin = rnd(gtot, 50_000)
wide = {}
for t in (0.10, 0.15, 0.50, 0.55):
    q1 = P.p1(t)
    q0 = P.p0(t)
    vt = P.values(q1[0] - q0[0], T=t)
    wide[t] = (setof(vt) == GOLD, rnd(sum(vt[c] for c in GOLD), 50_000) == gt_bin)
check("SF7 thresholds 0.10 to 0.55 (Basel's 50 per cent receipts test included) file the golden set",
      all(wide[t][0] for t in (0.10, 0.15, 0.50, 0.55)), str({t: a for t, (a, _) in wide.items()}))
check("SF7 thresholds 0.10 to 0.50 keep the total in its NZ$50,000 bin", all(wide[t][1] for t in (0.10, 0.15, 0.50)))
check("SF8 lookbacks of 3, 6 and 24 months before the payer's default give the same rate",
      all(P.p1(0.30, lookback=m)[:3] == (p1, k1, n1) for m in (3, 6, 24)))
dw = [(GD.D(2026, 7, 1), GD.D(2027, 1, 1)), (GD.D(2025, 1, 1), GD.D(2027, 1, 1)), (GD.D(2026, 10, 1), GD.D(2027, 1, 1))]
check("SF7 dependence read over 2026 H2, 2026 Q4 or 2025 to 2026: the same dependants",
      all(P.dependents(c, a=a, b=b) == P.dependents(c) for c in lines for a, b in dw))
# SF11: the uplift's grain. The record's payee outcomes, each with its receipt share before its payer's default
obs11 = []
for a11 in sorted(P.episodes):
    for s11, _ in P.episodes[a11]:
        if not (GD.D(2022, 1, 1) <= s11 <= GD.D(2025, 12, 31)):
            continue
        for p11 in sorted(U):
            if p11 == a11 or a11 not in P.payers_of[p11] or P.in_default(p11, s11):
                continue
            sh11 = P.share(p11, a11, GD.add_months(GD.D(s11.year, s11.month, 1), -12), GD.D(s11.year, s11.month, 1))
            if sh11 >= 0.30:
                obs11.append((a11, s11.year, sh11, any(s11 < t <= GD.add_months(s11, 12) for t in P.starts(p11))))


def vals_rate(rate):
    out = {}
    for c in lines:
        v = P.own(c)
        for d in P.dependents(c):
            v += P.pd(c) * max(0.0, rate(P.share(d, c, GD.D(2026, 1, 1), GD.D(2027, 1, 1))) - p0) * P.lgd_ead(d)
        out[c] = v
    return out


b0 = b1 = 0.0
for _ in range(60):
    g0 = g1 = h00 = h01 = h11 = 0.0
    for _, _, x, y in obs11:
        pi = 1 / (1 + math.exp(-(b0 + b1 * x)))
        g0 += y - pi
        g1 += (y - pi) * x
        wv = pi * (1 - pi)
        h00 += wv
        h01 += wv * x
        h11 += wv * x * x
    det = h00 * h11 - h01 * h01
    b0 += (h11 * g0 - h01 * g1) / det
    b1 += (-h01 * g0 + h00 * g1) / det
bands3 = [(0.0, 0.60), (0.60, 0.75), (0.75, 9.0)]
rate3 = {bd: sum(o[3] for o in obs11 if bd[0] <= o[2] < bd[1]) / sum(1 for o in obs11 if bd[0] <= o[2] < bd[1]) for bd in bands3}
fam11 = {"logistic on share": vals_rate(lambda x: 1 / (1 + math.exp(-(b0 + b1 * x)))),
         "three share bands": vals_rate(lambda x: next(v for bd, v in rate3.items() if bd[0] <= x < bd[1]))}
same11 = {k: setof(v) == GOLD and all(rnd(v[c], 50_000) == rnd(val[c], 50_000) for c in lines)
          and rnd(sum(v[c] for c in GOLD), 50_000) == rnd(gtot, 50_000) for k, v in fam11.items()}
check("SF11 a logistic fit of default on receipt share and three share bands file the golden set and every graded bin",
      all(same11.values()), "slope %.3f; %s" % (b1, same11))
cells = {}
for a11, y11, x11, d11 in obs11:
    for k11 in (("payer", a11), ("year", y11), ("band", next(bd for bd in bands3 if bd[0] <= x11 < bd[1]))):
        cells.setdefault(k11, []).append(d11)
degen = [k for k, v in cells.items() if len(v) >= 3 and (all(v) or not any(v))]
check("SF11 no payer, year or share band in the record has a payee default rate of nil or one", not degen, str(degen))
check("SF11 no payer that defaulted shares Matai Valley Foods' division, so a rate by the payer's division has no cell for it",
      all(P.cust[a]["sector"] != P.cust[key["MAT"]]["sector"] for a in set(o[0] for o in obs11)))
# baselines: pooled record, payers that never defaulted, payees' own PDs
def p0_never():
    nn = kk = 0
    for Y in (2022, 2023, 2024, 2025):
        y0, y1 = GD.D(Y, 1, 1), GD.D(Y + 1, 1, 1)
        for p in sorted(U):
            for a in P.payers_of[p]:
                if P.share(p, a, GD.D(Y - 1, 1, 1), y0) < 0.3 or P.starts(a):
                    continue
                if P.in_default(p, y0) or not P._active(p, Y):
                    continue
                nn += 1
                kk += any(y0 <= t < y1 for t in P.starts(p))
    return kk / nn
variants = {"pooled": val, "never": P.values(p1 - p0_never()), "model": P.values(None, baseline=p1)}
mat = key["MAT"]
bins = {k: rnd(v[mat], 50_000) for k, v in variants.items()}
tots = {k: rnd(v[key["KIN"]] + v[mat], 50_000) for k, v in variants.items()}
check("SF9 every licensed baseline files the golden set", all(setof(v) == GOLD for v in variants.values()))
check("SF9 Matai's figure in one NZ$50,000 bin under every baseline", len(set(bins.values())) == 1, str(bins))
check("SF9 the total in one NZ$50,000 bin under every baseline", len(set(tots.values())) == 1, str(tots))
check("SF9 a nil baseline is outside the bin (a method error, not a reading)", rnd(P.values(p1)[mat], 50_000) != bins["pooled"])
eds = {name[c]: round(edge(val[c], 50_000)) for c in lines}
check("SF10 every graded write-off clears its NZ$50,000 bin edge by NZ$2,000", min(eds.values()) >= 2_000, str(eds))
check("SF10 the total clears its bin edge by NZ$2,000", edge(gtot, 50_000) >= 2_000, str(round(edge(gtot, 50_000))))
mins = min(min(edge(v[mat], 50_000) for v in variants.values()), min(edge(v[key["KIN"]] + v[mat], 50_000) for v in variants.values()))
check("SF10 Matai and the total clear their edges under every baseline", mins >= 1_000, str(round(mins)))

# ---- margins and separation --------------------------------------------------------------------------------
check("margin: the golden set beats the default path's set by 5 per cent or more on the book",
      gtot >= 1.05 * sum(val[c] for c in TB), "%.0f vs %.0f" % (gtot, sum(val[c] for c in TB)))
check("margin: the golden set beats the runner-up by NZ$100,000", gtot - rtot >= 100_000, "%.0f" % (gtot - rtot))
r_star = (own[key["RID"]] - own[mat]) / (P.pd(mat) * sum(P.lgd_ead(s) for s in P.dependents(mat)) -
                                          P.pd(key["RID"]) * sum(P.lgd_ead(s) for s in P.dependents(key["RID"])))
check("ladder: an assumed uplift must exceed 0.26 to reach the golden", r_star > 0.26, "%.3f" % r_star)
dev_main = [df for df in w.defaults if df["kind"] in ("anchor", "contagion", "baseline_payee") and df["triggers"][0][0] != "UTP"]
check("separation: every payer and payee default the call reads opens on a customer-keyed row", not dev_main)
eps_utp = P._episodes("utp")
sv = P.episodes
P.episodes = eps_utp
same = P.p1(0.30)[:3] == (p1, k1, n1) and P.p0(0.30) == (p0, k0, n0)
P.episodes = sv
check("separation: the call reads the same rates with the register's account rows dropped", same)
check("separation: no watch-list payee is in default or stage 3", all(P.borrowers26()[s][0]["stage"] != "3"
                                                                     for c in lines for s in P.dependents(c)))

# ---- R2: each mess item neutral to the call ---------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="t127c-")
shutil.copytree(T, os.path.join(tmp, "t"))
with open(os.path.join(tmp, "t", "account_number_crosswalk_2023.csv"), "w") as fh:
    fh.write("legacy_account,new_account,converted_on,status\n")
P2 = GD.Pack(os.path.join(tmp, "t"), lines)
a1 = P2.p1(0.30)
a0 = P2.p0(0.30)
v2 = P2.values(a1[0] - a0[0])
check("R2 the 2023 crosswalk mishandled (legacy numbers unresolved): the call holds", setof(v2) == GOLD,
      "p1 %d/%d" % a1[1:3])
shutil.copy(os.path.join(T, "account_number_crosswalk_2023.csv"), os.path.join(tmp, "t"))
for d in meta["distractor_files"]:
    os.remove(os.path.join(tmp, "t", d))
P3 = GD.Pack(os.path.join(tmp, "t"), lines)
b1 = P3.p1(0.30)
b0 = P3.p0(0.30)
same3 = (setof(P3.values(b1[0] - b0[0])) == GOLD and P3.security() == P.security()
         and P3.commitment() == P.commitment() and P3.sector_table() == P.sector_table())
check("distractors deleted: the call and every ask figure are unchanged", same3)
shutil.rmtree(tmp, ignore_errors=True)


def _no_index(latest=True):
    raise RuntimeError("the property index was read")


_saved_index = P.index
P.index = _no_index
try:
    c1 = P.p1(0.30)
    c0 = P.p0(0.30)
    idx_free = setof(P.values(c1[0] - c0[0])) == GOLD
except RuntimeError:
    idx_free = False
P.index = _saved_index
prov = sum(1 for c in lines if rnd(P.security(latest=False)[c], 1000) != rnd(P.security()[c], 1000))
check("R2 the property index (either release) never enters the call; provisional releases move ask A only", idx_free,
      "ask A figures moved by the provisional reading: %d of 8" % prov)

# ---- asks: device mass and disjoint blocks ----------------------------------------------------------------
A = P.security()
A_reg = P.security(use_made=False, drop_discharged=False)
A_d = P.security(use_made=True, drop_discharged=False)
A_m = P.security(use_made=False, drop_discharged=True)
check("ask A: the register's dates with discharged kept miss every borrower by 3 bins or more",
      all(abs(rnd(A[c], 1000) - rnd(A_reg[c], 1000)) >= 3000 for c in lines))
dis = {c for c in lines if rnd(A[c], 1000) != rnd(A_d[c], 1000)}
check("ask A: discharged properties move exactly the three borrowers that sold one", dis == {key["RID"], key["HAR"], key["BRI"]},
      str(sorted(name[c] for c in dis)))
check("ask A: the register's dates move every borrower", all(rnd(A[c], 1000) != rnd(A_m[c], 1000) for c in lines))
check("ask A: figures clear their edges by NZ$50", min(edge(A[c], 1000) for c in lines) >= 50, str(round(min(edge(A[c], 1000) for c in lines))))
B = P.commitment()
B_lazy = P.commitment(former=False, drop_released=False)
B_f = P.commitment(former=True, drop_released=False)
B_r = P.commitment(former=False, drop_released=True)
check("ask B: NZBN and exact names with releases kept miss every borrower", all(rnd(B[c], 1000) != rnd(B_lazy[c], 1000) for c in lines))
rel = {c for c in lines if rnd(B[c], 1000) != rnd(B_f[c], 1000)}
fmr = {c for c in lines if rnd(B[c], 1000) != rnd(B_r[c], 1000)}
check("ask B: releases and former names move disjoint blocks of four", len(rel) == 4 and len(fmr) == 4 and not (rel & fmr),
      "%s | %s" % (sorted(name[c] for c in rel), sorted(name[c] for c in fmr)))
C = P.sector_table()
C_nl = P.sector_table(keys="noloan")
C_rs = P.sector_table(use_register=False)
C_nc = P.sector_table(use_cures=False)
check("ask C: account rows left unkeyed miss every division by 1.0 point or more",
      all(abs(C[s][0] - C_nl[s][0]) >= 1.0 for s in C), str({s: round(C[s][0] - C_nl[s][0], 1) for s in C}))
check("ask C: the run's stage as the year-end state misses every division", all(round(C[s][0], 1) != round(C_rs[s][0], 1) for s in C))
check("ask C: shares clear their edges", min(edge(C[s][0], 0.1) for s in C) >= 0.003, "%.4f" % min(edge(C[s][0], 0.1) for s in C))
check("ask C: seven divisions, each with forty or more borrowers", len(C) == 7 and min(v[2] for v in C.values()) >= 40)

# ---- realism ---------------------------------------------------------------------------------------------
def steps(vals):
    vs = sorted(set(vals))
    return set(b - a for a, b in zip(vs, vs[1:]))
cids = [int(r["customer_no"][1:]) for r in P.run26]
fids = [int(r["facility_id"][1:]) for r in P.run26]
check("realism: customer numbers are no arithmetic sequence", len(steps(cids)) > 5)
check("realism: facility ids are no arithmetic sequence", len(steps(fids)) > 5)
import openpyxl
wb = openpyxl.load_workbook(os.path.join(T, "customer_master_2026-12.xlsx"), read_only=True)
names_all = [r[1] for r in list(wb["Customers"].iter_rows(values_only=True))[1:]]
shapes = set()
for nm in names_all:
    shapes.add("year" if re.search(r"\(\d{4}\)", nm) else "amp" if " & " in nm else "ltd" if nm.endswith(" Ltd") else
               "coop" if "Co-operative" in nm else "family" if re.search(r"Brothers|and Sons|Family", nm) else "plain")
check("realism: legal names take more than two shapes", len(shapes) > 2, str(sorted(shapes)))
order_codes = [r[0] for r in list(wb["Customers"].iter_rows(values_only=True))[1:]]
check("realism: customer order is not alphabetical", order_codes != sorted(order_codes, key=lambda c: names_all[order_codes.index(c)]))
mt = {}
for (cid, ym), v in P.tot.items():
    if v > 0:
        mt.setdefault(ym, []).append(round(v, 2))
check("realism: no two customers share a month's receipts to the cent", all(len(v) == len(set(v)) for v in mt.values()))
def pdftext(f):
    return subprocess.run(["pdftotext", "-layout", os.path.join(T, f), "-"], capture_output=True, text=True).stdout
terms = pdftext("bsu_terms_of_reference_2027.pdf")
check("documents: the terms carry the envelope sentence (positive control)", "NZ$6.0 million of new working-capital lines" in terms)
check("documents: the terms name no payee, dependence or contagion", not re.search(r"payee|depend|contagi|supplier|receipt", terms, re.I))
val_txt = pdftext("ifrs9_pd_model_validation_2025.pdf")
check("documents: the validation report carries the default definition", "dated by" in val_txt and "first trigger" in val_txt)
wl = pdftext("watch_list_2027-01.pdf")
check("documents: the watch list names no payee or dependence", "Matai Valley Foods" in wl and not re.search(r"payee|depend|supplier", wl, re.I))
def pinfo(f):
    return subprocess.run(["pdfinfo", os.path.join(T, f)], capture_output=True, text=True).stdout
check("documents: every PDF exported by Writer, no ReportLab in the bytes",
      all(b"ReportLab" not in open(os.path.join(T, f), "rb").read() and re.search(r"Creator:\s+Writer", pinfo(f))
          and re.search(r"Producer:\s+LibreOffice", pinfo(f)) for f in files if f.endswith(".pdf")))
check("documents: no file dated after the pack", all(os.path.getmtime(os.path.join(T, f)) <= 1800560400 for f in files))
fig_ok = F["call"] == "Kinloch Engineering and Matai Valley Foods" and F["total_kept_off"] == rnd(gtot, 50_000)
check("figures.json carries the call and total", fig_ok)

print("%d checks, %d failed" % (n, len(fails)))
sys.exit(1 if fails else 0)
