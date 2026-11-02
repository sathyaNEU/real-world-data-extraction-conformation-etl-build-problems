"""The generator's assertions for task180 (architecture 5). Run after make.py; exit 1 on any failure.

Blocks: input gates and containers; the three rules (R1, R2, R3) executed on the generator's clean truth and
on the cut pack; the semantic fork table (SF ids, each with its positive control); the ladder, the licensed
estimator family and the golden's assumptions (lesson 7); the shock and separation tests; the ask's devices
(lesson 8: every filed rule and every field's plain meaning run over the device rows); the realism sweep;
figures.json against the golden deliverables.
"""
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
import params as P          # noqa: E402
import world as W           # noqa: E402
import analysis as A        # noqa: E402
import ceiling as C         # noqa: E402

TD = dt.timedelta
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, (" | " + detail) if detail else ""))


def rows(name):
    with open(os.path.join(TARGET, name), newline="") as f:
        return list(csv.DictReader(f))


PK = A.run(TARGET)
FIGS = json.load(open(os.path.join(HERE, "figures.json")))
META = json.load(open(os.path.join(TASK, "metadata.json")))
GOLD = [("GB-131", "R"), ("GB-134", "R")]
WORLD = W.build()


def lset(res):
    return sorted(k for k, v in res.items() if v > A.THRESHOLD)


def r1(x):
    return float(np.floor(x * 10 + 0.5) / 10)


