"""task166's independent verifier. It reads only the shipped bundle (target/, golden/, submission.md) on its own code path
(the csv module, numpy, openpyxl, pypdf and zoneinfo; no generator module and no pandas), recomputes the call, its
figure, the center second, the three lower rungs and all 32 ask counts, reads back every format the pack ships, and
compares the goldens, figures.json and submission.md with what it recomputed.

    python3 task166/generator/verify.py [target]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re
import struct
import sys
from zoneinfo import ZoneInfo

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

CENTERS = ["Grand Rapids", "The Lakeshore", "Kalamazoo and Battle Creek", "Muskegon and the North"]
KNOTS = (-1.0, 0.0, 0.5, 1.0, 1.5, 2.0)
QTRS = (("2025Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)), ("2026Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
        ("2026Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)), ("2026Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30)))
EASTERN = ZoneInfo("America/Detroit")

FAILS = []


def ok(label, cond, msg):
    print("%s  %-5s %s" % ("PASS" if cond else "FAIL", label, msg))
    if not cond:
        FAILS.append(label)


def rows(name):
    with open(os.path.join(TARGET, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def mi(y, m):
    """a month as an integer index"""
    return 12 * y + m - 1


def num(s):
    return float(str(s).replace(",", ""))


# ------------------------------------------------------------------------------------------------- formats read back
files = sorted(os.listdir(TARGET))
fmts = sorted({f.rsplit(".", 1)[1] for f in files})
ok("V1", len(files) >= 10 and len(fmts) >= 3, "%d files in %d formats (%s)" % (len(files), len(fmts), ", ".join(fmts)))
csv_rows = {f: rows(f) for f in files if f.endswith(".csv")}
ok("V2", all(len(v) > 0 for v in csv_rows.values()) and max(len(v) for v in csv_rows.values()) >= 25000,
   "every csv parses with a header; the largest holds %d rows" % max(len(v) for v in csv_rows.values()))

from openpyxl import load_workbook  # noqa: E402

plan_wb = load_workbook(os.path.join(TARGET, "planning_cycle_2027_rates.xlsx"), data_only=True)
base = plan_wb["Base case"]
hdr = [c.value for c in base[1]]
plan30, plan_he = {}, {120: {}, 180: {}, 240: {}}
for r in base.iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    t = mi(r[0].year, r[0].month)
    plan30[t] = float(r[hdr.index("30-year fixed mortgage")])
    plan_he[120][t] = float(r[hdr.index("Home equity fixed 10-year")])
    plan_he[180][t] = float(r[hdr.index("Home equity fixed 15-year")])
    plan_he[240][t] = float(r[hdr.index("Home equity fixed 20-year")])
ok("V3", sorted(plan30) == list(range(mi(2026, 12), mi(2027, 12) + 1)),
   "xlsx: the planning workbook's base case covers December 2026 to December 2027 (%d months)" % len(plan30))

from pypdf import PdfReader  # noqa: E402


def pdf_text(name):
    t = " ".join(p.extract_text() for p in PdfReader(os.path.join(TARGET, name)).pages)
    return re.sub(r"\s+", " ", t)


policy = pdf_text("lending_policy_7-4_he_payoff_forecast.pdf")
filed = ["Population: the fixed-rate closed-end home equity loans on the books at the close of business on 30 November 2026",
         "home equity lines of credit are a separate product and are not in it",
         "Window: payments posted from 1 January 2027 to 31 December 2027",
         "a balance charged off is not principal paid",
         "A loan the credit union refinances itself is paid in full",
         "the regional lending center of the county where the collateral property sits",
         "Rates: the planning cycle's base case",
         "Unit: dollars of principal, reported in millions"]
ok("V4", "7.4.3" in policy and all(s in policy for s in filed) and "Muskegon" not in policy,
   "pdf: the policy reads back with its %d filed sentences (positive control 7.4.3; it names no region)" % len(filed))
strict = []
for f in ("lending_policy_7-4_he_payoff_forecast.pdf", "alm_report_2026_q3.pdf"):
    try:
        PdfReader(os.path.join(TARGET, f), strict=True).pages[0].extract_text()
        strict.append(f)
    except Exception:          # noqa: BLE001
        pass
try:
    from pdfminer.high_level import extract_text as miner_text
    miner = re.sub(r"\s+", " ", miner_text(os.path.join(TARGET, "lending_policy_7-4_he_payoff_forecast.pdf")))
except ImportError:
    miner = policy
ok("V25", len(strict) == 2 and all(s in miner for s in filed),
   "pdf: a strict reader opens both documents and a second extractor reads the policy's filed sentences")
alm = pdf_text("alm_report_2026_q3.pdf")
mm = re.search(r"Fixed-rate home equity loans stood at \$([\d.]+) million across ([\d,]+) loans", alm)
core_rows = csv_rows["core_he_trial_balance_2024-09_2026-11.csv"]
sep = [r for r in core_rows if r["AsOfDate"] == "2026-09-30" and r["LoanStatus"] == "ACTIVE"]
ok("V5", mm is not None and abs(float(mm.group(1)) - sum(num(r["PrincipalBalance"]) for r in sep) / 1e6) < 0.05
   and int(mm.group(2).replace(",", "")) == len(sep),
   "pdf: the ALM report's home equity book ties to the 30 September 2026 trial balance (%.1f million, %d loans)"
   % (sum(num(r["PrincipalBalance"]) for r in sep) / 1e6, len(sep)))
with open(os.path.join(TARGET, "data_dictionary.txt"), encoding="utf-8") as fh:
    dic = fh.read()
ok("V6", all(f in dic for f in files if f.endswith((".csv", ".xlsx")) and f != "export_manifest.csv"),
   "txt: the dictionary describes every data file in the pack")
man = csv_rows["export_manifest.csv"]
ok("V7", {r["file"] for r in man} >= set(files) - {"export_manifest.csv"},
   "csv: the export manifest lists every other file")

# ------------------------------------------------------------------------------------------------- the rates


def posted_monthly(product):
    """a product's posted rate averaged over each month's days, a sheet in effect from its date to the next"""
    sh = sorted((dt.date.fromisoformat(r["effective_date"]), float(r["rate_pct"]))
                for r in csv_rows["posted_rate_sheets_2018-12_2026-11.csv"] if r["product"] == product)
    out, acc = {}, {}
    d, j = dt.date(2018, 12, 1), -1
    while d <= dt.date(2026, 11, 30):
        while j + 1 < len(sh) and sh[j + 1][0] <= d:
            j += 1
        acc.setdefault(mi(d.year, d.month), []).append(sh[max(j, 0)][1])
        d += dt.timedelta(days=1)
    for t, v in acc.items():
        out[t] = sum(v) / len(v)
    return out


sheets = csv_rows["posted_rate_sheets_2018-12_2026-11.csv"]
ok("V8", len({(r["product"], r["effective_date"]) for r in sheets}) == len(sheets),
   "one posted rate per product per sheet date")
m30 = posted_monthly("30 YR FIXED MORTGAGE")
he_posted = {120: posted_monthly("HOME EQUITY FIXED 10 YR"), 180: posted_monthly("HOME EQUITY FIXED 15 YR"),
             240: posted_monthly("HOME EQUITY FIXED 20 YR")}
all30 = dict(m30)
all30.update(plan30)
allhe = {k: dict(v, **{}) for k, v in he_posted.items()}
for k in allhe:
    allhe[k].update(plan_he[k])

# ------------------------------------------------------------------------------------------------- the loans
region_of = {r["county"]: r["regional_lending_center"] for r in csv_rows["county_region_map.csv"]}
xref = {r["legacy_loan_no"]: r["loan_number"] for r in csv_rows["core_conversion_xref.csv"]}
los_rows = csv_rows["he_lending_file_2009-2026.csv"]


def bal_after(P, rate, n, k):
    """balance of a level-payment loan after k payments (zero once the term has run)"""
    i = rate / 1200.0
    k = max(k, 0)
    if k >= n:
        return 0.0
    g = (1 + i) ** n
    return P * (g - (1 + i) ** k) / (g - 1)


def rate_for_balance(A, B, n, k):
    """the note rate at which A over n months leaves B after k payments, on 0.25 to 14 per cent (the balance after
    k payments rises with the rate); the bracket's end where B lies outside it"""
    lo, hi = 0.25, 14.0
    if bal_after(A, lo, n, k) > B:
        return lo
    if bal_after(A, hi, n, k) <= B:
        return hi
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if bal_after(A, mid, n, k) > B:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def mmyyyy(s):
    s = s.strip().zfill(6)
    return mi(int(s[2:]), int(s[:2]))


