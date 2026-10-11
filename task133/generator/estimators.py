"""Every graded figure of task133, every rung of the main ladder and every stop on the two ask ladders, read from the
shipped files alone."""
import datetime as dt
import math
import os
import re

import numpy as np
import openpyxl
import pandas as pd
from pypdf import PdfReader

F = dict(book="personal_loan_book_2026-09-30.csv", june="personal_loan_book_2026-06-30.csv",
         curve="pd_curve_personal_loans_2026-06.csv", dev="pd_model_development_sample.parquet",
         hardship="hardship_register_2026-09-30.xlsx", scen="ifrs9_scenarios_2026Q3.xlsx",
         note="scorecard_v4_migration_note.pdf", scores="behaviour_score_runs_2026-03_2026-08.parquet",
         defaults="collections_defaults_2023-24.csv", receipts="collections_receipts_2023-07_2026-09.csv",
         sale="debt_sale_2026-03_schedule.xlsx")
REPORT = dt.date(2026, 9, 30)
PRIOR = dt.date(2026, 6, 30)
SCEN_SHEET = "Q1 FY27 scenarios"
LGD = {"PL36": 0.70, "PL60": 0.76}
STAGE2_SCALAR = 2.4
QUARTERS = {1: "Jul to Sep 2023", 2: "Oct to Dec 2023", 3: "Jan to Mar 2024", 4: "Apr to Jun 2024"}


def _d(x):
    return dt.date.fromisoformat(str(x)[:10])


def months_due(first_rep, report=REPORT):
    if first_rep > report:
        return 0
    n = (report.year - first_rep.year) * 12 + (report.month - first_rep.month)
    if report.day >= first_rep.day:
        n += 1
    return n


# ------------------------------------------------------------------------------------------------- shared reads

def load_staging(target):
    """what staging needs: the September book, the hardship register and the v3 to v4 conversion"""
    bk = pd.read_csv(os.path.join(target, F["book"]))
    bk["first_rep"] = bk["first_repayment_date"].map(_d)
    hd = pd.read_excel(os.path.join(target, F["hardship"]), sheet_name=0)
    text = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, F["note"])).pages)
    m = re.search(r"v4 = ([0-9.]+) x v3 - ([0-9.]+)", text)
    return bk, hd, (float(m.group(1)), -float(m.group(2)))


def load(target):
    bk = pd.read_csv(os.path.join(target, F["book"]))
    bk["first_rep"] = bk["first_repayment_date"].map(_d)
    cv = pd.read_csv(os.path.join(target, F["curve"]), comment="#")
    curves = {p: g.sort_values("month_on_book")["cumulative_pd"].to_numpy() for p, g in cv.groupby("product")}
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


def sample_shares(target):
    """from the development sample: for each product, the share of its loans that had defaulted (D) and the share
    repaid in full, early or at term, without defaulting (Cl) by the end of each month on book"""
    dev = pd.read_parquet(os.path.join(target, F["dev"]))
    out = {}
    for p, g in dev.groupby("product"):
        T = int(g["term_months"].iloc[0])
        n = len(g)
        grid = np.arange(T + 1)
        dm = np.sort(g.loc[g["outcome"] == "default", "outcome_month_on_book"].to_numpy())
        cm = np.sort(g.loc[g["outcome"].isin(["prepaid", "matured"]), "outcome_month_on_book"].to_numpy())
        early = np.sort(g.loc[g["outcome"] == "prepaid", "outcome_month_on_book"].to_numpy())
        out[p] = dict(D=np.searchsorted(dm, grid, side="right") / n, Cl=np.searchsorted(cm, grid, side="right") / n,
                      Cl_early=np.searchsorted(early, grid, side="right") / n, n=n)
    return out


def in_force(hd, at, rule="dates"):
    """loans with a hardship arrangement in force on day `at`. 'dates' is CRM-ECL-04 2.2 (in force from its start date to
    its end date, both included, and not from the day it is cancelled); the others are the misreadings the ask ladders
    price"""
    at = pd.Timestamp(at)
    s, e, c = hd["arrangement_start"], hd["arrangement_end"], hd["cancelled_date"]
    status = hd["arrangement_status"]
    if rule == "dates":
        sel = (s <= at) & (e >= at) & (c.isna() | (c > at))
    elif rule == "excl_cancel":
        sel = (s <= at) & (e >= at) & (status != "Cancelled")
    elif rule == "ignore_cancel":
        sel = (s <= at) & (e >= at)
    elif rule == "label":
        sel = status == "Active"
    elif rule == "label_dated":
        sel = (status == "Active") & (s <= at)
    elif rule == "end_exclusive":
        sel = (s <= at) & (e > at) & (c.isna() | (c > at))
    elif rule == "cancel_inclusive":
        sel = (s <= at) & (e >= at) & (c.isna() | (c >= at))
    else:
        raise ValueError(rule)
    return set(hd.loc[sel, "loan_no"])


