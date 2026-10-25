"""task166 checks: the build's assertions, run on the cut pack in target/ and on the generator's clean truth.

Blocks: G input gates; C the call and its bin; L the ladder and its rivals on the shipped files; F the standing family;
R1 to R3c the three rules on the clean truth; M each Layer 1 item mishandled; SF1 to SF21 the semantic fork table;
A the ask and its devices; S the separation of the ask from the call and the distractors; D the documents; Q realism."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A            # noqa: E402
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
RES = []
MN, LS, GR, KB = C.REG_ORDER[3], C.REG_ORDER[1], C.REG_ORDER[0], C.REG_ORDER[2]
LO, HI = 35.0, 45.0          # the $40 million bin at the nearest 10


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))
    print("%s  %-6s %s" % ("PASS" if ok else "FAIL", label, detail))


def pick(s):
    s = s.reindex(C.REG_ORDER)
    return s.idxmax(), float(s.max() / s.drop(s.idxmax()).max())


def in_bin(x):
    return LO <= x < HI


# ------------------------------------------------------------------------------------------------- G: input gates
files = sorted(os.listdir(TARGET))
fmts = sorted({f.rsplit(".", 1)[1] for f in files})
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("G1", len(files) >= 10, "%d files" % len(files))
check("G2", len(fmts) >= 3, "formats %s" % fmts)
check("G3", meta["input_gates"]["largest_file_rows"] >= 25000,
      "%s %d rows" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
dis = meta["distractor_files"]
check("G4", len(dis) >= 2 and all(d in files for d in dis) and not any("distract" in f.lower() for f in files),
      "distractors %s" % dis)
check("G5", sorted(os.listdir(GOLDEN)) == ["he_payoff_pilot_2027.xlsx", "payoff_quotes_by_center.png"],
      "goldens %s" % sorted(os.listdir(GOLDEN)))
bad = [f for f in files if re.search(r"stack|blend|lock|consolid|cash.?out|incentive|answer|golden", f, re.I)]
check("G6", not bad, "no file name names the step %s" % bad)

# ------------------------------------------------------------------------------------------------- C: the call
gold, ctx = C.golden(TARGET)
g_pick, g_margin = pick(gold)
second = gold.drop(g_pick).idxmax()
check("C1", g_pick == MN, "pick %s" % g_pick)
check("C2", in_bin(gold[MN]) and min(gold[MN] - LO, HI - gold[MN]) >= 2.5,
      "%.2f in [35, 45), %.2f from the nearer edge" % (gold[MN], min(gold[MN] - LO, HI - gold[MN])))
check("C3", second == LS and gold[LS] / gold.drop([MN, LS]).max() >= 1.15,
      "second %s, %.2f over the third" % (second, gold[LS] / gold.drop([MN, LS]).max()))
check("C4", g_margin >= 1.5, "margin %.2f" % g_margin)
figs = json.load(open(os.path.join(HERE, "figures.json")))
check("C5", figs["call"]["center"] == MN and figs["call"]["principal_2027_musd"] == 40 and figs["call"]["second"] == LS,
      "figures.json carries the call")

# ------------------------------------------------------------------------------------------------- L: the ladder
routes = {}
he = C.he_posted_monthly(TARGET)
ph = C.plan_he(TARGET)
H2 = C.add_own(ctx["H"], he)
FW2 = C.add_own(ctx["FW"], he, ph)
dev = {}
for name, cov, kw in (("own", ["own"], {}), ("first", ["first"], {}), ("own_first", ["own", "first"], {}),
                      ("walt", ["walt"], {}), ("own_fe", ["own"], {"fe": True}), ("first_fe", ["first"], {"fe": True})):
    f = C.fit(H2, cov, **kw)
    dev[name] = f.deviance
    routes[name] = C.project(FW2, f.predict(C.design(FW2, cov, **kw)), ctx["curt"])
dev["blend"] = ctx["model"].deviance
tr = ctx["H"][(ctx["H"].t >= C.mo(2025, 12)) & (ctx["H"].y == 1)]
routes["trailing"] = (tr.groupby("region").H.sum() / 1e6).reindex(C.REG_ORDER)
p, m = pick(routes["own"])
check("L0", p == GR and m >= 1.15, "rung 0, own rate: %s by %.2f (%.1f)" % (p, m, routes["own"].max()))
p, m = pick(routes["trailing"])
check("L1", p == KB and m >= 1.15, "rung 1, trailing payoffs: %s by %.2f" % (p, m))
p, m = pick(routes["first"])
check("L2", p == LS and m >= 1.15, "rung 2, the first mortgage alone: %s by %.2f" % (p, m))
check("L3", g_pick == MN and g_margin >= 1.5, "rung 3, the stack: %s by %.2f" % (g_pick, g_margin))
p, m = pick(routes["own_first"])
check("L4", p != MN, "own and first side by side: %s by %.2f" % (p, m))
check("L5", not in_bin(routes["walt"][MN]), "each lien at its own rate: %s, Muskegon and the North %.1f outside the bin"
      % (pick(routes["walt"])[0], routes["walt"][MN]))
check("L6", pick(routes["own_fe"])[0] == GR and pick(routes["first_fe"])[0] == LS, "region effects keep rungs 0 and 2")
check("L7", dev["blend"] < dev["walt"] < dev["own_first"] < dev["first"] < dev["own"],
      "deviance blend %.1f < lien by lien %.1f < side by side %.1f < first %.1f < own %.1f"
      % (dev["blend"], dev["walt"], dev["own_first"], dev["first"], dev["own"]))
check("L8", dev["walt"] - dev["blend"] > 100, "the record selects the blend by %.1f" % (dev["walt"] - dev["blend"]))
rank0 = routes["own"].sort_values(ascending=False).index.tolist()
check("L9", rank0.index(MN) == 1 and routes["own"][GR] / routes["own"][MN] >= 1.2,
      "the golden second on rung 0 only, by %.2f" % (routes["own"][GR] / routes["own"][MN]))

# ------------------------------------------------------------------------------------------------- F: the standing family
import statsmodels.api as sm   # noqa: E402
cache = {}
fam = {}
fam["complementary log-log"] = C.variant(TARGET, cache, model={"link": sm.families.links.CLogLog()})[0]
fam["three knots"] = C.variant(TARGET, cache, model={"knots": [0.0, 1.0, 2.0]})[0]
fam["no seasonality"] = C.variant(TARGET, cache, model={"seasonal": False})[0]
fam["no purchase marker"] = C.variant(TARGET, cache, model={"young": False})[0]
fam["region effects"] = C.variant(TARGET, cache, model={"fe": True})[0]
for name, s in fam.items():
    p, m = pick(s)
    check("F" + str(list(fam).index(name) + 1), p == MN and in_bin(s[MN]),
          "%s: %s %.2f (margin %.2f)" % (name, p, s[MN], m))

# ------------------------------------------------------------------------------------------------- SF: the fork table
book = ctx["book"]
core = ctx["core"]
nov = core[core.AsOfDate == "2026-11-30"]
check("SF1", (nov[nov.LoanStatus != "ACTIVE"].PrincipalBalance.astype(float) == 0).all(),
      "November's closed rows carry no balance: same call")
s2 = C.variant(TARGET, cache, curtail=False)[0]
check("SF2", pick(s2)[0] == MN and in_bin(s2[MN]), "payoffs only: %.2f" % s2[MN])
s3 = C.variant(TARGET, cache, with_december=True)[0]
check("SF3", pick(s3)[0] == MN and in_bin(s3[MN]), "December 2026 counted too: %.2f" % s3[MN])
los = ctx["los"]
check("SF4", los.region.notna().all() and set(los.region) == set(C.REG_ORDER), "every loan's county maps to a center")
check("SF5", not set(pd.read_csv(os.path.join(TARGET, R.F_HELOC), dtype=str).line_number) & set(book.key),
      "lines are not in the book")
pol = " ".join(DOC.policy_text())
check("SF6", "the planning cycle's base case" in pol, "the policy files the base case")
s7 = C.variant(TARGET, cache, rates_mode="simple")[0]
check("SF7", pick(s7)[0] == MN and in_bin(s7[MN]), "simple monthly averages: %.2f" % s7[MN])
s8a = C.variant(TARGET, cache, lag=0)[0]
s8b = C.variant(TARGET, cache, lag=2)[0]
check("SF8", all(pick(s)[0] == MN and in_bin(s[MN]) for s in (s8a, s8b)), "lag 0 %.2f, lag 2 %.2f" % (s8a[MN], s8b[MN]))
s9 = C.variant(TARGET, cache, hist={"exits_as_payoffs": True})[0]
check("SF9", pick(s9)[0] == MN and in_bin(s9[MN]) and "including the final scheduled payment" in pol,
      "maturities and charge-offs counted as payoffs: %.2f" % s9[MN])
check("SF10", "a balance charged off is not principal paid" in pol, "the policy excludes charge-offs")
check("SF11", "A loan the credit union refinances itself is paid in full" in pol, "the policy counts own refinances")
s12 = C.variant(TARGET, cache, fm={"blank_360": True})[0]
check("SF12", pick(s12)[0] == MN and in_bin(s12[MN]), "blank terms read as 360 months: %.2f" % s12[MN])
# one payment fewer by the reported month
s13 = C.variant(TARGET, cache, fm={"one_fewer": True})[0]
check("SF13", pick(s13)[0] == MN and in_bin(s13[MN]), "one payment fewer by the reported month: %.2f" % s13[MN])
s14 = C.variant(TARGET, cache, hist={"legacy_from_funding": True})[0]
check("SF14", pick(s14)[0] == MN and in_bin(s14[MN]), "legacy balances from the funding: %.2f" % s14[MN])
check("SF15", round(gold[MN] / 10) * 10 == 40, "%.2f prints 40" % gold[MN])
check("SF16", second == LS, "second: %s" % second)

# ------------------------------------------------------------------------------------------------- A: the ask
paid = C.paid_by_asof(core)
S = C.statement_loans(TARGET, los, core)
ask = C.ask_table(S, paid)
crack = C.ask_table(C.statement_loans(TARGET, los, core, with_mortgages=False, with_manual=True), paid)
mirror = C.ask_table(C.statement_loans(TARGET, los, core, with_mortgages=False, with_manual=False), paid)
check("A1", all(ask[k][0] != crack[k][0] and ask[k][1] != crack[k][1] for k in ask),
      "the cracker misses all 32 counts")
check("A2", all(ask[k][0] != mirror[k][0] and ask[k][1] != mirror[k][1] for k in ask), "the mirror misses all 32")
mt = S[S.how == "mortgage"]
check("A3", all(((mt.region == r) & (mt.quarter == q)).any() for r in C.REG_ORDER for q, _, _ in C.QUARTERS),
      "every cell holds a home equity loan quoted on a first-mortgage statement (%d)" % len(mt))
check("A4", (S[S.how == "manual"].quarter == "2026Q1").all() and len(S[S.how == "manual"]) > 0,
      "the outage log's loans all fall in the first quarter of 2026 (%d)" % len(S[S.how == "manual"]))
# every first-mortgage statement ties to the cent: the first mortgage's payoff alone, or the two payoffs at the
# good-through date with one fee when it also quoted the home equity loan behind it
log = pd.read_csv(os.path.join(TARGET, A.F_LOG), dtype={"account_reference": str})
serv = pd.read_csv(os.path.join(TARGET, R.F_SERV), dtype=str).set_index("mortgage_loan_number")
addr = {}
for k, row in los.iterrows():
    addr.setdefault((C.norm_addr(row.property_street), str(row.property_zip)), []).append(k)
hbal = C.he_balance_lookup(core, TARGET)
ties = alone = both = total_mtg = 0
for r in log[(log.product_on_file == "MTG") & log.statement_status.isin(["ISSUED", "UPDATED"])].itertuples(index=False):
    m = serv.loc[r.account_reference]
    d = C.eastern_date(r.issued_utc)
    pm = "%04d-%02d" % ((d.year, d.month - 1) if d.month > 1 else (d.year - 1, 12))
    mb = C.mortgage_balance(m, d)
    days = (dt.date.fromisoformat(r.good_through_date) - d).days
    first = mb + mb * float(m.note_rate_pct) / 36500 * days
    total_mtg += 1
    hit = abs(round(first + 25.0, 2) - float(r.statement_amount)) <= 0.05
    alone += hit
    for key in addr.get((C.norm_addr(m.property_street), str(m.property_zip)), []):
        hb = hbal(key, d)
        if not hb:
            continue
        rate = float(los.loc[key].note_rate_pct)
        if abs(round(hb + hb * rate / 36500 * days + first + 25.0, 2) - float(r.statement_amount)) <= 0.05:
            both += 1
            hit = True
    ties += hit
check("A5", total_mtg > 0 and ties == total_mtg and both > 0 and alone > 0,
      "%d of %d first-mortgage statements tie to the cent (%d the first mortgage alone, %d both liens)"
      % (ties, total_mtg, alone, both))
loose = C.ask_table(C.statement_loans(TARGET, los, core, loose=True), paid)
check("A11", loose == ask, "a coarser reconciliation (more than half the home equity balance above the first's "
      "scheduled balance) gives the same 32 counts")
unrec = C.ask_table(C.statement_loans(TARGET, los, core, reconcile=False), paid)
check("A12", sum(unrec[k][0] != ask[k][0] for k in ask) >= 12,
      "every first-mortgage statement counted without its amount misses %d of 16 quote counts"
      % sum(unrec[k][0] != ask[k][0] for k in ask))
wb_rows = pd.read_excel(os.path.join(TARGET, A.F_MANUAL), header=2)
he_rows = wb_rows[wb_rows.Liens.str.contains("home equity", case=False)]
addr2 = {}
for k, row in los.iterrows():
    addr2.setdefault(C.norm_addr("%s %s %s" % (row.property_street, row.property_city, row.property_zip)), []).append(k)
check("A6", all(len(addr2.get(C.norm_addr(p), [])) == 1 for p in he_rows.Property),
      "each of the outage log's %d home equity rows matches one collateral address" % len(he_rows))
check("A7", all(ask[k][1] <= ask[k][0] for k in ask) and len({v[0] for v in ask.values()}) > 10,
      "paid never exceeds quoted; the counts vary across cells")
# hazards: legacy references, lines, updates, voids, UTC
legacy_refs = log.account_reference.isin(pd.read_csv(os.path.join(TARGET, R.F_XREF), dtype=str).legacy_loan_no).sum()
check("A8", legacy_refs > 0, "%d requests name a legacy loan number" % legacy_refs)
from zoneinfo import ZoneInfo
_et = ZoneInfo("America/Detroit")
local = [dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(_et)
         for t in log.issued_utc]
local_h = [t.hour for t in local]
check("A9", all(8 <= h <= 18 for h in local_h), "every statement issued between 8 a.m. and 7 p.m. Eastern (UTC inert)")
figq = figs["asks"]
check("A10", all(figq["%s|%s" % k]["quoted"] == v[0] and figq["%s|%s" % k]["paid_in_full"] == v[1] for k, v in ask.items()),
      "figures.json carries the 32 counts")
check("SF17", sum(1 for v in ask.values()) == 16 and len(mt) > 0, "statements quoting the loan, the mortgage's included")
check("SF18", all(ask[k][0] == S[(S.region == k[0]) & (S.quarter == k[1])].key.nunique() for k in ask),
      "distinct loans per quarter")
check("SF19", all(t.date().isoformat() == u[:10] for t, u in zip(local, log.issued_utc)),
      "the Eastern and UTC dates agree for every issue")
check("SF20", paid == set(core[(core.LoanStatus == "PIF") & (core.CloseDate <= "2026-11-30")].LoanNumber),
      "paid in full is PIF on or before 30 November 2026")
check("SF21", ((log.statement_status == "VOID") & (log.statement_amount == 0)).sum() == (log.statement_status == "VOID").sum(),
      "voided requests carry no amount")

# ------------------------------------------------------------------------------------------------- S: separation
_scratch = os.environ.get("TASK166_SCRATCH")
if _scratch:
    os.makedirs(_scratch, exist_ok=True)
tmp = tempfile.mkdtemp(prefix="c166_", dir=_scratch)
try:
    t2 = os.path.join(tmp, "t")
    shutil.copytree(TARGET, t2)
    for f in (A.F_LOG, A.F_MANUAL, R.F_SERV, R.F_HELOC, R.F_HPI, DOC.F_ALM, DOC.F_DICT, DOC.F_MANIFEST):
        os.remove(os.path.join(t2, f))
    g2, _ = C.golden(t2)
    check("S1", (g2.round(6) == gold.round(6)).all(), "the call reads none of the ask's files, the distractors or the "
          "documents beside the policy")
    t3 = os.path.join(tmp, "t3")
    shutil.copytree(TARGET, t3)
    for f in dis:
        os.remove(os.path.join(t3, f))
    _, core3, los3 = C.load(t3)
    ask3 = C.ask_table(C.statement_loans(t3, los3, core3), C.paid_by_asof(core3))
    check("S2", ask3 == ask, "the asks unchanged with the distractors deleted")
finally:
    shutil.rmtree(tmp)
main_files = {R.F_LEGACY, R.F_CORE, R.F_XREF, R.F_LOS, R.F_MAP, R.F_RATES, DOC.F_PLAN}
check("S3", not ({A.F_LOG, A.F_MANUAL, R.F_SERV} & main_files), "no ask device sits in a file the call reads")

# ------------------------------------------------------------------------------------------------- M: Layer 1 neutral
sp = C.variant(TARGET, cache, fm={"by_payment": True})[0]
check("M1", pick(sp)[0] == MN and in_bin(sp[MN]), "first-mortgage rates from the reported payment: %.2f" % sp[MN])
sd = C.variant(TARGET, cache, hist={"drop_conversion": True})[0]
check("M2", pick(sd)[0] == MN and in_bin(sd[MN]), "the conversion month dropped: %.2f" % sd[MN])
check("M3", pick(s14)[0] == MN, "legacy balances from the funding (SF14)")
check("M4", pick(s7)[0] == MN, "rates as simple averages (SF7)")
check("M5", pick(s9)[0] == MN, "maturities and charge-offs as payoffs (SF9)")
check("M6", pick(s12)[0] == MN, "blank terms as 360 (SF12)")

# ------------------------------------------------------------------------------------------------- R: three rules, clean truth
W = WD.simulate_world()


def truth_frames(W):
    M = WD.M30
    rows = []
    for i in range(W.n):
        o2, ex = int(W.o2[i]), int(W.exit_m[i])
        end = ex if ex >= 0 else K.ASOF_M
        for t in range(max(o2 + 1, K.REC0), end + 1):
            if t == ex and W.exit_kind[i] in ("MATURED", "CHARGEOFF"):
                continue
            prev = W.bal.get((i, t - 1))
            if prev is None or prev <= 0:
                continue
            rows.append((i, t, prev, int(t == ex)))
    D = pd.DataFrame(rows, columns=["i", "t", "H", "y"])
    book = [int(i) for i in W.book]
    fw = []
    for j, t in enumerate(K.FORE):
        b0 = np.array([W.book_bal[i] for i in book])
        r = W.r2[book]
        bb = b0.copy()
        for _ in range(j):
            bb = np.maximum(bb - (W.pmt2[book] - bb * r / 1200.0), 0.0)
        fw.append(pd.DataFrame({"i": book, "t": t, "H": bb, "y": 0}))
    FWt = pd.concat(fw, ignore_index=True)
    FWt = FWt[FWt.H > 0]
    out = []
    for df in (D, FWt):
        df = df.copy()
        df["key"] = df.i
        df["region"] = [{v: k for k, v in K.RCODE.items()}[W.reg[i]] for i in df.i]
        df["r1"], df["r2"] = W.r1[df.i], W.r2[df.i]
        df["F"] = WD.sched_balance(W.F0[df.i], W.r1[df.i], W.n1[df.i], df.t - 1 - W.o1[df.i])
        df["m1"] = M[df.t - 1]
        df["blend"] = (df.F * df.r1 + df.H * df.r2) / (df.F + df.H) - df.m1
        df["first"] = df.r1 - df.m1
        df["own"] = df.r2 - (M[df.t - 1] + np.array([WD.HE_SPREAD[n] for n in W.n2[df.i]]))
        df["cal"] = df.t % 12 + 1
        df["s1"] = np.sin(2 * np.pi * df.cal / 12.0)
        df["s2"] = np.cos(2 * np.pi * df.cal / 12.0)
        df["young"] = ((df.t - W.o1[df.i]) < 24).astype(float)
        out.append(df)
    return out


Dt, FWt = truth_frames(W)
curt_t = WD.CURT_P * (WD.CURT_LO + WD.CURT_HI) / 2 + WD.BIG_CURT_P * 0.35
tro = {}
for name, cov in (("own", ["own"]), ("first", ["first"]), ("blend", ["blend"])):
    f = C.fit(Dt, cov)
    tro[name] = C.project(FWt, f.predict(C.design(FWt, cov)), curt_t)
cols = set()
for f in files:
    if f.endswith(".csv"):
        cols |= set(pd.read_csv(os.path.join(TARGET, f), nrows=1).columns.str.lower())
check("R1", not [c for c in cols if re.search(r"blend|stack|incentive|refi|lock", c)] and "senior_lien_balance" in cols,
      "the senior lien and the loan-months ship; no column holds the stack's incentive")
check("R2", all(pick(s)[0] == MN for s in (sp, sd, s14, s7, s9, s12)), "every Layer 1 item mishandled keeps the call (M1 to M6)")
check("R3a", pick(tro["own"])[0] == GR, "clean truth, the easy route (own rate): %s" % pick(tro["own"])[0])
check("R3b", pick(tro["blend"])[0] == MN and pick(tro["first"])[0] == LS,
      "clean truth, the decisive step alone: %s; the lower rung's single correction: %s"
      % (pick(tro["blend"])[0], pick(tro["first"])[0]))
truth = WD.truth_2027(W)
check("R3c", max(truth, key=truth.get) == "MN", "the world's own 2027 (reference): %s" % {k: round(v, 1) for k, v in truth.items()})

# ------------------------------------------------------------------------------------------------- D: documents
from pypdf import PdfReader   # noqa: E402


def pdf_text(path):
    return " ".join((p.extract_text() or "") for p in PdfReader(path).pages)


pt = re.sub(r"\s+", " ", pdf_text(os.path.join(TARGET, DOC.F_POLICY)))
check("D1", "fixed-rate closed-end home equity loans on the books at the close of business on 30 November 2026" in pt
      and len(pt) > 1500, "the policy PDF reads back (positive control)")
check("D2", not re.search(r"blend|stack|cash-out|consolidat|first mortgage's rate|lock", pt, re.I),
      "the policy names no method")
at = re.sub(r"\s+", " ", pdf_text(os.path.join(TARGET, DOC.F_ALM)))
sep = core[core.AsOfDate == "2026-09-30"]
he_sep = sep[sep.LoanStatus == "ACTIVE"].PrincipalBalance.astype(float).sum()
check("D3", ("$%.1f million" % (he_sep / 1e6)) in at, "the ALM report's book ties to the September trial balance (%.1f)"
      % (he_sep / 1e6))
check("D4", not re.search(r"Grand Rapids|Lakeshore|Kalamazoo|Muskegon|prepay|speed|CPR", at),
      "the ALM report ranks no region and carries no speed")
latest = max(core.AsOfDate.max(), log.issued_utc.str[:10].max())
check("D5", latest <= "2026-11-30", "no extract dated after the as-of (%s)" % latest)
dic = open(os.path.join(TARGET, DOC.F_DICT), encoding="utf-8").read()
check("D6", not re.search(r"blend|stack|cash-out|consolidat|lock", dic, re.I) and "senior lien" in dic,
      "the dictionary describes rows, not the step")

# ------------------------------------------------------------------------------------------------- Q: realism
rs = pd.read_csv(os.path.join(TARGET, R.F_RATES))
off = (rs.apr_pct - rs.rate_pct).round(3)
check("Q1", off.nunique() > 20, "APR spreads vary (%d values)" % off.nunique())
check("Q2", abs(book.bal.sum() / 1e6 - round(book.bal.sum() / 1e6)) > 0.05, "the book's total is not round")
blob = b"".join(open(os.path.join(TARGET, f), "rb").read() for f in files if not f.endswith(".csv"))
check("Q3", not re.search(rb"ReportLab|openpyxl|matplotlib|python", blob, re.I), "containers carry no library banner")
people = set(K.PEOPLE.values())
txt = pt + at + dic
check("Q4", all(p in txt or p in json.dumps(meta) for p in [K.PEOPLE["clo"], K.PEOPLE["alm"]]),
      "the documents' people are the drawn personas")
tbc = core.groupby("AsOfDate").size()
check("Q5", tbc.nunique() == len(tbc), "the trial balance's monthly counts all differ")
vals = [v[0] for v in ask.values()]
check("Q6", len(set(vals)) >= 12, "the quote counts are not uniform")

fails = [r for r in RES if not r[1]]
print("%d checks, %d failed" % (len(RES), len(fails)))
sys.exit(1 if fails else 0)