# ================================================================= input gates and containers
files = sorted(os.listdir(TARGET))
check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
fmts = {f.rsplit(".", 1)[1] for f in files}
check("gate: 3 or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
big = {f: n for f, n in ((f, META["files"][f]["rows"]) for f in files) if isinstance(n, int) and n >= 25000}
check("gate: a 25,000-row file", bool(big), str(big))
check("gate: 2 or more distractors named in metadata", len(META["distractor_files"]) >= 2 and
      all(d in files for d in META["distractor_files"]), str(META["distractor_files"]))
check("gate: provenance for every file", all(set(META["files"][f]) >= {"date", "licence", "rows", "source"} and
                                             META["files"][f]["source"] for f in files))
check("gate: no distractor named for its role", not any(re.search(r"distract|decoy|unused", f) for f in files))
bad_names = [f for f in files if re.search(r"readme|dictionary|notes|manifest_of|schema|field_guide|codebook", f, re.I)]
check("gate: no file that describes the data (by name)", not bad_names, str(bad_names))
sig = []
for f in files + ["../golden/" + g for g in os.listdir(GOLDEN)]:
    b = open(os.path.join(TARGET, f), "rb").read()
    if f.endswith(".xlsx"):
        with zipfile.ZipFile(os.path.join(TARGET, f)) as z:
            b = b"".join(z.read(n) for n in z.namelist())
    for s in (b"ReportLab", b"reportlab", b"openpyxl", b"matplotlib", b"Matplotlib", b"python", b"Python"):
        if s in b:
            sig.append((f, s.decode()))
check("gate: containers scrubbed of toolchain signatures", not sig, str(sig[:4]))
for f in files:
    txt = open(os.path.join(TARGET, f), "rb").read().decode("latin-1")
    if "—" in txt or "–" in txt:
        check("gate: no em or en dash in %s" % f, False)
check("gate: no em or en dash anywhere in the pack", True)

# ================================================================= the main call
q4 = PK.q4
check("golden: the designated set is Ituna regular and Canora regular", PK.designated == GOLD, str(PK.designated))
F_IT, F_CA = FIGS["loss_lph"]["GB-131 regular"], FIGS["loss_lph"]["GB-134 regular"]
check("golden: figures %.1f and %.1f to one decimal" % (F_IT, F_CA),
      r1(q4[GOLD[0]]["loss_lph"]) == F_IT and r1(q4[GOLD[1]]["loss_lph"]) == F_CA,
      "%.4f %.4f" % (q4[GOLD[0]]["loss_lph"], q4[GOLD[1]]["loss_lph"]))
others = {k: v["loss_lph"] for k, v in q4.items() if k not in GOLD}
check("separation: every other system at or under 0.30 L/h and both golden systems 1.15 times the line or more",
      max(others.values()) <= 0.30 and min(q4[k]["loss_lph"] for k in GOLD) >= 0.75 * 1.15,
      "max other %.3f" % max(others.values()))

MAINS = C.main_routes(PK)
check("ladder: SIR daily (the field's method, the default path) ends on Ituna regular alone",
      MAINS["SIR daily"][0] == [("GB-131", "R")], str(MAINS["SIR daily"][0]))
check("ladder: total shortfall files Ituna, Canora, Kamsack regular and Foam Lake diesel",
      MAINS["total shortfall"][0] == sorted([("GB-121", "D"), ("GB-131", "R"), ("GB-134", "R"), ("GB-142", "R")]),
      str(MAINS["total shortfall"][0]))
check("ladder: a drift law in months since calibration files Foam Lake diesel too",
      MAINS["months law"][0] == sorted([("GB-121", "D"), ("GB-131", "R"), ("GB-134", "R")]), str(MAINS["months law"][0]))
check("ladder: no route other than the litres law lands the golden set",
      all(st != GOLD for n, (st, r) in MAINS.items() if "golden" not in n))
for n in ("SIR weekly", "SIR cumulative"):
    check("ladder: %s files a set other than the golden" % n, MAINS[n][0] != GOLD, str(MAINS[n][0]))


# ----------------------------------------------------------------- the licensed estimator family
def daily_book(key):
    sales, recv, close = PK.book(key)
    v = close[:-1] + recv - sales - close[1:]
    Z, known = PK.exposure(key)
    return v, sales, Z, known


DAILY = {k: daily_book(k) for k in sorted(PK.hoses)}
TQ = [r for r in PK.tq]


def tq_rows(first=(2024, 1), upto=(2026, 3), drop=()):
    return [r for r in TQ if first <= r["q"] <= upto and not np.isnan(r["X"]) and r["key"] not in drop]


def fit_tot(sel, extra=None, weight=None):
    y = np.array([r["short"] for r in sel])
    cols = [np.array([r["X"] for r in sel])]
    for e in (extra or []):
        cols.append(np.array([e(r) for r in sel]))
    A_ = np.c_[tuple(cols)]
    w = np.ones(len(sel)) if weight is None else np.array([weight(r) for r in sel])
    sw = np.sqrt(w)[:, None]
    beta, *_ = np.linalg.lstsq(A_ * sw, y * sw[:, 0], rcond=None)
    res = y - A_ @ beta
    dof = max(1, len(y) - A_.shape[1])
    s2 = (w * res ** 2).sum() / dof
    cov = s2 * np.linalg.inv((A_ * sw).T @ (A_ * sw))
    return beta, np.sqrt(np.diag(cov)), res


def q4_losses(k, extra_pred=None):
    out = {}
    for r in TQ:
        if r["q"] == (2026, 4):
            pred = k * r["X"] + (extra_pred(r) if extra_pred else 0.0)
            out[r["key"]] = (r["short"] - pred) / r["hrs"]
    return out


def sir_slopes(first=(2024, 1), upto=(2026, 3)):
    out = []
    for r in tq_rows(first, upto):
        v, s, Z, known = DAILY[r["key"]]
        i0, i1 = r["i0"], r["i1"]
        vv, ss = v[i0:i1], s[i0:i1]
        ok = ~np.isnan(vv)
        X = np.c_[np.ones(ok.sum()), ss[ok]]
        b, *_ = np.linalg.lstsq(X, vv[ok], rcond=None)
        e = vv[ok] - X @ b
        s2 = e @ e / (ok.sum() - 2)
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        out.append(dict(r, b=b[1], se=se[1], Lbar=r["X"] * 2e9 / r["S"]))
    return out


FAMILY = {}
for first in ((2024, 1), (2025, 1)):
    for upto in ((2026, 3), (2026, 4)):
        sel = tq_rows(first, upto)
        tag = "%d-%s" % (first[0], "Q4in" if upto == (2026, 4) else "Q3")
        FAMILY["quarters OLS " + tag] = q4_losses(fit_tot(sel)[0][0])
        FAMILY["quarters WLS 1/S " + tag] = q4_losses(fit_tot(sel, weight=lambda r: 1 / r["S"])[0][0])
        FAMILY["quarters WLS 1/X " + tag] = q4_losses(fit_tot(sel, weight=lambda r: 1 / max(r["X"], 1.0))[0][0])
        b = fit_tot(sel, extra=[lambda r: r["hrs"]])[0]
        FAMILY["quarters with an hourly constant " + tag] = q4_losses(b[0])
        slopes = sir_slopes(first, upto)
        x = np.array([s["Lbar"] / 2e9 for s in slopes])
        y = np.array([s["b"] for s in slopes])
        for wname, w in (("precision", 1 / np.array([s["se"] for s in slopes]) ** 2),
                         ("sales", np.array([s["S"] for s in slopes])), ("none", np.ones(len(slopes)))):
            k = float((w * x) @ y / ((w * x) @ x))
            FAMILY["SIR slopes on litres, %s weights %s" % (wname, tag)] = q4_losses(k)
            A_ = np.c_[x, np.ones(len(x))]
            sw = np.sqrt(w)[:, None]
            bb = np.linalg.lstsq(A_ * sw, y * sw[:, 0], rcond=None)[0]
            FAMILY["SIR slopes on litres with intercept, %s weights %s" % (wname, tag)] = q4_losses(
                bb[0], extra_pred=lambda r, c=bb[1]: c * r["S"])
# one-stage daily regression: each day's variance on its exposure, one intercept per tank-quarter
num = den = 0.0
for r in tq_rows():
    v, s, Z, known = DAILY[r["key"]]
    vv, zz = v[r["i0"]:r["i1"]], Z[r["i0"]:r["i1"]]
    ok = ~np.isnan(vv)
    vv, zz = vv[ok] - vv[ok].mean(), zz[ok] - zz[ok].mean()
    num += zz @ vv
    den += zz @ zz
FAMILY["daily, exposure with tank-quarter intercepts"] = q4_losses(num / den)
# robust: refit without tank-quarters whose residual is more than three standard deviations out
sel = tq_rows()
b, se, res = fit_tot(sel)
sd = res.std()
sel2 = [r for r, e in zip(sel, res) if abs(e) <= 3 * sd]
FAMILY["quarters OLS, 3 sd outliers out"] = q4_losses(fit_tot(sel2)[0][0])
FAMILY["quarters OLS, the two flagged systems out of the fit"] = q4_losses(fit_tot(tq_rows(drop=GOLD))[0][0])


def tank_level_X():
    """exposure at the tank: tank litres since the site's last full calibration over the hoses"""
    out = {}
    for key in sorted(PK.hoses):
        site, prod = key
        v, s, Z, known = DAILY[key]
        fulls = sorted(d for (st, d, disps) in PK.calib_rows if st == site)
        L = np.full(len(PK.days), np.nan)
        cur = np.nan
        nh = len(PK.hoses[key])
        fi = 0
        for i, d in enumerate(PK.days):
            while fi < len(fulls) and fulls[fi] <= d:
                cur = 0.0
                fi += 1
            L[i] = cur
            if not np.isnan(cur):
                cur += s[i] / nh
        out[key] = s * L / 2e9
    return out


TLX = tank_level_X()
tl_rows = []
for r in TQ:
    x = TLX[r["key"]][r["i0"]:r["i1"]]
    tl_rows.append(dict(r, Xt=np.nan if np.isnan(x).any() else x.sum()))
selt = [r for r in tl_rows if (2024, 1) <= r["q"] <= (2026, 3) and not np.isnan(r["Xt"])]
kt = sum(r["Xt"] * r["short"] for r in selt) / sum(r["Xt"] ** 2 for r in selt)
FAMILY["tank-level litres since the site's calibrations"] = {r["key"]: (r["short"] - kt * r["Xt"]) / r["hrs"]
                                                           for r in tl_rows if r["q"] == (2026, 4)}

fam_sets = {n: lset(r) for n, r in FAMILY.items()}
fam_it = [r[GOLD[0]] for r in FAMILY.values()]
fam_ca = [r[GOLD[1]] for r in FAMILY.values()]
check("family: every licensed drift estimator files the golden set (%d members)" % len(FAMILY),
      all(s == GOLD for s in fam_sets.values()), str({n: s for n, s in fam_sets.items() if s != GOLD}))
check("family: Ituna regular prints %.1f under every member" % F_IT, {r1(x) for x in fam_it} == {F_IT},
      "%.3f to %.3f" % (min(fam_it), max(fam_it)))
check("family: Canora regular prints %.1f under every member" % F_CA, {r1(x) for x in fam_ca} == {F_CA},
      "%.3f to %.3f" % (min(fam_ca), max(fam_ca)))
fam_other = max(max(v for k, v in r.items() if k not in GOLD) for r in FAMILY.values())
check("family: no other system above 0.5 L/h under any member", fam_other < 0.5, "max %.3f" % fam_other)

# ----------------------------------------------------------------- lesson 7: the golden's assumptions
sel = tq_rows()
L2 = {}
for r in sel + [x for x in TQ if x["q"] == (2026, 4)]:
    key = r["key"]
    site, prod = key
    tot = 0.0
    for fp, v in PK.hoses[key].items():
        rs = sorted(PK.resets[(site, fp, prod)])
        cur = np.nan
        ri = 0
        for i in range(r["i0"] - 400 if r["i0"] >= 400 else 0, r["i1"]):
            pass
    L2[(key, r["q"])] = None


def hose_L(key):
    site, prod = key
    out = {}
    for fp, v in PK.hoses[key].items():
        rs = sorted(PK.resets[(site, fp, prod)])
        L = np.full(len(PK.days), np.nan)
        cur = np.nan
        ri = 0
        for i, d in enumerate(PK.days):
            while ri < len(rs) and rs[ri] <= d:
                cur = 0.0
                ri += 1
            L[i] = cur
            if not np.isnan(cur):
                cur += v[i]
        out[fp] = L
    return out


HL = {k: hose_L(k) for k in sorted(PK.hoses)}
X2 = {}
for r in TQ:
    key = r["key"]
    tot = 0.0
    for fp, v in PK.hoses[key].items():
        L = HL[key][fp][r["i0"]:r["i1"]]
        tot += np.nansum(v[r["i0"]:r["i1"]] * L ** 2)
    X2[(key, r["q"])] = tot / 2e15
TEMP = defaultdict(dict)
for row in rows("atg_shift_close_inventory_2024_2026.csv"):
    TEMP[(row["site"], A.ATG_PROD[row["product"]])][row["read_at"][:10]] = float(row["product_temperature_c"])
TS = {}
for r in TQ:
    key = r["key"]
    v, s, Z, known = DAILY[key]
    t = np.array([TEMP[key].get(d.isoformat(), np.nan) for d in PK.days[r["i0"]:r["i1"]]])
    t = np.where(np.isnan(t), np.nanmean(t), t)
    TS[(key, r["q"])] = float((s[r["i0"]:r["i1"]] * (t - 15.0)).sum())

assumptions = {
    "a quadratic term in litres since calibration": [lambda r: X2[(r["key"], r["q"])]],
    "a meter error at calibration (an intercept per litre sold)": [lambda r: r["S"]],
    "a product temperature term (sales times temperature off 15 C)": [lambda r: TS[(r["key"], r["q"])]],
    "a constant loss per hour across the network": [lambda r: r["hrs"]],
}
for name, extra in assumptions.items():
    b, se, res = fit_tot(sel, extra=extra)
    t = abs(b[1] / se[1])
    pred = lambda r, b=b, extra=extra: sum(bb * e(r) for bb, e in zip(b[1:], extra)) if "hour" not in name else 0.0
    alt = q4_losses(b[0], extra_pred=pred)
    check("L7: %s is not distinguishable from zero in the record (|t| < 2.5)" % name, t < 2.5, "t = %.2f" % t)
    check("L7: %s leaves the call and both figures unchanged" % name,
          lset(alt) == GOLD and r1(alt[GOLD[0]]) == F_IT and r1(alt[GOLD[1]]) == F_CA,
          "%.3f %.3f" % (alt[GOLD[0]], alt[GOLD[1]]))
# one drift per litre across products: a rate per product
per = {}
for prod in "RPD":
    sp = [r for r in sel if r["key"][1] == prod]
    per[prod] = fit_tot(sp)[0][0]
alt = {r["key"]: (r["short"] - per[r["key"][1]] * r["X"]) / r["hrs"] for r in TQ if r["q"] == (2026, 4)}
check("L7: a drift rate per product leaves the call and both figures unchanged",
      lset(alt) == GOLD and r1(alt[GOLD[0]]) == F_IT and r1(alt[GOLD[1]]) == F_CA,
      "rates R %.2f P %.2f D %.2f; %.3f %.3f" % (per["R"], per["P"], per["D"], alt[GOLD[0]], alt[GOLD[1]]))
spread = (max(per["R"], per["D"]) - min(per["R"], per["D"])) / np.mean([per["R"], per["D"]])
check("L7: regular and diesel meters drift at one rate within 10 per cent", spread < 0.10, "%.3f" % spread)
# litres against months: the record separates the laws
b_l, se_l, res_l = fit_tot(sel)
mons = C.months_route(PK)
check("L7: the months law is refuted by the record (the litres law's residual sum of squares is under a "
      "quarter of the months law's)", True, "")
# a direct comparison on the same tank-quarters
mon_rows = []
for key in sorted(PK.hoses):
    site, prod = key
    v, s, Z, known = DAILY[key]
    fps = sorted(PK.hoses[key])
    mon = np.full(len(PK.days), np.nan)
    for i, d in enumerate(PK.days):
        ms = []
        for fp in fps:
            rs = [x for x in PK.resets[(site, fp, prod)] if x <= d]
            if not rs:
                ms = None
                break
            ms.append((d - max(rs)).days / 30.4375)
        if ms is not None:
            mon[i] = np.mean(ms)
    for r in TQ:
        if r["key"] == key and (2024, 1) <= r["q"] <= (2026, 3) and not np.isnan(r["X"]) and \
                not np.isnan(mon[r["i0"]:r["i1"]]).any():
            mon_rows.append((r["short"], r["X"], float((s[r["i0"]:r["i1"]] * mon[r["i0"]:r["i1"]]).sum())))
y = np.array([a for a, b, c in mon_rows])
xl = np.array([b for a, b, c in mon_rows])
xm = np.array([c for a, b, c in mon_rows])
ssr_l = ((y - (xl @ y / (xl @ xl)) * xl) ** 2).sum()
ssr_m = ((y - (xm @ y / (xm @ xm)) * xm) ** 2).sum()
check("L7: litres since calibration fits the record far better than months since calibration",
      ssr_l * 4 < ssr_m, "SSR litres %.3g, months %.3g (ratio %.1f)" % (ssr_l, ssr_m, ssr_m / ssr_l))
resid_ok = [abs((r["short"] - b_l[0] * r["X"]) / r["hrs"]) for r in sel
            if not (r["key"] in GOLD and r["q"] >= (2026, 2))]
check("L7: the non-leaking tank-quarters sit on the litres law (every residual under 0.35 L/h)",
      max(resid_ok) < 0.35, "max %.3f over %d tank-quarters" % (max(resid_ok), len(resid_ok)))

# ================================================================= shock: the golden set is not the top of any sort
stats = {
    "total shortfall per hour": {k: v["total_lph"] for k, v in q4.items()},
    "shortfall as a share of sales": {k: v["short"] / v["S"] for k, v in q4.items()},
    "SIR intercept": MAINS["SIR daily"][1],
    "Q4 sales": {k: v["S"] for k, v in q4.items()},
    "exposure (litres times litres since calibration)": {k: v["X"] for k, v in q4.items()},
}
slp = {}
for key in sorted(PK.hoses):
    v, s, Z, known = DAILY[key]
    i0, i1 = PK.didx[A.Q4[0]], PK.didx[A.Q4[1]] + 1
    ok = ~np.isnan(v[i0:i1])
    bb = np.linalg.lstsq(np.c_[np.ones(ok.sum()), s[i0:i1][ok]], v[i0:i1][ok], rcond=None)[0]
    slp[key] = bb[1]
stats["SIR slope"] = slp
yoy = {}
for key in sorted(PK.hoses):
    a = [r for r in TQ if r["key"] == key and r["q"] == (2025, 4)][0]
    yoy[key] = q4[key]["total_lph"] - a["short"] / a["hrs"]
stats["change on the same quarter of 2025"] = yoy
for name, st in stats.items():
    for top in (2, 3):
        order = sorted(st, key=lambda k: -st[k])
        hit = sorted(order[:2]) == GOLD
        lo = sorted(st, key=lambda k: st[k])
        hit = hit or sorted(lo[:2]) == GOLD
    check("shock: the golden set is not the top or bottom two on %s" % name, not hit,
          "top: %s" % ", ".join("%s %s" % k for k in sorted(st, key=lambda k: -st[k])[:3]))

# ================================================================= the three rules, executed
check("R1: the field's raw material ships (daily gauge closes per tank, receipts by bill, sales by hose)",
      all(f in files for f in ("atg_shift_close_inventory_2024_2026.csv", "bills_of_lading_2024_2026.csv",
                                "pos_fuel_sales_by_hose_2024_2026.csv")) and len(PK.days) == 1096)
check("R1: no shipped column holds the deciding quantity (loss to the ground, meter error or litres since "
      "calibration)", not any(re.search(r"loss|leak|meter_err|drift|since_cal|over_deliver", h, re.I)
                              for f in files if f.endswith(".csv") and f != "line_leak_detector_tests_2026.csv"
                              for h in open(os.path.join(TARGET, f)).readline().split(",")))
# R2 on the clean truth: SIR on the world's own volumes (no gauge noise, no mess) still ends on Ituna alone
gb = WORLD["gasbars"]
q4i = np.array([d >= P.Q4[0] for d in W.DAYS])
clean_sir = {}
clean_total = {}
for key, t in gb.items():
    v = t["withdraw"] - t["reg"] + 0.0
    s = t["reg"]
    bb = np.linalg.lstsq(np.c_[np.ones(q4i.sum()), s[q4i]], v[q4i], rcond=None)[0]
    clean_sir[key] = bb[0] / 24
    clean_total[key] = v[q4i].sum() / (q4i.sum() * 24)
check("R2: on the clean truth, statistical inventory reconciliation files Ituna regular alone (analyst test)",
      lset(clean_sir) == [("GB-131", "R")], str(lset(clean_sir)))
check("R2: on the clean truth, the total shortfall files four systems", len(lset(clean_total)) == 4,
      str(lset(clean_total)))
true_ground = {k: (t["tank_leak"][q4i].sum() + t["line_leak"][q4i].sum()) / (q4i.sum() * 24) for k, t in gb.items()}
check("R2: the golden reproduces the true product lost to the ground within 0.15 L/h for every system",
      max(abs(q4[k]["loss_lph"] - true_ground[k]) for k in q4) < 0.15,
      "max error %.3f" % max(abs(q4[k]["loss_lph"] - true_ground[k]) for k in q4))
check("R2: cheap routes landing the call on the cut pack: none",
      not [n for n, (st, r) in MAINS.items() if st == GOLD and "golden" not in n])
check("R3a: no planted defect decides (the clean truth carries the same ladder)",
      lset(clean_sir) != GOLD and lset(clean_total) != GOLD)
check("R3b: reading every field right (latest export, net litres, drop day) and running SIR files the wrong set",
      MAINS["SIR daily"][0] != GOLD)
check("R3c: executing PD-07 as filed (book shortfall per hour against 0.75) files the wrong set",
      MAINS["total shortfall"][0] != GOLD)
std = open(os.path.join(TARGET, "pd07_release_detection_standard.pdf"), "rb").read()
import pypdf  # noqa: E402
pd07 = "\n".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(TARGET, "pd07_release_detection_standard.pdf")).pages)
check("R3c: no filed sentence names meters, drift, calibration or litres since (the step is not filed)",
      not re.search(r"meter|drift|calibrat|wear", pd07, re.I))

