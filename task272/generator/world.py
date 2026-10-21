"""The world: the households that applied to each member hospital for financial assistance in 2024 and 2025, their
income month by month, and the applications the counsellors decided under the collaborative's common policy.

A household's income over a year is its level (a share of the poverty guideline for its size) spread over the months
by the calendar of the main earner's work in the hospital's region: flat for year-round work, peaked for field work,
packing, fishing, resort and woods work, each region's peak where its crops, catches and seasons put it. A household
applies a month or two after the bill for an episode of care; an approval covers the household's care for six months;
a household denied or given only part of its balance applies again, some of the time, once its pay has fallen.

The 2025 policy assessed income from the three full calendar months before the month of application, times four, and
set the discount from that figure: free care in full to 200 percent of the guideline, then 75, 50 and 25 percent to
250, 300 and 400 percent. The criteria file the household's income over the twelve full calendar months before the
month of application instead; the generator keeps both, and the analysis has only the first.

The world is drawn once; each hospital's rate of denials for documents not received is then set so that its share under
the golden calendar estimate sits on its designed side of the six-percent line with room to spare."""
import calendar as cal_
import datetime as dt

import numpy as np

import common as K

SEED = 27202

# The 2025 and 2024 HHS poverty guidelines for the 48 contiguous states: the first person, then each additional person.
FPL = {2025: (15650, 5500), 2024: (15060, 5380), 2023: (14580, 5140)}


def fpl(year, size):
    a, b = FPL[year]
    return a + b * (size - 1)


def months_from(y, m, k):
    """The (year, month) k months after (y, m); k may be negative."""
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


def cal(peaks, rest):
    s = np.full(12, float(rest))
    for m, w in peaks.items():
        s[m - 1] = w
    return s / s.mean()


