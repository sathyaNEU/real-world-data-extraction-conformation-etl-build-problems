"""task166 checks: the three rules executed on the clean truth (R1 to R3c), the ladder and its grid, the golden family,
the out-of-sample choice, every semantic fork row (SF1 to SF19), the ask and its devices, the separation line, the
distractors, the input gates and the realism sweep. Exit 1 on any failure.

    python3 checks.py            reads task166/target, the generator's world and generator/figures.json"""
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import cracker as CR        # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402
import swaps as SW          # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
PACK = os.path.join(TASK, "target")
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-44s %s" % ("PASS" if ok else "FAIL", label, detail))


def bin25(x):
    return int(25 * round(x / 25.0))


def edge25(x):
    return 12.5 - abs(x - bin25(x))


# ------------------------------------------------------------------------------------------------- the golden
G = C.golden(PACK)
RT = C.routes(G)
FIG = json.load(open(os.path.join(HERE, "figures.json")))
CRE = G.CRE / 1e6
POOLS = {k: v / 1e6 for k, v in G.pools.items()}


def ranking(vals):
    return sorted(vals, key=vals.get, reverse=True)


def with_cre(x, mort=None):
    v = dict(POOLS)
    v["Fixed-rate commercial real estate"] = x
    if mort is not None:
        v["2023-24 residential mortgages"] = mort
    return v


check("GOLDEN call", G.call == "Fixed-rate commercial real estate", G.call)
check("GOLDEN figure", bin25(CRE) == 150 and FIG["call_loss_musd_nearest25"] == 150, "%.2f -> %d" % (CRE, bin25(CRE)))
check("GOLDEN mid-bin", edge25(CRE) >= 6.25, "%.2f from the nearest edge (quarter bin 6.25)" % edge25(CRE))
check("GOLDEN eligibility", all(v >= 1.2e9 for v in G.principal.values()),
      ", ".join("%s %.1f" % (k.split()[0], v / 1e6) for k, v in G.principal.items()))

# ------------------------------------------------------------------------------------------------- three rules, R1
log_rows = len(G.cre.log)
stmt_rows = sum(len(v) for v in G.cre.stmts.values())
check("R1 raw material ships", len(G.cre_hist) >= 600 and stmt_rows >= 4000 and len(G.wall) >= 300,
      "%d maturities with outcomes, %d statements, %d balloons due by December 2027" % (len(G.cre_hist), stmt_rows,
                                                                                        len(G.wall)))
heads = []
for f in sorted(os.listdir(PACK)):
    p = os.path.join(PACK, f)
    if f.endswith(".csv"):
        heads += [h.lower() for h in open(p, encoding="utf-8").readline().strip().split(",")]
    elif f.endswith(".xlsx"):
        from openpyxl import load_workbook
        wb = load_workbook(p, read_only=True)
        for ws in wb.worksheets:
            for r in ws.iter_rows(min_row=1, max_row=1, values_only=True):
                heads += [str(c).lower() for c in r if c is not None]
        wb.close()
bad_heads = [h for h in heads if re.search(r"cover|dscr|debt.?yield|extension|probab|refinanc|cpr|speed|duration|eve\b",
                                           h)]
check("R1 no column holds the deciding quantity", not bad_heads, ", ".join(bad_heads) or "none")

# ------------------------------------------------------------------------------------------------- R2: mess neutrality
def call_and_bin(cre_val, mort_val=None, mbs_val=None, t_val=None, auto_val=None):
    v = with_cre(cre_val, mort_val)
    if mbs_val is not None:
        v["Agency MBS"] = mbs_val
    if t_val is not None:
        v["Treasury ladder"] = t_val
    if auto_val is not None:
        v["Indirect auto loans"] = auto_val
    return ranking(v)[0], bin25(v["Fixed-rate commercial real estate"])


GOLD_CALL = ("Fixed-rate commercial real estate", 150)
M = C.load_mortgages(PACK)
pool = G.m_pool
# R2a the conversion: the curve fitted on the new platform's extract only
rows_new = [r for r in M.rows if r[1] >= C.mo(2024, 9)]
Mn = C.Mort()
Mn.rows = rows_new
th, _ = C.fit_mortgage(*C.mortgage_panel(Mn, G.rates))
m_new = C.measure(C.mortgage_cf(pool, C.mortgage_smm_plan(th, pool, G.plan.mortgage), G.m_curt), G.W)[0] / 1e6
check("R2 conversion: new platform only", call_and_bin(CRE, m_new) == GOLD_CALL, "mortgages %.1f" % m_new)
# R2b loans held for sale counted, their deliveries read as payoffs
leg = C.read_csv(os.path.join(PACK, R.F_LEGACY))
new = C.read_csv(os.path.join(PACK, R.F_SERV))
extra = []
for r in leg:
    if r["PORTF"] == "HFS":
        cyc = r["CYCLE"]
        extra.append(("H" + r["LOAN_NO"], C.mo(int(cyc[:4]), int(cyc[4:])), C.pdate(r["ORIG_DT"]), int(r["TERM"]),
                      float(r["NOTE_RT"]), float(r["BEG_PRIN"]), float(r["SCHED_PRIN"]), 0.0, float(r["PIF_PRIN"]),
                      float(r["END_PRIN"]), 1 if r["STAT"] == "S" else 0))
