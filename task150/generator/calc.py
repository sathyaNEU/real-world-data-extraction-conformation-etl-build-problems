"""Every figure the build owes, computed from the shipped files under target/ alone (no generator state): the pupils
linked across the two membership layouts, the between-October flows, the golden gross-flow projection and every
construction of it, the default and every rival, the back-test from 2019, the sampling error, the placement under
Policy FEA-R2, and both asks with their stops."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re

import numpy as np
import openpyxl

import asks as AS
import docs as DOC
import records as R

G = 6
LAST = 2026
FUT = list(range(2027, 2033))
WIN = list(range(2028, 2033))
SEATS, SITE_CAP, TOTAL = 24, 8, 24
ALLW = list(range(2014, 2027))
W8 = list(range(2019, 2027))
W5 = list(range(2022, 2027))
W3 = list(range(2024, 2027))
W10 = list(range(2017, 2027))
OCT1 = dt.date(2026, 10, 1)


class Data:
    pass


def _d(s):
    return dt.date.fromisoformat(s) if s else None


def load(target, link="crosswalk", drop_legacy=False):
    """The October rolls keyed by pupil: legacy rows by the state ID their student number converted to (the
    crosswalk), or by the legacy number for pupils who left before 2018-19; current rows by state ID."""
    D = Data()
    with open(os.path.join(target, R.F_CODES), encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    D.codes = [r["state_school_code"] for r in rows]
    D.names = [r["school_name"] for r in rows]
    D.NS = len(rows)
    area = {r["attendance_area"]: i for i, r in enumerate(rows)}
    leg = {r["legacy_school_code"]: i for i, r in enumerate(rows)}
    st = {r["state_school_code"]: i for i, r in enumerate(rows)}
    xw = {}
    with open(os.path.join(target, R.F_XWALK), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            xw[r["STU_NBR"]] = r["STATE_ID"]
    D.snap = {}
    D.rows = {}
    if not drop_legacy:
        with open(os.path.join(target, R.F_LEGACY), encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter="|"):
                y = int(r["SCHL_YR"][:4])
                if link == "crosswalk":
                    key = xw.get(r["STU_NBR"], "L" + r["STU_NBR"])
                else:                         # the mishandling: the SASID on the row, the legacy number where blank
                    key = r["SASID"] or "L" + r["STU_NBR"]
                g = 0 if r["GRADE"] == "KG" else int(r["GRADE"])
                D.snap.setdefault(y, {})[key] = (leg[r["SCH_CD"]], g)
                D.rows[y] = D.rows.get(y, 0) + 1
    with open(os.path.join(target, R.F_MEMBERS), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            y = int(r["school_year"][:4])
            D.snap.setdefault(y, {})[r["student_id"]] = (st[r["school_code"]], int(r["grade_level"]))
            D.rows[y] = D.rows.get(y, 0) + 1
    D.years = sorted(D.snap)
    D.E = {}
    for y in D.years:
        E = np.zeros((D.NS, G))
        for (i, g) in D.snap[y].values():
            E[i, g] += 1
        D.E[y] = E
    D.births = {i: {} for i in range(D.NS)}
    D.births_other = {}
    with open(os.path.join(target, R.F_BIRTHS), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["attendance_area"] in area:
                D.births[area[r["attendance_area"]]][int(r["birth_year"])] = int(r["births"])
            else:
                D.births_other.setdefault(r["attendance_area"], {})[int(r["birth_year"])] = int(r["births"])
    D.cap = read_capacity(target, D)
    return D


def read_capacity(target, D):
    p = os.path.join(target, DOC.F_CAPACITY)
    if not os.path.exists(p):
        return None
    ws = openpyxl.load_workbook(p, data_only=True).active
    hdr = None
    cap = {}
    for row in ws.iter_rows(values_only=True):
        if hdr is None:
            if row and "Rated capacity (K-5)" in row:
                hdr = list(row)
            continue
        if not row or row[0] is None:
            break
        cap[str(row[hdr.index("State code")])] = int(row[hdr.index("Rated capacity (K-5)")])
    return np.array([cap[c] for c in D.codes], dtype=float)


# ---------------------------------------------------------------------------------------------------- flows
def flows(D):
    """Between each October and the next: pupils in K to 4 at each school (the base), those not on the next roll
    (exits), those on it at another school (moves, by destination), those on it in the same grade (repeats), and the
    pupils new to the roll (kindergarten entrants, arrivals into grades 1 to 5)."""
    F = {}
    NS = D.NS
    for y in D.years[1:]:
        prev, now = D.snap[y - 1], D.snap[y]
        base = np.zeros(NS)
        out = np.zeros(NS)
        mv = np.zeros((NS, NS))
        ret = np.zeros((NS, G))
        arr = np.zeros((NS, G))
        kent = np.zeros(NS)
        base_g = np.zeros((NS, G))
        out_g = np.zeros((NS, G))
        mv_g = np.zeros((NS, NS, G))
        for key, (s, g) in prev.items():
            if g == G - 1:
                continue
            base[s] += 1
            base_g[s, g] += 1
            nxt = now.get(key)
            if nxt is None:
                out[s] += 1
                out_g[s, g] += 1
            elif nxt[0] != s:
                mv[s, nxt[0]] += 1
                mv_g[s, nxt[0], g] += 1
            elif nxt[1] == g:
                ret[s, g] += 1
        for key, (s, g) in now.items():
            if key not in prev:
                if g >= 1:
                    arr[s, g] += 1
                else:
                    kent[s] += 1
        F[y] = dict(base=base, out=out, mv=mv, ret=ret, arr=arr, kent=kent, base_g=base_g, out_g=out_g, mv_g=mv_g)
    return F


def births_proj(D, i, y, how="avg3"):
    if y <= 2025:
        return float(D.births[i][y])
    if how == "avg3":
        return float(np.mean([D.births[i][t] for t in (2023, 2024, 2025)]))
    if how == "last":
        return float(D.births[i][2025])
    if how == "trend":
        xs = np.arange(2019, 2026)
        vs = np.array([D.births[i][t] for t in xs], dtype=float)
        return float(np.polyval(np.polyfit(xs, vs, 1), y))
    if how == "complete2025":
        b = {t: D.births[i][t] * (1.016 if t == 2025 else 1.0) for t in (2023, 2024, 2025)}
        if y <= 2025:
            return b[y]
        return float(np.mean(list(b.values())))
    raise ValueError(how)


def gross_params(D, F, rwin, kwin, awin=None, kmode="ros", bygrade=False):
    NS = D.NS
    awin = awin or rwin
    base = sum(F[y]["base"] for y in rwin)
    mvr = sum(F[y]["mv"] for y in rwin) / base[:, None]
    outr = sum(F[y]["out"] for y in rwin) / base
    if bygrade:
        bg = sum(F[y]["base_g"] for y in rwin)
        outr = sum(F[y]["out_g"] for y in rwin)[:, :G - 1] / bg[:, :G - 1]
        mvr = sum(F[y]["mv_g"] for y in rwin)[:, :, :G - 1] / bg[:, None, :G - 1]
    retr = np.zeros((NS, G))
    for i in range(NS):
        for g in range(G - 1):
            retr[i, g] = sum(F[y]["ret"][i, g] for y in rwin) / sum(D.E[y - 1][i, g] for y in rwin)
    arrc = sum(F[y]["arr"] for y in awin) / len(awin)
    if kmode == "ros":
        kr = np.array([sum(F[y]["kent"][i] for y in kwin) / sum(D.births[i][y - 5] for y in kwin) for i in range(NS)])
    else:
        kr = np.array([np.mean([F[y]["kent"][i] / D.births[i][y - 5] for y in kwin]) for i in range(NS)])
    mvcount = sum(F[y]["mv"] for y in rwin) / len(rwin)
    return dict(mvr=mvr, outr=outr, retr=retr, arrc=arrc, kr=kr, mvcount=mvcount, awin=awin)


def roll_gross(D, P0, prm, bhow="avg3", internal="od", external="count", years=None, births=None):
    """The cohort roll: each grade's pupils repeat, promote, move or leave at the rates of the school they are at;
    kindergartens from births five years earlier; arrivals into grades 1 to 5 as each school's count per grade."""
    NS = D.NS
    mvr, outr, retr, arrc, kr = prm["mvr"], prm["outr"], prm["retr"], prm["arrc"], prm["kr"]
    years = years or FUT
    cur = P0.copy()
    P = {years[0] - 1: cur.copy()}
    if external == "rate":
        hb = np.zeros((NS, G))
        for j in range(NS):
            for g in range(1, G):
                hb[j, g] = np.mean([D.E[t - 1][j, g - 1] for t in prm["awin"]])
    for y in years:
        nxt = np.zeros((NS, G))
        for i in range(NS):
            b = births[i][y - 5] if births is not None else births_proj(D, i, y - 5, bhow)
            nxt[i, 0] = kr[i] * b
        bygrade = np.ndim(outr) == 2
        for i in range(NS):
            for g in range(G - 1):
                n = cur[i, g]
                o = outr[i, g] if bygrade else outr[i]
                m = mvr[i, :, g] if bygrade else mvr[i]
                nxt[i, g] += n * retr[i, g]
                nxt[i, g + 1] += n * (1.0 - m.sum() - o - retr[i, g])
                if internal == "od":
                    for j in range(NS):
                        if j != i:
                            nxt[j, g + 1] += n * m[j]
        if internal != "od":
            tot_in = prm["mvcount"].sum(axis=0)
            for j in range(NS):
                for g in range(1, G):
                    nxt[j, g] += tot_in[j] / 5.0
        for j in range(NS):
            for g in range(1, G):
                if external == "count":
                    nxt[j, g] += arrc[j, g]
                else:
                    nxt[j, g] += cur[j, g - 1] * arrc[j, g] / hb[j, g]
        P[y] = nxt.copy()
        cur = nxt
    return P


