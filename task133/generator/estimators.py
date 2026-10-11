"""Every graded figure and every rung of task133, from the shipped files alone."""
import datetime as dt
import math
import os
import re

import openpyxl
import pandas as pd
from pypdf import PdfReader

F = dict(book="personal_loan_book_2026-09-30.csv", curve="pd_curve_personal_loans_2026-06.csv",
         hardship="hardship_register_2026-09-30.xlsx", scen="ifrs9_scenarios_2026Q3.xlsx",
         note="scorecard_v4_migration_note.pdf")
REPORT = dt.date(2026, 9, 30)
SCEN_SHEET = "Q1 FY27 scenarios"
LGD = {"PL36": 0.70, "PL60": 0.76}
STAGE2_SCALAR = 2.4


def _d(x):
    return dt.date.fromisoformat(str(x)[:10])


def months_due(first_rep, report=REPORT):
    if first_rep > report:
        return 0
    n = (report.year - first_rep.year) * 12 + (report.month - first_rep.month)
    if report.day >= first_rep.day:
        n += 1
    return n


BANDS = [(0, 6, "0-6"), (7, 12, "7-12"), (13, 24, "13-24"), (25, 36, "25-36"), (37, 59, "37-59")]


def band_of(m):
    for lo, hi, lab in BANDS:
        if lo <= m <= hi:
            return lab
    raise ValueError(m)


def load(target):
    bk = pd.read_csv(os.path.join(target, F["book"]))
    bk["first_rep"] = bk["first_repayment_date"].map(_d)
    cv = pd.read_csv(os.path.join(target, F["curve"]), comment="#")
    curves = {p: g.sort_values("month_on_book")["cumulative_pd"].tolist() for p, g in cv.groupby("product")}
    hd = pd.read_excel(os.path.join(target, F["hardship"]), sheet_name=0)
    wb = openpyxl.load_workbook(os.path.join(target, F["scen"]), data_only=True)
    ws = wb[SCEN_SHEET]
    scen = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if not r or r[0] is None:
            break
        scen.append((r[0], float(r[1]), float(r[2])))
    text = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, F["note"])).pages)
    m = re.search(r"v4 = ([0-9.]+) x v3 - ([0-9.]+)", text)
    mapping = (float(m.group(1)), -float(m.group(2)))
    return bk, curves, hd, scen, mapping


def stage(bk, hd, mapping, use_hardship=True, map_v3=True):
    a, b = mapping
    live = hd[hd["arrangement_status"] != "Cancelled"].copy()
    live["s"] = live["arrangement_start"].map(_d)
    live["e"] = live["arrangement_end"].map(_d)
    inforce = set(live[(live["s"] <= REPORT) & (live["e"] >= REPORT)]["loan_no"])
    o = bk["origination_score"].astype(float)
    if map_v3:
        o = [int(math.floor(a * v + b + 0.5)) if c == "v3" else int(v) for v, c in zip(o, bk["origination_scorecard"])]
    drop = pd.Series(o, index=bk.index) - bk["current_score_v4"]
    st = pd.Series(1, index=bk.index)
    st[(bk["days_past_due"] >= 30) | (drop >= 60)] = 2
    if use_hardship:
        st[bk["loan_no"].isin(inforce)] = 2
    st[bk["days_past_due"] >= 90] = 3
    return st


def ead_path(balance, rate, rem):
    """balance at the start of each month k = 1..rem, re-amortising the current balance over rem months"""
    i = rate / 12.0
    if rem <= 0:
        return []
    p = balance * i / (1 - (1 + i) ** -rem)
    out, b = [], balance
    for _ in range(rem):
        out.append(b)
        b = b * (1 + i) - p
    return out


def loan_ecl(row, st, curves, mult, variant="cond", disc=True, flat_ead=False, by_month=None, pm_zero=False):
    a = months_due(row["first_rep"])
    T = int(row["term_months"])
    rem = T - a
    if rem <= 0:
        # past its contractual maturity and not in stage 3: one month remaining (CRM-ECL-04 3.2), so the loan stands
        # at the month on book that leaves one month of its term, the last month of its product's curve
        if pm_zero:
            return 0.0
        a, rem = T - 1, 1
    H = rem if st == 2 else min(12, rem)
    C = curves[row["product"]]
    r = float(row["contract_rate"])
    eads = ead_path(float(row["current_balance"]), r, rem)
    sa = 1.0 - C[a]
    tot = 0.0
    for k in range(1, H + 1):
        if variant == "cond":
            mp = (C[a + k] - C[a + k - 1]) / sa
        elif variant == "shift":
            mp = C[a + k] - C[a + k - 1]
        else:
            mp = C[k] - C[k - 1]
        ead = float(row["current_balance"]) if flat_ead else eads[k - 1]
        df = (1 + r / 12.0) ** (-k) if disc else 1.0
        e = mp * (STAGE2_SCALAR if st == 2 else 1.0) * mult * LGD[row["product"]] * ead * df
        tot += e
        if by_month is not None:
            by_month[k] = by_month.get(k, 0.0) + e
    return tot


def solve(target, **kw):
    bk, curves, hd, scen, mapping = load(target)
    st = stage(bk, hd, mapping, kw.get("use_hardship", True), kw.get("map_v3", True))
    mult = sum(w * m for _, w, m in scen)
    variant = kw.get("variant", "cond")
    disc = kw.get("disc", True)
    flat = kw.get("flat_ead", False)
    by_month = {}
    ecl = []
    for idx, row in bk.iterrows():
        s = int(st[idx])
        ecl.append(0.0 if s == 3 else loan_ecl(row, s, curves, mult, variant, disc, flat, by_month, kw.get("pm_zero", False)))
    mob = [months_due(f) for f in bk["first_rep"]]
    bk = bk.assign(stage=st.values, ecl=ecl, mob=mob,
                   band=[str(d)[:4] if str(d)[:4] >= "2024" else "2023 and earlier" for d in bk["drawdown_date"]])
    inb = bk[bk["stage"] < 3]
    out = dict(total=float(inb["ecl"].sum()), mult=mult, loans=inb[["loan_no", "product", "stage", "band", "current_balance", "ecl"]].copy())
    out["by_band"] = {(p, b): float(g["ecl"].sum()) for (p, b), g in inb.groupby(["product", "band"])}
    for s in (1, 2):
        g = inb[inb["stage"] == s]
        out["stage%d" % s] = float(g["ecl"].sum())
        out["n%d" % s] = int(len(g))
        out["gca%d" % s] = float(g["current_balance"].sum())
        for p in ("PL36", "PL60"):
            gp = g[g["product"] == p]
            out["%s_s%d" % (p, s)] = float(gp["ecl"].sum())
            out["%s_s%d_gca" % (p, s)] = float(gp["current_balance"].sum())
            out["%s_s%d_cov" % (p, s)] = 100.0 * float(gp["ecl"].sum()) / float(gp["current_balance"].sum())
    # by calendar period of the default month: October to December 2026, then calendar years
    per = {}
    for k, v in by_month.items():
        y = 2026 + (9 + k - 1) // 12          # month k after September 2026
        per[y] = per.get(y, 0.0) + v
    out["by_year"] = dict(sorted(per.items()))
    out["n3"] = int((bk["stage"] == 3).sum())
    pm = (bk["mob"] >= bk["term_months"]) & (bk["stage"] < 3)
    out["n_pm"] = int(pm.sum())
    out["ecl_pm"] = float(bk.loc[pm, "ecl"].sum())
    return out
