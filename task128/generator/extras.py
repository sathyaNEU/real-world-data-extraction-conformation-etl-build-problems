"""Everything the outcome model does not decide, drawn from a second stream so it never moves a list, a dial or a
roll: account numbers and opening dates, balances, each dialled record's result and attempts, the arrangements,
the delinquency history by cycle date, the capacity log, the QA team's test calls and the treasury's booking rates."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

RPC_MIX = (("PTP", 0.38), ("ARR", 0.22), ("RTP", 0.14), ("CBK", 0.08), ("RPC", 0.18))
NC_MIX = (("NOA", 0.46), ("MACH", 0.34), ("BSY", 0.08), ("WRN", 0.07), ("DIS", 0.05))
BAL_MEAN = {"VCL": 2900.0, "VGD": 5200.0, "VIF": 8800.0, "VSD": 1350.0, "VUSD": 3300.0}
AGENTS = {"TBY": 4, "SUD": 5, "KGN": 9, "LON": 7, "WPG": 9}
POD_MERGE = dt.date(2025, 9, 2)         # London's two pods become one team


def pick(rng, n, mix):
    codes = np.array([c for c, _ in mix])
    w = np.array([p for _, p in mix])
    return codes[rng.choice(len(codes), n, p=w / w.sum())]


def luhn(digits):
    s = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return str((10 - s % 10) % 10)


def account_numbers(A, rng):
    """Account numbers issued in opening order, gaps of a few numbers where other products took the next ones."""
    opened = open_dates(A, rng)
    order = np.argsort(np.array([d.toordinal() for d in opened]) * 4.0 + rng.random(len(A)), kind="stable")
    gaps = rng.geometric(0.42, len(A))
    seq = 31104000 + np.cumsum(gaps)
    num = np.empty(len(A), object)
    for rank, i in enumerate(order):
        body = "4%09d" % seq[rank]
        num[i] = body + luhn(body)
    return num, opened


def open_dates(A, rng):
    n = len(A)
    out = np.empty(n, object)
    base = dt.date(2003, 1, 1).toordinal()
    span = dt.date(2024, 6, 30).toordinal() - base
    x = rng.random(n) ** 0.7
    ords = (base + x * span).astype(int)
    camp = A.camp.values
    cords = dt.date(2024, 8, 1).toordinal() + rng.integers(0, 110, n)
    usd = (A["product"].values == "VUSD")
    ords = np.where(camp, cords, ords)
    ords = np.where(usd, np.maximum(ords, dt.date(2009, 3, 1).toordinal()), ords)
    for i in range(n):
        out[i] = dt.date.fromordinal(int(ords[i]))
    return out


def booking_rates(rng):
    """Ferncliffe Treasury's daily USD/CAD booking rate, business days January 2025 to October 2026."""
    days = [d for (y, m) in W.MONTHS for d in W.bdays(y, m) if d <= dt.date(2026, 10, 8)]
    x = np.log(1.4352)
    out = []
    drift = {2025: -0.00011, 2026: 0.00002}
    for d in days:
        x += drift[d.year] + rng.normal(0, 0.0031)
        out.append((d, round(float(np.exp(x)), 4)))
    return pd.DataFrame(out, columns=["day", "rate"])


def shift_minutes(rank, cap, rng):
    """Minutes after 08:00 local of a record's first attempt, the list worked in load order through the shift."""
    frac = (rank - 1 + rng.random(len(rank))) / np.maximum(cap, 1)
    return np.clip(frac * 690 + rng.normal(0, 4, len(rank)), 0, 714)


