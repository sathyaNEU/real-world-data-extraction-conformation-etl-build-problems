"""Course-level truth for the Lyrevo safety database: who started when, which reaction began on which
day of which course, how it was reported, and how each case evolved until the extraction run."""
import datetime as dt
import math

import numpy as np

import shapes as S
import world as W

TD = dt.timedelta
LOCK = W.LOCK
EXPORT = W.EXPORT

# onset distributions (percent of reactions per 30-day month of the course), incidence per course
RISK_PARAMS = {
    "ild": dict(inc=0.010, maxd=705, salt=0.113,
                months=[2.33, 11.8, 14.8, 12.2, 10.5, 9, 7.6, 6.9, 4.8, 1.4, 1.0, 0.8, 0.8, 0.8, 0.9, 1.35, 1.2, 1.5, 2.13, 4.2, 1.17, 0.57, 0.25, 0.3]),
    "zoster": dict(inc=0.030, maxd=715, salt=0.271,
                   months=[1.4, 12.5, 15.5, 12.0, 9.5, 7.6, 6.2, 4.8, 3.6, 3.37, 5.0, 1.23, 1.0, 0.7, 0.7, 1.36, 1.1, 1.4, 1.73, 1.74, 3.73, 1.84, 0.44, 0.47]),
    "infection": dict(inc=0.030, maxd=700, salt=0.389,
                      months=[13, 25, 15.5, 10.79, 7.5, 5.85, 5.0, 2.46, 1.6, 1.0, 0.98, 0.73, 0.98, 0.85, 0.39, 0.36, 1.13, 3.2, 2.01, 1.04, 0.19, 0.16, 0.18, 0.1]),
    "vte": dict(inc=0.012, maxd=640, salt=0.457,
                months=[18.64, 25.28, 14, 10.31, 7.69, 4.58, 2.96, 1.79, 0.79, 0.68, 1.27, 1.2, 0.68, 0.88, 1.24, 3.72, 2.76, 0.69, 0.22, 0.21, 0.2, 0.22]),
    "hepatic": dict(inc=0.020, maxd=390, salt=0.523,
                    months=[24.46, 35.7, 17.52, 5.38, 3.38, 2.2, 2.21, 2.56, 4.08, 0.91, 0.9, 0.5, 0.2]),
    "neutropenia": dict(inc=0.018, maxd=360, salt=0.647,
                        months=[39.86, 37.87, 4.55, 3.8, 2.3, 2.29, 2.62, 3.94, 1.26, 0.91, 0.4, 0.2]),
}
TARGET_MONTHS = {"ild": (9, 20), "zoster": (11, 21), "infection": (7, 18), "vte": (6, 16), "hepatic": (4, 9),
                 "neutropenia": (3, 8)}

PSP_MARKETS = ("DE", "DK", "SE", "NO", "FI", "NL", "FR", "IT", "ES")
RESTART_SHARE = {"zoster": 0.25, "infection": 0.30}
ESCALATE_SHARE = {"vte": 0.45, "zoster": 0.08, "infection": 0.08, "hepatic": 0.05, "neutropenia": 0.05}
# chance of a short pause before onset per year of treatment before the reaction (capped at a year)
PAUSE_SHARE = {"vte": 0.16, "zoster": 0.40, "infection": 0.52, "hepatic": 0.16, "neutropenia": 0.16}
PSP_DATED_SHARE = 2.0 / 3.0
PARTIAL_ONSET = 0.07
PARTIAL_START = 0.02


def frac(v):
    return v - math.floor(v)


class Rng:
    """Seeded uniform stream for attributes that must be independent of the onset quantiles."""

    def __init__(self, *tag):
        self.g = np.random.default_rng([254] + [int(round(t * 1000)) if isinstance(t, float) else int(t) for t in tag])

    def __call__(self):
        return float(self.g.random())


class Seq:
    """Additive-recurrence low-discrepancy stream (onset quantiles only)."""

    def __init__(self, alpha, salt=0.0):
        self.a, self.s, self.k = alpha, salt, 0

    def __call__(self):
        u = frac((self.k + 0.5) * self.a + self.s)
        self.k += 1
        return u