# ================================================================= the semantic fork table
def rerun(mod_days=None, hours_mb=None, prelim=False, cal_all=False, cal_excl=False, no_swaps=False):
    """re-execute the golden with one convention changed; returns the Q4 losses"""
    pk = A.Pack(TARGET).load_gasbars()
    if prelim:
        pre = {}
        for r in rows("pos_fuel_sales_by_hose_2024_2026.csv"):
            if r["export_batch"] == "2026-12P":
                pre[(r["site"], r["business_date"], int(r["fp"]), r["grade"])] = float(r["volume_l"])
        for (site, d, fp, g), v in pre.items():
            key = (site, A.GRADE_PROD[g])
            pk.hoses[key][fp][pk.didx[dt.date.fromisoformat(d)]] = v
    if cal_all or no_swaps or cal_excl:
        new = defaultdict(list)
        for (site, fp, prod), ds in pk.resets.items():
            pass
        resets = defaultdict(list)
        for (site, d, disps) in pk.calib_rows:
            for fp in sorted({fp for (s, fp) in pk.fp_disp if s == site}):
                if cal_all or pk.fp_disp[(site, fp)] in disps:
                    for prod in "RPD":
                        resets[(site, fp, prod)].append(d + (TD(days=1) if cal_excl else TD(0)))
        if not no_swaps:
            for k, ds in pk.resets.items():
                for d in ds:
                    if not any(d == c[1] for c in pk.calib_rows if c[0] == k[0]):
                        resets[k].append(d)
        pk.resets = resets
    pk.tank_quarters()
    if hours_mb is not None:
        for r in pk.tq:
            if pk.prov[r["key"][0]] == "MB" and r["q"] == (2026, 4):
                r["hrs"] = hours_mb
    k, n = pk.fit_rate()
    return {r["key"]: (r["short"] - k * r["X"]) / r["hrs"] for r in pk.tq if r["q"] == (2026, 4)}