for r in new:
    if r["investor_type"] == "HELD FOR SALE":
        y, m = r["reporting_period"].split("-")
        extra.append(("H" + r["loan_id"], C.mo(int(y), int(m)), C.pdate(r["origination_date"]),
                      int(r["original_term_months"]), float(r["interest_rate"]) * 100, float(r["beginning_principal"]),
                      float(r["scheduled_principal"]), 0.0, float(r["unscheduled_principal"]), float(r["ending_principal"]),
                      1 if r["zero_balance_code"] == "15" else 0))
Mh = C.Mort()
Mh.rows = M.rows + extra
th, _ = C.fit_mortgage(*C.mortgage_panel(Mh, G.rates))
m_hfs = C.measure(C.mortgage_cf(pool, C.mortgage_smm_plan(th, pool, G.plan.mortgage), G.m_curt), G.W)[0] / 1e6
check("R2 held-for-sale deliveries as payoffs", call_and_bin(CRE, m_hfs) == GOLD_CALL,
      "mortgages %.1f (%d held-for-sale loan-months)" % (m_hfs, len(extra)))
# R2c the trailer row read as a loan: it carries no portfolio code and no balance in BEG_PRIN
trl = [r for r in leg if r["LOAN_NO"] == "TRL"]
check("R2 legacy trailer", len(trl) == 1 and trl[0]["PORTF"] == "" and trl[0]["BEG_PRIN"] == "",
      "trailer count %s" % (trl[0]["CYCLE"] if trl else "-"))
# R2d the rate sheet codes renamed in 2024: only the new codes read
rates_new = {k: v for k, v in G.rates.items() if k[1] >= C.mo(2024, 1)}
Hn = [h for h in C.cre_history(G.cre, {**rates_new, **{(c, o): v for (c, o), v in G.rates.items() if o < C.mo(2024, 1)}})
      if h["date"] >= dt.date(2024, 1, 1)]
b = C.logit_fit(np.array([h["cover"] for h in Hn]), np.array([h["y"] for h in Hn]))
fut = [L for L in G.cre_loans if not L["extended"]]
cre_24 = C.measure(C.cre_cf(G.cre_loans, lambda L: float(C.logit_pred(b, np.array([G.cre_cover[id(L)]]))[0])
                            if not L["extended"] else 0.0), G.W)[0] / 1e6
check("R2 rate codes renamed: 2024 onward only", call_and_bin(cre_24) == GOLD_CALL, "CRE %.1f on %d maturities" % (cre_24,
                                                                                                                len(Hn)))
# R2e ACT/360 read as 30/360
check("R2 interest basis", call_and_bin(RT["family"]["interest on 30/360"]) == GOLD_CALL,
      "%.1f" % RT["family"]["interest on 30/360"])
# R2f the log's two layouts: only the 2020 onward sheets read
H20 = [h for h in G.cre_hist if h["date"] >= dt.date(2020, 1, 1)]
b = C.logit_fit(np.array([h["cover"] for h in H20]), np.array([h["y"] for h in H20]))
cre_20 = C.measure(C.cre_cf(G.cre_loans, lambda L: float(C.logit_pred(b, np.array([G.cre_cover[id(L)]]))[0])
                            if not L["extended"] else 0.0), G.W)[0] / 1e6
check("R2 maturity log: 2020 layout only", call_and_bin(cre_20) == GOLD_CALL, "%.1f" % cre_20)
# R2g statements by fiscal year end, whatever the review date
check("R2 statements by fiscal year end", call_and_bin(RT["family"]["statement by fiscal year end"]) == GOLD_CALL,
      "%.1f" % RT["family"]["statement by fiscal year end"])
# R2h floating loans in the pool at their monthly repricing (a month of duration each)
flt = [r for r in G.cre.pos if r["rate_type"] == "FLOATING"]
fl_add = sum(float(r["principal_balance"]) for r in flt) * float(np.mean(G.W[:1])) / 1e6
check("R2 floating loans at their repricing", call_and_bin(CRE + fl_add) == GOLD_CALL,
      "%d floating loans add %.2f" % (len(flt), fl_add))
# R2i the custodian's thousands read as dollars
cust = C.load_custody(PACK)
fac = C.load_factors(PACK)
check("R2 custody thousands", call_and_bin(CRE, mbs_val=G.MBS / 1e9, t_val=G.T / 1e9) == GOLD_CALL,
      "MBS %.3f, Treasury %.3f" % (G.MBS / 1e9, G.T / 1e9))
# R2j every agency pool in the account read as the MBS pool
orig_pools = C.mbs_pools
C.mbs_pools = lambda cu: [r for r in cu if r["security_type"] == "AGENCY MBS"]
mbs_all = C.measure(C.mbs_cf(cust, fac)[0], G.W)[0] / 1e6
C.mbs_pools = orig_pools
check("R2 newer agency pools included", call_and_bin(CRE, mbs_val=mbs_all) == GOLD_CALL and CRE / mbs_all >= 1.15,
      "MBS %.1f, margin %.2f" % (mbs_all, CRE / mbs_all))
