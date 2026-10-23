"""Reads task483's cut pack the way a solver must and computes every figure from it: each program's test figure under
the golden construction and under each rung and licensed variant, the system's share and the call, each short-term
program's clock hours attended in fiscal 2025 (ask A) and each degree program's borrowers and median Direct Loan
principal (ask B). golden.py, checks.py and ceiling.py call it; verify.py recomputes the golden without it.

The golden construction. A degree program's median is the half point of its campus-by-cohort cells' earnings
distributions pooled by completers with earnings: each published cell's distribution is rebuilt from its five
percentiles (2024 earnings in 2025 dollars), joined straight between them, and the pooled share at or below a value is
the completer-weighted mean of the cells' shares. A short-term grant completer works on day 180 when a job paid in the
quarter holding that day was running on it: paid in the quarters on both sides, or its start (paid in the next quarter
and not the one before) or its exit (paid in the one before and not the next) dated inside the quarter from its pay
there against its pay in its adjacent full quarter."""
import csv
import datetime as dt
import os
from collections import defaultdict
from math import log

import numpy as np

D = dt.date
TD = dt.timedelta
BENCH, CPI, PLACED, SHARE = 34200.0, 1.0294, 70.0, 75.0
MIN_DEGREE, MIN_SHORT, DAY = 30, 20, 180
WINDOW = (D(2024, 7, 1), D(2025, 6, 30))
FY25 = WINDOW
AID_SWITCH, FEE = D(2024, 7, 1), 0.01057
SYSTEM = "Larkspur Basin Community College"
PROVIDER = "TP-0417"
PS = (0.10, 0.25, 0.50, 0.75, 0.90)
FILES = {
    "standard": "workforce_value_designation_standard_2027-28.pdf",
    "release24": "postsecondary_earnings_outcomes_2024_edition.xlsx",
    "release25": "postsecondary_earnings_outcomes_2025_edition.csv",
    "inventory": "larkspur_program_inventory_2025-26.xlsx",
    "older": "fennimore_ridgefield_completions_2024-25.xlsx",
    "newer": "copper_flats_antelope_springs_completions_2024-25.csv",
    "roster": "ctg_participant_roster_2023-2026.csv",
    "wages": "ctg_participant_wage_records_2022q3-2026q2.csv",
    "attendance": "larkspur_ctg_attendance_2023-2026.csv",
    "loans": "larkspur_direct_loan_disbursements_2019-2026.csv",
}