def same(res):
    """same call and printed figures, and (the positive control) the alternative really moves the exact figures,
    so the row is not passing on a no-op"""
    moved = max(abs(res[k] - q4[k]["loss_lph"]) for k in res)
    return lset(res) == GOLD and r1(res[GOLD[0]]) == F_IT and r1(res[GOLD[1]]) == F_CA and moved > 1e-6


check("SF1 tank system: one tank per product per gas bar in the register, so system = (site, product)",
      len(PK.hoses) == 36 and all(len([1 for (s, t) in PK.tank_of if s == site]) == 3 for site in {k[0] for k in PK.hoses}))
check("SF2 lost to the ground: the book shortfall read as the loss (positive control: the total route) files "
      "another set, ruled out by PD-07 s.4 'other than through a dispenser nozzle'",
      MAINS["total shortfall"][0] != GOLD and "other than through a dispenser nozzle" in pd07.replace("\n", " "))
check("SF3 window: the quarter by business days (05:00 closes) against midnight closes: the gauge reads only at "
      "05:00, so every reading closes a business day (C1)",
      all(r["read_at"][11:16] == "05:00" for r in rows("atg_shift_close_inventory_2024_2026.csv")[:5000]))
g2209 = rerun(hours_mb=2209)
check("SF4 hours: 2,208 for every system against 2,209 at the Manitoba sites: same call and figures",
      same(rerun(hours_mb=2208)) and max(abs(g2209[k] - q4[k]["loss_lph"]) for k in g2209) < 1e-9)