FLAT = np.ones(12)
# The calendar of each kind of seasonal work in each region (January first), mean one over the year.
CAL = {
    ("Willamette Valley", "FIELD"): cal({3: 1.2, 4: 1.6, 5: 1.8, 6: 2.0, 7: 2.0, 8: 1.7, 9: 1.3}, 0.5),
    ("Willamette Valley", "PACK"): cal({7: 2.0, 8: 2.6, 9: 2.6, 10: 1.9}, 0.6),
    ("Willamette Valley", "WOODS"): cal({10: 1.8, 11: 3.0, 12: 2.6}, 0.6),
    ("Southern Oregon", "FIELD"): cal({8: 2.8, 9: 3.0, 10: 1.6}, 0.6),
    ("Southern Oregon", "PACK"): cal({9: 2.0, 10: 2.4, 11: 2.4, 12: 2.0, 1: 1.6}, 0.55),
    ("Southern Oregon", "WOODS"): cal({5: 1.4, 6: 1.6, 7: 1.6, 8: 1.5, 9: 1.6, 10: 1.4}, 0.55),
    ("Central Oregon", "RESORT"): cal({12: 2.0, 1: 2.3, 2: 2.3, 3: 1.6, 7: 1.8, 8: 1.8}, 0.55),
    ("Central Oregon", "BUILD"): cal({4: 1.3, 5: 1.5, 6: 1.6, 7: 1.6, 8: 1.6, 9: 1.5, 10: 1.3}, 0.5),
    ("Klamath Basin", "FIELD"): cal({7: 1.7, 8: 2.3, 9: 2.6, 10: 2.4}, 0.5),
    ("Klamath Basin", "PACK"): cal({9: 1.8, 10: 2.2, 11: 2.0, 12: 1.6, 1: 1.4, 2: 1.2}, 0.55),
    ("Columbia Basin", "FIELD"): cal({6: 1.3, 7: 1.9, 8: 2.4, 9: 2.6, 10: 2.3}, 0.45),
    ("Columbia Basin", "PACK"): cal({8: 1.6, 9: 2.0, 10: 2.2, 11: 2.0, 12: 1.6, 1: 1.3, 2: 1.2}, 0.5),
    ("Columbia Basin", "BUILD"): cal({4: 1.3, 5: 1.5, 6: 1.6, 7: 1.6, 8: 1.6, 9: 1.5, 10: 1.3}, 0.5),
    ("Columbia Gorge", "FIELD"): cal({6: 2.8, 7: 2.8, 8: 2.0, 9: 1.6}, 0.5),
    ("Columbia Gorge", "PACK"): cal({7: 1.8, 8: 2.0, 9: 2.2, 10: 2.0, 11: 1.6, 12: 1.3}, 0.5),
    ("Oregon Coast", "FISH"): cal({12: 2.8, 1: 3.0, 2: 2.4, 3: 1.4, 7: 1.4, 8: 1.6, 9: 1.2}, 0.4),
    ("Oregon Coast", "RESORT"): cal({6: 1.8, 7: 2.6, 8: 2.6, 9: 1.6}, 0.55),
    ("Oregon Coast", "WOODS"): cal({5: 1.4, 6: 1.6, 7: 1.6, 8: 1.5, 9: 1.6, 10: 1.4}, 0.55),
    ("Central Washington", "FIELD"): cal({6: 1.6, 7: 1.4, 8: 2.2, 9: 2.8, 10: 2.6, 11: 1.0}, 0.45),
    ("Central Washington", "PACK"): cal({10: 1.7, 11: 2.0, 12: 2.0, 1: 1.9, 2: 1.8, 3: 1.6, 4: 1.3}, 0.55),
    ("Central Washington", "RESORT"): cal({12: 2.4, 1: 2.8, 2: 2.7, 3: 2.0}, 0.55),
    ("Northwest Washington", "FIELD"): cal({4: 1.6, 5: 1.3, 6: 2.0, 7: 2.6, 8: 2.4, 9: 1.4}, 0.45),
    ("Northwest Washington", "FISH"): cal({6: 2.8, 7: 3.4, 8: 3.2, 9: 2.0}, 0.35),
    ("Northwest Washington", "PACK"): cal({6: 1.6, 7: 2.4, 8: 2.4, 9: 1.8}, 0.6),
    ("Southwest Washington", "FISH"): cal({12: 2.6, 1: 3.0, 2: 2.8, 3: 2.0}, 0.45),
    ("Southwest Washington", "WOODS"): cal({5: 1.4, 6: 1.6, 7: 1.6, 8: 1.5, 9: 1.6, 10: 1.4}, 0.55),
    ("Olympic Peninsula", "RESORT"): cal({6: 1.9, 7: 2.6, 8: 2.6, 9: 1.7}, 0.55),
    ("Olympic Peninsula", "FISH"): cal({12: 2.6, 1: 3.0, 2: 2.6, 3: 1.8}, 0.45),
    ("Olympic Peninsula", "WOODS"): cal({5: 1.4, 6: 1.6, 7: 1.6, 8: 1.5, 9: 1.6, 10: 1.4}, 0.55),
    ("Inland Northwest", "BUILD"): cal({4: 1.3, 5: 1.5, 6: 1.6, 7: 1.6, 8: 1.6, 9: 1.5, 10: 1.3}, 0.5),
    ("Puget Sound", "BUILD"): cal({5: 1.2, 6: 1.25, 7: 1.25, 8: 1.25, 9: 1.2}, 0.86),
    ("Portland and Vancouver", "BUILD"): cal({5: 1.2, 6: 1.25, 7: 1.25, 8: 1.25, 9: 1.2}, 0.86),
}
SEASONAL = ("FIELD", "PACK", "FISH", "RESORT", "WOODS", "BUILD")
YEAR_ROUND = ("CARE", "SHOP", "OFFICE", "PLANT", "OTHER", "NONE")


def calendar_of(region, kind):
    return CAL.get((region, kind), FLAT)


def seasonal_kinds(region):
    return [k for (r, k) in CAL if r == region]


def draw_hospital(code, r):
    """The hospital's applicant households: how many, how its seasonal work divides, its pace of applications."""
    region = K.REGION[code]
    kinds = seasonal_kinds(region)
    weights = {k: float(r.uniform(0.6, 1.4)) * (0.35 if k == "BUILD" else 1.0) for k in kinds}
    tot = sum(weights.values()) or 1.0
    s_share = float(r.uniform(*K.SEASONAL_SHARE[code]))
    mix = {k: s_share * w / tot for k, w in weights.items()}
    return dict(code=code, region=region, households=int(r.integers(*K.HOUSEHOLDS[code])), mix=mix,
                other_cov=float(r.uniform(0.006, 0.014)), not_resident=float(r.uniform(0.001, 0.005)))