LOAN = {}
for r in los_rows:
    key = xref.get(r["loan_number"], r["loan_number"])
    A = num(r["senior_lien_original_amount"])
    B = num(r["senior_lien_balance"])
    o1 = mmyyyy(r["senior_lien_opened"])
    k = mmyyyy(r["senior_lien_balance_as_of"]) - o1
    pay = num(r["senior_lien_monthly_payment"])
    term = r["senior_lien_term_months"].strip()
    given = r["senior_lien_note_rate_pct"].strip()
    n1 = int(term) if term else 360
    r1 = float(given) if given else rate_for_balance(A, B, n1, k)
    if not term:
        # a blank term: 180 months where that term's principal and interest sits nearer the reported payment and
        # does not exceed it
        r15 = rate_for_balance(A, B, 180, k)
        i30, i15 = r1 / 1200, r15 / 1200
        p30 = A * i30 / (1 - (1 + i30) ** -360)
        p15 = A * i15 / (1 - (1 + i15) ** -180)
        if abs(pay - p15) < abs(pay - p30) and p15 <= pay + 1.0:
            n1, r1 = 180, r15
    LOAN[key] = dict(center=region_of.get(r["property_county"]), r2=float(r["note_rate_pct"]),
                     n2=int(r["term_months"]), A1=A, n1=n1, r1=r1, o1=o1,
                     street=r["property_street"], city=r["property_city"], zip=r["property_zip"])