def allocate(inc, salt):
    """Reaction-courses of one risk: (course start, market), by cumulative rounding of starts x incidence."""
    out, cum, prev, k = [], 0.0, 0, 0
    for w in W.weeks():
        for c in W.MARKET_ORDER:
            e = W.weekly_starts(w, c) * inc
            if e <= 0:
                continue
            cum += e
            n = int(round(cum)) - prev
            prev += n
            for _ in range(n):
                off = int(7 * frac((k + 0.5) * W.SQ2 + salt))
                k += 1
                out.append((w + TD(days=off), c, k))
    out.sort(key=lambda t: (t[0], W.MARKET_ORDER.index(t[1]), t[2]))
    return [(s, c) for s, c, _ in out]


def delay_days(u, kind):
    if kind == "LI":
        return S.lognormal_days(u, 150, 0.45, lo=40, hi=500)
    if kind == "PSP":
        return S.lognormal_days(u, 9, 0.5, lo=2, hi=40)
    return S.lognormal_days(u, 18, 1.1, lo=1, hi=420)


def _positions(n, p):
    """1-indexed order-statistic positions the common quantile readings interpolate between:
    inverted CDF, linear (R type 7), Hazen (5), Weibull (6), median-unbiased (8), normal-unbiased (9)."""
    hs = [(n - 1) * p + 1, n * p + 0.5, (n + 1) * p, (n + 1.0 / 3) * p + 1.0 / 3, (n + 0.25) * p + 0.375]
    lo = [math.ceil(n * p - 1e-9)] + [math.floor(h + 1e-9) for h in hs]
    hi = [math.ceil(n * p - 1e-9)] + [math.ceil(h - 1e-9) for h in hs]
    return max(1, min(lo)), min(n, max(hi))


def _a(n, p):
    """Fewest values above the month's lower edge so every reading clears it."""
    return n + 1 - _positions(n, p)[0]


def _b(n, p):
    """Most values above the month's upper edge so every reading stays inside it."""
    return n - _positions(n, p)[1]


def herd(values, tmonths, n_from, caps=None, slack=1):
    """Order a pool of onset days along courses in start order so that every prefix of n_from or more
    courses has its 80 and 95 per cent cuts inside the target months under every common quantile reading,
    with `slack` spare values on each side where the pool allows it. caps[k] is the longest onset course k
    can hold (its own truncation time); any such permutation leaves the reverse-time estimate unchanged,
    because R(s) = #{x <= s} - #{T < s} depends on the two multisets only."""
    m80, m95 = tmonths
    t1, t2, t3, t4 = 30 * (m80 - 1), 30 * m80, 30 * (m95 - 1), 30 * m95
    N = len(values)
    if caps is None:
        caps = [10 ** 6] * N
    bins = [[], [], [], [], []]
    for v in sorted(values):
        b = 0 if v <= t1 else 1 if v <= t2 else 2 if v <= t3 else 3 if v <= t4 else 4
        bins[b].append(v)
    share = [len(b) / N for b in bins]
    pools = []
    for b in bins:
        k = len(b)
        idx = sorted(range(k), key=lambda j: frac((j + 0.5) * W.PHI))
        pools.append([b[j] for j in idx])
    used = [0] * 5
    out = []
    for n in range(1, N + 1):
        cap = caps[n - 1]
        above1 = sum(used[1:])
        above2 = sum(used[2:])
        above3 = used[3] + used[4]
        above4 = used[4]
        nb = max(n, n_from)
        fits = [any(v <= cap for v in pools[b]) for b in range(5)]
        allowed = list(fits)
        cap4 = _b(nb, 0.95) - slack
        cap2 = _b(nb, 0.80) - slack
        if above4 + 1 > cap4:
            allowed[4] = False
        if above2 + 1 > cap2:
            allowed[2] = allowed[3] = allowed[4] = False
        a95 = (_a(n, 0.95) if n >= n_from else _a(n_from, 0.95) - (n_from - n)) + slack
        a80 = (_a(n, 0.80) if n >= n_from else _a(n_from, 0.80) - (n_from - n)) + slack
        reserve = max(0, _a(nb, 0.95) + slack - above3)
        if above2 + 1 + reserve > cap2:
            allowed[2] = False
        need = None
        if above3 < a95:
            need = [3, 4]
        elif above1 < a80:
            need = [1, 2, 3, 4]
        cands = [b for b in (need or range(5)) if allowed[b]]
        if not cands:
            cands = [b for b in range(5) if allowed[b]]
        if not cands:
            cands = [b for b in range(5) if fits[b]]
        b = max(cands, key=lambda bb: (n * share[bb] - used[bb], -bb))
        tight = min(caps[n - 1:])
        if max(pools[b]) > tight:
            j = max((i for i, v in enumerate(pools[b]) if v <= cap), key=lambda i: pools[b][i])
        else:
            j = next(i for i, v in enumerate(pools[b]) if v <= cap)
        out.append(pools[b].pop(j))
        used[b] += 1
    return out