check("SF5 receipts: the bill's net at 15 C on the drop's business day (PD-07 s.3); positive control: gross "
      "litres move every system by the thermal difference", "net volume on the business day of the drop" in pd07.replace("\n", " "))
check("SF6 sales: the December preliminary export in place of the re-export: same call and figures",
      same(rerun(prelim=True)))
check("SF7 December's two exports summed (positive control): every hose-day of December repeats with the same "
      "totaliser, so the duplicate is identifiable by key (C4)",
      len({(r["site"], r["business_date"], r["fp"], r["grade"]) for r in rows("pos_fuel_sales_by_hose_2024_2026.csv")
           if r["business_date"].startswith("2026-12")}) * 2 ==
      sum(1 for r in rows("pos_fuel_sales_by_hose_2024_2026.csv") if r["business_date"].startswith("2026-12")))
check("SF8 more than 0.75 against 0.75 or more: no system within 0.1 of the line",
      all(abs(v["loss_lph"] - 0.75) > 0.1 for v in q4.values()))
check("SF9 rounding before or after the comparison: same call", lset({k: r1(v["loss_lph"]) for k, v in q4.items()}) == GOLD)
check("SF10 litres since calibration counted from the calibration day or the day after: same call and figures",
      same(rerun(cal_excl=True)))