ok("V9", len(LOAN) == len(los_rows) and all(v["center"] in CENTERS for v in LOAN.values()),
   "%d funded loans, each with one key and a center by its collateral county" % len(LOAN))

# ------------------------------------------------------------------------------------------------- loan-month history
legacy = csv_rows["legacy_he_loans_2019-01_2024-08.csv"]
D18, JAN19, AUG24, SEP24 = mi(2018, 12), mi(2019, 1), mi(2024, 8), mi(2024, 9)
hist = []          # (key, month, balance at the start of the month, paid in full in the month)
conv_bal = {}
for r in legacy:
    key = xref.get(r["LOAN_NO"], r["LOAN_NO"])
    od = r["OPEN_DT"]
    om = mi(int(od[6:]), int(od[:2]))
    cd = r["CLOSE_DT"].strip()
    cm = mi(int(cd[6:]), int(cd[:2])) if cd else None
    if r["BAL_AT_CONV"].strip():
        conv_bal[key] = num(r["BAL_AT_CONV"])
    rate, n = float(r["NOTE_RT"]), int(r["TERM_MOS"])
    first, last = max(om + 1, JAN19), (cm if cm is not None else AUG24)
    for t in range(first, last + 1):
        if om < JAN19:
            h = bal_after(num(r["BAL_12_31_2018"]), rate, n - (D18 - om), t - 1 - D18)
        else:
            h = bal_after(num(r["ORIG_AMT"]), rate, n, t - 1 - om)
        if t == cm:
            if r["CLOSE_CD"] == "PIF":
                hist.append((key, t, h, 1))
            continue
        hist.append((key, t, h, 0))
by_loan = {}
for r in core_rows:
    by_loan.setdefault(r["LoanNumber"], []).append(r)
for key, rs in by_loan.items():
    rs.sort(key=lambda r: r["AsOfDate"])
    prev = None
    for r in rs:
        t = mi(int(r["AsOfDate"][:4]), int(r["AsOfDate"][5:7]))
        p = conv_bal.get(key) if (t == SEP24 and key in conv_bal) else prev
        prev = num(r["PrincipalBalance"])
        if p is None or p <= 0 or r["LoanStatus"] in ("MAT", "CHGOFF"):
            continue
        hist.append((key, t, p, int(r["LoanStatus"] != "ACTIVE")))
hist = [h for h in hist if h[0] in LOAN]
pays = sum(h[3] for h in hist)