def prefix_violations(x, start_ord, tmonths, L_from=None, L_to=913):
    """Mature-cohort subsets (course started at least L days before the lock, every L from the longest
    onset to L_to, and courses started in 2023): number of subsets whose cuts leave the target months under
    any of the common quantile readings."""
    x = np.asarray(x)
    st = np.asarray(start_ord)
    o = np.argsort(st, kind="stable")
    xs, ss = x[o], st[o]
    m80, m95 = tmonths
    edges = [30 * (m80 - 1), 30 * m80, 30 * (m95 - 1), 30 * m95]
    b = np.searchsorted(np.array(edges), xs, side="left")
    cum = np.zeros((len(xs) + 1, 5), dtype=int)
    for k in range(5):
        cum[1:, k] = np.cumsum(b == k)
    lock_o = LOCK.toordinal()
    if L_from is None:
        L_from = int(x.max())
    sizes = set()
    for L in range(L_from, L_to + 1):
        sizes.add(int(np.searchsorted(ss, lock_o - L + 1, side="right")))
    sizes.add(int(np.searchsorted(ss, dt.date(2023, 12, 31).toordinal(), side="right")))
    bad = 0
    for n in sizes:
        if n < 5:
            bad += 1
            continue
        c = cum[n]
        if (n - c[0] < _a(n, 0.80) or n - c[0] - c[1] > _b(n, 0.80)
                or c[3] + c[4] < _a(n, 0.95) or c[4] > _b(n, 0.95)):
            bad += 1
    return bad


def build_risk(r):
    P = RISK_PARAMS[r]
    dist = S.Dist(P["months"], P["maxd"])
    alloc = allocate(P["inc"], P["salt"])
    sp = Rng(1, P["salt"])
    ss = Rng(2, P["salt"])
    srs = Rng(3, P["salt"])
    sps = Rng(4, P["salt"])
    recs = []
    for i, (s, c) in enumerate(alloc):
        rec = dict(risk=r, market=c, start=s, T=(LOCK - s).days + 1, i=i)
        rec["psp_mon"] = r in ("hepatic", "neutropenia") and c in PSP_MARKETS and srs() < 0.80
        u_part = sp()
        rec["partial_onset"] = (not rec["psp_mon"]) and u_part < PARTIAL_ONSET
        rec["partial_start"] = False
        rec["u_start"] = ss()
        rec["u_struct"] = sps()
        recs.append(rec)
    # course before a restart (A-D1): first course, gap over 28 days, the reaction's course
    if r in RESTART_SHARE:
        sq = Rng(5, P["salt"])
        for rec in recs:
            u1, u2, u3 = sq(), sq(), sq()
            if u1 < RESTART_SHARE[r] / 0.82:
                len1 = 60 + int(u2 * 271)
                gap = 34 + int(u3 * 117)
                s1 = rec["start"] - TD(days=gap + len1)
                if s1 >= W.MARKETS[rec["market"]][0]:
                    rec["restart"] = dict(s1=s1, len1=len1, gap=gap)
    for rec in recs:
        if "restart" not in rec and rec["u_start"] < PARTIAL_START:
            rec["partial_start"] = True
    # onsets: low-discrepancy assignment in start order, then the mature zone ordered by herding
    useq = Seq(W.PHI, P["salt"])
    for rec in recs:
        rec["x"] = dist.q(useq())
    zone = [rec for rec in recs if rec["T"] >= P["maxd"] - 60 and not rec["partial_onset"] and not rec["partial_start"]]
    n2023 = sum(1 for rec in zone if rec["start"] <= dt.date(2023, 12, 31))
    vals = herd([rec["x"] for rec in zone], TARGET_MONTHS[r], n2023, caps=[rec["T"] for rec in zone])
    for rec, v in zip(zone, vals):
        rec["x"] = v
        rec["zone"] = True
    _settle_partials(recs, dist, r)
    return recs, dist