# R2k the agency payment delay ignored
mbs_d0 = C.measure(C.mbs_cf(cust, fac, delay=0)[0], G.W)[0] / 1e6
check("R2 agency payment delay", call_and_bin(CRE, mbs_val=mbs_d0) == GOLD_CALL, "MBS %.1f" % mbs_d0)
# R2l the auto roll read on the ABS convention (prepayments over the loans' original amounts)
tape, roll = C.load_auto(PACK)
orig_amt = sum(float(r["amount_financed"]) for r in tape)
abs_rate = np.mean([float(r["prepaid_principal"]) for r in roll[-12:]]) / orig_amt
bal = np.array([float(r["principal_balance"]) for r in tape])
smm_abs = min(0.2, abs_rate * orig_amt / bal.sum())
auto_abs = C.measure(C.auto_cf(tape, smm_abs), G.W)[0] / 1e6
check("R2 auto on ABS", call_and_bin(CRE, auto_val=auto_abs) == GOLD_CALL, "auto %.1f" % auto_abs)

# ------------------------------------------------------------------------------------------------- R3 on the clean truth
TW = WD.simulate()
H_ = K.HORIZON
Wt = K.discount(np.arange(1, H_ + 1) / 12) - K.discount(np.arange(1, H_ + 1) / 12, K.SHOCK)


def tmeasure(Cf):
    Cf = np.asarray(Cf, float)
    return np.mean([(Cf[m:] * Wt[:len(Cf) - m]).sum() for m in range(2, 14)]) / 1e6


def t_level(bal, rate, nrem, smm):
    return C.level_pay(bal, rate, nrem, smm)


mp = TW.m_pool
tb = np.array([L["bal_asof"] for L in mp])
tn = np.array([L["note"] for L in mp])
tr = np.array([L["term"] - (K.ASOF_M - L["orig"]) for L in mp])
ta = np.array([K.ASOF_M - L["orig"] for L in mp])
S = np.zeros((len(mp), H_))
for t in range(H_):
    S[:, t] = WD.m_smm((tn - K.PLAN_MORTGAGE) / 100.0, [(K.PROJ_START + t) % 12 + 1] * len(mp), ta + t + 1)
t_M = tmeasure(t_level(tb, tn, tr, S))
hist = np.array([(h[1], h[2], h[3], h[5]) for h in TW.m_hist])
sel = hist[:, 0] > K.ASOF_M - 12
s12 = hist[sel, 3].sum() / (hist[sel, 1] - hist[sel, 2]).sum()
t_M_trail = tmeasure(t_level(tb, tn, tr, np.full((len(mp), H_), s12)))
cf = np.zeros(H_)
for Pm in TW.mbs:
    B = Pm["face"] * Pm["factors"][K.ASOF_M]
    n = Pm["wam0"] - (K.ASOF_M - Pm["issue"])
    inc = (Pm["wac"] - K.PLAN_MORTGAGE_15 - (0.70 if Pm["term"] == 360 else 0)) / 100
    for t in range(H_ - 1):
        if n <= 0 or B <= 0:
            break
        smm = WD.M_TURN * 0.95 * WD.SEASON[(K.PROJ_START + t) % 12] * (0.62 if inc < -0.02 else 0.8 if inc < -0.01 else 1) \
            + 0.030 / (1 + np.exp(-(inc - 0.0075) / 0.0022))
        rr = Pm["wac"] / 1200
        pay = B * rr / (1 - (1 + rr) ** (-n))
        sch = B if n <= 1 else min(pay - B * rr, B)
        pre = (B - sch) * smm
        cf[t + 1] += B * Pm["cpn"] / 1200 + sch + pre
        B -= sch + pre
        n -= 1
t_MBS = tmeasure(cf)
cfT = np.zeros(H_)
for (pm, cpn, md, par) in TW.ust:
    mm = K.mo(md.year, md.month)
    o = mm
    while o > K.ASOF_M:
        cfT[o - K.PROJ_START] += par * cpn / 200
        o -= 6
    cfT[mm - K.PROJ_START] += par
t_T = tmeasure(cfT)
ap = TW.auto_pool
ab = np.array([a["bal"] for a in ap])
ab0 = np.array([a["bal0"] for a in ap])
t_A = tmeasure(t_level(ab, np.array([a["apr"] for a in ap]), np.array([a["term"] - a["age"] for a in ap]),
                       np.repeat(np.minimum(1, WD.AUTO_ABS * ab0 / np.maximum(ab, 1))[:, None], H_, 1)))
tpool = [L for L in TW.cre if R.cre_alive(L)]


def t_cre(pfun):
    Cf = np.zeros(H_)
    for L in tpool:
        k0 = K.ASOF_M - L["orig"]
        prev = L["bal_path"][k0 - 1]
        ext_now = L["mat"] <= K.ASOF_M
        mat = L["mat"] + (WD.CRE_EXT_MONTHS if ext_now else 0)
        p = 0.0 if ext_now else pfun(L)
        last = mat + (WD.CRE_EXT_MONTHS if p > 0 else 0)
        for t in range(last - K.ASOF_M):
            o = K.PROJ_START + t
            kk = o - L["orig"]
            days = WD.days_in(o - 1) if L["basis"] == "ACT/360" else 30
            it = prev * L["r0"] / 100 * days / 360
            nb = L["bal_path"][kk - 1]
            sch = prev - nb
            if o < mat:
                Cf[t] += it + sch
            elif o == mat:
                Cf[t] += it + sch + (1 - p) * nb
            elif o < last:
                Cf[t] += p * (it + sch)
            else:
                Cf[t] += p * (it + sch + nb)
            prev = nb
    return tmeasure(Cf)