def proj_gross(D, F, rwin=ALLW, kwin=ALLW, bhow="avg3", internal="od", external="count", awin=None, kmode="ros",
               bygrade=False):
    prm = gross_params(D, F, rwin, kwin, awin, kmode, bygrade)
    return roll_gross(D, D.E[LAST], prm, bhow, internal, external)


def gpr_params(D, win, kwin=None, mor=False):
    NS = D.NS
    kwin = kwin or win
    gpr = np.zeros((NS, G))
    for i in range(NS):
        for g in range(1, G):
            if mor:
                gpr[i, g] = np.mean([D.E[y][i, g] / D.E[y - 1][i, g - 1] for y in win])
            else:
                gpr[i, g] = sum(D.E[y][i, g] for y in win) / sum(D.E[y - 1][i, g - 1] for y in win)
    kr = np.array([sum(D.E[y][i, 0] for y in kwin) / sum(D.births[i][y - 5] for y in kwin) for i in range(NS)])
    return gpr, kr


def proj_gpr(D, win, kwin=None, mor=False, bhow="avg3"):
    """Grade progression ratios: next October's grade g+1 over this October's grade g, summed over the window; the
    kindergarten as the window's kindergarten-to-births ratio times births five years earlier."""
    gpr, kr = gpr_params(D, win, kwin, mor)
    cur = D.E[LAST].copy()
    P = {LAST: cur.copy()}
    for y in FUT:
        nxt = np.zeros((D.NS, G))
        for i in range(D.NS):
            nxt[i, 0] = kr[i] * births_proj(D, i, y - 5, bhow)
            for g in range(1, G):
                nxt[i, g] = cur[i, g - 1] * gpr[i, g]
        P[y] = nxt.copy()
        cur = nxt
    return P


