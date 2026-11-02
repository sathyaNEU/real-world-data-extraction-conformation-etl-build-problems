"""The golden computation, reading only the pack: the 2027 claims from a Poisson rate per kilometre on the clock band and
the light each kilometre was driven in (the handbook's Appendix C), carried onto the 2027 schedule; what other insurers
paid back towards each quarter's collisions; and the bodyshop repair cost of each depot's collisions."""
import collections
import csv
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd
import pdfplumber
from openpyxl import load_workbook

import analysis as AN

MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
DEPOT_OF_NAME = {"cramlington": "CRA", "team valley": "GAT", "gateshead": "GAT", "carlisle": "CAR", "darlington": "DAR"}
HANDBOOK_COLS = ["CRA", "GAT", "CAR", "DAR"]       # Cramlington, Team Valley, Carlisle, Darlington, as printed
REC_END = dt.date(2026, 9, 30)
QS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"]
PERIODS = ["2025H1", "2025H2", "2026H1"]
SUMMER = (4, 5, 6, 7, 8, 9)          # April to September; the other six months are January to March and October to December
SHARES = [0.75, 2 / 3, 0.5, 1 / 3, 0.25]


def find(target, pat):
    m = [f for f in os.listdir(target) if re.search(pat, f)]
    assert len(m) == 1, (pat, m)
    return os.path.join(target, m[0])


def norm_reg(r):
    return re.sub(r"\s+", "", str(r)).upper()


def depot_code(name):
    n = str(name).lower()
    for k, v in DEPOT_OF_NAME.items():
        if n.startswith(k):
            return v
    raise KeyError(name)


# ---------------------------------------------------------------- the handbook: sunrise, sunset and the clock rule
def last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def bst(d):
    """1 while British Summer Time is in force on a delivery day (Monday to Saturday), else 0."""
    return 1 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 0


def sun_table(target):
    """{(depot, row): (sunrise min GMT, sunset min GMT)} and the rows' (first month-day, last month-day)."""
    txt = ""
    with pdfplumber.open(find(target, r"handbook.*\.pdf$")) as pdf:
        for p in pdf.pages:
            txt += (p.extract_text() or "") + "\n"
    pat = re.compile(r"^(\d{1,2}) ([A-Z][a-z]{2})(?: to (\d{1,2}) ([A-Z][a-z]{2}))?((?: \d\d:\d\d){8})$")
    T, rows = {}, []
    for line in txt.splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        a = (MON[m.group(2)], int(m.group(1)))
        b = (MON[m.group(4)], int(m.group(3))) if m.group(3) else a
        k = len(rows)
        rows.append((a, b))
        t = [int(x[:2]) * 60 + int(x[3:]) for x in m.group(5).split()]
        for j, code in enumerate(HANDBOOK_COLS):
            T[(code, k)] = (t[2 * j], t[2 * j + 1])
    return T, rows


def row_finder(rows):
    def row_of(d):
        md = (d.month, d.day) if not (d.month == 2 and d.day == 29) else (2, 28)
        for k, (a, b) in enumerate(rows):
            if a <= md <= b:
                return k
        raise KeyError(d)
    return row_of


# ---------------------------------------------------------------- the records
def register(target):
    wb = load_workbook(find(target, r"fleet_register.*\.xlsx$"), read_only=True)
    ws = wb["Trucks"]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    reg = {}
    for r in it:
        x = dict(zip(head, r))
        reg[norm_reg(x["Registration"])] = {"depot": depot_code(x["Depot"]), "sensors": x["Forward sensors"]}
    return reg