t_hist = [L for L in TW.cre if L["outcome"] and L["mat"] >= K.mo(2015, 1)]
t_recent = np.mean([L["ext"] for L in t_hist if L["mat"] > K.ASOF_M - 12])


def t_cover_now(L):
    s = R.latest_stmt(L)
    return s["noi"] / (L["bal_mat"] * float(WD.dc(K.PLAN_CRE, 300)))


t_C0 = t_cre(lambda L: 0.0)
t_Crec = t_cre(lambda L: t_recent)
t_Ccov = t_cre(lambda L: float(WD.cre_p_ext(t_cover_now(L))))
tv = {"Treasury ladder": t_T, "Agency MBS": t_MBS, "2023-24 residential mortgages": t_M, "Indirect auto loans": t_A}
r3a = ranking({**tv, "Fixed-rate commercial real estate": t_Crec})[0]
check("R3a analyst test on the clean truth", r3a == "Agency MBS",
      "default path names %s (MBS %.1f, mortgages %.1f, CRE %.1f at the recent share %.3f)" % (r3a, t_MBS, t_M, t_Crec,
                                                                                            t_recent))
r3b = ranking({**tv, "Fixed-rate commercial real estate": t_Ccov})[0]
check("R3b the decisive step alone, clean truth", r3b == "Fixed-rate commercial real estate" and bin25(t_Ccov) == 150,
      "%s, CRE %.1f" % (r3b, t_Ccov))
lower = {"R0 (every pool at last year's speed)": ranking({**tv, "2023-24 residential mortgages": t_M_trail,
                                                          "Fixed-rate commercial real estate": t_C0})[0],
         "R0 + the prepayment curve": ranking({**tv, "Fixed-rate commercial real estate": t_C0})[0],
         "R0 + the recent share": ranking({**tv, "2023-24 residential mortgages": t_M_trail,
                                           "Fixed-rate commercial real estate": t_Crec})[0]}
check("R3b each lower correction alone is wrong", all(v != "Fixed-rate commercial real estate" for v in lower.values()),
      "; ".join("%s: %s" % kv for kv in lower.items()))
# R3c no plant: no repeated monthly block in the servicing data, no memo or ranking among the documents
seqs = {}
for r in new:
    if r["investor_type"] == "PORTFOLIO":
        seqs.setdefault(r["loan_id"], []).append((r["scheduled_principal"], r["unscheduled_principal"]))
sig = {}
dup = 0
for k, v in seqs.items():
    if len(v) >= 6:
        key = tuple(v)
        dup += key in sig
        sig[key] = k
check("R3c no copied block", dup == 0, "%d loans with six or more periods, %d repeated sequences" % (len(sig), dup))
texts = [DOC.notes_text({**{f: 1 for f in os.listdir(PACK)}, **{R.F_LEGACY: 1, R.F_SERV: 1, R.F_XREF: 1, R.F_RATES: 1,
                                                               R.F_CRE: 1, DOC.F_LOG: 1, R.F_STMT: 1, R.F_CUSTODY: 1,
                                                               R.F_FACTORS: 1, R.F_AUTO: 1, R.F_ROLL: 1,
                                                               DOC.F_REGISTER: 1, R.F_SCHED: 1, R.F_CLEAR: 1,
                                                               R.F_LOCKS: 1}})]
texts += [p for _, ps in DOC.POLICY for p in ps] + [b for _, b in DOC.SCHEDULE_A] + DOC.PLAN_NOTE
plant = [w for w in ("recommend", "we suggest", "should be designated", "draft", "rank", "largest loss", "extend more",
                     "refinanc", "cover", "debt yield", "dscr", "trailing")
         if any(w in t.lower() for t in texts)]
check("R3c no decoy or method text", not plant, ", ".join(plant) or "none")

# ------------------------------------------------------------------------------------------------- the ladder
R0 = ranking(with_cre(RT["cre_contractual"], G.M_trailing / 1e6))
R1 = ranking(with_cre(RT["cre_contractual"]))
v0 = with_cre(RT["cre_contractual"], G.M_trailing / 1e6)
check("LADDER R0 names the mortgages, CRE 4th or 5th", R0[0] == "2023-24 residential mortgages" and
      R0.index("Fixed-rate commercial real estate") >= 3 and v0[R0[0]] / v0[R0[1]] >= 1.15,
      "%s %.1f / %s %.1f = %.2f; CRE %d" % (R0[0], v0[R0[0]], R0[1], v0[R0[1]], v0[R0[0]] / v0[R0[1]],
                                            R0.index("Fixed-rate commercial real estate") + 1))
v1 = with_cre(RT["cre_contractual"])
check("LADDER R1 default names Agency MBS", R1[0] == "Agency MBS" and v1[R1[0]] / v1[R1[1]] >= 1.15,
      "%.2f over %s" % (v1[R1[0]] / v1[R1[1]], R1[1]))