def proj_gpr_trend(D, win):
    _, kr = gpr_params(D, win)
    coef = {}
    for i in range(D.NS):
        for g in range(1, G):
            vs = np.array([D.E[y][i, g] / D.E[y - 1][i, g - 1] for y in win])
            coef[i, g] = np.polyfit(np.array(win, dtype=float), vs, 1)
    cur = D.E[LAST].copy()
    P = {LAST: cur.copy()}
    for y in FUT:
        nxt = np.zeros((D.NS, G))
        for i in range(D.NS):
            nxt[i, 0] = kr[i] * births_proj(D, i, y - 5)
            for g in range(1, G):
                nxt[i, g] = cur[i, g - 1] * float(np.polyval(coef[i, g], y))
        P[y] = nxt.copy()
        cur = nxt
    return P


def proj_ccd(D, win):
    """Cohort change differences: next grade = this grade plus the window's mean difference."""
    _, kr = gpr_params(D, win)
    dif = np.zeros((D.NS, G))
    for i in range(D.NS):
        for g in range(1, G):
            dif[i, g] = np.mean([D.E[y][i, g] - D.E[y - 1][i, g - 1] for y in win])
    cur = D.E[LAST].copy()
    P = {LAST: cur.copy()}
    for y in FUT:
        nxt = np.zeros((D.NS, G))
        for i in range(D.NS):
            nxt[i, 0] = kr[i] * births_proj(D, i, y - 5)
            for g in range(1, G):
                nxt[i, g] = cur[i, g - 1] + dif[i, g]
        P[y] = nxt.copy()
        cur = nxt
    return P