def telematics(target, REG):
    runs = {}
    with open(find(target, r"gridtrak.*2023-10.*\.csv$"), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            d = dt.datetime.strptime(x["Date"], "%d/%m/%Y").date()
            on = int(x["First Ignition On (UTC)"][:2]) * 60 + int(x["First Ignition On (UTC)"][3:])
            off = int(x["Last Ignition Off (UTC)"][:2]) * 60 + int(x["Last Ignition Off (UTC)"][3:])
            runs[(norm_reg(x["Vehicle"]), d)] = (on, off, float(x["Distance (mi)"]) * 1.609344)
    with open(find(target, r"gridtrak.*2026-09.*\.csv$"), encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            d = dt.date.fromisoformat(x["day_utc"])
            a = dt.datetime.strptime(x["ignition_on_utc"], "%Y-%m-%dT%H:%M:%SZ")
            b = dt.datetime.strptime(x["ignition_off_utc"], "%Y-%m-%dT%H:%M:%SZ")
            runs[(norm_reg(x["registration"]), d)] = (a.hour * 60 + a.minute, b.hour * 60 + b.minute, float(x["distance_km"]))
    out = []
    for (reg, d), (on, off, km) in sorted(runs.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        h = bst(d)
        out.append((d, REG[reg]["depot"], on / 60.0 + h, off / 60.0 + h, km))
    return out


def listing(target):
    wb = load_workbook(find(target, r"claims_listing.*\.xlsx$"), read_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    k = next(i for i, r in enumerate(rows) if r and r[0] == "Claim no.")
    head = list(rows[k])
    out = []
    for r in rows[k + 1:]:
        if not r or not r[0]:
            continue
        x = dict(zip(head, r))
        for c in ("Notified", "Incident date"):
            if isinstance(x[c], dt.datetime):
                x[c] = x[c].date()
        out.append(x)
    return out


def truck_claims(L, REG):
    """The fund's claims: trucks on the register, duplicates and withdrawn notifications out."""
    out = []
    for x in L:
        st = str(x["Status"])
        if st.startswith("Closed - duplicate") or st == "Withdrawn":
            continue
        reg = norm_reg(x["Registration"])
        if reg not in REG:
            continue
        hh, mm = str(x["Incident time (UK)"]).split(":")
        out.append({"no": x["Claim no."], "date": x["Incident date"], "depot": REG[reg]["depot"], "reg": reg,
                    "h": int(hh) + int(mm) / 60.0, "fault": x["Fault"], "tp": x["Third-party insurer"] or ""})
    return out


def schedule(target):
    wb = load_workbook(find(target, r"route_schedule_2027\.xlsx$"), read_only=True)
    it = wb["Routes"].iter_rows(values_only=True)
    head = list(next(it))
    routes = []
    for r in it:
        x = dict(zip(head, r))
        dep = str(x["Departs from 2 Jan 2027"])
        hh, mm = str(x["Planned day (h:mm)"]).split(":")
        routes.append((x["Depot"], int(dep[:2]) + int(dep[3:5]) / 60.0, int(hh) + int(mm) / 60.0, float(x["Planned km"])))
    it = wb["Calendar 2027"].iter_rows(values_only=True)
    head = list(next(it))
    days = []
    for r in it:
        x = dict(zip(head, r))
        if x["Deliveries"] == "Yes":
            d = x["Date"].date() if isinstance(x["Date"], dt.datetime) else x["Date"]
            days.append(d)
    return routes, days


# ---------------------------------------------------------------- the main call
def frames(target):
    REG = register(target)
    T, rows = sun_table(target)
    row_of = row_finder(rows)
    runs = [r for r in telematics(target, REG) if r[0] <= REC_END]
    L = listing(target)
    TC = truck_claims(L, REG)
    claims = [(c["date"], c["depot"], c["h"]) for c in TC if c["date"] <= REC_END]
    routes, days = schedule(target)
    plan = [(d, dep, a, a + dur, km) for d in days for dep, a, dur, km in routes]
    E = AN.exposure(runs, T, row_of, bst)
    C = AN.claim_frame(claims, T, row_of, bst)
    F = AN.exposure(plan, T, row_of, bst)
    return E, C, F, {"REG": REG, "T": T, "rows": rows, "row_of": row_of, "L": L, "TC": TC, "routes": routes,
                     "days": days, "runs": runs}


def main_call(E, C, F):
    m, names = AN.poisson_fit(E, C, ["band", "dark"])
    q = AN.predict(m, names, F, ["band", "dark"], by="quarter")
    mo = AN.predict(m, names, F, ["band", "dark"], by="month")
    rates = AN.cells(E, C, ["band", "dark"])
    rates["fitted_per_100k_km"] = [float(np.exp(m.params["const"] + m.params.get("band_%d" % b, 0.0)
                                                 + (m.params["dark_1"] if dk else 0.0)) * 1e5)
                                   for b, dk in zip(rates.band, rates.dark)]
    return {"quarters": {int(k): float(v) for k, v in q.items()}, "months": {int(k): float(v) for k, v in mo.items()},
            "year": float(q.sum()), "dark_mult": float(np.exp(m.params["dark_1"])), "rates": rates, "model": m}


def backtest(E, C):
    """The record's own test of the light model where it extrapolates: the 04:00 to 07:00 kilometres driven in the dark
    (the May to August schedule's earliest starts), predicted by the band-and-light model fitted without them, by the
    04:00 to 07:00 rate and by each clock hour's rate."""
    import statsmodels.api as sm
    tE = (E.band == 1) & (E.dark == 1)
    tC = (C.band == 1) & (C.dark == 1)
    m, names = AN.poisson_fit(E[~tE], C[~tC], ["band", "dark"])
    km = float(E[tE].km.sum())
    Xp = sm.add_constant(pd.get_dummies(pd.DataFrame({"band": ["1"], "dark": ["1"]}), drop_first=False).astype(float),
                         has_constant="add").reindex(columns=names, fill_value=0.0)
    light = float(m.predict(Xp, offset=np.log([km]))[0])
    band = float(AN.cell_rates(E, C, ["band"]).loc[1] * km)
    rh = AN.cell_rates(E, C, ["hour"])
    hour = float(sum(rh.loc[h] * E[tE & (E.hour == h)].km.sum() for h in sorted(E[tE].hour.unique())))
    return {"km": km, "share": km / float(E.km.sum()), "obs": int(tC.sum()), "light": light, "band": band, "hour": hour,
            "months": sorted(int(x) for x in E[tE].groupby("month").km.sum().loc[lambda s: s > 1000].index)}


# ---------------------------------------------------------------- the asks
def quarter(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def period(d):
    if d.year == 2025:
        return "2025H1" if d.month <= 6 else "2025H2"
    return "2026H1" if (d.year == 2026 and d.month <= 6) else None


def claim_index(L, REG):
    """Every listing number (a duplicate's resolved to the claim it duplicates) to the claim's own row."""
    own = {x["Claim no."]: x for x in L}
    out = {}
    for no, x in own.items():
        st = str(x["Status"])
        if st.startswith("Closed - duplicate of "):
            out[no] = own[st.split()[-1]]
        else:
            out[no] = x
    return out


def jobs(target):
    with open(find(target, r"brantwick_jobs.*\.csv$"), encoding="utf-8") as fh:
        return {x["Job No"]: x for x in csv.DictReader(fh)}


def ap(target):
    with open(find(target, r"ap_ledger.*\.csv$"), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def genuine_lines(AP, J, CI, REG):
    """Each invoice counted once: identical lines (job, invoice date, description, net) are one invoice posted more than
    once, except that a truck fitted with camera and radar has each sensor calibrated, so up to two identical ADAS
    calibration lines on its job are two invoices."""
    seen = collections.Counter()
    out = []
    for x in sorted(AP, key=lambda x: (dt.datetime.strptime(x["Posting Date"], "%d/%m/%Y"), x["Doc No"])):
        k = (x["Supplier Ref"], x["Invoice Date"], x["Description"], x["Net"])
        lim = 1
        if x["Description"] == "ADAS calibration":
            reg = norm_reg(CI[J[x["Supplier Ref"]]["Claim Ref"]]["Registration"])
            lim = 2 if REG[reg]["sensors"] == "Camera and radar" else 1
        if seen[k] >= lim:
            continue
        seen[k] += 1
        out.append(x)
    return out


def outlays(lines, J, CI):
    o = collections.defaultdict(float)
    for x in lines:
        o[CI[J[x["Supplier Ref"]]["Claim Ref"]]["Claim no."]] += float(x["Net"])
    return {k: round(v, 2) for k, v in o.items()}


def repair_costs(lines, J, CI, REG):
    t = {(d, p): 0.0 for d in ["CRA", "GAT", "CAR", "DAR"] for p in PERIODS}
    for x in lines:
        c = CI[J[x["Supplier Ref"]]["Claim Ref"]]
        p = period(c["Incident date"])
        reg = norm_reg(c["Registration"])
        if p and reg in REG:
            t[(REG[reg]["depot"], p)] += float(x["Net"])
    return t


def bank(target):
    with open(find(target, r"recovery_account.*\.csv$"), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def insurer_crosswalk(L):
    names = sorted({x["Third-party insurer"] for x in L if x["Third-party insurer"]})
    return {n.split()[0].upper(): n for n in names}


def recoveries(B, L, CI, OUT):
    xw = insurer_crosswalk(L)
    own = {x["Claim no."]: x for x in L}
    res, unmatched = [], []
    for x in B:
        if x["Type"] != "BAC" or not x["Paid in"]:
            continue
        desc = x["Description"]
        payer = xw.get(desc.split()[0])
        if payer is None:
            continue                      # not another insurer (the salvage agent)
        d = dt.datetime.strptime(x["Date"], "%d/%m/%Y").date()
        amt = round(float(x["Paid in"]), 2)
        m = re.search(r"\b(RVM\d{6})\b", desc)
        if m:
            res.append((d, amt, CI[m.group(1)]["Claim no."], "quoted"))
            continue
        cands = []
        for no, c in own.items():
            if c["Third-party insurer"] != payer or c["Fault"] not in ("Non-fault", "Split") or no not in OUT:
                continue
            if c["Incident date"] >= d:
                continue
            shares = [1.0] if c["Fault"] == "Non-fault" else SHARES
            if any(abs(round(OUT[no] * s + 1e-9, 2) - amt) < 0.005 for s in shares):
                cands.append(no)
        if len(cands) == 1:
            res.append((d, amt, cands[0], "matched"))
        else:
            unmatched.append((d, amt, payer, cands))
    return res, unmatched


def asks(target, REG, L):
    J = jobs(target)
    CI = claim_index(L, REG)
    AP = ap(target)
    lines = genuine_lines(AP, J, CI, REG)
    OUT = outlays(lines, J, CI)
    RC = repair_costs(lines, J, CI, REG)
    B = bank(target)
    res, unmatched = recoveries(B, L, CI, OUT)
    own = {x["Claim no."]: x for x in L}
    A1 = {q: 0.0 for q in QS}
    for d, amt, no, how in res:
        q = quarter(own[no]["Incident date"])
        if q in A1:
            A1[q] += amt
    return {"A1": A1, "B1": RC, "n_receipts": len(res), "n_matched": sum(1 for r in res if r[3] == "matched"),
            "unmatched": unmatched, "n_lines": len(lines), "n_ap": len(AP)}


def r50(x, k):
    return int(k * round(x / k + 1e-9))


def compute(target):
    E, C, F, X = frames(target)
    M = main_call(E, C, F)
    BT = backtest(E, C)
    K = asks(target, X["REG"], X["L"])
    # the chart's record: truck claims by incident month, October 2023 to September 2026
    cm = collections.Counter((c["date"].year, c["date"].month) for c in X["TC"] if c["date"] <= REC_END)
    months = []
    y, m = 2023, 10
    while (y, m) <= (2026, 9):
        months.append(("%d-%02d" % (y, m), cm.get((y, m), 0)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    F_out = {
        "claims_2027": r50(M["year"], 50), "claims_2027_unrounded": round(M["year"], 1),
        "claims_2027_apr_sep": r50(sum(v for k, v in M["months"].items() if k in SUMMER), 50),
        "claims_2027_other_months": r50(sum(v for k, v in M["months"].items() if k not in SUMMER), 50),
        "claims_2027_apr_sep_unrounded": round(sum(v for k, v in M["months"].items() if k in SUMMER), 1),
        "claims_2027_other_months_unrounded": round(sum(v for k, v in M["months"].items() if k not in SUMMER), 1),
        "claims_2027_months_unrounded": {"%02d" % k: round(v, 1) for k, v in sorted(M["months"].items())},
        "dark_multiplier": round(M["dark_mult"], 2),
        "recoveries_by_collision_quarter": {q: r50(v, 100) for q, v in K["A1"].items()},
        "recoveries_unrounded": {q: round(v, 2) for q, v in K["A1"].items()},
        "repair_cost_by_depot": {"%s %s" % k: r50(v, 100) for k, v in sorted(K["B1"].items())},
        "repair_cost_unrounded": {"%s %s" % k: round(v, 2) for k, v in sorted(K["B1"].items())},
        "record_claims_by_month": dict(months),
    }
    qb, yb, _ = AN.forecast(E, C, F, ["band"])
    F_out["default_path_2027"] = r50(yb, 50)
    F_out["default_path_2027_unrounded"] = round(yb, 1)
    F_out["dark_km_share_2027_pct"] = round(100 * float(F[F.dark == 1].km.sum() / F.km.sum()), 1)
    F_out["dark_km_share_record_pct"] = round(100 * float(E[E.dark == 1].km.sum() / E.km.sum()), 1)
    F_out["claims_in_record"] = int(len(C))
    F_out["dark_multiplier_1dp"] = round(M["dark_mult"], 1)
    F_out["backtest"] = {"km": round(BT["km"]), "claims": BT["obs"], "expected_light_model": round(BT["light"], 1),
                         "expected_band_rate": round(BT["band"], 1), "expected_hour_rate": round(BT["hour"], 1)}
    return F_out, {"E": E, "C": C, "F": F, "X": X, "M": M, "K": K, "BT": BT}