for lab, key in (("R2a recent share", "cre_recent"), ("R2b rate gap", "cre_gap"), ("R2c note-rate DSCR", "cre_cur")):
    v = with_cre(RT[key])
    rk = ranking(v)
    m = v[rk[0]] / v[rk[1]]
    pos = rk.index("Fixed-rate commercial real estate") + 1
    check("LADDER %s names Agency MBS" % lab, rk[0] == "Agency MBS" and m >= (1.20 if pos == 2 else 1.15),
          "CRE %.1f, %d, margin %.2f" % (RT[key], pos, m))
v3 = with_cre(CRE)
rk3 = ranking(v3)
check("LADDER R3 decisive names the pool", rk3[0] == "Fixed-rate commercial real estate" and
      v3[rk3[0]] / v3[rk3[1]] >= 1.2, "%.2f over %s" % (v3[rk3[0]] / v3[rk3[1]], rk3[1]))
dom = (CRE - RT["cre_contractual"]) / (POOLS["Agency MBS"] - RT["cre_contractual"])
check("DOMINANCE", dom >= 1.2, "%.2f" % dom)
grid = {
    "cover with last year's mortgage speed": (ranking(with_cre(CRE, G.M_trailing / 1e6))[0], "Fixed-rate commercial real estate"),
    "debt yield, every maturity": (ranking(with_cre(RT["cre_dy"]))[0] + " %d" % bin25(RT["cre_dy"]), None),
    "note-rate DSCR since 2023": (str(bin25(RT["cre_cur_2023"])), "125"),
    "every balloon extended": (str(bin25(RT["cre_all_extend"])), "200"),
    "wall only": (str(bin25(RT["cre_wall_only"])), "150"),
}
okg = grid["cover with last year's mortgage speed"][0] == grid["cover with last year's mortgage speed"][1] and \
    bin25(RT["cre_dy"]) != 150 and grid["note-rate DSCR since 2023"][0] == "125" and \
    grid["every balloon extended"][0] == "200" and grid["wall only"][0] == "150"
check("GRID cells", okg, "; ".join("%s: %s" % (k, v[0]) for k, v in grid.items()))
for k in ("cre_recent", "cre_since2023", "cre_pooled", "cre_gap", "cre_gap_2023", "cre_cur", "cre_cur_2023", "cre_dy",
          "cre_ptype", "cre_all_extend", "cre_contractual"):
    pass
rivals_out = [k for k in ("cre_recent", "cre_since2023", "cre_pooled", "cre_gap", "cre_gap_2023", "cre_cur",
                          "cre_cur_2023", "cre_dy", "cre_ptype", "cre_all_extend", "cre_contractual")
              if bin25(RT[k]) == 150]
check("RIVALS outside the golden bin", not rivals_out, ", ".join(rivals_out) or
      "every rival misses: " + ", ".join("%s %.1f" % (k[4:], RT[k]) for k in ("cre_recent", "cre_gap", "cre_cur",
                                                                               "cre_cur_2023", "cre_dy", "cre_ptype",
                                                                               "cre_all_extend")))
# ------------------------------------------------------------------------------------------------- the golden family
fam = RT["family"]
check("FAM every construction in the bin", all(bin25(v) == 150 for v in fam.values()),
      "%.1f to %.1f" % (min(fam.values()), max(fam.values())))
H = G.cre_hist
xs = np.array([h["cover"] for h in H])
ys = np.array([h["y"] for h in H])
cf0, cf1, base = [], [], 0.0
for L in G.cre_loans:
    if L["extended"]:
        base += C.measure(C.cre_cf([L], lambda L: 0.0), G.W)[0]
    else:
        cf0.append(C.measure(C.cre_cf([L], lambda L: 0.0), G.W)[0])
        cf1.append(C.measure(C.cre_cf([L], lambda L: 1.0), G.W)[0])
cf0, cf1 = np.array(cf0), np.array(cf1)
covs = np.array([G.cre_cover[id(L)] for L in G.cre_loans if not L["extended"]])
g = np.random.default_rng(1661214)
boot = []
for _ in range(200):
    i = g.integers(0, len(H), len(H))
    bb = C.logit_fit(xs[i], ys[i])
    boot.append((base + (cf0 + C.logit_pred(bb, covs) * (cf1 - cf0)).sum()) / 1e6)
sig1 = float(np.std(boot))
lo, hi = min(fam.values()) - sig1, max(fam.values()) + sig1
check("FAM one sigma inside the bin", bin25(lo) == 150 and bin25(hi) == 150,
      "sigma %.2f; %.1f to %.1f" % (sig1, lo, hi))
check("FAM debt constants ruled out by the sheet", "25-year amortization" in R.DESC["CRE5F"], R.DESC["CRE5F"])
# ------------------------------------------------------------------------------------------------- out of sample
oos = C.oos_table(G)
check("OOS cover beats every rival by half", all(oos["cover"] <= 0.5 * oos[k] for k in ("gap", "cur", "dy",
                                                                                          "last_year_share",
                                                                                          "pooled_share")),
      ", ".join("%s %.3f" % (k, v) for k, v in oos.items() if isinstance(v, float)))
low = [h for h in H if h["cover"] < 1.0]
check("OOS history below a cover of 1.0 all extended", low and all(h["y"] == 1 for h in low),
      "%d of %d" % (sum(h["y"] for h in low), len(low)))