def stage(bk, hd, mapping, use_hardship=True, map_v3=True, at=REPORT, rule="dates", score=None):
    """CRM-ECL-04 section 2 at day `at`: stage 3 at 90 or more days past due; stage 2 at 30 or more, a hardship
    arrangement in force, or a behaviour score 60 or more points below the origination score on v4 (v3 converted)"""
    a, b = mapping
    o = bk["origination_score"].astype(float)
    if map_v3:
        o = [int(math.floor(a * v + b + 0.5)) if c == "v3" else int(v) for v, c in zip(o, bk["origination_scorecard"])]
    sc = bk["current_score_v4"] if score is None else score
    drop = pd.Series(o, index=bk.index) - pd.Series(sc, index=bk.index)
    st = pd.Series(1, index=bk.index)
    st[(bk["days_past_due"] >= 30) | (drop >= 60).fillna(False)] = 2
    if use_hardship:
        st[bk["loan_no"].isin(in_force(hd, at, rule))] = 2
    st[bk["days_past_due"] >= 90] = 3
    return st


# ------------------------------------------------------------------------------------------------- the main call

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


def loan_ecl(row, st, C, Cl, mult, variant="cond", disc=True, flat_ead=False, pm_zero=False, a_shift=0, Dsa=None):
    """the loan's ECL under CRM-ECL-04 section 3. variant: 'cond' (the curve's increments from the loan's months on
    book over the share of development loans still open and never defaulted), 'r4' (over one less the curve to date),
    'shift' (no division), 'uncond' (the curve from origination), 'hazard' (the sample's default hazard rolled forward
    with no repayment in the forward months), 'r4b' ('cond' with the balance also run off by the sample's payout rate)"""
    a = months_due(row["first_rep"]) - a_shift
    T = int(row["term_months"])
    rem = T - a
    if rem <= 0:
        # past contractual maturity and not in stage 3: one month remaining (CRM-ECL-04 3.2), so the loan stands at the
        # month on book that leaves one month of its term
        if pm_zero:
            return 0.0
        a, rem = T - 1, 1
    H = rem if st == 2 else min(12, rem)
    r = float(row["contract_rate"])
    bal = float(row["current_balance"])
    eads = ead_path(bal, r, rem)
    Sa = 1.0 - (C if Dsa is None else Dsa)[a] - Cl[a]
    surv = 1.0                       # 'hazard': no default between a and the month before; 'r4b': no payout
    tot = 0.0
    for k in range(1, H + 1):
        m = a + k
        inc = C[m] - C[m - 1]
        if variant == "cond" or variant == "r4b":
            mp = inc / Sa
        elif variant == "r4":
            mp = inc / (1.0 - C[a])
        elif variant == "shift":
            mp = inc
        elif variant == "uncond":
            mp = C[k] - C[k - 1] if k <= T else 0.0
        elif variant == "hazard":
            h = inc / (1.0 - C[m - 1] - Cl[m - 1])
            mp = surv * h
            surv *= 1.0 - h
        else:
            raise ValueError(variant)
        ead = bal if flat_ead else eads[k - 1]
        if variant == "r4b":
            ead *= surv
            surv *= 1.0 - (Cl[m] - Cl[m - 1]) / (1.0 - C[m - 1] - Cl[m - 1])
        df = (1 + r / 12.0) ** (-k) if disc else 1.0
        tot += mp * (STAGE2_SCALAR if st == 2 else 1.0) * mult * LGD[row["product"]] * ead * df
    return tot


