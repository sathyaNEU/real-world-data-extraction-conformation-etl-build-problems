"""Attribution arithmetic for task500 v3: the office's standing matched-reference method (as a function of its choices,
so every rival construction can be swept) and the comparisons a solver reaches for first. Works on a Panel built either
from the generator's memory or from the shipped files."""
import datetime as dt
from collections import defaultdict

import numpy as np

import world as W

LODGING = ("FS", "LS", "ES", "MO", "BB", "CG")
CLASS_FOR = {"ES": "LS"}          # no untouched extended-stay hotel exists in fiscal 2026
EXACT = dict(universe="any_lodging", own_region="exclude", continuity=24, profile="standardised", k=5, cap=2,
             order="pre_receipts_desc", ratio="median", window="own_month")


class Panel:
    """filers: list of dicts (filer_id, region, county, cls, rooms, flags); lines: (filer_id, period, county,
    taxable_receipts, tax)."""

    def __init__(self, filers, lines):
        self.f = {x["filer_id"]: x for x in filers}
        self.ids = [x["filer_id"] for x in filers]
        self.ix = {fid: i for i, fid in enumerate(self.ids)}
        n = len(self.ids)
        self.R = np.zeros((n, 48))
        self.T = np.zeros((n, 48))
        self.filed = np.zeros((n, 48), dtype=bool)
        self.county_lines = defaultdict(lambda: np.zeros(48))      # (filer, county) -> receipts (facilitators)
        mi = {m: i for i, m in enumerate(W.MONTHS)}
        for fid, period, county, rec, tax in lines:
            i, j = self.ix[fid], mi[period]
            self.R[i, j] += rec
            self.T[i, j] += tax
            self.filed[i, j] = self.filed[i, j] or rec > 0
            self.county_lines[(fid, county)][j] += rec

        self.prior = {"HW": {x["filer_id"] for x in filers if x.get("highway14")},
                      "SD": {x["filer_id"] for x in filers if x.get("stadium")}}

    def col(self, key):
        return np.array([self.f[fid][key] for fid in self.ids])


def touched_sets(pn, year):
    """Which filers each change of a statement year touched."""
    region, cls, county = pn.col("region"), pn.col("cls"), pn.col("county")
    out = {}
    if year == 2026:
        out["CC"] = (region == "Capital City Downtown") & np.isin(cls, ["FS", "LS"])
        out["LX"] = cls == "ES"
        out["CO"] = np.isin(county, W.CUT_COUNTIES)
        out["PC"] = cls == "STR"
        out["AH"] = (region == "Airport Corridor") & np.isin(cls, ["FS", "LS"])
    elif year == 2025:
        out["SD"] = np.array([fid in pn.prior["SD"] for fid in pn.ids])
    elif year == 2024:
        out["HW"] = np.array([fid in pn.prior["HW"] for fid in pn.ids])
    return out


EFFECTIVE = {"CC": dt.date(2025, 9, 1), "LX": dt.date(2026, 1, 1), "CO": dt.date(2025, 10, 1),
             "PC": dt.date(2025, 8, 1), "AH": dt.date(2025, 11, 1), "HW": dt.date(2024, 3, 1),
             "SD": dt.date(2024, 9, 1)}


def month_index(d):
    return W.MONTHS.index(d)