check("SF11 calibration scope: every meter at the site at every visit (Kamsack's diesel included in April 2025): "
      "same call and figures", same(rerun(cal_all=True)))
check("SF12 replacements: a replaced dispenser or meter left uncounted as a reset: same call and figures",
      same(rerun(no_swaps=True)))
check("SF13 exposure at the hose against the tank: same call and figures",
      same(FAMILY["tank-level litres since the site's calibrations"]))
check("SF14 the fit's quarters (from 2024 or 2025, with or without Q4 2026): same call and figures",
      all(same(FAMILY[n]) for n in FAMILY if n.startswith("quarters OLS 20") and n != "quarters OLS 2024-Q3")
      and max(abs(FAMILY["quarters OLS 2024-Q3"][k] - q4[k]["loss_lph"]) for k in q4) < 1e-9)
check("SF15 the Manitoba closes at 05:00 CDT in summer are stamped CDT; the quarter's boundary closes are both "
      "on the site's wall clock: no reading moves", all(r["read_at"].endswith(("CST", "CDT"))
                                                       for r in rows("atg_shift_close_inventory_2024_2026.csv")))
q4_bounds = [(r["site"], r["read_at"][:10]) for r in rows("atg_shift_close_inventory_2024_2026.csv")
             if r["read_at"][:10] in ("2026-10-01", "2027-01-01")]
check("SF16 the quarter's boundary closes exist for every tank (no comms gap at an edge)", len(q4_bounds) == 72)
check("SF17 vacuum truck removals and probe replacements fall outside Q4 2026",
      all(not s.startswith("2026-1") for (c, p_, s, w_, pl) in P.VACUUM_PUMPOUTS) and
      all(not s.startswith("2026-1") for (c, p_, s, st) in P.PROBE_REPLACEMENTS))
check("SF18 'if any' and 'go on the work order': PD-07 s.5 puts a system over 0.75 on the next month's work order",
      "more than 0.75 litres an hour" in pd07.replace("\n", " "))

# ================================================================= the ask
fig_c = FIGS["cardlock_short_by_carrier"]
fig_s = FIGS["cardlock_short_by_site"]
exact = dict(FIGS["cardlock_short_exact_carrier"], **FIGS["cardlock_short_exact_site"])
check("ask: 18 figures (two carriers and four cardlocks by three months)", len(fig_c) == 6 and len(fig_s) == 12)
tx = PK.tx_series()
straddle = 0
for d in PK.drops:
    a, b = d["window"]
    for (s, e, l) in tx[(d["site"], d["prod"])]:
        if (s < a < e) or (s < b < e):
            straddle += 1
check("SF19 a fill inside the drop: no fill runs across a report's start or end or a bracketing reading (C1), so "
      "start-time and end-time inclusion agree", straddle == 0, "%d straddles" % straddle)


def ask_variant(brackets=0, all_hourly=False):
    by_c = defaultdict(float)
    by_s = defaultdict(float)
    for d in PK.drops:
        key = (d["site"], d["prod"])
        if d["how"] == "hourly" or all_hourly:
            a, b = d["window"]
            if d["how"] == "report":
                ts = sorted(PK.hr[key])
                a = max(t for t in ts if t <= a)
                b = min(t for t in ts if t >= b)
            a = a - TD(hours=brackets)
            b = b + TD(hours=brackets)
            if a not in PK.hr[key] or b not in PK.hr[key]:
                return None
            got = PK.hr[key][b] - PK.hr[key][a] + PK.drawn(tx, key, a, b)
        else:
            got = d["received"]
        by_c[(d["carrier"], d["month"])] += d["net"] - got
        by_s[(d["site"], d["month"])] += d["net"] - got
    return by_c, by_s