def frame(recs, rates):
    """the covariates of a list of (key, month, balance) rows: the stack's blended rate less the posted 30-year rate a
    month earlier, the first mortgage alone, the loan's own rate less the posted home equity rate for its term, the
    young-first marker and the calendar month"""
    out = {c: np.empty(len(recs)) for c in ("blend", "first", "own", "young", "s1", "s2", "H")}
    for j, (key, t, h) in enumerate(recs):
        L = LOAN[key]
        F = bal_after(L["A1"], L["r1"], L["n1"], t - 1 - L["o1"])
        m = rates[t - 1]
        out["blend"][j] = (F * L["r1"] + h * L["r2"]) / (F + h) - m
        out["first"][j] = L["r1"] - m
        out["own"][j] = L["r2"] - allhe[L["n2"]][t - 1]
        out["young"][j] = 1.0 if t - L["o1"] < 24 else 0.0
        cal = t % 12 + 1
        out["s1"][j] = math.sin(2 * math.pi * cal / 12)
        out["s2"][j] = math.cos(2 * math.pi * cal / 12)
        out["H"][j] = h
    return out


def matrix(X, cov):
    x = X[cov]
    cols = [np.ones(len(x)), x] + [np.maximum(x - k, 0.0) for k in KNOTS] + [X["young"], X["s1"], X["s2"]]
    return np.column_stack(cols)


def logit_fit(M, y):
    """maximum likelihood logistic regression by Newton steps"""
    b = np.zeros(M.shape[1])
    b[0] = math.log(y.mean() / (1 - y.mean()))
    for _ in range(100):
        p = 1 / (1 + np.exp(-(M @ b)))
        w = p * (1 - p)
        step = np.linalg.solve((M * w[:, None]).T @ M, M.T @ (y - p))
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    p = np.clip(1 / (1 + np.exp(-(M @ b))), 1e-300, 1 - 1e-16)
    dev = -2 * float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return b, dev


HX = frame([(k, t, h) for k, t, h, _ in hist], m30)
yv = np.array([h[3] for h in hist], float)

# curtailments: principal above the schedule on active loans, over the balance at the prior month-end
extra = base_bal = 0.0
for key, rs in by_loan.items():
    prev = None
    for r in rs:
        if r["LoanStatus"] != "ACTIVE":
            continue
        if prev is not None and prev > 0:
            extra += max(num(r["PrincipalPaid"]) - num(r["ScheduledPrincipal"]), 0.0)
            base_bal += prev
        prev = num(r["PrincipalBalance"])
curt = extra / base_bal

# the book at the close of 30 November 2026, run forward on its payments from December 2026 to December 2027
book = [r for r in core_rows if r["AsOfDate"] == "2026-11-30" and r["LoanStatus"] == "ACTIVE"]
months = [mi(2026, 12)] + [mi(2027, m) for m in range(1, 13)]
fw = []
for r in book:
    i = num(r["InterestRate"]) * 100 / 1200
    b, pmt = num(r["PrincipalBalance"]), num(r["PaymentAmount"])
    for j, t in enumerate(months):
        if j:
            b = max(b - (pmt - b * i), 0.0)
        if b > 0:
            fw.append((r["LoanNumber"], t, b))
FX = frame(fw, all30)


def forecast(cov):
    b, dev = logit_fit(matrix(HX, cov), yv)
    h = 1 / (1 + np.exp(-(matrix(FX, cov) @ b)))
    tot = {c: 0.0 for c in CENTERS}
    surv = {}
    for (key, t, bal), hh in zip(fw, h):
        s = surv.get(key, 1.0)
        if t >= mi(2027, 1):
            tot[LOAN[key]["center"]] += s * hh * bal + s * (1 - hh) * curt * bal
        surv[key] = s * (1 - hh)
    return {c: v / 1e6 for c, v in tot.items()}, dev


gold, dev_b = forecast("blend")
own, dev_o = forecast("own")
first, dev_f = forecast("first")
trail = {c: 0.0 for c in CENTERS}
for key, t, h, y in hist:
    if y and t >= mi(2025, 12):
        trail[LOAN[key]["center"]] += h / 1e6
rank = sorted(CENTERS, key=lambda c: -gold[c])
pick, second = rank[0], rank[1]
figs = json.load(open(os.path.join(HERE, "figures.json")))
print("  recomputed 2027 principal paid ahead of schedule, $ millions: " +
      ", ".join("%s %.2f" % (c, gold[c]) for c in CENTERS))