def solve(target, **kw):
    bk, curves, hd, scen, mapping = load(target)
    sh = sample_shares(target)
    st = stage(bk, hd, mapping, kw.get("use_hardship", True), kw.get("map_v3", True), rule=kw.get("rule", "dates"))
    if kw.get("stage_fn") is not None:
        st = kw["stage_fn"](bk, hd, mapping)
    mult = sum(w * m for _, w, m in scen)
    variant = kw.get("variant", "cond")
    D_from = kw.get("D_from", "curve")
    ecl = []
    for idx, row in bk.iterrows():
        s = int(st[idx])
        if s == 3:
            ecl.append(0.0)
            continue
        p = row["product"]
        C = curves[p] if D_from == "curve" else sh[p]["D"]
        Cl = sh[p]["Cl_early"] if kw.get("early_only") else sh[p]["Cl"]
        ecl.append(loan_ecl(row, s, C, Cl, mult, variant, kw.get("disc", True), kw.get("flat_ead", False),
                            kw.get("pm_zero", False), kw.get("a_shift", 0),
                            sh[p]["D"] if kw.get("S_from") == "sample" else None))
    bk = bk.assign(stage=st.values, ecl=ecl, mob=[months_due(f) for f in bk["first_rep"]])
    inb = bk[bk["stage"] < 3]
    out = dict(total=float(inb["ecl"].sum()), mult=mult, loans=inb[["loan_no", "product", "stage", "current_balance", "ecl"]].copy())
    for s in (1, 2):
        g = inb[inb["stage"] == s]
        out["stage%d" % s] = float(g["ecl"].sum())
        out["n%d" % s] = int(len(g))
        out["gca%d" % s] = float(g["current_balance"].sum())
    out["n3"] = int((bk["stage"] == 3).sum())
    pm = (bk["mob"] >= bk["term_months"]) & (bk["stage"] < 3)
    out["n_pm"] = int(pm.sum())
    out["ecl_pm"] = float(bk.loc[pm, "ecl"].sum())
    out["stages"] = dict(zip(bk["loan_no"], bk["stage"]))
    return out


# ------------------------------------------------------------------------------------------------- ask A

def collections(target):
    fy = pd.read_csv(os.path.join(target, F["defaults"]), dtype={"loan_no": str})
    led = pd.read_csv(os.path.join(target, F["receipts"]), dtype={"loan_no": str, "receipt_ref": str})
    wb = openpyxl.load_workbook(os.path.join(target, F["sale"]), data_only=True)
    ws = wb.worksheets[0]
    head, rows, cols = {}, [], None
    for r in ws.iter_rows(values_only=True):
        if cols is None:
            if r[0] == "loan_no":
                cols = list(r)
            elif r[0]:
                head[r[0]] = r[1]
            continue
        if r[0]:
            rows.append(dict(zip(cols, r)))
    sale = pd.DataFrame(rows)
    price = float(re.match(r"([0-9.]+) cents", str(head["Price"])).group(1)) / 100.0
    return fy, led, sale, price, head


def _month(s):
    s = str(s)
    return int(s[:4]) * 12 + int(s[5:7]) - 1