def households(h, r):
    """One row per household: its kind of work, size, level and personal seasonality."""
    n = h["households"]
    kinds = list(h["mix"]) + list(YEAR_ROUND)
    rest = 1.0 - sum(h["mix"].values())
    yr_w = np.array([0.20, 0.22, 0.20, 0.12, 0.12, 0.14])
    p = np.array(list(h["mix"].values()) + list(rest * yr_w / yr_w.sum()))
    kind = r.choice(len(kinds), size=n, p=p / p.sum())
    size = r.choice([1, 2, 3, 4, 5, 6], size=n, p=[0.24, 0.22, 0.19, 0.18, 0.11, 0.06])
    out = []
    for i in range(n):
        k = kinds[kind[i]]
        if k in SEASONAL and k != "BUILD":
            level = float(np.exp(r.normal(np.log(150), 0.30)))
        elif k == "NONE":
            level = float(np.exp(r.normal(np.log(105), 0.35)))
        else:
            level = float(np.exp(r.normal(np.log(175), 0.42)))
        gamma = float(r.uniform(0.85, 1.15)) if k in SEASONAL else 0.0
        out.append(dict(kind=k, size=int(size[i]), level=level, gamma=gamma,
                        u_doc=float(r.random()), u_cov=float(r.random()), u_res=float(r.random())))
    return out


def monthly_income(hh, region, r, rr):
    """The household's income in each month from January 2022 to December 2025 (48 months), in dollars: its level in
    2025, earlier years' pay lower by an uneven yearly rise (about 3 percent), the shape of its work through the year,
    and month-to-month variation in hours and overtime."""
    s = calendar_of(region, hh["kind"]) ** hh["gamma"] if hh["gamma"] else FLAT
    s = s / s.mean()
    base = hh["level"] / 100.0 * fpl(2025, hh["size"]) / 12.0
    eps = r.normal(0, 0.05 if hh["kind"] in SEASONAL else 0.0, 48)
    rise = rr.normal(0.03, 0.06, 3)
    year = np.repeat(np.exp(np.concatenate([-np.cumsum(rise[::-1])[::-1], [0.0]])), 12)
    hours = rr.normal(0, 0.06, 48)
    plan = base * year * np.tile(s, 4)
    return np.round(plan * (1 + eps) * (1 + hours), 2), plan


def month_index(y, m):
    return (y - 2022) * 12 + (m - 1)


def tier_2025(pct):
    if pct <= 200:
        return 100
    if pct <= 250:
        return 75
    if pct <= 300:
        return 50
    if pct <= 400:
        return 25
    return 0


def episodes(hh, region, r):
    """Months (index from January 2022) in which the household has an episode of care, 2023 to 2025; 2023's applications
    are not in the extracts and only set who is already covered when 2024 opens."""
    s = calendar_of(region, hh["kind"])
    lam = (0.55 + (0.25 if hh["kind"] in SEASONAL else 0.0)) / 12.0
    rate = np.tile(lam * (0.6 + 0.4 * s), 3)
    return 12 + np.flatnonzero(r.random(36) < rate)


def applications(h, hhs, r, rr):
    """Each household's applications: received month and day, the window's income, the policy's assessment. Months are
    indexed from January 2022; applications received from January 2024 are kept."""
    region = h["region"]
    out = []
    for hi, hh in enumerate(hhs):
        inc, plan = monthly_income(hh, region, r, rr)
        covered_until = -1
        applied = set()
        for ei, e in enumerate(episodes(hh, region, r)):
            a = int(e) + 1 + int(r.choice([0, 1, 2], p=[0.5, 0.35, 0.15]))
            if a <= covered_until or a > 47 or a in applied:
                continue
            case = None
            while a <= 47 and a not in applied:
                applied.add(a)
                y, m = 2022 + a // 12, a % 12 + 1
                inc3 = float(np.round(inc[a - 3:a].sum(), 2))
                inc12 = float(np.round(inc[a - 12:a].sum(), 2))
                pct = inc3 * 4 / fpl(y, hh["size"]) * 100.0
                tier = tier_2025(pct)
                day = int(r.integers(1, cal_.monthrange(y, m)[1] + 1))
                rec = dict(hh=hi, kind=hh["kind"], size=hh["size"], level=hh["level"], received=dt.date(y, m, day),
                           amonth=a, inc3=inc3, inc12=inc12, pct_policy=pct, tier_policy=tier,
                           u_doc=float(r.random()), u_cov=float(r.random()), u_res=float(r.random()),
                           u_wd=float(r.random()), delay=int(r.integers(5, 41)))
                rec["case"] = case if case is not None else (hi, ei)
                rec["first_in_case"] = case is None
                case = rec["case"]
                if y >= 2024:
                    out.append(rec)
                if tier == 100:
                    covered_until = a + 6
                    break
                if tier > 0:
                    covered_until = a + 6
                # denied or only part of the balance: apply again, now and then, once the household's work takes its
                # pay down (the season it knows, not a month's luck)
                p_re = K.REAPPLY[0] if hh["kind"] in SEASONAL else K.REAPPLY[1]
                if r.random() >= p_re:
                    break
                nxt = None
                for d in range(2, 8):
                    if a + d > 47:
                        break
                    if plan[a + d - 3:a + d].sum() < plan[a - 3:a].sum() * 0.8:
                        nxt = a + d
                        break
                if nxt is None:
                    break
                a = nxt
    return out