# ------------------------------------------------------------------------------------------------- semantic forks
pol = " ".join(DOC.policy_sentences())


def cfs():
    tape_, roll_ = C.load_auto(PACK)
    return {"Treasury ladder": C.treasury_cf(cust)[0], "Agency MBS": C.mbs_cf(cust, fac)[0],
            "2023-24 residential mortgages": G.m_cf, "Indirect auto loans": C.auto_cf(tape_, G.auto_smm),
            "Fixed-rate commercial real estate": G.cre_cf}


CF = cfs()


def call_with(fn):
    v = {k: fn(c) / 1e6 for k, c in CF.items()}
    return ranking(v)[0], v["Fixed-rate commercial real estate"]


check("SF1 five pools", "the eligible pool in Schedule A" in pol and len(DOC.SCHEDULE_A) == 5, "Schedule A, 5 pools")
check("SF2 designated against", "ALCO designates each overlay, before it is traded" in pol, "policy section 3")
c3, v3_ = call_with(lambda c: C.measure(c, G.W, months=[C.ASOF])[0])
check("SF3 averaged, not the as-of", "averaged over the month-ends of the overlay's first twelve months" in pol and
      bin25(v3_) != 150, "the as-of alone: %s %.1f" % (c3, v3_))
c4, v4 = call_with(lambda c: C.measure(c, G.W, months=[C.mo(2026, 12)] + [C.mo(2027, k) for k in range(1, 12)])[0])
c4b, v4b = call_with(lambda c: C.measure(c, G.W, months=C.MEASURE + [C.mo(2028, 1)])[0])
check("SF4 the twelve month-ends", c4 == c4b == G.call and bin25(v4) == bin25(v4b) == 150, "%.1f, %.1f" % (v4, v4b))
t_ = np.arange(0, C.HORIZON + 14) / 12.0
z_ = np.interp(t_, G.plan.tenors, G.plan.zeros) / 100.0
D0, D2 = np.exp(-z_ * t_), np.exp(-(z_ + 0.02) * t_)


def fwd(c):
    vals = []
    for m in C.MEASURE:
        k = m - C.START
        tail = c[k + 1:]
        j = np.arange(1, len(tail) + 1)
        a = k + 1
        vals.append(float((tail * (D0[a + j] / D0[a] - D2[a + j] / D2[a])).sum()))
    return np.mean(vals)


c5, v5 = call_with(fwd)
check("SF5 the same zero rates at every month-end", "the same zero rates at every month-end" in pol and c5 == G.call and
      bin25(v5) == 150, "forwards: %.1f" % v5)
check("SF6 time and placement", "a month counting as a twelfth of a year" in pol and
      "placed at the end of the month in which it is paid" in pol, "filed")
check("SF7 before credit losses", "before credit losses" in pol, "filed")
check("SF8 the pool at the as-of", "positions added after it are not part of it" in pol, "filed")
check("SF9 eligible at the as-of", "its principal outstanding at the close on the as-of date" in pol, "filed")
check("SF10 the base case", "ALCO's most recent planning cycle" in pol and G.plan.cre == 6.95 and
      G.plan.mortgage == 6.25 and G.plan.conf15 == 5.55, "6.25, 5.55, 6.95")
cre_noext = C.measure(C.cre_cf([L for L in G.cre_loans if not L["extended"]],
                               lambda L: float(C.logit_pred(G.cover_beta, np.array([G.cre_cover[id(L)]]))[0])), G.W)[0] / 1e6
check("SF11 extended loans in the pool", bin25(cre_noext) == 150 and "with a fixed note rate" in pol,
      "without them %.1f" % cre_noext)
check("SF12 agency MBS bought 2020-21", "bought in 2020 and 2021" in pol and call_and_bin(CRE, mbs_val=mbs_all) == GOLD_CALL,
      "every agency pool: %.1f" % mbs_all)
hfs_left = sum(1 for r in new if r["investor_type"] == "HELD FOR SALE" and r["reporting_period"] == "2026-11")
check("SF13 held for investment", "held for investment" in pol and hfs_left == 0, "%d held for sale at the as-of" % hfs_left)
check("SF14 rounding to $25 million", FIG["call_loss_musd_nearest25"] == 150, "filed in the prompt")
prog = C.programme(PACK)
reg = C.load_register(PACK)
cust_book = [t for t in reg if t["Book"] == "CUSTOMER" and t["Status"] == "LIVE"]
check("SF15 the hedge programme is the ALM book", "are not part of the programme" in pol and len(cust_book) > 50,
      "%d live customer-programme trades excluded" % len(cust_book))
qe = set(C.QUARTER_ENDS)
on_qe = [t for t in reg if t["Book"] == "ALM" and t["Maturity date"] in qe]
check("SF16 no maturity on a quarter-end", not on_qe, "%d" % len(on_qe))
by_code = C.programme(PACK, by="strategy")
mv = [round((a - b) / 1e6, 1) for a, b in zip(prog["overlay"], by_code["overlay"])]
check("SF17 parts by what each swap is designated against", "Overlays are pay-fixed swaps designated against a fixed-rate "
      "asset pool" in pol and all(x == mv[0] and x > 0 for x in mv), "strategy code moves overlays by %.1f" % mv[0])