ok("V10", pick == figs["call"]["center"] and int(10 * round(gold[pick] / 10)) == figs["call"]["principal_2027_musd"],
   "the call: %s, %.2f million, printed %d" % (pick, gold[pick], int(10 * round(gold[pick] / 10))))
ok("V11", second == figs["call"]["second"] and abs(gold[pick] - figs["call"]["principal_2027_musd_unrounded"]) < 0.02,
   "second: %s (%.2f); margin %.2f" % (second, gold[second], gold[pick] / gold[second]))
edge = 5 - abs(gold[pick] - 10 * round(gold[pick] / 10))
ok("V12", edge >= 2.0, "the figure sits %.2f million inside its $10 million cell" % edge)
ok("V13", max(own, key=own.get) == figs["steps"]["own_rate_pick"] == "Grand Rapids"
   and abs(max(own.values()) - figs["steps"]["own_rate_pick_musd"]) < 0.06,
   "rung 0, the own rate: %s %.1f" % (max(own, key=own.get), max(own.values())))
ok("V14", max(trail, key=trail.get) == figs["steps"]["trailing_pick"] == "Kalamazoo and Battle Creek",
   "rung 1, the trailing year's payoffs: %s %.1f" % (max(trail, key=trail.get), max(trail.values())))
ok("V15", max(first, key=first.get) == figs["steps"]["first_alone_pick"] == "The Lakeshore",
   "rung 2, the first mortgage alone: %s %.1f" % (max(first, key=first.get), max(first.values())))
ok("V16", dev_b < min(dev_o, dev_f) and abs(dev_b - figs["steps"]["deviance"]["blend"]) < 0.5,
   "deviance: the stack %.1f, the own rate %.1f, the first alone %.1f" % (dev_b, dev_o, dev_f))
ok("V17", len(book) == figs["components"]["book_loans"]
   and abs(sum(num(r["PrincipalBalance"]) for r in book) / 1e6 - figs["components"]["book_musd"]) < 0.06
   and pays == figs["components"]["payoffs_2019_2026"],
   "%d loans and %.1f million on the books; %d payoffs in full since January 2019"
   % (len(book), sum(num(r["PrincipalBalance"]) for r in book) / 1e6, pays))

# ------------------------------------------------------------------------------------------------- the ask


def norm(s):
    s = s.upper().replace(".", "").replace(",", " ")
    return " ".join(s.split())


def eastern(ts):
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(EASTERN).date()


def quarter(d):
    for q, a, b in QTRS:
        if a <= d <= b:
            return q
    return None


month_end = {}
opened = {}
for key, rs in by_loan.items():
    for r in rs:
        month_end[(key, r["AsOfDate"][:7])] = num(r["PrincipalBalance"])
    opened[key] = (rs[0]["OpenDate"], num(rs[0]["OriginalAmount"]))


def he_balance(key, d):
    """the principal a statement quotes: the prior month-end balance, or the amount funded earlier in the month"""
    pm = dt.date(d.year, d.month, 1) - dt.timedelta(days=1)
    v = month_end.get((key, pm.isoformat()[:7]))
    if v is None:
        o = opened.get(key)
        if o and o[0][:7] == d.isoformat()[:7] and o[0] <= d.isoformat():
            return o[1]
        return None
    return v if v > 0 else None


by_addr, by_full = {}, {}
for key, L in LOAN.items():
    by_addr.setdefault((norm(L["street"]), L["zip"]), []).append(key)
    by_full.setdefault(norm("%s %s %s" % (L["street"], L["city"], L["zip"])), []).append(key)