def results(E, rng):
    """Each dialled record's final result and its attempts. Before a centre's dialler upgrade an arrangement was
    coded AR and a machine AM; from the upgrade an arrangement is ARR and AR is a machine with a message left."""
    E = E.copy()
    n = len(E)
    up = np.array([W.UPGRADE[W.CODES[c]] for c in E.centre.values])
    pre = np.array([d < u for d, u in zip(E.day.values, up)])
    code = np.full(n, "", object)
    code[E.skipped.values & (E.skip.values == 1)] = "DNC"
    code[E.skipped.values & (E.skip.values == 2)] = "NDN"
    d = E.dialled.values
    r = E.reached.values
    rp = np.empty(n, object)
    for c in range(5):
        k = W.PTP_SHARE[c]
        mix = [("PTP", k)] + [(a, b * (1 - k) / 0.62) for a, b in RPC_MIX if a != "PTP"]
        m = E.centre.values == c
        rp[m] = pick(rng, int(m.sum()), mix)
    nc = pick(rng, n, NC_MIX)
    code[d & r] = rp[d & r]
    code[d & ~r] = nc[d & ~r]
    arr = code == "ARR"
    mach = code == "MACH"
    code[arr & pre] = "AR"
    code[mach & pre] = "AM"
    code[mach & ~pre] = "AR"
    E["code"] = code
    E["pre"] = pre
    k = np.zeros(n, int)
    rk = rng.choice([1, 2, 3], n, p=[0.6, 0.28, 0.12])
    ends = np.isin(nc, ["WRN", "DIS"])
    nk = np.where(ends, rng.choice([1, 2], n, p=[0.7, 0.3]), 3)
    k[d & r] = rk[d & r]
    k[d & ~r] = nk[d & ~r]
    E["attempts"] = k
    return E


TALK = {"PTP": (150, 520), "ARR": (330, 960), "RTP": (70, 260), "CBK": (35, 140), "RPC": (60, 320), "WRN": (12, 75)}


def attempts(E, caps_day, rng):
    """One row per dial in the review year: each dialled record's attempts in order, earlier ones without contact."""
    D = E[E.dialled & (E.day >= W.YEAR_FROM) & (E.day <= W.YEAR_TO)].copy()
    first = shift_minutes(D.dial_rank.values, D.cap.values, rng)
    rows = []
    agents = {c: ["%s%04d" % (c[:2], 1000 + 37 * i + int(rng.integers(0, 30))) for i in range(AGENTS[c])] for c in W.CODES}
    for idx, (code, k, pre, c, t0) in enumerate(zip(D.code.values, D.attempts.values, D.pre.values, D.centre.values, first)):
        cc = W.CODES[c]
        t = t0
        for a in range(1, k + 1):
            final = a == k
            if final:
                rc = code
            else:
                rc = rng.choice(["NOA", "MACH", "BSY"], p=[0.6, 0.32, 0.08])
                rc = ("AM" if pre else "AR") if rc == "MACH" else rc
            if rc in TALK or (rc == "AR" and pre):
                lo, hi = TALK["ARR"] if rc == "AR" else TALK[rc]
                talk = int(rng.integers(lo, hi))
                agent = agents[cc][int(rng.integers(0, len(agents[cc])))]
            elif rc == "AR":
                talk, agent = int(rng.integers(19, 44)), ""
            else:
                talk, agent = 0, ""
            rows.append((idx, a, round(float(t), 2), rc, talk, agent))
            t = t + 95 + rng.random() * 150 + talk / 60.0
            if t > 714:
                t = 714 - rng.random() * 8
    R = pd.DataFrame(rows, columns=["i", "attempt", "minute", "code", "talk", "agent"])
    R = R.merge(D[["acct", "centre", "day", "pre"]].reset_index(drop=True).reset_index().rename(columns={"index": "i"}), on="i")
    return R, agents


DIALS_PER_SEAT = 46.0


def balances(A, E, rng, rates):
    """Each entry's balance in the account's own currency (US dollars on the US-dollar card) and in Canadian dollars."""
    base = np.array([BAL_MEAN[p] for p in A["product"].values]) * rng.lognormal(-0.18, 0.6, len(A))
    E = E.copy()
    bal = base[E.acct.values] * rng.lognormal(0, 0.08, len(E))
    E["bal"] = np.round(np.maximum(bal, 120.0), 2)
    E["usd"] = A["product"].values[E.acct.values] == "VUSD"
    rmap = dict(zip(rates.day, rates.rate))
    fx = np.array([rmap[d] for d in E.day.values])
    E["fx"] = fx
    E["bal_cad"] = np.round(np.where(E.usd.values, E.bal.values * fx, E.bal.values), 2)
    E["dpd0"] = 30 + rng.integers(0, 3, len(E))
    return E