def _imputed(rec, day):
    """(onset day, truncation) of a partial-dated reaction if its partial date is imputed to day `day`."""
    x, T = rec["x"], rec["T"]
    if rec["partial_onset"]:
        dom = (rec["start"] + TD(days=x - 1)).day
        return x - (dom - day), T
    dom = rec["start"].day
    return x + (dom - day), T + (dom - day)


def _settle_partials(recs, dist, r):
    """Partial-dated reactions are kept out of time to onset; choose their days so that letting them in
    with the month imputed to day 1 or day 15 leaves every mature-cohort cut where it is."""
    P = RISK_PARAMS[r]
    tm = TARGET_MONTHS[r]
    gold = [rec for rec in recs if not rec["partial_onset"] and not rec["partial_start"]]
    lo = P["maxd"] - 60
    part = [rec for rec in recs if (rec["partial_onset"] or rec["partial_start"]) and rec["T"] >= lo - 30]
    seq = Rng(6, P["salt"])
    base_x = [rec["x"] for rec in gold if rec["T"] >= lo - 30]
    base_s = [rec["start"].toordinal() for rec in gold if rec["T"] >= lo - 30]
    lfrom = max(rec["x"] for rec in gold if rec["T"] >= lo)
    chosen = {1: ([], []), 15: ([], [])}
    for rec in sorted(part, key=lambda q: q["start"]):
        for attempt in range(400):
            v = dist.q(seq()) if attempt else rec["x"]
            if v + 20 > rec["T"] or v < 31:
                continue
            rec["x"] = v
            ok = True
            for day in (1, 15):
                xi, Ti = _imputed(rec, day)
                xs = base_x + chosen[day][0] + [xi]
                ss = base_s + chosen[day][1] + [(LOCK - TD(days=Ti - 1)).toordinal()]
                if xi < 1 or prefix_violations(xs, ss, tm, L_from=lfrom):
                    ok = False
                    break
            if ok:
                break
        else:
            raise SystemExit("no day for a partial-dated %s reaction" % r)
        for day in (1, 15):
            xi, Ti = _imputed(rec, day)
            chosen[day][0].append(xi)
            chosen[day][1].append((LOCK - TD(days=Ti - 1)).toordinal())


def report_and_delay(recs, r):
    """Report kind, reporting delay, receipt date and whether the case is in the database at the lock."""
    P = RISK_PARAMS[r]
    sl = Rng(7, P["salt"])
    sd = Rng(8, P["salt"])
    for rec in recs:
        lit = sl() < 0.03
        rec["psp_dated"] = rec["psp_mon"] and rec["x"] >= 85
        kind = "PSP" if rec["psp_dated"] else ("LI" if lit else "GEN")
        d = delay_days(sd(), kind)
        if rec.get("zone"):
            room = rec["T"] - rec["x"]
            if kind == "LI" and room < 40:
                kind = "GEN"
                d = delay_days(frac(d * W.PHI), "GEN")
            d = min(d, room)
        rec["kind"] = kind
        rec["delay"] = d
        rec["onset_date"] = rec["start"] + TD(days=rec["x"] - 1)
        rec["receipt"] = rec["onset_date"] + TD(days=d)
        rec["at_lock"] = rec["receipt"] <= LOCK
        rec["post_lock"] = LOCK < rec["receipt"] <= EXPORT
    return recs


# ---------------------------------------------------------------- dosage lines of each case