def hround(x):
    """round half away from zero (the deliverables' rounding)"""
    return int(np.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def iso(s):
    return D(int(s[:4]), int(s[5:7]), int(s[8:10]))


def qstart(d):
    return D(d.year, 3 * ((d.month - 1) // 3) + 1, 1)


def qnext(q):
    return D(q.year + (q.month == 10), 1 if q.month == 10 else q.month + 3, 1)


def qprev(q):
    return D(q.year - (q.month == 1), 10 if q.month == 1 else q.month - 3, 1)


def qend(q):
    return qnext(q) - TD(days=1)


def rows_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheet(path, name, header=1):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[name]
    it = ws.iter_rows(values_only=True)
    for _ in range(header - 1):
        next(it)
    head = [h for h in next(it)]
    out = [dict(zip(head, r)) for r in it if any(v is not None for v in r)]
    wb.close()
    return out


class Inputs:
    def __init__(self, target):
        f = lambda k: os.path.join(target, FILES[k])
        inv = sheet(f("inventory"), "Programs")
        self.programs = [r["Program"] for r in inv]
        self.kind = {r["Program"]: ("short" if "clock hours" in str(r["Length"]) else "degree") for r in inv}
        self.by_cip = {}
        for r in inv:
            if self.kind[r["Program"]] == "degree":
                self.by_cip[str(r["CIP 2020"])] = r["Program"]
                if r["CIP before fall 2022"]:
                    self.by_cip[str(r["CIP before fall 2022"])] = r["Program"]
        self.by_old = {r["Fennimore and Ridgefield code"]: r["Program"] for r in inv}
        self.by_new = {str(r["Copper Flats and Antelope Springs ID"]): r["Program"] for r in inv}
        self.by_etp = {r["Career Training Grant program ID"]: r["Program"] for r in inv
                       if r["Career Training Grant program ID"]}
        self.fee = {r["Program"]: float(r["Materials and testing fee per section"]) for r in inv
                    if r["Materials and testing fee per section"]}
        self.degree = [p for p in self.programs if self.kind[p] == "degree"]
        self.short = [p for p in self.programs if self.kind[p] == "short"]
        self._release(f("release24"), f("release25"))
        self._completions(f("older"), f("newer"))
        self._roster(f("roster"))
        self._wage_path = f("wages")
        self._wages(f("wages"))
        self.attendance = rows_csv(f("attendance"))
        self.loans = rows_csv(f("loans"))

    def _release(self, p24, p25):
        cells = defaultdict(list)          # program -> [(campus, cohort, earnings year, n, (p10..p90) 2025 dollars)]
        for r in sheet(p24, "Program earnings", header=4):
            if r["Institution"] != SYSTEM or r["Years after award"] != 3 or r["Award year"] != "2020-21":
                continue
            prog = self.by_cip[str(r["CIP code"])]
            if r["Completers with earnings"] == "S":
                cells[prog].append((r["Campus"], "2020-21", r["Earnings year"], None, None))
                continue
            q = tuple(float(r[k]) * (CPI if r["Earnings year"] == 2024 else 1.0)
                      for k in ("10th percentile", "25th percentile", "Median", "75th percentile", "90th percentile"))
            cells[prog].append((r["Campus"], "2020-21", r["Earnings year"], int(r["Completers with earnings"]), q))
        long = defaultdict(dict)
        for r in rows_csv(p25):
            if r["institution"] != SYSTEM or r["years_after_award"] != "3" or r["award_year"] != "2021-22":
                continue
            long[(r["campus"], r["cip_2020"], r["earnings_year"])][r["measure"]] = (r["value"], r["suppression"])
        for (camp, cip, ey), m in long.items():
            prog = self.by_cip[cip]
            if m["completers_with_earnings"][1] == "S":
                cells[prog].append((camp, "2021-22", int(ey), None, None))
                continue
            f = CPI if ey == "2024" else 1.0
            q = tuple(float(m[k][0]) * f for k in ("p10", "p25", "p50", "p75", "p90"))
            cells[prog].append((camp, "2021-22", int(ey), int(m["completers_with_earnings"][0]), q))
        self.cells = {p: sorted(v, key=lambda c: (c[0], c[1])) for p, v in cells.items()}

    def _completions(self, po, pn):
        n = defaultdict(int)
        self.completers = []               # (program, ssid)
        for r in sheet(po, "Completions 2024-25"):
            prog = self.by_old[r["Program Code"]]
            d = r["Conferred"].date() if hasattr(r["Conferred"], "date") else r["Conferred"]
            if WINDOW[0] <= d <= WINDOW[1]:
                n[prog] += 1
                self.completers.append((prog, str(r["SSID"])))
        for r in rows_csv(pn):
            prog = self.by_new[r["program_id"]]
            d = iso(r["completion_date"])
            if WINDOW[0] <= d <= WINDOW[1]:
                n[prog] += 1
                self.completers.append((prog, r["state_student_id"].replace("-", "")))
        self.c2425 = dict(n)

    def _roster(self, path):
        self.roster = rows_csv(path)
        self.program_of = {}
        self.crn_program = {r["section_id"]: self.by_etp[r["etp_program_id"]] for r in self.roster}
        self.grant = defaultdict(list)     # program -> [(participant, completion day)]
        for r in self.roster:
            prog = self.by_etp[r["etp_program_id"]]
            self.program_of[r["participant_id"]] = prog
            end = iso(r["section_end"])
            if r["exit_reason"] == "Completed" and WINDOW[0] <= end <= WINDOW[1]:
                self.grant[prog].append((r["participant_id"], end))
        self.ids = set(self.program_of)

    def _wages(self, path):
        latest = {}
        for r in rows_csv(path):
            pid = r["participant_id"]
            if pid not in self.ids:
                continue
            q = D(int(r["year"]), 3 * (int(r["quarter"]) - 1) + 1, 1)
            key = (pid, r["ui_account"], q)
            stamp = (r["received_date"], r["report_type"] == "Amended")
            if key not in latest or stamp > latest[key][0]:
                latest[key] = (stamp, float(r["wages"]))
        self.rec = defaultdict(dict)
        for (pid, acct, q), (_, v) in latest.items():
            self.rec[pid][(acct, q)] = v

    def wage_variant(self, how):
        """employer-quarter pay under a mishandling of the amended reports: 'original' keeps the first report, 'sum'
        adds every report"""
        out = defaultdict(dict)
        for r in rows_csv(self._wage_path):
            pid = r["participant_id"]
            if pid not in self.ids:
                continue
            q = D(int(r["year"]), 3 * (int(r["quarter"]) - 1) + 1, 1)
            k = (r["ui_account"], q)
            v = float(r["wages"])
            if how == "sum":
                out[pid][k] = out[pid].get(k, 0.0) + v
            elif r["report_type"] == "Original":
                out[pid][k] = v
        return out


# ---------------------------------------------------------------------------------------------------------------------
# the degree half
def cdf(xv, q, how="lin", lo=0.45, hi=1.7):
    pts = [lo * q[0]] + list(q) + [hi * q[-1]]
    ps = [0.0] + list(PS) + [1.0]
    if how == "lin":
        return float(np.interp(xv, pts, ps))
    if how == "log":
        return float(np.interp(log(xv), np.log(pts), ps))
    from scipy.interpolate import PchipInterpolator
    if how == "pchip":
        if xv <= pts[0]:
            return 0.0
        if xv >= pts[-1]:
            return 1.0
        return float(PchipInterpolator(pts, ps)(xv))
    raise ValueError(how)


def published(cells):
    return [(c[3], c[4]) for c in cells if c[3] is not None]


def pooled(cells, how="lin", lo=0.45, hi=1.7):
    cs = published(cells)
    n = sum(k for k, _ in cs)
    a, b = 1000.0, 400000.0
    for _ in range(80):
        m = (a + b) / 2
        f = sum(k * cdf(m, q, how, lo, hi) for k, q in cs) / n
        a, b = (m, b) if f < 0.5 else (a, m)
    return (a + b) / 2


def averaged(cells):
    cs = published(cells)
    return sum(k * q[2] for k, q in cs) / sum(k for k, _ in cs)


def unweighted(cells):
    return float(np.mean([q[2] for _, q in published(cells)]))


def median_of_medians(cells):
    return float(np.median([q[2] for _, q in published(cells)]))


def pseudo(cells):
    """the cells' percentile values pooled as points, each carrying a fifth of its cell's completers"""
    pts = sorted((v, k / 5.0) for k, q in published(cells) for v in q)
    tot = sum(w for _, w in pts)
    acc = 0.0
    for v, w in pts:
        acc += w
        if acc >= tot / 2:
            return v
    return pts[-1][0]


def lognormal(cells):
    from statistics import NormalDist
    z = [NormalDist().inv_cdf(p) for p in PS]
    fits = []
    for k, q in published(cells):
        b, a = np.polyfit(z, np.log(q), 1)
        fits.append((k, a, b))
    n = sum(f[0] for f in fits)
    lo, hi = 1000.0, 400000.0
    for _ in range(80):
        m = (lo + hi) / 2
        f = sum(k * NormalDist().cdf((log(m) - a) / b) for k, a, b in fits) / n
        lo, hi = (m, hi) if f < 0.5 else (lo, m)
    return (lo + hi) / 2


DEGREE_ROUTES = {"golden": lambda c: pooled(c, "lin"), "log": lambda c: pooled(c, "log"),
                 "pchip": lambda c: pooled(c, "pchip"), "naive": averaged, "unweighted": unweighted,
                 "median_of_medians": median_of_medians, "pseudo": pseudo, "lognormal": lognormal}


def degree_figures(I, route="golden", cpi=True):
    out = {}
    for p in I.degree:
        cells = I.cells.get(p, [])
        if not cpi:
            cells = [(c[0], c[1], c[2], c[3], None if c[4] is None else tuple(v / (CPI if c[2] == 2024 else 1.0)
                                                                          for v in c[4])) for c in cells]
        n = sum(k for k, _ in published(cells))
        if n < MIN_DEGREE:
            out[p] = dict(tested=False, n=n, figure=None, passes=None)
            continue
        v = DEGREE_ROUTES[route](cells)
        out[p] = dict(tested=True, n=n, figure=v, passes=v >= BENCH)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# the short-term half
def full_quarters(rec, e):
    return sorted(k for (ee, k) in rec if ee == e and (e, qprev(k)) in rec and (e, qnext(k)) in rec)


def ratio_status(rec, d180, ref="adjacent", shift=0, qlen=None):
    """(working, undated) under the golden or one of its variants"""
    q = qstart(d180)
    ql = qlen or (qend(q) - q).days + 1
    on, undated = False, False
    for e in sorted({e for e, qq in rec if qq == q}):
        has = lambda k: (e, k) in rec
        if has(qprev(q)) and has(qnext(q)):
            on = True
            continue
        side = "start" if has(qnext(q)) else "exit" if has(qprev(q)) else None
        if side is None:
            undated = True
            continue
        adj = qnext(q) if side == "start" else qprev(q)
        far = qnext(adj) if side == "start" else qprev(adj)
        if not has(far):
            undated = True
            continue
        if ref == "mean":
            fq = full_quarters(rec, e)
            base = float(np.mean([rec[(e, k)] for k in fq])) if fq else rec[(e, adj)]
        elif ref == "two":
            base = (rec[(e, adj)] + rec[(e, far)]) / 2.0
        elif ref == "median":
            base = float(np.median([v for (ee, k), v in rec.items() if ee == e and k != q]))
        else:
            base = rec[(e, adj)]
        frac = min(rec[(e, q)] / base, 1.0)
        if side == "start":
            on = on or (qend(q) - TD(days=frac * ql) - TD(days=shift)) <= d180
        else:
            on = on or (q + TD(days=frac * ql) - TD(days=shift)) >= d180
    return on, undated


FAMILY = [dict(ref=r, shift=sh, qlen=ql) for r in ("adjacent", "mean", "two", "median") for sh in (0, 7, 14)
          for ql in (None, 91)]


def status(rec, comp, route="golden"):
    """a grant completer's day-180 status (True, False, or a probability for 'prorate') under a route"""
    d180 = comp + TD(days=DAY)
    q = qstart(d180)
    ql = (qend(q) - q).days + 1
    pos = (d180 - q).days
    emps = {e for e, _ in rec}
    paid = lambda e, k: (e, k) in rec
    if route == "golden":
        return ratio_status(rec, d180)[0]
    if route.startswith("family"):
        return ratio_status(rec, d180, **FAMILY[int(route[6:])])[0]
    if route == "quarter":
        return any(k == q for _, k in rec)
    if route == "q2_after":
        return any(k == qnext(qnext(qstart(comp))) for _, k in rec)
    if route == "full_quarter":
        return any(paid(e, qprev(q)) and paid(e, q) and paid(e, qnext(q)) for e in emps)
    if route == "end_of_quarter":
        return any(paid(e, q) and paid(e, qnext(q)) for e in emps)
    if route == "start_of_quarter":
        return any(paid(e, qprev(q)) and paid(e, q) for e in emps)
    if route == "pos_qwi":
        return status(rec, comp, "start_of_quarter" if pos < ql / 2 else "end_of_quarter")
    if route == "prorate":
        pn = 1.0
        for e in emps:
            if not paid(e, q):
                continue
            b, a = paid(e, qprev(q)), paid(e, qnext(q))
            pn *= 1 - (1.0 if (a and b) else (pos / ql if a else ((1 - pos / ql) if b else 0.0)))
        return 1 - pn
    if route.startswith("min_"):
        return sum(v for (e, k), v in rec.items() if k == q) >= float(route[4:])
    if route == "half_quarter":
        for e in emps:
            if not paid(e, q):
                continue
            if paid(e, qprev(q)) and paid(e, qnext(q)):
                return True
            fulls = [rec[(e, k)] for k in (qprev(q), qnext(q)) if paid(e, k) and paid(e, qprev(k)) and paid(e, qnext(k))]
            if fulls and rec[(e, q)] >= 0.5 * max(fulls):
                return True
        return False
    if route == "person_ratio":
        tot = lambda k: sum(v for (e, kk), v in rec.items() if kk == k)
        if tot(q) <= 0:
            return False
        if tot(qprev(q)) > 0 and tot(qnext(q)) > 0:
            return True
        if tot(qnext(q)) > 0:
            return qend(q) - TD(days=min(tot(q) / tot(qnext(q)), 1.0) * ql) <= d180
        if tot(qprev(q)) > 0:
            return q + TD(days=min(tot(q) / tot(qprev(q)), 1.0) * ql) >= d180
        return False
    raise ValueError(route)


SHORT_ROUTES = ("golden", "quarter", "q2_after", "end_of_quarter", "start_of_quarter", "pos_qwi", "full_quarter",
                "prorate", "half_quarter", "person_ratio", "min_500", "min_1000", "min_2500")


def short_figures(I, route="golden", rec=None):
    rec = rec or I.rec
    out = {}
    for p in I.short:
        ps = I.grant.get(p, [])
        n = len(ps)
        if n < MIN_SHORT:
            out[p] = dict(tested=False, n=n, figure=None, passes=None, working=None)
            continue
        w = sum(float(status(rec.get(pid, {}), comp, route)) for pid, comp in ps)
        v = 100.0 * w / n
        out[p] = dict(tested=True, n=n, figure=v, passes=v >= PLACED, working=w)
    return out


def share(I, deg, sh, weights=None):
    weights = weights or I.c2425
    num = den = 0
    for p, d in list(deg.items()) + list(sh.items()):
        if not d["tested"]:
            continue
        w = weights.get(p, 0)
        den += w
        num += w * bool(d["passes"])
    return 100.0 * num / den, num, den


def call(I, deg_route="golden", short_route="golden"):
    deg, sh = degree_figures(I, deg_route), short_figures(I, short_route)
    s, num, den = share(I, deg, sh)
    return dict(deg=deg, short=sh, share=s, num=num, den=den, renews=s >= SHARE)


# ---------------------------------------------------------------------------------------------------------------------
# ask A
def hours(v, basis="golden"):
    """a session's time in hours: the export writes hours and minutes after a point (7.30 is seven hours thirty)"""
    if basis in ("decimal", "decimal_resent"):
        return float(v)
    h, m = v.split(".")
    return int(h) + int(m) / 60.0


def ask_a(I, basis="golden"):
    """each short-term program's clock hours its grant participants attended from July 2024 to June 2025, whole hours:
    {program: (hours, unrounded)}. The golden: every session dated in the year once (the export's repeated rows
    dropped), its time read as hours and minutes, each to the program of the participant's section.
    decimal: the times read as decimal hours. resent: the repeated rows kept. decimal_resent: both. by_end: the
    sessions of the sections that ended in the year. completers: the completers' sessions only"""
    out = {p: 0.0 for p in I.short}
    seen = set()
    ends = {r["section_id"]: iso(r["section_end"]) for r in I.roster}
    done = {r["participant_id"] for r in I.roster if r["exit_reason"] == "Completed"}
    for r in I.attendance:
        key = (r["participant_id"], r["crn"], r["session_date"], r["hours"])
        if basis not in ("resent", "decimal_resent"):
            if key in seen:
                continue
            seen.add(key)
        if basis == "by_end":
            if not (FY25[0] <= ends[r["crn"]] <= FY25[1]):
                continue
        elif not (FY25[0] <= iso(r["session_date"]) <= FY25[1]):
            continue
        if basis == "completers" and r["participant_id"] not in done:
            continue
        out[I.crn_program[r["crn"]]] += hours(r["hours"], basis)
    return {p: (hround(v), v) for p, v in out.items()}


ASK_A_BASES = ("decimal", "resent", "decimal_resent", "by_end", "completers")


# ---------------------------------------------------------------------------------------------------------------------
# ask B
def ask_b(I, basis="golden"):
    """each degree program's 2024-25 completers who borrowed Direct Subsidized or Unsubsidized Loans at the college and
    the median of all the principal they borrowed there and their total, to the nearest 10 dollars: {program:
    (borrowers, median, unrounded median, total)}. The golden: every disbursement's amount before July 2024 with returns netted, and from July 2024, where
    each of a loan's rows carries the loan's amount for its award year, each loan's amount once; parent PLUS loans out.
    rows: every row as exported. per_loan: one amount per loan in every year. dedupe: rows alike in borrower, loan,
    amount and status kept once. with_plus, disbursed_only, ay2425 (one award year), gross_up (amounts read as net)"""
    per, seen = defaultdict(float), set()
    for r in I.loans:
        if "PLUS" in r["LOAN_TYPE"] and basis != "with_plus":
            continue
        if basis == "disbursed_only" and r["DISB_STATUS"] != "Disbursed":
            continue
        if basis == "ay2425" and r["AWARD_YEAR"] != "2024-25":
            continue
        if basis == "per_loan":
            if r["DISB_STATUS"] == "Disbursed":
                if r["LOAN_ID"] in seen:
                    continue
                seen.add(r["LOAN_ID"])
        elif basis == "dedupe":
            key = (r["SSID"], r["LOAN_ID"], r["GROSS_AMT"], r["DISB_STATUS"])
            if key in seen:
                continue
            seen.add(key)
        elif basis != "rows" and iso(r["DISB_DATE"]) >= AID_SWITCH:
            if r["LOAN_ID"] in seen:
                continue
            seen.add(r["LOAN_ID"])
        v = float(r["GROSS_AMT"])
        if basis == "gross_up":
            v = round(v / (1 - FEE))
        per[r["SSID"]] += v
    out = {}
    for p in I.degree:
        vals = sorted(per[s] for prog, s in I.completers if prog == p and per.get(s, 0.0) > 0.005)
        med = float(np.median(vals)) if vals else 0.0
        out[p] = (len(vals), hround(med / 10.0) * 10, med, hround(sum(vals) / 10.0) * 10)
    return out


ASK_B_BASES = ("rows", "per_loan", "dedupe", "with_plus", "disbursed_only", "ay2425", "gross_up")