def standing_method(pn, year, code, choice=None, return_detail=False):
    """Matched-reference attribution of one change: per touched filer, a counterfactual for each month from the
    filer's own effective month to the June that closes the statement year, built from the same months a year
    earlier times the reference group's month growth."""
    c = dict(EXACT)
    if choice:
        c.update(choice)
    sets = touched_sets(pn, year)
    touched = sets[code]
    any_touched = np.zeros(len(pn.ids), dtype=bool)
    for v in sets.values():
        any_touched |= v
    end = month_index(dt.date(year, 6, 1))
    eff = month_index(EFFECTIVE[code]) if c["window"] == "own_month" else month_index(dt.date(year - 1, 7, 1))
    cls, region = pn.col("cls"), pn.col("region")
    # the reference universe
    uni = ~any_touched & np.isin(cls, LODGING if c["universe"] == "any_lodging" else LODGING)
    # continuity: a positive return in every month of the screen ending at the statement year's June
    span = c["continuity"]
    if span == "both_years":
        uni &= pn.filed[:, end - 23:end + 1].sum(axis=1) > 0
    else:
        uni &= pn.filed[:, end - span + 1:end + 1].all(axis=1)
    # profiles over the 12 months before the window opens
    prof = pn.R[:, eff - 12:eff]
    if c["profile"] == "standardised":
        mu = prof.mean(axis=1, keepdims=True)
        sd = prof.std(axis=1, keepdims=True)
        sd[sd == 0] = 1
        z = (prof - mu) / sd
    elif c["profile"] == "share":
        tot = prof.sum(axis=1, keepdims=True)
        tot[tot == 0] = 1
        z = prof / tot
    else:
        z = prof
    order = np.where(touched)[0]
    pre = pn.R[order, eff - 12:eff].sum(axis=1)
    if c["order"] == "pre_receipts_desc":
        order = order[np.argsort(-pre, kind="stable")]
    else:
        order = order[np.argsort([pn.ids[i] for i in order], kind="stable")]
    used = defaultdict(int)
    detail = {}
    total = 0.0
    for i in order:
        cand = np.where(uni)[0]
        if c["own_region"] == "exclude":
            cand = cand[region[cand] != region[i]]
        if c.get("same_class"):
            cand = cand[cls[cand] == cls[i]]
        if c["cap"]:
            cand = cand[np.array([used[j] < c["cap"] for j in cand], dtype=bool)]
        d = np.sqrt(((z[cand] - z[i]) ** 2).sum(axis=1))
        pick = cand[np.argsort(d, kind="stable")[:c["k"]]]
        for j in pick:
            used[j] += 1
        cf_months = []
        eff_i = eff
        for t in range(eff_i, end + 1):
            ratios = pn.R[pick, t] / np.where(pn.R[pick, t - 12] > 0, pn.R[pick, t - 12], np.nan)
            if c["ratio"] == "median":
                g = np.nanmedian(ratios)
            elif c["ratio"] == "mean":
                g = np.nanmean(ratios)
            else:
                g = pn.R[pick, t].sum() / pn.R[pick, t - 12].sum()
            cf_months.append(pn.R[i, t - 12] * g)
        cf = np.array(cf_months)
        actual = pn.R[i, eff_i:end + 1]
        rate = np.where(actual > 0, pn.T[i, eff_i:end + 1] / np.where(actual > 0, actual, 1),
                        W.STATE_RATE + W.COUNTY_RATE)
        eff_tax = float((rate * (actual - cf)).sum())
        detail[pn.ids[i]] = dict(actual=float(actual.sum()), reference=float(cf.sum()), tax_effect=eff_tax,
                                 peers=[pn.ids[j] for j in pick])
        total += eff_tax
    return (total, detail) if return_detail else total


def county_cut_effect(pn):
    """A rate change is measured on actual taxable receipts at the old and the new rate."""
    tot = 0.0
    for (fid, county), arr in pn.county_lines.items():
        if county in W.CUT_COUNTIES:
            for t in range(month_index(dt.date(2025, 10, 1)), 48):
                tot += (W.CUT_NEW - W.CUT_OLD) * arr[t]
    return tot


def reference_universe(pn, year, continuity=24):
    sets = touched_sets(pn, year)
    any_t = np.zeros(len(pn.ids), dtype=bool)
    for v in sets.values():
        any_t |= v
    end = month_index(dt.date(year, 6, 1))
    return ~any_t & np.isin(pn.col("cls"), LODGING) & pn.filed[:, end - continuity + 1:end + 1].all(axis=1)


def platform_effect(pn, choice=None):
    """Receipts that move from one set of filers to another are measured as one group: hosts and facilitators
    together, against the hosts' same month a year earlier grown at the median month growth of the reference
    universe."""
    uni = np.where(reference_universe(pn, 2026))[0]
    cls = pn.col("cls")
    hosts, pf = np.where(cls == "STR")[0], np.where(cls == "PF")[0]
    tot = 0.0
    for t in range(month_index(dt.date(2025, 8, 1)), 48):
        g = np.median(pn.R[uni, t] / pn.R[uni, t - 12])
        actual = pn.T[hosts, t].sum() + pn.T[pf, t].sum()
        tot += actual - pn.T[hosts, t - 12].sum() * g
    return float(tot)