def structure(recs, r):
    """Dosage lines of the reaction's course (and a course before it), and what was done after onset."""
    P = RISK_PARAMS[r]
    sq = Rng(9, P["salt"])
    act_mix = {
        "ild": [("WITHDRAWN", 0.72), ("DOSE NOT CHANGED", 0.12), ("UNKNOWN", 0.16)],
        "zoster": [("INTERRUPTED", 0.30), ("DOSE NOT CHANGED", 0.50), ("WITHDRAWN", 0.12), ("UNKNOWN", 0.08)],
        "infection": [("INTERRUPTED", 0.45), ("WITHDRAWN", 0.18), ("DOSE NOT CHANGED", 0.27), ("UNKNOWN", 0.10)],
        "vte": [("WITHDRAWN", 0.58), ("DOSE NOT CHANGED", 0.30), ("UNKNOWN", 0.12)],
        "hepatic": [("INTERRUPTED", 0.30), ("WITHDRAWN", 0.22), ("DOSE NOT CHANGED", 0.36), ("UNKNOWN", 0.12)],
        "neutropenia": [("INTERRUPTED", 0.40), ("WITHDRAWN", 0.14), ("DOSE NOT CHANGED", 0.36), ("UNKNOWN", 0.10)],
    }[r]
    for rec in recs:
        u = [sq() for _ in range(8)]
        s, x = rec["start"], rec["x"]
        lines = []
        dose0 = 15
        if "restart" in rec:
            rs = rec["restart"]
            lines.append(dict(start=rs["s1"], stop=rs["s1"] + TD(days=rs["len1"] - 1), dose=15, end="INTERRUPTED"))
        esc = r in ESCALATE_SHARE and x >= 45 and u[0] < ESCALATE_SHARE[r] / 0.93
        pause = (not esc) and r in PAUSE_SHARE and x >= 40 and u[1] < PAUSE_SHARE[r] * min(1.0, x / 365.0)
        cur_start = s
        if esc:
            if r == "vte":
                # venous thrombosis two to seventeen weeks after the step up to 30 mg
                e = max(29, x - 14 - int(u[2] * 106))
            else:
                e = 29 + int(u[2] * (x - 39))
            lines.append(dict(start=s, stop=s + TD(days=e - 2), dose=15, end="DOSE CHANGED"))
            cur_start, dose0 = s + TD(days=e - 1), 30
            rec["esc_day"] = e
        elif pause:
            g = 5 + int(u[3] * 21)
            p = 10 + int(u[2] * max(1, min(x - 15 - g - 10, 140)))
            lines.append(dict(start=s, stop=s + TD(days=p - 1), dose=15, end="INTERRUPTED"))
            cur_start = s + TD(days=p + g)
            rec["pause"] = (p, g)
        onset = rec["onset_date"]
        acc, act = 0.0, act_mix[-1][0]
        for a, w in act_mix:
            acc += w
            if u[4] < acc:
                act = a
                break
        if act == "DOSE NOT CHANGED" and dose0 == 30 and u[5] < 0.4:
            act = "DOSE REDUCED"
        rec["action"] = act
        known = rec.get("info_until", EXPORT)
        d = int(u[6] * 10)
        if act in ("WITHDRAWN", "INTERRUPTED", "DOSE REDUCED"):
            stop = min(onset + TD(days=d), rec["receipt"])
            stop = max(stop, onset)
            lines.append(dict(start=cur_start, stop=stop, dose=dose0,
                              end={"WITHDRAWN": "DISCONTINUED", "INTERRUPTED": "INTERRUPTED",
                                   "DOSE REDUCED": "DOSE CHANGED"}[act]))
            if act == "INTERRUPTED":
                g2 = 7 + int(u[7] * 70)
                rs2 = stop + TD(days=g2 + 1)
                if rs2 <= known and rs2 <= LOCK:
                    lines.append(dict(start=rs2, stop=None, dose=dose0, end="ONGOING"))
            elif act == "DOSE REDUCED":
                lines.append(dict(start=stop + TD(days=1), stop=None, dose=15, end="ONGOING"))
        elif act == "DOSE NOT CHANGED" and u[5] < 0.30:
            stop = onset + TD(days=30 + int(u[7] * 370))
            if stop <= min(known, LOCK - TD(days=1)):
                lines.append(dict(start=cur_start, stop=stop, dose=dose0, end="DISCONTINUED"))
                rec["unrelated_stop"] = stop
            else:
                lines.append(dict(start=cur_start, stop=None, dose=dose0, end="ONGOING"))
        else:
            lines.append(dict(start=cur_start, stop=None, dose=dose0,
                              end="ONGOING" if act == "DOSE NOT CHANGED" else "UNKNOWN"))
        rec["lines"] = lines
    return recs


# ---------------------------------------------------------------- laboratories of the patient support programme