def world(seed=SEED):
    """Every hospital's households and applications, drawn once; the documents rates are set in decide()."""
    out = []
    for code in K.CODES:
        r = np.random.default_rng([seed, int(code[1:])])
        h = draw_hospital(code, r)
        hhs = households(h, r)
        h["hh"] = hhs
        h["apps"] = applications(h, hhs, r, np.random.default_rng([seed, int(code[1:]), 77]))
        out.append(h)
    return out


def working(d):
    """The first working day on or after d."""
    while d.weekday() >= 5 or d in K.HOLIDAYS_ALL:
        d += dt.timedelta(days=1)
    return d


def decide(hs, doc):
    """The counsellors' first-review decisions under the 2025 policy, with each hospital's rate of denials for documents
    not received; a decision falls on the first working day after the received date plus the application's own
    processing time. A few applications are withdrawn before any decision."""
    rows = []
    for h in hs:
        code = h["code"]
        for a in h["apps"]:
            a.pop("decided", None)
            if a["u_wd"] < K.WITHDRAWN:
                a["status"] = "withdrawn"
                continue
            decided = working(a["received"] + dt.timedelta(days=a["delay"]))
            if decided.year > 2025:
                a["status"] = "after"
                continue
            a["status"] = "decided"
            if a["u_doc"] < doc[code]:
                outcome, tier, reason = "deny", 0, "INCOMPLETE"
            elif a["u_cov"] < h["other_cov"]:
                outcome, tier, reason = "deny", 0, "OTHER_COVERAGE"
            elif a["u_res"] < h["not_resident"]:
                outcome, tier, reason = "deny", 0, "NOT_RESIDENT"
            elif a["tier_policy"] == 0:
                outcome, tier, reason = "deny", 0, "OVER_INCOME"
            else:
                outcome, tier, reason = "approve", a["tier_policy"], None
            a.update(decided=decided, outcome=outcome, tier=tier, reason=reason)
            rows.append(dict(code=code, region=h["region"], kind=a["kind"], hh="%s-%d" % (code, a["hh"]), size=a["size"],
                             month=a["received"].month, mindex=a["amonth"] - 24, annual=round(a["inc3"] * 4, 2),
                             year=decided.year, writeoff=tier, inc12=a["inc12"]))
    return rows


def golden_eligible(rows):
    """The golden's eligible decisions per hospital (2025): calendars by region and kind of work, read from every
    first-review decision's income, which no decision changes."""
    import models as M
    cals = M.cal_cross(rows, M.k_region_kind)
    est = M.by_calendar(cals, M.k_region_kind)
    out = {}
    for i, x in enumerate(rows):
        if x["year"] == 2025 and M.pct(x, est(x)) <= M.LIMIT:
            out.setdefault(x["code"], []).append(i)
    return out


def tune(hs):
    """Each hospital's documents-denial rate, set so that its golden share lands on K.TARGET exactly: among its eligible
    decisions not already left owing more than half, the ones whose documents draw is lowest are the ones denied."""
    rows = decide(hs, {c: 0.0 for c in K.CODES})
    keyed = {}
    for h in hs:
        for a in h["apps"]:
            if "decided" in a and a["decided"].year <= 2025:
                keyed[(h["code"], a["hh"], a["amonth"])] = a
    elig = golden_eligible(rows)
    doc = {}
    for h in hs:
        code = h["code"]
        idx = elig[code]
        base = sum(1 for i in idx if rows[i]["writeoff"] < 50)
        need = int(np.ceil(K.TARGET[code] / 100.0 * len(idx) - base - 1e-9))
        pool = sorted(keyed[(code, int(rows[i]["hh"].split("-")[1]), rows[i]["mindex"] + 24)]["u_doc"]
                      for i in idx if rows[i]["writeoff"] >= 50)
        doc[code] = (pool[need - 1] + pool[need]) / 2.0 if need > 0 else pool[0] / 2.0
        h["doc"] = doc[code]
    return doc