def fy2026_attribution(pn, choice=None):
    out = {code: standing_method(pn, 2026, code, choice) for code in ("CC", "LX", "AH")}
    out["CO"] = county_cut_effect(pn)
    out["PC"] = platform_effect(pn, choice)
    return out


# ---------------------------------------------------------------------------------- the comparisons solvers run first
def fy_tax(pn, mask, y, months=None):
    a = month_index(dt.date(y - 1, 7, 1))
    sl = slice(a, a + 12) if months is None else slice(a + months[0], a + months[1])
    return pn.T[mask, sl].sum()


def naive(pn, code, control="all_untouched"):
    """Touched against a comparison group, fiscal 2026 against fiscal 2025, in tax dollars."""
    sets = touched_sets(pn, 2026)
    touched = sets[code]
    any_t = np.zeros(len(pn.ids), dtype=bool)
    for v in sets.values():
        any_t |= v
    cls, region, rooms = pn.col("cls"), pn.col("region"), pn.col("rooms")
    base = ~any_t & np.isin(cls, LODGING)
    if control == "all_untouched":
        comp = base
    elif control == "same_class":
        comp = base & np.isin(cls, [CLASS_FOR.get(x, x) for x in np.unique(cls[touched])])
    elif control == "same_class_size":
        lo, hi = np.percentile(rooms[touched], [10, 90])
        comp = base & np.isin(cls, [CLASS_FOR.get(x, x) for x in np.unique(cls[touched])]) & (rooms >= lo) & (rooms <= hi)
    elif control == "neighbour_region":
        nb = {"Capital City Downtown": "Capital City North"}.get(region[touched][0], None)
        comp = base & (region == nb) & np.isin(cls, [CLASS_FOR.get(x, x) for x in np.unique(cls[touched])]) if nb else base
    elif control == "same_class_balanced":
        comp = base & np.isin(cls, [CLASS_FOR.get(x, x) for x in np.unique(cls[touched])]) & pn.filed[:, 12:36].all(axis=1)
    g = fy_tax(pn, comp, 2026) / fy_tax(pn, comp, 2025)
    return float(fy_tax(pn, touched, 2026) - fy_tax(pn, touched, 2025) * g)


# ---------------------------------------------------------------------------------- from the shipped files
def load(T):
    import csv
    from pathlib import Path
    from openpyxl import load_workbook
    T = Path(T)
    with open(T / "lodging_filer_register_2026-08.csv", newline="") as fh:
        reg = list(csv.DictReader(fh))
    filers = [dict(filer_id=r["filer_id"], cls=r["class"], region=r["region"], county=r["county"],
                   rooms=int(r["rooms_or_units"] or 0)) for r in reg]
    lines = []
    with open(T / "lodging_tax_returns_fy2023-fy2026.csv", newline="") as fh:
        for r in csv.DictReader(fh):
            y, m = map(int, r["period"].split("-"))
            lines.append((r["filer_id"], dt.date(y, m, 1), r["county"], float(r["taxable_receipts"]),
                          float(r["tax_due"])))
    pn = Panel(filers, lines)
    wb = load_workbook(T / "variance_statements_appendix_b_fy2024_fy2025.xlsx", data_only=True)
    cert = {}
    for code, ws in zip(("HW", "SD"), wb.worksheets):
        rows = {}
        for row in ws.iter_rows(min_row=5, values_only=True):
            if row[0] and str(row[0]).startswith("LT"):
                rows[row[0]] = dict(actual=row[4], reference=row[5], tax_effect=row[7])
        cert[code] = rows
    pn.prior = {code: set(rows) for code, rows in cert.items()}
    with open(T / "adopted_forecast_lodging_fy2026.csv", newline="") as fh:
        forecast = {r["period"]: int(r["adopted_forecast_tax"]) for r in csv.DictReader(fh)}
    with open(T / "treasury_lodging_deposits_fy2025-fy2026.csv", newline="") as fh:
        ledger = list(csv.DictReader(fh))
    return dict(pn=pn, cert=cert, forecast=forecast, ledger=ledger)