def _district(D, win):
    Dd = {y: D.E[y].sum(axis=0) for y in D.years}
    gpr = np.array([0.0] + [sum(Dd[y][g] for y in win) / sum(Dd[y - 1][g - 1] for y in win) for g in range(1, G)])
    bt = {y: sum(D.births[i][y] for i in range(D.NS)) for y in range(2008, 2026)}
    kr = sum(Dd[y][0] for y in win) / sum(bt[y - 5] for y in win)
    return Dd, gpr, bt, kr


def proj_share(D, win):
    """A district projection by progression ratios, split by each school's mean share of the district."""
    Dd, gpr, bt, kr = _district(D, win)
    share = np.array([np.mean([D.E[y][i].sum() / Dd[y].sum() for y in win]) for i in range(D.NS)])
    cur = Dd[LAST].copy()
    P = {}
    for y in FUT:
        nxt = np.zeros(G)
        b5 = bt[y - 5] if y - 5 <= 2025 else np.mean([bt[t] for t in (2023, 2024, 2025)])
        nxt[0] = kr * b5
        for g in range(1, G):
            nxt[g] = cur[g - 1] * gpr[g]
        M = np.outer(share, nxt)
        P[y] = M * (nxt.sum() / M.sum())
        cur = nxt
    return P


def proj_control(D, Pschool, win):
    """School projections raked to a district total projected by district progression ratios."""
    Dd, gpr, bt, kr = _district(D, win)
    cur = Dd[LAST].copy()
    P = {}
    for y in FUT:
        nxt = np.zeros(G)
        b5 = bt[y - 5] if y - 5 <= 2025 else np.mean([bt[t] for t in (2023, 2024, 2025)])
        nxt[0] = kr * b5
        for g in range(1, G):
            nxt[g] = cur[g - 1] * gpr[g]
        P[y] = Pschool[y] * (nxt.sum() / Pschool[y].sum())
        cur = nxt
    return P


def avg5(D, P):
    return np.array([np.mean([P[y][i].sum() for y in WIN]) for i in range(D.NS)])


def allocate(D, avg, cap):
    """Policy FEA-R2 sections 2(e) and 3."""
    exc = avg - cap
    need = np.array([max(0, math.ceil(e / SEATS)) if e > 0 else 0 for e in exc])
    oct26 = D.E[LAST].sum(axis=1)
    order = sorted([i for i in range(D.NS) if exc[i] > 0], key=lambda i: (-exc[i], -oct26[i]))
    left = TOTAL
    alloc = np.zeros(D.NS, int)
    for i in order:
        take = min(need[i], SITE_CAP, left)
        alloc[i] = take
        left -= take
    return dict(avg=avg, exc=exc, need=need, alloc=alloc, left=left, order=order)


# ---------------------------------------------------------------------------------------------------- the ladder
def constructions(D, F):
    """Every defensible construction of the golden (C1): one schedule and one set of needs."""
    nowin = [y for y in ALLW if y != 2019]
    return {
        "all transitions": proj_gross(D, F),
        "last eight": proj_gross(D, F, W8, W8),
        "last five": proj_gross(D, F, W5, W5),
        "last three": proj_gross(D, F, W3, W3),
        "last ten": proj_gross(D, F, W10, W10),
        "rates all, kindergarten last five": proj_gross(D, F, ALLW, W5),
        "rates last five, kindergarten all": proj_gross(D, F, W5, ALLW),
        "births 2026-27 at 2025": proj_gross(D, F, bhow="last"),
        "births 2026-27 on the 2019-25 trend": proj_gross(D, F, bhow="trend"),
        "arrivals last five": proj_gross(D, F, awin=W5),
        "arrivals last three": proj_gross(D, F, awin=W3),
        "conversion year dropped": proj_gross(D, F, nowin, nowin),
        "kindergarten mean of ratios": proj_gross(D, F, kmode="mor"),
        "exits and moves by grade": proj_gross(D, F, bygrade=True),
    }