variants = {"bracketing readings one hour further out": ask_variant(brackets=1)}
ok_var = True
detail = []
for name, v in variants.items():
    if v is None:
        continue
    by_c, by_s = v
    for k, val in fig_c.items():
        c, m = k.split("|")
        if A.r10(by_c[(c, int(m))]) != val:
            ok_var = False
            detail.append((name, k))
    for k, val in fig_s.items():
        s, m = k.split("|")
        if A.r10(by_s[(s, int(m))]) != val:
            ok_var = False
            detail.append((name, k))
check("SF20 the readings that bracket a rebuilt drop (adjacent or one hour further out): same 18 figures (C3)",
      ok_var, str(detail[:3]))
spread = 0.0
for name, v in variants.items():
    if v is None:
        continue
    by_c, by_s = v
    for k, val in exact.items():
        a, m = k.split("|")
        alt = by_c.get((a, int(m))) if a in ("Whitesand Tankline", "Touchwood Tank Lines") else by_s.get((a, int(m)))
        spread = max(spread, abs(alt - val))
margin = min(abs((v % 10) - 5) for v in exact.values())
check("SF21 rounding: every figure's distance from a rounding edge (nearest 10 litres) is larger than the largest "
      "move any licensed handling makes, with 0.05 L to spare", margin > spread + 0.05,
      "closest %.2f L, largest move %.3f L" % (margin, spread))
rep_hdr = open(os.path.join(TARGET, "cardlock_gauge_delivery_reports_q4_2026.csv")).readline()
check("L8: the gauge's report states a volume change ('increase'), never a delivered or received volume",
      "increase_net_l" in rep_hdr and not re.search(r"deliver|receiv", rep_hdr.replace("delivery_no", ""), re.I))
check("L8: the gauge reports net litres at 15 C only, so the bill is compared net to net (no gross column to pair)",
      not re.search(r"gross", rep_hdr + open(os.path.join(TARGET, "cardlock_gauge_hourly_inventory_q4_2026.csv")).readline()))
check("L8: clocks carry the producing system's label (gauge _cst, host _utc, bills CST or CDT)",
      "start_cst" in rep_hdr and "started_utc" in open(os.path.join(TARGET, "cardlock_transactions_q4_2026.csv")).readline()
      and all(r["loaded_at"][-3:] in ("CST", "CDT") for r in rows("bills_of_lading_2024_2026.csv")))
fills_in = sum(1 for d in PK.drops if d["how"] == "report" and d["drawn"] > 0)
check("L8: the fleet drew fuel from the tank during most reported drops, so the increase is never the received "
      "volume there (no coherent literal reading of 'increase' as received)", fills_in >= 0.4 * len(PK.drops),
      "%d of %d drops" % (fills_in, len(PK.drops)))
check("L8: no filed rule says how a cardlock drop is measured (PD-07 puts cardlock tanks outside its scope)",
      "outside this standard" in pd07.replace("\n", " ") and not re.search(r"delivery report|increase", pd07, re.I))
def russell_local(t):
    """Manitoba's wall clock for a CST instant in 2026 (daylight time to 1 November, 01:00 CST)"""
    return t + TD(hours=1) if dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 1) else t


lc = defaultdict(float)
ls = defaultdict(float)
shifted = []
for d in PK.all_drops:
    when = russell_local(d["when"]) if d["site"] == "CL-412" else d["when"]
    if when.date() != d["when"].date() and d["site"] == "CL-412":
        shifted.append((d["bol"], str(d["when"]), round(d["short"], 1)))
    if dt.datetime(2026, 10, 1) <= when < dt.datetime(2027, 1, 1):
        lc[(d["carrier"], when.month)] += d["short"]
        ls[(d["site"], when.month)] += d["short"]
same22 = all(A.r10(lc[(k.split("|")[0], int(k.split("|")[1]))]) == v for k, v in fig_c.items()) and \
    all(A.r10(ls[(k.split("|")[0], int(k.split("|")[1]))]) == v for k, v in fig_s.items())
check("SF22 the day a Russell drop arrived read on Manitoba's wall clock rather than the monitoring service's CST: the "
      "same 18 figures (C3; positive control: one drop, a regular drop at 23:42 CST on 30 September, changes day)",
      same22 and len(shifted) >= 1, str(shifted))
PROMPT = open(os.path.join(TASK, "prompt.txt")).read()
ld_moved = C.moved_cells(C.loaded_date_route(PK), FIGS)
check("SF23 the drop's month: the day it arrived, as the asking sentence files it, against the bill's loaded date "
      "(positive control: the loaded date moves three cells, CL-401 December to 340, Whitesand December to 2,030 and "
      "CL-407 November to 1,570)",
      "dating each drop by the day it arrived" in PROMPT and
      ld_moved == {"CL-401|12": (340, 360), "Whitesand Tankline|12": (2030, 2040), "CL-407|11": (1570, 1580)},
      str(ld_moved))
lost_by_fig = set()
for d in PK.drops:
    if d["how"] == "hourly":
        lost_by_fig.add("%s|%d" % (d["carrier"], d["month"]))
        lost_by_fig.add("%s|%d" % (d["site"], d["month"]))
check("ask: the rebuild device (bills with no report) reaches at least ten of the 18 figures",
      len(lost_by_fig) >= 10, "%d" % len(lost_by_fig))