def next_bday(d, k=1):
    out = d
    while k > 0:
        out += dt.timedelta(1)
        if out.weekday() < 5 and out not in W.HOLIDAYS:
            k -= 1
    return out


def arrangements(E, rng, agents):
    """Arrangements the early-stage teams set up: on the call (arrangement result) and on a customer's callback."""
    lo, hi = dt.date(2025, 1, 2), dt.date(2026, 9, 30)
    arr = E[E.code.isin(["ARR"]) | ((E.code == "AR") & E.pre)].copy()
    lag = np.where(rng.random(len(arr)) < 0.08, 1, 0)
    arr["setup"] = [next_bday(d, k) if k else d for d, k in zip(arr.day.values, lag)]
    cb = E[E.code == "CBK"].copy()
    cb = cb[rng.random(len(cb)) < 0.30]
    cb["setup"] = [next_bday(d, int(k)) for d, k in zip(cb.day.values, rng.choice([1, 2], len(cb), p=[0.75, 0.25]))]
    R = pd.concat([arr, cb], ignore_index=True)
    R = R[(R.setup >= lo) & (R.setup <= hi)].copy()
    R["agent"] = [agents[W.CODES[c]][int(rng.integers(0, len(agents[W.CODES[c]])))] for c in R.centre.values]
    R["instalments"] = rng.choice([2, 3, 4, 5, 6], len(R), p=[0.18, 0.34, 0.24, 0.14, 0.10])
    R["freq"] = np.where(rng.random(len(R)) < 0.72, "MONTHLY", "BIWEEKLY")
    R["first_due"] = [s + dt.timedelta(int(k)) for s, k in zip(R.setup.values, rng.integers(7, 22, len(R)))]
    R["arr_bal"] = np.round(R.bal.values * rng.uniform(0.97, 1.0, len(R)) * np.array(W.ARR_K)[R.centre.values], 2)
    step = np.where(R.freq.values == "MONTHLY", 30, 14)
    end = [f + dt.timedelta(int(s * (n - 1))) for f, s, n in zip(R.first_due.values, step, R.instalments.values)]
    broke = R.roll.values | (rng.random(len(R)) < 0.18)
    R["status"] = np.where(broke, "BROKEN", np.where(np.array(end) <= W.PULL, "COMPLETED", "ACTIVE"))
    R = R.sort_values(["setup", "centre", "acct"]).reset_index(drop=True)
    R["ref"] = ["PA%09d" % (204118000 + i * 3 + int(g)) for i, g in enumerate(rng.integers(0, 3, len(R)))]
    return R


def history(E, rng):
    """The delinquency history by cycle date for every 30-day entry: 30 days past due on the entry, then each later
    cycle date while the account stays delinquent, counted in the platform's cycle buckets (30, 60, 90 and so on plus
    the days since the cycle's due date); a roll reaches 90 two cycle dates on, and charges off at 180."""
    rows = []
    for e in E.itertuples(index=False):
        y, m = e.day.year, e.day.month
        dpd0 = int(e.dpd0)
        steps = []
        if e.roll:
            steps = [(1, 60), (2, 90), (3, 120), (4, 150), (5, 180)]
        else:
            u = rng.random()
            if u < 0.20:
                steps = [(1, 30)] + ([(2, 30)] if rng.random() < 0.35 else [])
            elif u < 0.34:
                steps = [(1, 60)] + ([(2, 60)] if rng.random() < 0.55 else [])
        rows.append((e.acct, e.cycle, e.day, dpd0, e.bal_cad, "", e.hold))
        bal = e.bal_cad
        for j, bucket in steps:
            yy, mm = W.add_months(y, m, j)
            if (yy, mm) not in W.MONTHS:
                break
            cdt = W.collections_day(yy, mm, e.cycle)
            if cdt > dt.date(2026, 10, 8):
                break
            bal = round(bal * (1.0 + rng.uniform(0.012, 0.024)) if bucket >= 60 else bal * rng.uniform(0.94, 1.0), 2)
            dpd = dpd0 + (bucket - 30) + int(rng.integers(0, 3))
            rows.append((e.acct, e.cycle, cdt, dpd, bal, "CO" if bucket == 180 else "", ""))
    H = pd.DataFrame(rows, columns=["acct", "cycle", "cdt", "dpd", "bal_cad", "status", "hold"])
    return H