def rivals(D, F):
    R_ = {
        "five-year progression ratios (default)": proj_gpr(D, W5),
        "three-year progression ratios": proj_gpr(D, W3),
        "latest-year progression ratios": proj_gpr(D, [2026]),
        "eight-year progression ratios": proj_gpr(D, W8),
        "all-year progression ratios": proj_gpr(D, ALLW),
        "five-year mean of ratios": proj_gpr(D, W5, mor=True),
        "ratios trended over eight years": proj_gpr_trend(D, W8),
        "ratios trended over five years": proj_gpr_trend(D, W5),
        "cohort change differences, five years": proj_ccd(D, W5),
        "cohort change differences, all years": proj_ccd(D, ALLW),
        "district ratios split by school share": proj_share(D, W5),
        "arrivals as a share of the receiving class": proj_gross(D, F, external="rate"),
        "arrivals as a share, last five": proj_gross(D, F, W5, W5, external="rate"),
        "moves in as counts": proj_gross(D, F, internal="count"),
        "moves in as counts, last five": proj_gross(D, F, W5, W5, internal="count"),
        "moves in as counts, arrivals as a share": proj_gross(D, F, internal="count", external="rate"),
    }
    R_["five-year ratios raked to a district total"] = proj_control(D, R_["five-year progression ratios (default)"], W5)
    return R_


DEFAULT = "five-year progression ratios (default)"
GOLDEN = "all transitions"


def backtest(D, F, origin=2019):
    """Fitted on the transitions to the origin, projected from the origin's counts to 2026 with the births on file;
    each model's error at each school in 2026 (per cent of the actual count) and the mean absolute error."""
    yrs = [y for y in sorted(F) if y <= origin]
    w5 = yrs[-5:]
    prm = gross_params(D, F, yrs, yrs)
    gpr, kr5 = gpr_params(D, w5)
    years = list(range(origin + 1, LAST + 1))
    out = {}
    models = ("gross-flow", "five-year progression ratios", "moves in as counts", "arrivals as a share",
              "cohort change differences")
    for name in models:
        if name == "gross-flow":
            P = roll_gross(D, D.E[origin], prm, years=years, births=D.births)
        elif name == "moves in as counts":
            P = roll_gross(D, D.E[origin], prm, internal="count", years=years, births=D.births)
        elif name == "arrivals as a share":
            P = roll_gross(D, D.E[origin], prm, external="rate", years=years, births=D.births)
        else:
            cur = D.E[origin].copy()
            P = {}
            for y in years:
                nxt = np.zeros((D.NS, G))
                for i in range(D.NS):
                    nxt[i, 0] = kr5[i] * D.births[i][y - 5]
                    for g in range(1, G):
                        if name == "five-year progression ratios":
                            nxt[i, g] = cur[i, g - 1] * gpr[i, g]
                        else:
                            nxt[i, g] = cur[i, g - 1] + np.mean([D.E[t][i, g] - D.E[t - 1][i, g - 1] for t in w5])
                P[y] = nxt.copy()
                cur = nxt
        errs = np.array([(P[y].sum(axis=1) - D.E[y].sum(axis=1)) / D.E[y].sum(axis=1) * 100 for y in years])
        out[name] = dict(last=errs[-1], mape=np.abs(errs).mean(axis=0))
    return out