def reproduction(pn, cert, choice=None):
    hit = tot = 0
    for year, code in ((2024, "HW"), (2025, "SD")):
        _, det = standing_method(pn, year, code, choice, return_detail=True)
        for fid, v in cert[code].items():
            tot += 1
            r = det[fid]["reference"]
            hit += bool(np.isfinite(r)) and round(r) == v["reference"]
    return hit, tot


NAMES = {c["code"]: c["name"] for c in W.CHANGES_FY2026}


def cash_collections(ledger, fy=2026):
    """Treasury cash basis: tax deposits booked in the fiscal year, the latest amendment of each return standing in
    for any earlier one, refunds netted, penalty and interest left out."""
    a, b = dt.date(fy - 1, 7, 1), dt.date(fy, 6, 30)
    latest = {}
    tot = 0.0
    for r in ledger:
        d = dt.date.fromisoformat(r["deposit_date"])
        if r["type"] == "AMEND":
            key = (r["filer_id"], r["period"])
            if key not in latest or r["amendment_seq"] > latest[key][0]:
                latest[key] = (r["amendment_seq"], d, float(r["amount"]))
            continue
        if not (a <= d <= b) or r["type"] == "PEN_INT":
            continue
        tot += float(r["amount"])
    for seq, d, amt in latest.values():
        if a <= d <= b:
            tot += amt
    return tot


def all_figures(T):
    d = load(T)
    pn = d["pn"]
    eff = fy2026_attribution(pn)
    named = min(eff, key=eff.get)
    ranked = sorted(eff, key=eff.get)
    f = dict(effects={k: v for k, v in eff.items()}, named=named, runner_up=ranked[1])
    actual = pn.T[:, 36:48].sum()
    fc = sum(d["forecast"].values())
    f["actual_fy2026"] = float(actual)
    f["forecast_fy2026"] = float(fc)
    f["shortfall"] = float(fc - actual)
    f["residual"] = float((actual - fc) - sum(eff.values()))
    f["reproduced"] = reproduction(pn, d["cert"])
    details = {}
    for code in ("CC", "LX", "AH"):
        _, det = standing_method(pn, 2026, code, return_detail=True)
        details[code] = det
    f["details"] = details
    f["cash_fy2026"] = cash_collections(d["ledger"])
    return f, d


def cash_reconciliation(pn, ledger, fy=2026):
    """Liability (returns as filed for the year's periods) to the treasury's cash collections for the year."""
    a, b = dt.date(fy - 1, 7, 1), dt.date(fy, 6, 30)
    in_year = lambda d: a <= d <= b
    per_in = lambda per: a <= dt.date(int(per[:4]), int(per[5:7]), 1) <= b
    liability = float(pn.T[:, month_index(a):month_index(b.replace(day=1)) + 1].sum())
    tax_in_year_own = tax_in_year_other = 0.0
    refunds = 0.0
    latest = {}
    for r in ledger:
        d = dt.date.fromisoformat(r["deposit_date"])
        amt = float(r["amount"])
        if r["type"] == "TAX" and in_year(d):
            if per_in(r["period"]):
                tax_in_year_own += amt
            else:
                tax_in_year_other += amt
        elif r["type"] == "REFUND" and in_year(d):
            refunds += amt
        elif r["type"] == "AMEND":
            key = (r["filer_id"], r["period"])
            if key not in latest or r["amendment_seq"] > latest[key][0]:
                latest[key] = (r["amendment_seq"], d, amt)
    amend = sum(amt for seq, d, amt in latest.values() if in_year(d))
    unpaid_own = liability - tax_in_year_own
    cash = tax_in_year_own + tax_in_year_other + amend + refunds
    return dict(liability=liability, own_periods_not_deposited=unpaid_own, earlier_periods_deposited=tax_in_year_other,
                amendments=amend, refunds=refunds, cash=cash)