# code: (laboratory, country, markets served, ALT unit, ALT ULN male, ALT ULN female, NEUT unit, NEUT factor, NEUT LLN)
LABS = {
    "NCL-AAR": ("Central laboratory, Aarhus (Nordic markets)", "DK", ("DK", "SE", "NO", "FI"), "µkat/L", 1.10, 0.75, "10^9/L", 1.0, 1.6),
    "DE-HH04": ("Partner laboratory, Hamburg", "DE", ("DE",), "U/L", 50, 35, "/nl", 1.0, 1.8),
    "DE-M11": ("Partner laboratory, Munich", "DE", ("DE",), "U/L", 45, 34, "/µl", 1000.0, 1900),
    "NL-AMS2": ("Partner laboratory, Amsterdam", "NL", ("NL",), "U/L", 45, 35, "10^9/L", 1.0, 1.5),
    "FR-LYO1": ("Laboratoire partenaire, Lyon", "FR", ("FR",), "UI/L", 55, 35, "/mm3", 1000.0, 1700),
    "FR-NTE3": ("Laboratoire partenaire, Nantes", "FR", ("FR",), "UI/L", 50, 33, "/mm3", 1000.0, 1800),
    "IT-MI07": ("Laboratorio partner, Milano", "IT", ("IT",), "UI/L", 41, 33, "cell/µL", 1000.0, 2000),
    "IT-NA02": ("Laboratorio partner, Napoli", "IT", ("IT",), "U/L", 45, 34, "cell/µL", 1000.0, 1900),
    "ES-VLC1": ("Laboratorio colaborador, Valencia", "ES", ("ES",), "U/L", 41, 33, "10^3/µL", 1.0, 1.8),
}
LAB_BY_MARKET = {}
for _code, _v in LABS.items():
    for _m in _v[2]:
        LAB_BY_MARKET.setdefault(_m, []).append(_code)


def _fmt_alt(v_uln_mult, lab, sex):
    name, _, _, unit, um, uf, *_ = LABS[lab]
    uln = um if sex == "M" else uf
    v = v_uln_mult * uln
    return ("%.2f" % v) if unit == "µkat/L" else str(int(round(v)))


def _fmt_neut(v109, lab):
    unit, fac = LABS[lab][6], LABS[lab][7]
    if fac == 1000.0:
        return str(int(round(v109 * 1000 / 10.0)) * 10)
    return "%.2f" % v109


def psp_schedule(rec, sq):
    """Laboratory sample days of a monitored course, from the first PSP sample after the hospital's 12 weeks."""
    end_day = rec["T"] if rec.get("course_end_day") is None else rec["course_end_day"]
    end_day = min(end_day, (rec.get("info_until", EXPORT) - rec["start"]).days + 1)
    x = rec["x"]
    days, grade1 = [], set()
    if rec.get("psp_dated"):
        if x <= 98:
            first = x
        else:
            first = 85 + int(sq() * 14)
        d = first
        while d < x - 13:
            days.append(d)
            d += 84 + int(sq() * 15)
        if days and x - days[-1] < 70:
            grade1.add(days[-1])
        elif days and sq() < 0.45:
            grade1.add(days[-1])
        days.append(x)
        nd = x + 14 + int(sq() * 22)
        if nd <= end_day:
            days.append(nd)
    else:
        d = 85 + int(sq() * 14)
        while d <= end_day:
            days.append(d)
            d += 84 + int(sq() * 15)
    return days, grade1


# ---------------------------------------------------------------- terms, people and outcomes