def withdrawn_cures(target, fy, led):
    """the 2023-24 defaults Collections closed as cured on a collections hardship arrangement that was withdrawn before it
    started: the register holds an arrangement received after the default month end, starting on the case's resolution
    date and cancelled before that start. Returns those loans, and the ones among them that went on to be written off
    (the agency remits only on written-off accounts) rather than catching up"""
    hd = pd.read_excel(os.path.join(target, F["hardship"]), sheet_name=0)
    cur = fy[fy["resolution"] == "Cured"][["loan_no", "default_month", "resolution_date"]].copy()
    cur["dme"] = pd.to_datetime(cur["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    cur["res"] = pd.to_datetime(cur["resolution_date"])
    x = hd.merge(cur, on="loan_no")
    w = x[(x["received_date"] > x["dme"]) & (x["arrangement_start"] == x["res"]) & (x["arrangement_status"] == "Cancelled")
          & (x["cancelled_date"] < x["arrangement_start"])]
    withdrawn = set(w["loan_no"])
    agency = set(led.loc[led["source"] == "Agency remittance", "loan_no"].dropna())
    return withdrawn, withdrawn & agency


def realised_lgd(target, variant="gold", cures="gold"):
    """what the 2023-24 defaults have lost, as a share of their balance at default, by product and quarter of the
    default month, in per cent. 'gold' is CRM-ECL-04 3.3: every amount received after default to the reporting date, the
    loan's share of the March 2026 sale proceeds (its face value at the cut-off times the price) included, counted at the
    end of the month it was received and discounted to the default month end monthly at the contract rate; a loan that
    returned to performing has lost nothing. cures: 'gold' takes a loan as returned to performing when Collections closed
    it as cured, unless the arrangement it was closed on never started and the loan was written off; 'label' takes every
    case closed as cured at its word; 'no_withdrawn' takes none closed on a withdrawn arrangement (the over-cleaner).
    The other variants are the stops on the ask's ladder"""
    fy, led, sale, price, head = collections(target)
    fy = fy.copy()
    fy["B"] = fy["balance_at_default"].astype(float)
    fy["r"] = fy["contract_rate"].astype(float)
    fy["M"] = fy["default_month"].map(_month)
    fy["q"] = [((int(m[5:7]) - 7) % 12) // 3 + 1 for m in fy["default_month"]]
    rec = led[led["loan_no"].notna()].merge(fy[["loan_no", "M", "r", "default_month"]], on="loan_no", how="inner")
    rec["amt"] = rec["amount_aud"].astype(float)
    rec["n"] = rec["received_date"].map(_month) - rec["M"]
    me = pd.to_datetime(rec["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    rec["days"] = (pd.to_datetime(rec["received_date"]) - me).dt.days
    rec["pv"] = rec["amt"] * (1 + rec["r"] / 12) ** (-rec["n"])
    rec["pv_days"] = rec["amt"] * (1 + rec["r"] / 12) ** (-rec["days"] / (365.25 / 12))
    rec["pv_start"] = rec["amt"] * (1 + rec["r"] / 12) ** (-(rec["n"] - 1))
    rec["pv_annual"] = rec["amt"] * (1 + rec["r"]) ** (-rec["n"] / 12.0)
    rec["pv_kept"] = np.where(rec["amt"] < 0, 0.0, rec["pv"])
    by = rec.groupby("loan_no")
    for c in ("amt", "pv", "pv_days", "pv_start", "pv_annual", "pv_kept"):
        fy[c] = fy["loan_no"].map(by[c].sum()).fillna(0.0)
    bulk = led[led["loan_no"].isna() & (led["source"] == "Debt sale")]
    sale_m = _month(bulk["received_date"].iloc[0])
    sale_day = pd.Timestamp(bulk["received_date"].iloc[0])
    consideration = float(bulk["amount_aud"].astype(float).sum())
    face = dict(zip(sale["loan_no"], sale["face_value_aud"].astype(float)))
    fy["sale"] = fy["loan_no"].map(face).fillna(0.0) * price
    fy["sale_pv"] = fy["sale"] * (1 + fy["r"] / 12) ** (-(sale_m - fy["M"]))
    dme = pd.to_datetime(fy["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    fy["sale_pv_days"] = fy["sale"] * (1 + fy["r"] / 12) ** (-((sale_day - dme).dt.days) / (365.25 / 12))
    fy["sale_pv_start"] = fy["sale"] * (1 + fy["r"] / 12) ** (-(sale_m - fy["M"] - 1))
    fy["sale_pv_annual"] = fy["sale"] * (1 + fy["r"]) ** (-(sale_m - fy["M"]) / 12.0)
    withdrawn, written_off = withdrawn_cures(target, fy, led)
    label = fy["resolution"] == "Cured"
    if cures == "gold":
        cured = label & ~fy["loan_no"].isin(written_off)
    elif cures == "label":
        cured = label
    elif cures == "no_withdrawn":
        cured = label & ~fy["loan_no"].isin(withdrawn)
    else:
        raise ValueError(cures)
    wo = fy["resolution"] == "Written off"
    pop = None
    if variant == "gold":
        loss = np.where(cured, 0.0, fy["B"] - fy["pv"] - fy["sale_pv"])
    elif variant == "s1":            # cases closed as written off only, undiscounted, the sale left out
        loss, pop = fy["B"] - fy["amt"], wo
    elif variant == "s2":            # cures in at full recovery, undiscounted, the sale left out
        loss = np.where(cured, 0.0, fy["B"] - fy["amt"])
    elif variant == "s3":            # discounted, the sale left out
        loss = np.where(cured, 0.0, fy["B"] - fy["pv"])
    elif variant == "s4":            # the sale receipt spread over the 2023-24 written-off loans by balance at default
        share = np.where(wo, fy["B"] / fy.loc[wo, "B"].sum(), 0.0)
        loss = np.where(cured, 0.0, fy["B"] - fy["pv"] - consideration * share * (1 + fy["r"] / 12) ** (-(sale_m - fy["M"])))
    elif variant == "cures_receipts":
        loss = fy["B"] - fy["pv"] - fy["sale_pv"]
    elif variant == "excl_cures":
        loss, pop = fy["B"] - fy["pv"] - fy["sale_pv"], ~cured
    elif variant == "sale_undisc":
        loss = np.where(cured, 0.0, fy["B"] - fy["pv"] - fy["sale"])
    elif variant == "all_undisc":
        loss = np.where(cured, 0.0, fy["B"] - fy["amt"] - fy["sale"])
    elif variant == "floor":
        loss = np.maximum(np.where(cured, 0.0, fy["B"] - fy["pv"] - fy["sale_pv"]), 0.0)
    elif variant == "days":
        loss = np.where(cured, 0.0, fy["B"] - fy["pv_days"] - fy["sale_pv_days"])
    elif variant == "month_start":
        loss = np.where(cured, 0.0, fy["B"] - fy["pv_start"] - fy["sale_pv_start"])
    elif variant == "cure_disc":      # a cure read as recovering its balance at the cure, discounted to the default
        nres = pd.to_datetime(fy["resolution_date"]).dt.year * 12 + pd.to_datetime(fy["resolution_date"]).dt.month - 1
        loss = np.where(cured, fy["B"] * (1 - (1 + fy["r"] / 12) ** (-(nres - fy["M"]))), fy["B"] - fy["pv"] - fy["sale_pv"])
    elif variant == "annual":         # the annual contract rate compounded per whole month, (1 + r) ** (-n / 12)
        loss = np.where(cured, 0.0, fy["B"] - fy["pv_annual"] - fy["sale_pv_annual"])
    elif variant == "lazy":           # every receipt summed as it stands, cures taken from their receipts, no sale
        loss = fy["B"] - fy["amt"]
    elif variant == "no_reversals":   # the negative ledger rows dropped as errors, the dishonoured attempts kept
        loss = np.where(cured, 0.0, fy["B"] - fy["pv_kept"] - fy["sale_pv"])
    elif variant == "face_alloc":     # the sale receipt shared over the sold loans in proportion to face value
        alloc = fy["loan_no"].map(face).fillna(0.0) / sum(face.values()) * consideration
        loss = np.where(cured, 0.0, fy["B"] - fy["pv"] - alloc * (1 + fy["r"] / 12) ** (-(sale_m - fy["M"])))
    else:
        raise ValueError(variant)
    d = fy.assign(loss=loss)
    if pop is not None:
        d = d[pop]
    g = d.groupby(["product", "q"])
    val = 100.0 * g["loss"].sum() / g["B"].sum()
    return {(p, int(q)): float(v) for (p, q), v in val.items()}


def lgd_path(target, cures="gold", sale="share", disc="monthly"):
    """the ask A figures along one path, each knob a way of handling one device or hazard: cures 'gold', 'label' (every
    case closed as cured at its word), 'no_withdrawn' (none closed on a withdrawn arrangement) or 'receipts' (every loan on
    its receipts); sale 'share' (each sold loan's face value times the price), 'none', 'spread' (the receipt over the
    2023-24 written-off cases by balance) or 'flat' (shares not discounted); disc 'monthly' (3.3 and 3.5), 'none',
    'annual' ((1 + r) ** (-n / 12)), 'days' or 'month_start'"""
    fy, led, sale_sch, price, head = collections(target)
    fy = fy.copy()
    fy["B"] = fy["balance_at_default"].astype(float)
    fy["r"] = fy["contract_rate"].astype(float)
    fy["M"] = fy["default_month"].map(_month)
    fy["q"] = [((int(m[5:7]) - 7) % 12) // 3 + 1 for m in fy["default_month"]]
    rec = led[led["loan_no"].notna()].merge(fy[["loan_no", "M", "r", "default_month"]], on="loan_no", how="inner")
    rec["amt"] = rec["amount_aud"].astype(float)
    rec["n"] = rec["received_date"].map(_month) - rec["M"]
    me = pd.to_datetime(rec["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    days = (pd.to_datetime(rec["received_date"]) - me).dt.days

    def factor(n, r, dd):
        if disc == "monthly":
            return (1 + r / 12) ** (-n)
        if disc == "none":
            return 1.0 + 0 * n
        if disc == "annual":
            return (1 + r) ** (-n / 12.0)
        if disc == "days":
            return (1 + r / 12) ** (-dd / (365.25 / 12))
        if disc == "month_start":
            return (1 + r / 12) ** (-(n - 1))
        raise ValueError(disc)
    rec["pv"] = rec["amt"] * factor(rec["n"], rec["r"], days)
    fy["pv"] = fy["loan_no"].map(rec.groupby("loan_no")["pv"].sum()).fillna(0.0)
    bulk = led[led["loan_no"].isna() & (led["source"] == "Debt sale")]
    sale_m = _month(bulk["received_date"].iloc[0])
    sale_day = pd.Timestamp(bulk["received_date"].iloc[0])
    dme = pd.to_datetime(fy["default_month"] + "-01") + pd.offsets.MonthEnd(0)
    f_sale = factor(sale_m - fy["M"], fy["r"], (sale_day - dme).dt.days)
    face = dict(zip(sale_sch["loan_no"], sale_sch["face_value_aud"].astype(float)))
    wo = fy["resolution"] == "Written off"
    if sale == "share":
        fy["sale_pv"] = fy["loan_no"].map(face).fillna(0.0) * price * f_sale
    elif sale == "flat":
        fy["sale_pv"] = fy["loan_no"].map(face).fillna(0.0) * price
    elif sale == "none":
        fy["sale_pv"] = 0.0
    elif sale == "spread":
        cons = float(bulk["amount_aud"].astype(float).sum())
        fy["sale_pv"] = np.where(wo, fy["B"] / fy.loc[wo, "B"].sum(), 0.0) * cons * f_sale
    else:
        raise ValueError(sale)
    withdrawn, written_off = withdrawn_cures(target, fy, led)
    label = fy["resolution"] == "Cured"
    cured = {"gold": label & ~fy["loan_no"].isin(written_off), "label": label,
             "no_withdrawn": label & ~fy["loan_no"].isin(withdrawn), "receipts": label & False}[cures]
    loss = np.where(cured, 0.0, fy["B"] - fy["pv"] - fy["sale_pv"])
    g = fy.assign(loss=loss).groupby(["product", "q"])
    val = 100.0 * g["loss"].sum() / g["B"].sum()
    return {(p, int(q)): float(v) for (p, q), v in val.items()}


# ------------------------------------------------------------------------------------------------- ask B

def score_runs(target):
    sc = pd.read_parquet(os.path.join(target, F["scores"]))
    sc["run_date"] = pd.to_datetime(sc["run_date"]).dt.date
    return sc


def migration(target, june_rule="dates", run="june", sept_rule="dates", june_dpd="close"):
    """the loans in stage 1 and stage 2 at 30 June 2026, by product and June stage: how many are in stage 1, 2 and 3
    at 30 September and how many have closed (not in the September extract). 'june' takes the scores of the month-end
    run on the 30 June position (made on 1 July); 'may' the last run made on or before 30 June; 'sept' the September
    extract's scores. june_dpd 'close' takes days past due at close of business on 30 June (CRM-ECL-04 1.3): the June
    extract, run at 07:30 on 1 July before CHG-26-0418, counts them to the run, a day more; 'extract' takes the column
    as it stands"""
    bk, hd, mapping = load_staging(target)
    jb = pd.read_csv(os.path.join(target, F["june"]))
    if june_dpd == "close":
        jb["days_past_due"] = (jb["days_past_due"] - 1).clip(lower=0)
    elif june_dpd != "extract":
        raise ValueError(june_dpd)
    sc = score_runs(target)
    if run == "june":
        pick = sc[sc["run_date"] == dt.date(2026, 7, 1)]
    elif run == "may":
        pick = sc[sc["run_date"] == max(d for d in sc["run_date"].unique() if d <= PRIOR)]
    elif run == "july":
        pick = sc[sc["run_date"] == dt.date(2026, 8, 1)]
    elif run == "sept":
        pick = bk[["loan_no", "current_score_v4"]].rename(columns={"current_score_v4": "score_v4"})
    else:
        raise ValueError(run)
    score = jb["loan_no"].map(dict(zip(pick["loan_no"], pick["score_v4"])))
    jst = stage(jb, hd, mapping, at=PRIOR, rule=june_rule, score=score)
    sst = stage(bk, hd, mapping, rule=sept_rule)
    now = dict(zip(bk["loan_no"], sst))
    cells = {}
    for p in ("PL36", "PL60"):
        for s0 in (1, 2):
            ids = jb.loc[(jb["product"] == p) & (jst == s0), "loan_no"]
            ss = ids.map(now)
            for s1 in (1, 2, 3):
                cells[(p, s0, "stage %d" % s1)] = int((ss == s1).sum())
            cells[(p, s0, "closed")] = int(ss.isna().sum())
    return cells