def bootstrap(D, F, cap, B=400, seed=7):
    """Parametric sampling error of each school's five-year excess: rates binomial on their bases, arrivals Poisson
    on their counts, kindergarten entrant ratios binomial on births."""
    NS = D.NS
    yrs = ALLW
    base = sum(F[y]["base"] for y in yrs)
    mvn = sum(F[y]["mv"] for y in yrs)
    outn = sum(F[y]["out"] for y in yrs)
    retn = np.zeros((NS, G))
    retd = np.zeros((NS, G))
    for i in range(NS):
        for g in range(G - 1):
            retn[i, g] = sum(F[y]["ret"][i, g] for y in yrs)
            retd[i, g] = sum(D.E[y - 1][i, g] for y in yrs)
    arrn = sum(F[y]["arr"] for y in yrs)
    kn = np.array([sum(F[y]["kent"][i] for y in yrs) for i in range(NS)])
    kd = np.array([sum(D.births[i][y - 5] for y in yrs) for i in range(NS)])
    r = np.random.default_rng(seed)
    exs = []
    for _ in range(B):
        mvr = np.zeros((NS, NS))
        outr = np.zeros(NS)
        for i in range(NS):
            p = np.concatenate([[outn[i]], mvn[i]]) / base[i]
            d = r.multinomial(int(base[i]), np.append(p, max(0.0, 1 - p.sum())))
            outr[i] = d[0] / base[i]
            mvr[i] = d[1:NS + 1] / base[i]
            mvr[i, i] = 0
        retr = np.where(retd > 0, r.binomial(retd.astype(int), np.where(retd > 0, retn / np.maximum(retd, 1), 0)) /
                        np.maximum(retd, 1), 0)
        arrc = r.poisson(arrn) / len(yrs)
        kr = np.array([r.binomial(int(kd[i]), min(1.0, kn[i] / kd[i])) / kd[i] for i in range(NS)])
        P = roll_gross(D, D.E[LAST], dict(mvr=mvr, outr=outr, retr=retr, arrc=arrc, kr=kr))
        exs.append(avg5(D, P) - cap)
    exs = np.array(exs)
    return exs.std(axis=0)


def flow_facts(D, F):
    """The in-sample facts the decisive step reads: each school's arrivals into grades 1 to 5 a year against its K-4
    base, and Ortega's moves to Bluestem and Kessler a year against Ortega's base."""
    yrs = ALLW
    out = {}
    for i in range(D.NS):
        arr = [F[y]["arr"][i].sum() for y in yrs]
        base = [F[y]["base"][i] for y in yrs]
        out[D.codes[i]] = dict(arr=arr, base=base)
    return out


# ---------------------------------------------------------------------------------------------------- the main call
def main_call(target, D=None, B=400):
    D = D or load(target)
    F = flows(D)
    C = constructions(D, F)
    Rv = rivals(D, F)
    res = {"D": D, "F": F}
    avgs = {k: avg5(D, P) for k, P in list(C.items()) + list(Rv.items())}
    res["avg"] = avgs
    res["P"] = dict(list(C.items()) + list(Rv.items()))
    if D.cap is not None:
        res["alloc"] = {k: allocate(D, a, D.cap) for k, a in avgs.items()}
        res["golden"] = res["alloc"][GOLDEN]
        res["default"] = res["alloc"][DEFAULT]
        res["sd"] = bootstrap(D, F, D.cap, B=B) if B else None
    res["constructions"] = list(C)
    res["rivals"] = list(Rv)
    res["backtest"] = backtest(D, F)
    return res


# ---------------------------------------------------------------------------------------------------- Ask A
def _band(course):
    return "K-2" if course in ("HR-K", "HR-1", "HR-2") else "3-5"


def read_sections(target):
    with open(os.path.join(target, AS.F_SECTIONS), encoding="utf-8", newline="") as f:
        secs = list(csv.DictReader(f))
    with open(os.path.join(target, AS.F_SECT_ENR), encoding="utf-8", newline="") as f:
        lines = list(csv.DictReader(f))
    return secs, lines


