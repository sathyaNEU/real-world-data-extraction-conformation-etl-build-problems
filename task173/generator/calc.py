"""task173 analysis from the shipped files alone: the golden booking, every defensible construction of it, every rival
route, the back-test and the screens. Reads target/; never imports the world."""
from __future__ import annotations

import csv
import datetime as dt
import io
import math
import os
import zipfile

import numpy as np
from scipy.optimize import curve_fit

import common as K

# the standard's filed numbers (read back from the standard in checks.py)
H_EXPERT = K.HANDLE_PER_EXPERT
H_BILLED = K.HANDLE_PER_BILLED
BLOCK = K.ORDER_BLOCK


# ------------------------------------------------------------------------------------------------- loading
def _read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def _xlsx_rows(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows


def parse_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def pdf_text(path):
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def calendar_classes(path):
    """The 2027 classes in the training calendar: go-live date and seats."""
    import re
    txt = pdf_text(path)
    out = []
    for m in re.finditer(r"(27-\d)\s+Room \w\s+(\d{1,2} \w+ 2027)\s+(\d{1,2} \w+ 2027)\s+(\d+)", txt):
        out.append((dt.datetime.strptime(m.group(3), "%d %B %Y").date(), int(m.group(4))))
    assert len(out) == 4, out
    return out


class Pack:
    """The shipped files, parsed once."""

    def __init__(self, target, queues=("Live Experts EN",)):
        self.target = target
        p = lambda f: os.path.join(target, f)
        import records as RC
        self.F = RC
        rows = _read_csv(p(RC.F_CRM))
        head = rows[0]
        ix = {c: i for i, c in enumerate(head)}
        data = rows[1:]
        self.n_crm = len(data)
        en = [r for r in data if r[ix["Queue"]] in queues]
        self.n_en = len(en)
        self.case = np.array([r[ix["Case Number"]] for r in en])
        self.iid = [r[ix["Interaction ID"]] for r in en]
        self.itype = np.array([r[ix["Interaction Type"]] for r in en])
        self.start_utc = [parse_utc(r[ix["Started (UTC)"]]) for r in en]
        self.start_local = [K.eastern(t) for t in self.start_utc]
        self.day = np.array([t.date().toordinal() for t in self.start_local])
        self.tsort = np.array([(t - dt.datetime(2026, 1, 1)).total_seconds() for t in self.start_utc])
        self.talk = np.array([float(r[ix["Talk Seconds"]]) for r in en])
        self.acw = np.array([float(r[ix["After-Contact Work Seconds"]]) for r in en])
        self.handled = np.array([r[ix["Handled By"]] for r in en])
        self.disp = np.array([r[ix["Disposition"]] for r in en])
        self.topic = np.array([r[ix["Topic"]] for r in en])
        self.channel = np.array([r[ix["Channel"]] for r in en])
        self.hmin = (self.talk + self.acw) / 60.0
        # roster: in-house experts' first season and 2026 go-live; vendor agents from the vendor sheet
        ros = _xlsx_rows(p(RC.F_ROSTER), "Seasonal experts")
        h = ros[0]
        ri = {c: i for i, c in enumerate(h)}
        self.roster = {r[ri["Employee No"]]: r for r in ros[1:] if r[ri["Employee No"]]}
        self.ri = ri
        vend = _xlsx_rows(p(RC.F_ROSTER), "HCS agents 2026")
        vh = vend[0]
        vi = {c: i for i, c in enumerate(vh)}
        self.vendor = {r[vi["Agent"]]: r for r in vend[1:] if r[vi["Agent"]]}
        grp, golive = [], []
        for u in self.handled:
            if u in self.vendor:
                grp.append("V"); golive.append(0)
            else:
                r = self.roster[u]
                fs = int(r[ri["First Season"]])
                if fs == 2026:
                    g = r[ri["2026 Go-Live"]]
                    g = g if isinstance(g, dt.date) else dt.date.fromisoformat(str(g)[:10])
                    grp.append("N"); golive.append(g.toordinal() if not isinstance(g, dt.datetime) else g.date().toordinal())
                else:
                    grp.append("R"); golive.append(0)
        self.grp = np.array(grp)
        self.golive = np.array(golive)
        self.wk = np.where(self.grp == "N", (self.day - self.golive) / 7.0, -1.0)
        # case structure: each interaction's successor on its case
        order = np.lexsort((self.tsort, self.case))
        self.order = order
        cs = self.case[order]
        nxt = np.zeros(len(cs), dtype=bool)
        nxt[:-1] = cs[1:] == cs[:-1]
        self.followed = np.zeros(len(cs), dtype=bool)
        self.followed[order] = nxt
        first = np.ones(len(cs), dtype=bool)
        first[1:] = cs[1:] != cs[:-1]
        self.first = np.zeros(len(cs), dtype=bool)
        self.first[order] = first
        self.case_first_grp = {}
        # demand plan
        dp = _xlsx_rows(p(RC.F_DEMAND), "Daily forecast")
        dh = dp[0]
        di = {c: i for i, c in enumerate(dh)}
        self.plan = []
        for r in dp[1:]:
            if r[di["Date"]] is None:
                continue
            d = r[di["Date"]]
            d = d.date() if isinstance(d, dt.datetime) else (d if isinstance(d, dt.date) else dt.date.fromisoformat(str(d)))
            self.plan.append((d, int(r[di["New expert cases"]])))
        f0, f1 = K.fortnight(2027)
        self.F27 = sum(n for d, n in self.plan if f0 <= d <= f1)
        g0, g1 = K.fortnight(2026)
        self.F26 = int(sum(1 for d, t in zip(self.day, self.itype) if t == "New case"
                           and g0.toordinal() <= d <= g1.toordinal()))
        # the 2027 classes, from the training calendar
        self.classes27 = calendar_classes(p("training_calendar_2027.pdf"))
        self.confirmed27 = {u for u, r in self.roster.items()
                            if r[ri["Queue"]] == "EN" and r[ri["2027 Recall"]] == "Confirmed"}
        self.returning27 = sum(1 for r in self.roster.values()
                               if r[ri["Queue"]] == "EN" and r[ri["2027 Recall"]] == "Confirmed")


# ------------------------------------------------------------------------------------------------- estimators
def expo(x, a, b, t):
    return a + b * np.exp(-x / t)


def binned(xw, y, width=1.0):
    b = np.floor(xw / width).astype(int)
    ub = np.unique(b)
    yb = np.array([y[b == k].mean() for k in ub])
    nb = np.array([(b == k).sum() for k in ub])
    return (ub + 0.5) * width, yb, nb


def fit_expo(xw, y, p0):
    x, yb, nb = binned(xw, y)
    c, _ = curve_fit(expo, x, yb, p0=p0, sigma=1 / np.sqrt(nb), maxfev=40000)
    return c


class Est:
    """The 2026 rates every construction draws on, from the English queue's interactions."""

    def __init__(self, P, mask=None, fortnight_only=False):
        m = np.ones(P.n_en, dtype=bool) if mask is None else mask
        f0, f1 = K.fortnight(2026)
        fn = (P.day >= f0.toordinal()) & (P.day <= f1.toordinal())
        self.fn = fn
        R, N, V = (P.grp == "R") & m, (P.grp == "N") & m, (P.grp == "V") & m
        first, fol = P.first, P.followed.astype(float)
        sel = fn if fortnight_only else np.ones(P.n_en, dtype=bool)
        self.pR = fol[R & first & sel].mean()
        self.pO = fol[V & first].mean()
        self.q = fol[~first & m & sel].mean()
        self.aR = P.hmin[R & sel].mean()
        self.aO = P.hmin[V].mean()
        self.cp = fit_expo(P.wk[N & first], fol[N & first], (0.14, 0.3, 5.0))
        self.ca = fit_expo(P.wk[N], P.hmin[N], (31.0, 14.0, 5.0))
        self.P = P
        self.mN = N
        self.N_first = N & first


def bench27(P):
    f0, f1 = K.fortnight(2027)
    days = [f0 + dt.timedelta(k) for k in range(14)]
    return days


def inhouse(P, pf, af, pR, aR, nR=None):
    """Contacts the 2027 in-house bench takes in the fortnight at the standard's handle hours, and the sum of their
    first-contact follow-up chances (contacts weighted)."""
    nR = P.returning27 if nR is None else nR
    days = bench27(P)
    Kc = Kp = 0.0
    for d in days:
        kr = nR * (H_EXPERT / 14) * 60 / aR
        Kc += kr
        Kp += kr * pR
        for g, n in P.classes27:
            x = (d - g).days / 7.0
            kn = n * (H_EXPERT / 14) * 60 / af(x)
            Kc += kn
            Kp += kn * pf(x)
    return Kc, Kp


def solve_booking(Kc, Kp, pO, aO, q, F):
    """Billed vendor hours that balance the fortnight: the bench's contacts and the vendor's equal the new cases
    and every follow-up they bring, each case's follow-ups set by who takes its first contact."""
    kO = H_BILLED * 60 / aO
    lo, hi = 0.0, 2e5
    for _ in range(200):
        mid = (lo + hi) / 2
        Ct = Kc + mid * kO
        Pbar = (Kp + mid * kO * pO) / Ct
        if Ct - F * (1 + Pbar / (1 - q)) < 0:
            lo = mid
        else:
            hi = mid
    return lo


def golden(P, E=None):
    E = E or Est(P)
    Kc, Kp = inhouse(P, lambda x: expo(x, *E.cp), lambda x: expo(x, *E.ca), E.pR, E.aR)
    B = solve_booking(Kc, Kp, E.pO, E.aO, E.q, P.F27)
    kO = H_BILLED * 60 / E.aO
    Ct = Kc + B * kO
    Pbar = (Kp + B * kO * E.pO) / Ct
    contacts = P.F27 * (1 + Pbar / (1 - E.q))
    return dict(B=B, order=K.ceil_to(B, BLOCK), contacts=contacts, followups=contacts - P.F27,
                inhouse_contacts=Kc, vendor_contacts=B * kO, pbar=Pbar, est=E)


# ------------------------------------------------------------------------------------------------- constructions
def constructions(P, E=None):
    E = E or Est(P)
    out = {}
    first, fol = P.first, P.followed.astype(float)
    N = P.grp == "N"
    for wd in (1, 2, 3, 4):
        xw, yb, _ = binned(P.wk[N & first], fol[N & first], wd)
        xa, ab, _ = binned(P.wk[N], P.hmin[N], wd)
        pf = lambda x, xw=xw, yb=yb, wd=wd: float(yb[np.argmin(np.abs(xw - (math.floor(x / wd) + 0.5) * wd))])
        af = lambda x, xa=xa, ab=ab, wd=wd: float(ab[np.argmin(np.abs(xa - (math.floor(x / wd) + 0.5) * wd))])
        out["tenure bands of %d week%s" % (wd, "" if wd == 1 else "s")] = solve_booking(
            *inhouse(P, pf, af, E.pR, E.aR), E.pO, E.aO, E.q, P.F27)

    def logit_curve(x, a, b):
        return 1 / (1 + np.exp(-(a + b * np.log(x + 0.5))))
    xw, yb, nb = binned(P.wk[N & first], fol[N & first])
    cl, _ = curve_fit(logit_curve, xw, yb, p0=(-0.5, -0.5), sigma=1 / np.sqrt(nb), maxfev=40000)
    out["logistic in log weeks"] = solve_booking(*inhouse(P, lambda x: logit_curve(x, *cl), lambda x: expo(x, *E.ca),
                                                          E.pR, E.aR), E.pO, E.aO, E.q, P.F27)

    def powc(x, a, b, c):
        return a + b * (x + 1) ** (-c)
    cpw, _ = curve_fit(powc, xw, yb, p0=(0.12, 0.3, 0.7), sigma=1 / np.sqrt(nb), maxfev=40000)
    out["power law in weeks"] = solve_booking(*inhouse(P, lambda x: powc(x, *cpw), lambda x: expo(x, *E.ca),
                                                       E.pR, E.aR), E.pO, E.aO, E.q, P.F27)
    Ef = Est(P, fortnight_only=True)
    out["returning rates and q from the 2026 fortnight"] = solve_booking(
        *inhouse(P, lambda x: expo(x, *E.cp), lambda x: expo(x, *E.ca), Ef.pR, Ef.aR), E.pO, E.aO, Ef.q, P.F27)
    # contact level: every interaction's chance of a successor by its handler, positions pooled, chains geometric
    cpp = fit_expo(P.wk[N], fol[N], (0.14, 0.3, 5.0))
    pRp = fol[P.grp == "R"].mean()
    pOp = fol[P.grp == "V"].mean()
    Kc, Kp = inhouse(P, lambda x: expo(x, *cpp), lambda x: expo(x, *E.ca), pRp, E.aR)
    kO = H_BILLED * 60 / E.aO
    lo, hi = 0.0, 2e5
    for _ in range(200):
        mid = (lo + hi) / 2
        Ct = Kc + mid * kO
        Pb = (Kp + mid * kO * pOp) / Ct
        if Ct - P.F27 / (1 - Pb) < 0:
            lo = mid
        else:
            hi = mid
    out["contact level, positions pooled"] = lo
    # the returning rate and handle time from the confirmed experts' own 2026 records (veterans in 2026)
    conf = np.isin(P.handled, list(P.confirmed27)) & (P.grp == "R")
    pRc, aRc = fol[conf & first].mean(), P.hmin[conf].mean()
    out["returning rates from the confirmed veterans' own 2026 records"] = solve_booking(
        *inhouse(P, lambda x: expo(x, *E.cp), lambda x: expo(x, *E.ca), pRc, aRc), E.pO, E.aO, E.q, P.F27)
    # contact level with positions: first contacts by handler, follow-ups at their own rate (= the golden's form)
    out["case level, follow-ups charged to the first contact"] = golden(P, E)["B"]
    return out


# ------------------------------------------------------------------------------------------------- rival routes
def rivals(P, E=None):
    E = E or Est(P)
    g = golden(P, E)
    Kg = g["inhouse_contacts"]
    first, fol = P.first, P.followed.astype(float)
    fn = E.fn
    R, N, V = P.grp == "R", P.grp == "N", P.grp == "V"
    M26 = fn.sum() / (fn & first).sum()
    A26 = P.hmin[fn].mean()
    kO_own = H_BILLED * 60 / E.aO
    nR = P.returning27
    nN = sum(n for _, n in P.classes27)

    def B_contacts(C, cap, kO=kO_own):
        return max(0.0, (C - cap) / kO)
    out = {}
    out["last season's contacts per new case, last season's handle time"] = max(
        0.0, (P.F27 * M26 * A26 / 60 - (nR + nN) * H_EXPERT) / H_BILLED)
    out["last season's contacts per new case, handle time by weeks on queue"] = B_contacts(P.F27 * M26, Kg)
    season_share = (~first).mean()
    out["season follow-up share of contacts, pooled"] = B_contacts(P.F27 / (1 - season_share), Kg)
    out["first contacts only"] = B_contacts(P.F27, Kg)
    pN_season = fol[N & first].mean()
    out["first-contact rate by group, new hires at their season average"] = solve_booking(
        *inhouse(P, lambda x: pN_season, lambda x: expo(x, *E.ca), E.pR, E.aR), E.pO, E.aO, E.q, P.F27)
    pN_fn = fol[N & first & fn].mean()
    out["first-contact rate by group, new hires at last fortnight's rate"] = solve_booking(
        *inhouse(P, lambda x: pN_fn, lambda x: expo(x, *E.ca), E.pR, E.aR), E.pO, E.aO, E.q, P.F27)
    Kc, Kp = inhouse(P, lambda x: expo(x, *E.cp), lambda x: expo(x, *E.ca), E.pR, E.aR)
    out["vendor agents at the returning rate"] = solve_booking(Kc, Kp, E.pR, E.aO, E.q, P.F27)
    Pin = Kp / Kc
    out["bench's follow-ups only, vendor hours taken as pure capacity"] = B_contacts(P.F27 * (1 + Pin / (1 - E.q)), Kc)
    out["first-contact curve, pooled handle time"] = solve_booking(
        *inhouse(P, lambda x: expo(x, *E.cp), lambda x: A26, E.pR, A26), E.pO, A26, E.q, P.F27)
    aN_season = P.hmin[N].mean()
    out["first-contact curve, new hires' season-average handle time"] = solve_booking(
        *inhouse(P, lambda x: expo(x, *E.cp), lambda x: aN_season, E.pR, E.aR), E.pO, E.aO, E.q, P.F27)
    # the expert's own wrap-up code as the resolution
    unres = (P.disp != "Resolved").astype(float)
    dR = unres[R & first].mean()
    dO = unres[V & first].mean()
    dq = unres[~first].mean()
    dc = fit_expo(P.wk[N & first], unres[N & first], (0.12, 0.05, 5.0))
    out["resolution from the wrap-up code"] = solve_booking(
        *inhouse(P, lambda x: expo(x, *dc), lambda x: expo(x, *E.ca), dR, E.aR), dO, E.aO, dq, P.F27)
    # the naive tenure check: share of each group's contacts that are follow-ups
    share_fu = {gname: (~first[P.grp == gname]).mean() for gname in "RNV"}
    out["follow-up share of each group's own contacts"] = B_contacts(
        P.F27 / (1 - (share_fu["R"] * 0.33 + share_fu["N"] * 0.46 + share_fu["V"] * 0.21)), Kg)
    for u in (10, 20, 30):
        f = u / 100.0
        cap_r = nR * H_EXPERT * 60 / E.aR
        Kn = Kg - cap_r
        out["%d per cent off new experts' capacity, handle time by weeks" % u] = B_contacts(P.F27 * M26, Kg - f * Kn)
        out["%d per cent off new experts' capacity, returning handle time" % u] = B_contacts(
            P.F27 * M26, cap_r + nN * H_EXPERT * 60 / E.aR * (1 - f))
        out["new experts %d per cent slower than returning" % u] = B_contacts(
            P.F27 * M26, cap_r + nN * H_EXPERT * 60 / (E.aR * (1 + f)))
        out["%d per cent more load for the new share, pooled handle time" % u] = max(
            0.0, (P.F27 * M26 * (1 + f * nN / (nR + nN)) * A26 / 60 - (nR + nN) * H_EXPERT) / H_BILLED)
    out["textbook first-contact resolution of 75 per cent"] = B_contacts(P.F27 * (1 + 1 / 3), Kg)
    out["textbook first-contact resolution of 70 per cent"] = B_contacts(P.F27 * (1 + 0.3 / 0.7), Kg)
    # the old system's follow-ups per new ticket, carried onto 2027
    bt = backtest(P, E)
    old_fn = np.mean([r["observed"] for r in bt["fortnight"]])
    out["old system's fortnight follow-ups per new ticket, 2021 to 2025"] = B_contacts(P.F27 * (1 + old_fn), Kg)
    out["old system's 2025 fortnight follow-ups per new ticket"] = B_contacts(
        P.F27 * (1 + bt["fortnight"][-1]["observed"]), Kg)
    # last season's outsourcer hours, scaled by the demand plan
    inv26 = invoiced_hours_2026(P.target)
    out["last season's outsourcer hours scaled by the new cases"] = inv26 * P.F27 / P.F26
    # the customer survey's answers as the resolution
    cs = csat_answered(P)
    if cs:
        uR, uN, uV, uF = cs
        out["survey's unanswered share as the follow-up chance"] = solve_booking(
            *inhouse(P, lambda x: uN, lambda x: expo(x, *E.ca), uR, E.aR), uV, E.aO, uF, P.F27)
    return out, g


def invoiced_hours_2026(target):
    import re
    txt = pdf_text(os.path.join(target, "hcs_invoices_2026_deadline_period.pdf"))
    tot = {}
    for block in re.split(r"(?=INVOICE HCS-)", txt)[1:]:
        no = re.match(r"INVOICE (HCS-\d\d-\d{4})", block).group(1)
        m = re.search(r"Total hours\s+([\d,.]+)", block)
        rep = re.search(r"replaces invoice (HCS-\d\d-\d{4})", block)
        tot[no] = (float(m.group(1).replace(",", "")), rep.group(1) if rep else None)
    replaced = {r for _, r in tot.values() if r}
    return sum(h for no, (h, r) in tot.items() if no not in replaced)


def csat_answered(P):
    """The survey's No to 'Did the expert answer your question?', by the group of the interaction's expert, for
    new-case interactions, and for follow-ups."""
    path = os.path.join(P.target, "csat_survey_responses_2026.csv")
    rows = _read_csv(path)
    head = rows[0]
    ix = {c: i for i, c in enumerate(head)}
    if not hasattr(P, "iid"):
        return None
    pos = {k: i for i, k in enumerate(P.iid)}
    vals = {"R": [], "N": [], "V": [], "F": []}
    for r in rows[1:]:
        i = pos.get(r[ix["Interaction ID"]])
        if i is None:
            continue
        no = r[ix["Did the expert answer your question?"]] == "No"
        if P.first[i]:
            vals[P.grp[i]].append(no)
        else:
            vals["F"].append(no)
    return tuple(float(np.mean(vals[k])) for k in ("R", "N", "V", "F"))


# ------------------------------------------------------------------------------------------------- back-test
def old_rows(target):
    rows = []
    for f, cols in (("ticketing_agent_weekly_2021_2022.csv",
                     ("Season", "Week Starting", "Agent Code", "Team", "New Tickets", "Follow-up Tickets")),
                    ("ticketing_agent_weekly_2023_2025.csv",
                     ("season", "week_start", "agent_code", "team", "tickets_new", "tickets_followup"))):
        data = _read_csv(os.path.join(target, f))
        ix = {c: i for i, c in enumerate(data[0])}
        for r in data[1:]:
            ws = r[ix[cols[1]]]
            d = dt.datetime.strptime(ws, "%m/%d/%Y").date() if "/" in ws else dt.date.fromisoformat(ws)
            rows.append((int(r[ix[cols[0]]]), d, r[ix[cols[2]]], r[ix[cols[3]]], int(r[ix[cols[4]]]),
                         int(r[ix[cols[5]]])))
    return rows


def backtest(P, E):
    """The 2026 fit carried back onto 2021 to 2025: each season's (and each deadline fortnight's) follow-up tickets
    per new ticket on the English queue, against the tenure model's prediction from that season's own mix of who
    took the new tickets, and against carrying the 2026 rate."""
    hist = _read_csv(os.path.join(P.target, "seasonal_expert_history.csv"))
    ix = {c: i for i, c in enumerate(hist[0])}
    info = {(r[ix["old_agent_code"]], int(r[ix["season"]])): r for r in hist[1:] if r[ix["old_agent_code"]]}
    rows = old_rows(P.target)
    M26 = (E.fn.sum() / (E.fn & P.first).sum()) - 1

    def p_of(y, d, code):
        if code.startswith("EXT-"):
            return E.pO
        h = info[(code, y)]
        if int(h[ix["first_season"]]) < y:
            return E.pR
        gl = dt.date.fromisoformat(h[ix["go_live"]])
        return float(expo(max(((d + dt.timedelta(3)) - gl).days / 7.0, 0.0), *E.cp))
    out = {"fortnight": [], "season": [], "rate26": M26}
    for y in K.SEASONS_OLD:
        f0, f1 = K.fortnight(y)
        for key, sel in (("fortnight", [r for r in rows if r[0] == y and f0 <= r[1] <= f1]),
                         ("season", [r for r in rows if r[0] == y])):
            sel = [r for r in sel if r[3].startswith("EN") or r[3] == "HCS"]
            new = sum(r[4] for r in sel)
            fu = sum(r[5] for r in sel)
            pb = sum(r[4] * p_of(y, r[1], r[2]) for r in sel) / new
            obs = fu / new
            out[key].append(dict(season=y, new=new, followups=fu, observed=obs, model=pb / (1 - E.q), rate26=M26,
                                 err_model=100 * (pb / (1 - E.q) / obs - 1), err_rate=100 * (M26 / obs - 1)))
    return out


def report(target, F_override=None):
    P = Pack(target)
    if F_override:
        P.F27 = F_override
    E = Est(P)
    g = golden(P, E)
    cons = constructions(P, E)
    rv, _ = rivals(P, E)
    return P, E, g, cons, rv


# ------------------------------------------------------------------------------------------------- sampling error
def _est_idx(P, idx):
    class _E:
        pass
    E = _E()
    g, first, fol, wk, hm = P.grp[idx], P.first[idx], P.followed[idx].astype(float), P.wk[idx], P.hmin[idx]
    R, N, V = g == "R", g == "N", g == "V"
    E.pR = fol[R & first].mean(); E.pO = fol[V & first].mean(); E.q = fol[~first].mean()
    E.aR = hm[R].mean(); E.aO = hm[V].mean()
    E.cp = fit_expo(wk[N & first], fol[N & first], (0.14, 0.3, 5.0))
    E.ca = fit_expo(wk[N], hm[N], (31.0, 14.0, 5.0))
    return E


def bootstrap(P, n=200, seed=173):
    """Resample experts with replacement within the returning, first-season and vendor groups; the booking's spread
    across the resamples is the golden's one sigma."""
    R = np.random.default_rng(seed)
    order = np.argsort(P.handled, kind="stable")
    hs = P.handled[order]
    u, starts = np.unique(hs, return_index=True)
    ends = np.r_[starts[1:], len(hs)]
    rows_of = {k: order[s0:s1] for k, s0, s1 in zip(u, starts, ends)}
    grp_of = {k: P.grp[rows_of[k][0]] for k in u}
    groups = {gname: [k for k in u if grp_of[k] == gname] for gname in "RNV"}
    out = []
    for _ in range(n):
        idx = np.concatenate([np.concatenate([rows_of[k] for k in R.choice(ids, size=len(ids), replace=True)])
                              for ids in groups.values()])
        E = _est_idx(P, idx)
        Kc, Kp = inhouse(P, lambda x: expo(x, *E.cp), lambda x: expo(x, *E.ca), E.pR, E.aR)
        out.append(solve_booking(Kc, Kp, E.pO, E.aO, E.q, P.F27))
    return float(np.std(out)), np.array(out)