serv = {r["mortgage_loan_number"]: r for r in csv_rows["first_mortgage_servicing_2026-11.csv"]}
quoted = []      # (key, eastern date)
for r in csv_rows["payoff_statement_log_2025-10_2026-11.csv"]:
    if r["statement_status"] not in ("ISSUED", "UPDATED"):
        continue
    d = eastern(r["issued_utc"])
    ref = xref.get(r["account_reference"], r["account_reference"])
    if ref in LOAN:
        quoted.append((ref, d))
        continue
    m = serv.get(r["account_reference"])
    if r["product_on_file"] != "MTG" or m is None:
        continue
    nd = dt.date.fromisoformat(m["note_date"])
    k = (d.year - nd.year) * 12 + (d.month - nd.month) - 1
    days = (dt.date.fromisoformat(r["good_through_date"]) - d).days
    fb = bal_after(num(m["original_amount"]), float(m["note_rate_pct"]), int(m["term_months"]), k)
    left = num(r["statement_amount"]) - fb * (1 + float(m["note_rate_pct"]) / 36500 * days) - 25.0
    for key in by_addr.get((norm(m["property_street"]), m["property_zip"]), []):
        hb = he_balance(key, d)
        if hb is not None and abs(left - hb * (1 + LOAN[key]["r2"] / 36500 * days)) <= 1.0:
            quoted.append((key, d))
n_mtg = len(quoted)
mwb = load_workbook(os.path.join(TARGET, "payoff_statements_manual_2026-03.xlsx"), data_only=True)
ws = mwb.worksheets[0]
head_row = [c.value for c in ws[3]]
for r in ws.iter_rows(min_row=4, values_only=True):
    if r[0] is None:
        continue
    liens = str(r[head_row.index("Liens")]).lower()
    if "home equity" not in liens:
        continue
    d = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
    for key in by_full.get(norm(str(r[head_row.index("Property")])), []):
        if he_balance(key, d) is not None:
            quoted.append((key, d))
ok("V18", len(quoted) > n_mtg > 0, "xlsx: the outage workbook adds %d loan-quotes" % (len(quoted) - n_mtg))
paid = {r["LoanNumber"] for r in core_rows if r["LoanStatus"] == "PIF" and r["CloseDate"] <= "2026-11-30"}
table = {}
for c in CENTERS:
    for q, _, _ in QTRS:
        ks = {k for k, d in quoted if quarter(d) == q and LOAN[k]["center"] == c}
        table[(c, q)] = (len(ks), len(ks & paid))
fa = figs["asks"]
ok("V19", all(fa["%s|%s" % k]["quoted"] == v[0] and fa["%s|%s" % k]["paid_in_full"] == v[1] for k, v in table.items()),
   "all 32 ask counts recompute and match figures.json")

# ------------------------------------------------------------------------------------------------- the goldens
gwb = load_workbook(os.path.join(GOLDEN, "he_payoff_pilot_2027.xlsx"), data_only=True)
gtext = " ".join(str(v) for wsx in gwb.worksheets for row in wsx.iter_rows(values_only=True) for v in row if v is not None)
ok("V20", "Muskegon and the North opens the payoff-retention pilot" in gtext and "The Lakeshore" in gtext,
   "the golden workbook states the call and the center second")
QNAME = {"2025Q4": "October to December 2025", "2026Q1": "January to March 2026", "2026Q2": "April to June 2026",
         "2026Q3": "July to September 2026"}
cells = {}
for row in gwb["Payoff quotes"].iter_rows(values_only=True):
    if row and row[0] in CENTERS:
        cells[(row[0], row[1])] = (row[2], row[3])
ok("V21", len(cells) == 16 and all(cells.get((c, QNAME[q])) == table[(c, q)] for c, q in table),
   "the workbook's Payoff quotes sheet carries the 32 counts")
with open(os.path.join(GOLDEN, "payoff_quotes_by_center.png"), "rb") as fh:
    png = fh.read(32)
w, h = struct.unpack(">II", png[16:24])
ok("V22", png[:8] == b"\x89PNG\r\n\x1a\n" and w >= 1200 and h >= 700, "png: the chart reads back (%d by %d)" % (w, h))
with open(os.path.join(TASK, "submission.md"), encoding="utf-8") as fh:
    sub = fh.read()
ok("V23", "Muskegon and the North" in sub.split("## 2.")[0] and "$40 million" in sub.split("## 2.")[0],
   "submission.md block 1 carries the call and its figure")
blk4 = sub.split("## 4.")[1].replace("*", "")
ok("V24", all(("%s, %s: %d quoted, %d paid in full" % (c, QNAME[q], v[0], v[1])) in blk4 for (c, q), v in table.items()),
   "submission.md block 4 carries every count")

print("%d failed" % len(FAILS))
sys.exit(1 if FAILS else 0)