def capacity_log(E, rng):
    """The workforce and dialler log by centre and working day: seats, agent hours, records loaded, accounts dialled.
    London ran two pods until they merged; each pod logged its own seats and dials, the first pod the list it loaded."""
    L = E[E.onlist]
    g = L.groupby(["centre", "day"]).agg(loaded=("acct", "size"), dialled=("dialled", "sum"), cap=("cap", "first")).reset_index()
    rows = []
    for r in g.itertuples(index=False):
        cc = W.CODES[r.centre]
        seats = max(2, int(round(r.cap / DIALS_PER_SEAT + rng.normal(0, 0.25))))
        hrs = round(seats * 7.5 - rng.choice([0, 0, 0, 0.5, 1.0, 3.75]), 2)
        ver = "PD8.4" if r.day < W.UPGRADE[cc] else "CX2.1"
        if cc == "LON" and r.day < POD_MERGE:
            sa = int(np.ceil(seats / 2)); sb = seats - sa
            da = int(round(r.dialled * sa / seats))
            ha = round(hrs * sa / seats, 2)
            rows.append((r.day, cc, "LON-A", ver, sa, ha, r.loaded, da))
            rows.append((r.day, cc, "LON-B", ver, sb, round(hrs - ha, 2), None, int(r.dialled) - da))
        else:
            rows.append((r.day, cc, cc, ver, seats, hrs, r.loaded, int(r.dialled)))
    return pd.DataFrame(rows, columns=["day", "centre", "team", "ver", "seats", "hours", "loaded", "dialled"])


def test_calls(rng, agents):
    """The QA team's test calls to the dialler's test accounts, a few a working day at each centre, review year only."""
    rows = []
    test_accts = {c: ["4000%06d" % (100 + 11 * i) for i in range(3)] for c in W.CODES}
    days = [d for (y, m) in W.MONTHS for d in W.bdays(y, m) if W.YEAR_FROM <= d <= W.YEAR_TO]
    for d in days:
        for c in W.CODES:
            for _ in range(int(rng.integers(1, 4))):
                code = rng.choice(["RPC", "PTP", "NOA", "CBK"], p=[0.5, 0.3, 0.1, 0.1])
                rows.append((d, c, rng.choice(test_accts[c]), float(rng.uniform(5, 700)), code,
                             int(rng.integers(20, 95)) if code != "NOA" else 0,
                             agents[c][0] if code != "NOA" else ""))
    return pd.DataFrame(rows, columns=["day", "centre", "acct_no", "minute", "code", "talk", "agent"])


def ls60_summary(H, A_centre, rng):
    """The late-stage (60-day) team's daily list summary by centre, from the accounts 60 days past due on a cycle date."""
    h = H[(H.dpd >= 60) & (H.dpd < 90)].copy()
    h["centre"] = A_centre[h.acct.values]
    g = h.groupby(["centre", "cdt"]).size().reset_index(name="loaded")
    g = g[(g.cdt >= dt.date(2025, 1, 2)) & (g.cdt <= dt.date(2026, 9, 30))]
    g["dialled"] = np.round(g.loaded * rng.uniform(0.82, 0.97, len(g))).astype(int)
    g["rpc"] = rng.binomial(g.dialled.values, 0.31)
    g["ptp"] = rng.binomial(g.rpc.values, 0.36)
    return g


def headcount(rng):
    """Collections workforce by centre and quarter (every collections role, not only the 30-day teams)."""
    rows = []
    base = {"TBY": 31, "SUD": 38, "KGN": 52, "LON": 74, "WPG": 61}
    qs = [(2025, q) for q in (1, 2, 3, 4)] + [(2026, q) for q in (1, 2, 3)]
    for c in W.CODES:
        h = base[c]
        for (y, q) in qs:
            h = max(10, h + int(rng.integers(-3, 4)))
            vac = int(rng.integers(0, 6))
            leavers = int(rng.integers(1, 7))
            rows.append(("%d Q%d" % (y, q), W.NAMES[c], h, vac, leavers, round(100.0 * leavers / h, 1)))
    return pd.DataFrame(rows, columns=["quarter", "centre", "headcount", "vacancies", "leavers", "attrition_pct"])