no_new = C.programme(PACK, include_overlay=False)
check("SF18 the new overlay included", all(round((a - b) / 1e6, 1) == 1200.0 for a, b in zip(prog["overlay"],
                                                                                         no_new["overlay"])), "1,200.0")
flat = sum(1 for t in reg if t["Amortizing"] == "Y" and t["Book"] == "ALM")
NOTES = re.sub(r"\s+", " ", open(os.path.join(PACK, DOC.F_NOTES), encoding="utf-8").read())
check("SF19 notional of the period in effect", flat == 2 and "an amortizing swap's current period" in NOTES,
      "%d amortizing trades; the register's note" % flat)

# ------------------------------------------------------------------------------------------------- the ask
gold_fig = {k: [round(v / 1e6, 1) for v in prog[k]] for k in prog}
check("ASK A golden in figures.json", gold_fig == FIG["programme_musd"], json.dumps(gold_fig))
truth = SW.ask_a_truth(SW.build())
check("ASK A golden equals the truth", all(abs(a - b) < 1 for k in prog for a, b in zip(prog[k], truth[k])), "")
exact = all(abs(v / 1e5 - round(v / 1e5)) < 1e-6 for k in prog for v in prog[k])
check("ASK A figures exact to the printed unit", exact, "every figure is a whole number of $0.1 million (0.05 from both edges)")
meas = CR.measure(PACK, quiet=True)
check("ASK A cracker misses all twelve", meas["res"]["cracker"]["figures"] == 0, "%d hit" % meas["res"]["cracker"]["figures"])
check("ASK A over-cleaner misses", meas["res"]["over-cleaner"]["figures"] <= 4, "%d hit" % meas["res"]["over-cleaner"]["figures"])
check("ASK A pair ceiling and leakage", meas["pair"] <= 40 and meas["leak"] < 35, "pair %.1f, leakage %.1f" % (meas["pair"],
                                                                                                         meas["leak"]))
clr = C.load_clearing(PACK)
tradenos = {str(t["Trade No."]) for t in reg}
live_bil = {str(t["Trade No."]) for t in reg if t["Cleared"] == "N" and t["Status"] == "LIVE"}
held_refs = [c["client_trade_ref"] for c in clr if c["client_trade_ref"] in live_bil]
check("ASK A device A1 rows", len(held_refs) == 4, "%d live bilateral trades held as client references" % len(held_refs))
ids = [str(t["Trade No."]) for t in reg]
refs_ok = all(str(t["Clearing ref"]) in {c["ccp_trade_id"] for c in clr} for t in reg if t["Cleared"] == "Y" and
              t["Status"] == "LIVE")
check("ASK A device A1 silent", len(ids) == len(set(ids)) and refs_ok and
      not any("backload" in x.lower() for x in texts), "unique numbers, every clearing ref on the statement, no sentence")
terms = {}
for t in reg:
    if t["Book"] == "ALM" and t["Status"] == "LIVE":
        terms.setdefault((t["Bank pays"], t["Notional (USD)"], t["Effective date"], t["Maturity date"],
                          t["Fixed rate (%)"]), []).append(t)
pairs = [v for v in terms.values() if len(v) == 2]
check("ASK A over-cleaning half", len(pairs) == 6, "%d repeated-terms pairs (4 backloads, 2 genuine)" % len(pairs))

# ------------------------------------------------------------------------------------------------- separation and distractors
tmp = tempfile.mkdtemp(prefix="b166_sep_")
try:
    for f in os.listdir(PACK):
        if f not in (DOC.F_REGISTER, R.F_SCHED, R.F_CLEAR, DOC.F_NMD, R.F_LOCKS):
            shutil.copy(os.path.join(PACK, f), tmp)
    G2 = C.golden(tmp)
    check("DEVICE separation: the call reads no swap file", G2.call == G.call and abs(G2.CRE - G.CRE) < 1 and
          all(abs(G2.pools[k] - G.pools[k]) < 1 for k in G.pools), "unchanged with the swap files deleted")
    check("DISTRACTOR deletion", G2.call == G.call and abs(G2.CRE - G.CRE) < 1,
          "call unchanged without %s and %s" % (DOC.F_NMD, R.F_LOCKS))
finally:
    shutil.rmtree(tmp)
tmp = tempfile.mkdtemp(prefix="b166_sep_")
try:
    for f in os.listdir(PACK):
        if f not in (DOC.F_NMD, R.F_LOCKS):
            shutil.copy(os.path.join(PACK, f), tmp)
    check("DISTRACTOR deletion, the ask", C.programme(tmp) == prog, "Ask A unchanged")
finally:
    shutil.rmtree(tmp)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("DISTRACTORS declared", sorted(meta["distractor_files"]) == sorted([DOC.F_NMD, R.F_LOCKS]) and
      not any("distractor" in f for f in os.listdir(PACK)), ", ".join(meta["distractor_files"]))

# ------------------------------------------------------------------------------------------------- input gates
files = sorted(os.listdir(PACK))
fmts = sorted({f.rsplit(".", 1)[1] for f in files})
check("GATE files", len(files) >= 10, "%d files" % len(files))
check("GATE formats", len(fmts) >= 3, ", ".join(fmts))
check("GATE a file of 25,000 rows", meta["input_gates"]["largest_file_rows"] >= 25000,
      "%s %d" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))