def ask_a(target, codes):
    """Homeroom classes meeting on October 1, 2026: homeroom sections running that day with at least one pupil line
    open that day, one class for each room and session; by the band of the sections' grades."""
    secs, lines = read_sections(target)
    live = {}
    for l in lines:
        st, en = _d(l["start_date"]), _d(l["end_date"])
        if st <= OCT1 and (en is None or en >= OCT1):
            live[l["section_id"]] = live.get(l["section_id"], 0) + 1
    hr = [s for s in secs if s["course_code"].startswith("HR-")]

    def running(s):
        return _d(s["section_start"]) <= OCT1 <= _d(s["section_end"])

    out = {}
    stops = {k: {} for k in ("sections running with pupils", "merged by teacher", "merged by room",
                             "every fall homeroom section", "classes without the pupil test")}
    bands_of_class = {}
    for c in codes:
        for b in ("K-2", "3-5"):
            mine = [s for s in hr if s["school_code"] == c and _band(s["course_code"]) == b]
            run = [s for s in mine if running(s) and live.get(s["section_id"], 0) > 0]
            out[(c, b)] = len({(s["room"], s["session"]) for s in run})
            stops["sections running with pupils"][(c, b)] = len(run)
            stops["merged by teacher"][(c, b)] = len({s["teacher_id"] for s in run})
            stops["merged by room"][(c, b)] = len({s["room"] for s in run})
            stops["every fall homeroom section"][(c, b)] = len(mine)
            stops["classes without the pupil test"][(c, b)] = len({(s["room"], s["session"]) for s in mine if running(s)})
        # every class (room and session) keeps its sections in one band
        for s in hr:
            if s["school_code"] == c and running(s) and live.get(s["section_id"], 0) > 0:
                bands_of_class.setdefault((c, s["room"], s["session"]), set()).add(_band(s["course_code"]))
    one_band = all(len(v) == 1 for v in bands_of_class.values())
    return dict(golden=out, stops=stops, one_band=one_band)


# ---------------------------------------------------------------------------------------------------- Ask B
ROOM = re.compile(r"^(Rm \d+)")


def read_preschool(target):
    with open(os.path.join(target, AS.F_PRESCHOOL), encoding="utf-8", newline="") as f:
        plat = list(csv.DictReader(f))
    ws = openpyxl.load_workbook(os.path.join(target, AS.F_ECSE), data_only=True).active
    hdr = None
    roster = []
    for row in ws.iter_rows(values_only=True):
        if hdr is None:
            if row and row[0] == "State ID":
                hdr = list(row)
            continue
        if row[0] is None:
            continue
        roster.append(dict(zip(hdr, row)))
    return plat, roster


def ask_b(target, names):
    """Children enrolled in each preschool site's classes on October 1, 2026 (the platform's enrollments open that day
    and the special education roster's children in the site's classrooms, each child once by state ID) and the
    classrooms those classes use."""
    plat, roster = read_preschool(target)

    def active(p):
        st, en = _d(p["enroll_start"]), _d(p["enroll_end"])
        return st <= OCT1 and (en is None or en >= OCT1)

    sites = sorted({p["site"] for p in plat}, key=lambda n: names.index(n))
    out = {}
    stops = {k: {} for k in ("platform child records and class names", "platform and roster added",
                             "union by state ID, class names as classrooms", "platform by state ID and room",
                             "union with the itinerant children")}
    for site in sites:
        pa = [p for p in plat if p["site"] == site and active(p)]
        ro = [x for x in roster if x["Case school"] == site and x["Service model"] in ("ECSE classroom",
                                                                                         "Inclusive classroom")]
        ro_all = [x for x in roster if x["Case school"] == site]
        kids = {p["state_id"] for p in pa} | {str(x["State ID"]) for x in ro}
        rooms = {ROOM.match(p["class_name"]).group(1) for p in pa} | {x["Classroom"] for x in ro}
        out[site] = dict(children=len(kids), classrooms=len(rooms))
        stops["platform child records and class names"][site] = dict(children=len({p["child_id"] for p in pa}),
                                                                       classrooms=len({p["class_name"] for p in pa}))
        stops["platform and roster added"][site] = dict(children=len({p["child_id"] for p in pa}) + len(ro_all),
                                                        classrooms=len(rooms))
        stops["union by state ID, class names as classrooms"][site] = dict(
            children=len(kids), classrooms=len({p["class_name"] for p in pa} | {x["Classroom"] for x in ro}))
        stops["platform by state ID and room"][site] = dict(children=len({p["state_id"] for p in pa}),
                                                            classrooms=len({ROOM.match(p["class_name"]).group(1)
                                                                            for p in pa}))
        stops["union with the itinerant children"][site] = dict(
            children=len({p["state_id"] for p in pa} | {str(x["State ID"]) for x in ro_all}), classrooms=len(rooms))
    return dict(golden=out, stops=stops, sites=sites)