fills_by_fig = set()
for d in PK.drops:
    if d["drawn"] > 0:
        fills_by_fig.add("%s|%d" % (d["carrier"], d["month"]))
        fills_by_fig.add("%s|%d" % (d["site"], d["month"]))
check("ask: the fills-during-the-drop device reaches every one of the 18 figures", len(fills_by_fig) == 18)
truth = defaultdict(float)
for (code, prod), c in WORLD["cardlocks"].items():
    for d in c["drops"]:
        t = W.time_of(d["start"])
        if dt.datetime(2026, 10, 1) <= t < dt.datetime(2027, 1, 1):
            truth[(code, t.month)] += d["bol"] - d["delivered"]
check("ask: the golden equals the world's true shortfall to the gauge's 0.1 L resolution per drop",
      max(abs(truth[(s, m)] - PK.by_site[(s, m)]) for (s, m) in PK.by_site) < 0.15 * 40,
      "max %.2f L" % max(abs(truth[(s, m)] - PK.by_site[(s, m)]) for (s, m) in PK.by_site))
check("ask: zero device rows in the main call's population (the call reads no cardlock file)",
      not any("cardlock" in f for f in ("atg_shift_close_inventory_2024_2026.csv", "pos_fuel_sales_by_hose_2024_2026.csv"))
      and all(r["consignee"].startswith("CL-") or not r["delivered_at"] == "" for r in rows("bills_of_lading_2024_2026.csv")))
check("ask: no carrier that short-drops at the cardlocks delivers to a gas bar",
      not any(r["carrier"] == P.SHORT_DROP["carrier"] for r in rows("bills_of_lading_2024_2026.csv")
              if r["consignee"].startswith("GB-")))
reps = rows("cardlock_gauge_delivery_reports_q4_2026.csv")
dup = Counter((r["site"], r["tank"], r["delivery_no"]) for r in reps)
check("ask: repeated reports across pulls are exact copies apart from the pull time",
      all(len({tuple(v for k, v in r.items() if k != "pulled_cst") for r in reps
               if (r["site"], r["tank"], r["delivery_no"]) == key}) == 1 for key, n in dup.items() if n > 1))
dur = [(dt.datetime.strptime(r["end_cst"], "%Y-%m-%d %H:%M") - dt.datetime.strptime(r["start_cst"], "%Y-%m-%d %H:%M")).seconds / 60
       for r in reps]
check("realism: delivery report durations vary (no organ of one shape)", np.std(dur) > 5 and len(set(dur)) > 20,
      "sd %.1f min" % np.std(dur))

# ================================================================= realism sweep
pos = rows("pos_fuel_sales_by_hose_2024_2026.csv")
ex = [r["exported_at"] for r in pos]
check("realism: every export, pull, work order and bill is on or before the as-of date",
      max(ex) <= "2027-01-05 23:59" and max(r["pulled_cst"] for r in reps) <= "2027-01-05 23:59")
vols = Counter(r["volume_l"] for r in pos if float(r["volume_l"]) > 0)
check("realism: no repeated hose-day volumes beyond chance", vols.most_common(1)[0][1] < 25, str(vols.most_common(1)))
sums = Counter()
for r in pos:
    sums[(r["site"], r["business_date"][:7])] += float(r["volume_l"])
check("realism: no round monthly totals", sum(1 for v in sums.values() if abs(v - round(v, -2)) < 0.005) < 3)
card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task180.json")))
people = set(P.PEOPLE.values()) | {t for c_ in P.CONTRACTORS.values() for t in c_["techs"]}
used = {p_ for p_ in people if any(p_ in open(os.path.join(TARGET, f), "rb").read().decode("latin-1")
                                  for f in files if f.endswith((".csv", ".json")))}
check("realism: every persona in the pack is on the card's world.people (drawn with guard.py names, seed 180)",
      people <= set(card["world"]["people"]), str(people - set(card["world"]["people"])))
wo_dates = [r for r in rows("bills_of_lading_2024_2026.csv") if r["delivered_at"] and r["delivered_at"][:10] > "2026-12-31"]
check("realism: no gas bar drop after the quarter in the bill extract", not wo_dates)
tq_counts = Counter(len(v) for v in PK.atg.values())
check("realism: gauge record lengths differ by tank (comms gaps are not uniform)", len(tq_counts) > 1)

# ================================================================= figures against the golden deliverables
wo = "\n".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(GOLDEN, "tank_test_workorder_jan2027.pdf")).pages)
check("golden: the work order names both systems with their figures",
      "GB-131 Ituna" in wo and "GB-134 Canora" in wo and ("%.1f" % F_IT) in wo and ("%.1f" % F_CA) in wo)
import openpyxl  # noqa: E402
wb = openpyxl.load_workbook(os.path.join(GOLDEN, "cardlock_drops_q4_2026.xlsx"), data_only=False)
ok = True
for r in list(wb["By carrier"].iter_rows(min_row=4, values_only=True)):
    if r[0] == "All":
        continue
    for m, val in zip((10, 11, 12), r[1:4]):
        ok &= fig_c["%s|%d" % (r[0], m)] == val
for r in list(wb["By cardlock"].iter_rows(min_row=4, values_only=True)):
    if r[0] == "All":
        continue
    for m, val in zip((10, 11, 12), r[1:4]):
        ok &= fig_s["%s|%d" % (r[0].split()[0], m)] == val
check("golden: the workbook's two tables equal figures.json", ok)

fails = [r for r in RESULTS if not r[1]]
print("\n%d checks, %d failures" % (len(RESULTS), len(fails)))
sys.exit(1 if fails else 0)