TERMS = {
    "ild": [("Interstitial lung disease", 0.55), ("Pneumonitis", 0.30), ("Organising pneumonia", 0.06),
            ("Pulmonary fibrosis", 0.04), ("Acute interstitial pneumonitis", 0.03), ("Alveolitis", 0.02)],
    "zoster": [("Herpes zoster", 0.86), ("Ophthalmic herpes zoster", 0.08), ("Herpes zoster meningitis", 0.02),
               ("Varicella zoster virus infection", 0.04)],
    "infection": [("Pneumonia", 0.27), ("Urinary tract infection", 0.11), ("Cellulitis", 0.10), ("Sepsis", 0.08),
                  ("COVID-19 pneumonia", 0.06), ("Lower respiratory tract infection", 0.06), ("Pyelonephritis", 0.05),
                  ("Gastroenteritis", 0.05), ("Diverticulitis", 0.04), ("Influenza", 0.04), ("Erysipelas", 0.03),
                  ("Bronchitis", 0.03), ("Septic shock", 0.02), ("Osteomyelitis", 0.02), ("Appendicitis", 0.02),
                  ("Pneumocystis jirovecii pneumonia", 0.01), ("Cytomegalovirus infection", 0.01)],
    "vte": [("Deep vein thrombosis", 0.55), ("Pulmonary embolism", 0.35), ("Venous thrombosis limb", 0.04),
            ("Thrombosis", 0.03), ("Embolism venous", 0.01), ("Jugular vein thrombosis", 0.01),
            ("Retinal vein occlusion", 0.01)],
    "hepatic": [("Drug-induced liver injury", 0.25), ("Hepatotoxicity", 0.20), ("Transaminases increased", 0.20),
                ("Alanine aminotransferase increased", 0.20), ("Hepatic enzyme increased", 0.10), ("Hepatitis", 0.03),
                ("Hepatocellular injury", 0.02)],
    "neutropenia": [("Neutropenia", 0.60), ("Neutrophil count decreased", 0.30), ("Febrile neutropenia", 0.07),
                    ("Agranulocytosis", 0.03)],
}
LAB_TERMS = {"hepatic": [("Alanine aminotransferase increased", 0.60), ("Transaminases increased", 0.25),
                         ("Hepatic enzyme increased", 0.15)],
             "neutropenia": [("Neutrophil count decreased", 0.75), ("Neutropenia", 0.25)]}
# site-specific zoster terms and infection terms added to the list in v4; always coded beside their parent term
V4_ADDED = {"zoster": [("Herpes zoster oticus", "Herpes zoster"), ("Herpes zoster cutaneous disseminated", "Herpes zoster"),
                       ("Genital herpes zoster", "Herpes zoster")],
            "infection": [("Urosepsis", "Urinary tract infection"), ("Pneumonia bacterial", "Pneumonia")]}
CO_TERMS = {
    "ild": [("Dyspnoea", 0.40), ("Cough", 0.25), ("Hypoxia", 0.06), ("Pyrexia", 0.06)],
    "zoster": [("Rash", 0.10), ("Pain", 0.08), ("Post herpetic neuralgia", 0.07)],
    "infection": [("Pyrexia", 0.30), ("C-reactive protein increased", 0.10), ("Dyspnoea", 0.06)],
    "vte": [("Pain in extremity", 0.15), ("Dyspnoea", 0.15), ("Oedema peripheral", 0.08)],
    "hepatic": [("Aspartate aminotransferase increased", 0.30), ("Gamma-glutamyltransferase increased", 0.15),
                ("Fatigue", 0.06)],
    "neutropenia": [("White blood cell count decreased", 0.25), ("Pyrexia", 0.06), ("Lymphopenia", 0.05)],
}
SEX_F = {"ild": 0.46, "zoster": 0.66, "infection": 0.60, "vte": 0.55, "hepatic": 0.58, "neutropenia": 0.66, None: 0.64}
AGE_MU = {"ild": 66, "zoster": 61, "infection": 63, "vte": 62, "hepatic": 54, "neutropenia": 52, None: 53}


def pick(mix, u):
    acc = 0.0
    for v, w in mix:
        acc += w
        if u < acc:
            return v
    return mix[-1][0]


def seriousness(risk, u1, u2):
    if risk == "ild":
        return "Y", pick([("H", 0.70), ("OMI", 0.25), ("LT", 0.05)], u1), 0.05
    if risk == "infection":
        return "Y", pick([("H", 0.85), ("H;LT", 0.08), ("D", 0.04), ("OMI", 0.03)], u1), 0.03
    if risk == "vte":
        return "Y", pick([("H", 0.75), ("OMI", 0.20), ("H;LT", 0.05)], u1), 0.015
    if risk == "zoster":
        return ("Y", "H", 0.0) if u2 < 0.25 else ("N", "", 0.0)
    if risk == "hepatic":
        return ("Y", pick([("OMI", 0.6), ("H", 0.4)], u1), 0.0) if u2 < 0.35 else ("N", "", 0.0)
    if risk == "neutropenia":
        return ("Y", pick([("OMI", 0.5), ("H", 0.5)], u1), 0.0) if u2 < 0.30 else ("N", "", 0.0)
    return ("Y", pick([("H", 0.6), ("OMI", 0.4)], u1), 0.0) if u2 < 0.06 else ("N", "", 0.0)