# ------------------------------------------------------------------------------------------------- realism sweep
roll_cols = [[r[c] for r in roll] for c in ("prepaid_principal", "scheduled_principal", "charge_offs")]
check("REAL no constant stream", all(len(set(c)) == len(c) for c in roll_cols), "the auto roll's columns vary")
counts = {}
for r in new:
    if r["investor_type"] == "PORTFOLIO":
        counts[r["reporting_period"]] = counts.get(r["reporting_period"], 0) + 1
check("REAL no identical monthly counts", len(set(counts.values())) >= len(counts) - 2, "%d periods, %d distinct counts"
      % (len(counts), len(set(counts.values()))))
roundish = [k for k, v in G.principal.items() if abs(v / 1e6 - round(v / 1e8) * 100) < 0.5 and "Treasury" not in k]
check("REAL no round pool totals", not roundish, ", ".join(roundish) or "none")
names_ok = True
alltext = ""
for f in files:
    p = os.path.join(PACK, f)
    if f.endswith((".txt",)):
        alltext += open(p, encoding="utf-8").read()
    if f.endswith(".pdf"):
        from pypdf import PdfReader
        alltext += " ".join(pg.extract_text() for pg in PdfReader(p).pages)
for nm in re.findall(r"\b(?:Prepared by|Owner:|Questions to|Approved by)\s+([A-Z][a-z]+ [A-Z][a-z]+)", alltext):
    names_ok &= nm in K.PEOPLE.values()
check("REAL personas from guard names", names_ok and "Guy Morrison" not in alltext,
      "named: " + ", ".join(sorted(set(re.findall(r"(Sheri Roberts|Cody Li|Jeff Guzman|Joshua Boyd)", alltext)))))
check("REAL no em or en dash", chr(0x2014) not in alltext and chr(0x2013) not in alltext, "")
leaks = []
for f in files:
    b = open(os.path.join(PACK, f), "rb").read()
    if f.endswith((".xlsx", ".pptx", ".docx")):
        with zipfile.ZipFile(os.path.join(PACK, f)) as z:
            b = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps"))
    for w in (b"openpyxl", b"python-pptx", b"ReportLab", b"reportlab", b"Python"):
        if w in b:
            leaks.append("%s:%s" % (f, w.decode()))
check("REAL containers scrubbed (H1)", not leaks, ", ".join(leaks) or "clean")
mt = {int(os.path.getmtime(os.path.join(PACK, f))) for f in files}
check("REAL one export time", len(mt) == 1, "%s" % sorted(mt))
late = re.findall(r"\b(2026-12-(?:0[4-9]|[12]\d|3[01])|2027-\d\d-\d\d)\b", DOC.notes_text({f: 0 for f in [R.F_LEGACY,
                  R.F_SERV, R.F_XREF, R.F_RATES, R.F_CRE, DOC.F_LOG, R.F_STMT, R.F_CUSTODY, R.F_FACTORS, R.F_AUTO, R.F_ROLL,
                  DOC.F_REGISTER, R.F_SCHED, R.F_CLEAR, R.F_LOCKS]}))
check("REAL no document dated after the pull", not late, ", ".join(late) or "none")
plan_in = [w for w in ("6.25", "5.55", "6.95") if w in alltext]
check("REAL each planning rate in one file", not plan_in, ", ".join(plan_in) or "the planning workbook only")
listed = set(re.findall(r"^([\w.-]+\.(?:csv|xlsx|pdf|txt))\b", open(os.path.join(PACK, DOC.F_NOTES),
                                                                         encoding="utf-8").read(), re.M))
listed |= {DOC.F_POLICY, DOC.F_ALM} if (DOC.F_POLICY in NOTES and DOC.F_ALM in NOTES) else set()
check("H9 the notes register every shipped file", listed == set(files) - {DOC.F_NOTES},
      "missing: %s; extra: %s" % (sorted(set(files) - {DOC.F_NOTES} - listed), sorted(listed - set(files))))
pts = sorted(set(h["ptype"] for h in G.cre_hist))
Xp = np.column_stack([xs] + [[1.0 if h["ptype"] == p else 0.0 for h in G.cre_hist] for p in pts[1:]])
bp = C.logit_fit(Xp, ys)
pmap = {L_["prop"]: L_["ptype"] for L_ in G.cre_loans}


def p_pt(L):
    row = [G.cre_cover[id(L)]] + [1.0 if L["ptype"] == p else 0.0 for p in pts[1:]]
    return float(C.logit_pred(bp, np.array([row]))[0])


cre_pt = C.measure(C.cre_cf(G.cre_loans, lambda L: p_pt(L) if not L["extended"] else 0.0), G.W)[0] / 1e6
check("H14 a finer grain: cover with property type", bin25(cre_pt) == 150, "%.1f" % cre_pt)
check("FIGURES figures.json matches the golden", FIG["call_pool"] == G.call and FIG["call_loss_musd_unrounded"] ==
      round(CRE, 2) and FIG["runner_up"] == rk3[1], "%s %.2f, runner-up %s" % (FIG["call_pool"], CRE, rk3[1]))

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print("checks: %d run, %d failed" % (len(RESULTS), n_fail))
sys.exit(1 if n_fail else 0)
